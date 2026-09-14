"""OpenModelica behind the Backend contract.

Everything OMC-specific stops here: `buildModel`, `_init.xml`, `-override`,
`CC=gcc`, temporary directories, result parsing.

Two contracts this adapter honours carefully:

**A failed execution is still a result.** A run that dies in initialization
returns an `ExecutionResult` with the phase it reached, a classified failure and
the tool's own message — never `None`, never an empty result.

**No invented identity.** OMC reports variable *names*. It does not know Rumoca
DAE ids and this adapter does not pretend otherwise: observations carry a
`BackendAnchor` and no canonical anchor. `CANONICAL_IDENTITY` is absent from its
capabilities, so the planner can tell a sanitizer that needs it to stand down.
"""

from __future__ import annotations

import csv
import os
import re
import subprocess
import tempfile
from pathlib import Path

from ..fuzz.testcase import TestCase
from ..instrumentation.capability import Capability
from ..runtime.anchors import BackendAnchor, EntityKind
from ..runtime.failures import ExecutionFailure, ExecutionPhase, FailureKind
from ..runtime.observations import (
    InitializationFailure,
    ObservationStream,
    SimulationAbort,
    SimulationEnd,
    SimulationStart,
    SolverFailure,
    VariableObservation,
)
from .base import ExecutionResult, ExecutionStatus, Trace

ENV = {**os.environ, "CC": "gcc"}

# OMC names the offending expression when a divisor vanishes, which is far more
# than a generic solver error gives. Worth extracting rather than discarding.
DIVISION_BY_ZERO = re.compile(r"division by zero.*?divisor b expression is: (\S+)")

# Ordered: the first match wins, so more specific patterns come first.
CLASSIFIERS = (
    (re.compile(r"division by zero", re.I), FailureKind.DIVISION_BY_ZERO),
    (re.compile(r"singular", re.I), FailureKind.SINGULAR_SYSTEM),
    (re.compile(r"nonlinear system .*fail|no convergence", re.I),
     FailureKind.NONLINEAR_SOLVER_FAILURE),
    (re.compile(r"step size|too small", re.I), FailureKind.STEP_SIZE_TOO_SMALL),
    (re.compile(r"\b(nan|inf)\b", re.I), FailureKind.NON_FINITE_VALUE),
    (re.compile(r"assert", re.I), FailureKind.ASSERTION_VIOLATED),
)


def classify(text: str) -> FailureKind:
    """Normalize a backend message. Unknown is a valid answer.

    The raw text is always retained alongside, so an unrecognised message can be
    reclassified later without re-running anything.
    """
    for pattern, kind in CLASSIFIERS:
        if pattern.search(text):
            return kind
    return FailureKind.UNKNOWN


