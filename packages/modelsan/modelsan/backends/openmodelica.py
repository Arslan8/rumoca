"""OpenModelica behind the Backend interface.

Everything specific to OMC — `buildModel`, `_init.xml`, `-override`, `CC=gcc`,
where temporary files land — is confined to this file. Nothing above it knows
OMC exists, which is what lets DifferentialSan compare backends without
containing launch logic for either.

OMC takes Modelica source rather than canonical DAE bitcode. That is allowed by
the backend contract: a backend receives the DAE where it can consume one, and
the original model where the tool requires source.
"""

from __future__ import annotations

import csv
import os
import re
import subprocess
import tempfile
from pathlib import Path

from ..fuzz.testcase import TestCase
from ..instrumentation.request import RequestKind
from ..runtime.observations import (
    ObservationStream,
    Phase,
    SimulationEnd,
    SimulationStart,
    SolverFailure,
    VariableObservation,
)
from .base import ExecutionResult, Status

ENV = {**os.environ, "CC": "gcc"}

# OMC names the offending expression when a divisor vanishes, which is far more
# than a generic solver error gives. Worth extracting rather than discarding.
DIVISION_BY_ZERO = re.compile(r"division by zero.*divisor b expression is: (\S+)")
ASSERTION = re.compile(r"assert\w*\s*\|\s*(?:debug|info|error)\s*\|\s*(.+)")


class OpenModelicaBackend:
    """Builds once per model, then re-runs the executable per test case."""

    name = "openmodelica"

    #: What this backend can actually observe. The planner uses this to decide
    #: which sanitizers can run, rather than letting them silently see nothing.
    capabilities = frozenset({RequestKind.OBSERVE_VARIABLE, RequestKind.SOLVER_STATS})

    def __init__(self, libraries: list[str], t_end: float = 0.5,
                 timeout: float = 120.0) -> None:
        self.libraries = libraries
        self.t_end = t_end
        self.timeout = timeout
        self._work: tempfile.TemporaryDirectory | None = None
        self._executable: Path | None = None

    def prepare(self, model_path: str, model_name: str) -> bool:
        self._work = tempfile.TemporaryDirectory()
        work = Path(self._work.name)
        lines = [f'loadFile("{library}"); getErrorString();' for library in self.libraries]
        if not model_name.startswith(("Modelica.", "ModelicaTest.")):
            lines.insert(0, f'loadFile("{Path(model_path).resolve()}"); getErrorString();')
        lines.append(f"buildModel({model_name}, stopTime={self.t_end}); getErrorString();")
        script = work / "build.mos"
        script.write_text("\n".join(lines) + "\n")
        try:
            subprocess.run(["omc", str(script)], cwd=work, capture_output=True,
                           text=True, timeout=max(self.timeout, 600), env=ENV)
        except subprocess.TimeoutExpired:
            return False
        candidate = work / model_name
        self._executable = candidate if candidate.exists() else None
        return self._executable is not None

    def run(self, testcase: TestCase, instrumentation: list | None = None) -> ExecutionResult:
        if self._executable is None or self._work is None:
            return ExecutionResult(status=Status.BUILD_FAILED, backend=self.name,
                                   message="model was not built")
        work = Path(self._work.name)
        command = [str(self._executable), "-outputFormat=csv"]
        overrides = {**testcase.parameters,
                     **{f"{k}": v for k, v in testcase.initial_values.items()}}
        if overrides:
            command += ["-override", ",".join(f"{k}={v:g}" for k, v in overrides.items())]

        try:
            done = subprocess.run(command, cwd=work, capture_output=True, text=True,
                                  timeout=self.timeout, env=ENV)
        except subprocess.TimeoutExpired:
            return ExecutionResult(status=Status.TIMEOUT, backend=self.name)

        times, trace = self._read_trace(work / f"{self._executable.name}_res.csv")
        stream = ObservationStream()
        stream.add(SimulationStart())
        for name, values in trace.items():
            for index, value in enumerate(values):
                if index < len(times):
                    # variable_id stays -1: OMC reports names, not DAE ids, and
                    # inventing an id here would break every downstream anchor.
                    stream.add(VariableObservation(time=times[index], name=name,
                                                   value=value))
        completed = done.returncode == 0
        if not completed:
            # A failed run still carries evidence. Turning it into an
            # observation is what lets a sanitizer judge it, rather than the
            # pipeline silently having nothing to look at.
            text = " ".join((done.stdout + done.stderr).split())
            blamed = DIVISION_BY_ZERO.search(text)
            at_init = "at initialization" in text
            stream.add(SolverFailure(
                time=times[-1] if times else None,
                phase=Phase.INITIALIZATION if at_init else Phase.TRANSIENT,
                reason=(f"division by zero in `{blamed.group(1)}`" if blamed
                        else text[-200:]),
            ))
        stream.add(SimulationEnd(completed=completed,
                                 message="" if completed else done.stdout[-200:]))

        return ExecutionResult(
            status=Status.OK if completed else Status.FAILED,
            backend=self.name,
            observations=stream,
            trace=trace,
            times=times,
            final_state={n: v[-1] for n, v in trace.items() if v},
            message="" if completed else " ".join((done.stdout + done.stderr).split())[-220:],
        )

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
        times = columns.pop("time", [])
        return times, columns

    def close(self) -> None:
        if self._work is not None:
            self._work.cleanup()
            self._work = None