class OpenModelicaBackend:
    """Builds once per model, then re-runs the executable per test case."""

    name = "openmodelica"

    #: What this environment can observe. CANONICAL_IDENTITY is deliberately
    #: absent — OMC reports names, not DAE ids.
    capabilities = frozenset({
        Capability.OBSERVE_VARIABLE,
        Capability.OBSERVE_FAILURE,
    })

    def __init__(self, libraries: list[str], t_end: float = 0.5,
                 timeout: float = 120.0) -> None:
        self.libraries = libraries
        self.t_end = t_end
        self.timeout = timeout
        self._work: tempfile.TemporaryDirectory | None = None
        self._executable: Path | None = None

    def prepare(self, model_path: str, model_name: str) -> ExecutionResult | None:
        self._work = tempfile.TemporaryDirectory()
        work = Path(self._work.name)
        lines = [f'loadFile("{library}"); getErrorString();' for library in self.libraries]
        if model_path and not model_name.startswith(("Modelica.", "ModelicaTest.")):
            lines.insert(0, f'loadFile("{Path(model_path).resolve()}"); getErrorString();')
        lines.append(f"buildModel({model_name}, stopTime={self.t_end}); getErrorString();")
        script = work / "build.mos"
        script.write_text("\n".join(lines) + "\n")
        try:
            done = subprocess.run(["omc", str(script)], cwd=work, capture_output=True,
                                  text=True, timeout=max(self.timeout, 600), env=ENV)
            output = done.stdout + done.stderr
        except subprocess.TimeoutExpired:
            return ExecutionResult.backend_error(self.name, "build timed out")

        candidate = work / model_name
        if not candidate.exists():
            return ExecutionResult.backend_error(self.name, output.strip()[-400:])
        self._executable = candidate
        return None

    def run(self, testcase: TestCase, instrumentation: list | None = None) -> ExecutionResult:
        if self._executable is None or self._work is None:
            return ExecutionResult.backend_error(self.name, "model was not built")

        work = Path(self._work.name)
        command = [str(self._executable), "-outputFormat=csv"]
        overrides = {**testcase.parameters, **testcase.initial_values}
        if overrides:
            command += ["-override", ",".join(f"{k}={v:g}" for k, v in overrides.items())]

        try:
            done = subprocess.run(command, cwd=work, capture_output=True, text=True,
                                  timeout=self.timeout, env=ENV)
        except subprocess.TimeoutExpired:
            stream = ObservationStream()
            stream.add(SimulationAbort(kind=FailureKind.TIMEOUT,
                                       reason=f"exceeded {self.timeout:g}s"))
            return ExecutionResult(
                backend=self.name, status=ExecutionStatus.TIMEOUT,
                phase=ExecutionPhase.SIMULATION, observations=stream,
                failure=ExecutionFailure(kind=FailureKind.TIMEOUT,
                                         phase=ExecutionPhase.SIMULATION,
                                         message=f"exceeded {self.timeout:g}s"))

        times, columns = self._read_trace(work / f"{self._executable.name}_res.csv")
        trace = Trace(times=times, columns=columns) if times else None
        stream = self._stream(times, columns)
        text = " ".join((done.stdout + done.stderr).split())

        if done.returncode == 0:
            stream.add(SimulationEnd(completed=True))
            return ExecutionResult(backend=self.name, status=ExecutionStatus.SUCCESS,
                                   phase=ExecutionPhase.FINALIZATION,
                                   observations=stream, trace=trace)

        failure = self._failure(text, times)
        # The failure is an observation, not an absence. Without this, a
        # sanitizer would have to infer the failure from a missing trace.
        stream.add(self._observation(failure, text))
        stream.add(SimulationEnd(completed=False, message=failure.message))
        return ExecutionResult(
            backend=self.name, status=ExecutionStatus.FAILED, phase=failure.phase,
            observations=stream, trace=trace, failure=failure,
            backend_metadata={"returncode": done.returncode},
        )

    def _failure(self, text: str, times: list[float]) -> ExecutionFailure:
        at_init = "at initialization" in text or "initialization" in text.lower()
        phase = ExecutionPhase.INITIALIZATION if at_init else ExecutionPhase.SIMULATION
        blamed = DIVISION_BY_ZERO.search(text)
        message = (f"division by zero in `{blamed.group(1)}`" if blamed
                   else text[-200:] or "run failed with no message")
        return ExecutionFailure(kind=classify(text), phase=phase, message=message,
                                raw=text[-2000:],
                                time=times[-1] if times else None)

    def _observation(self, failure: ExecutionFailure, text: str):
        blamed = DIVISION_BY_ZERO.search(text)
        anchor = (BackendAnchor(self.name, blamed.group(1), EntityKind.VARIABLE)
                  if blamed else None)
        cls = (InitializationFailure
               if failure.phase is ExecutionPhase.INITIALIZATION else SolverFailure)
        return cls(time=failure.time, kind=failure.kind, reason=failure.message,
                   raw=failure.raw, backend=anchor)

    def _stream(self, times: list[float], columns: dict) -> ObservationStream:
        stream = ObservationStream()
        stream.add(SimulationStart())
        for name, values in columns.items():
            anchor = BackendAnchor(self.name, name, EntityKind.VARIABLE)
            for index, value in enumerate(values):
                if index >= len(times):
                    break
                stream.add(VariableObservation(time=times[index], backend=anchor,
                                               value=value))
        return stream

    @staticmethod
    def _read_trace(path: Path) -> tuple[list[float], dict[str, list[float]]]:
        if not path.exists():
            return [], {}
        columns: dict[str, list[float]] = {}
        with path.open(errors="replace") as handle:
            reader = csv.reader(handle)
            header = next(reader, None)
            if not header:
                return [], {}
            names = [h.strip().strip('"') for h in header]
            for name in names:
                columns[name] = []
            for row in reader:
                for name, cell in zip(names, row):
                    try:
                        columns[name].append(float(cell))
                    except ValueError:
                        columns[name].append(float("nan"))
        return columns.pop("time", []), columns

    def close(self) -> None:
        if self._work is not None:
            self._work.cleanup()
            self._work = None
