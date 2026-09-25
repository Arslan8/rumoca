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
import hashlib
import math
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
    EventTriggered,
    InitializationFailure,
    ObservationStream,
    SimulationAbort,
    SimulationEnd,
    SimulationStart,
    SolverFailure,
    UnorderedVariableObservation,
    VariableObservation,
)
from .base import ExecutionResult, ExecutionStatus, Trace
from .csv_trace import UnorderedTraceError, read_csv_trace
from .process import execute

ENV = {**os.environ, "CC": "gcc"}

# OMC names the offending expression when a divisor vanishes, which is far more
# than a generic solver error gives. Worth extracting rather than discarding.
DIVISION_BY_ZERO = re.compile(r"division by zero.*?divisor b expression is: (\S+)")

# `LOG_EVENTS | info | state event at time=0.4000000001`. Event *times* are all
# OMC reports; it does not say which condition fired, so these observations
# carry no anchor at all rather than a guessed one.
EVENT_AT = re.compile(r"(state|time) event at time=([0-9.eE+-]+)")
IDENTIFIER = r"(?:[A-Za-z_][A-Za-z_0-9]*|'(?:\\.|[^'\\\x00-\x1f])+')"
MODEL_NAME = re.compile(rf"{IDENTIFIER}(?:\.{IDENTIFIER})*")

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


def _modelica_string(value: str) -> str:
    """Quote a string literal without allowing paths to become MOS statements."""
    escapes = {"\\": "\\\\", '"': '\\"', "\n": "\\n", "\r": "\\r",
               "\t": "\\t", "\b": "\\b", "\f": "\\f"}
    if any(ord(char) < 32 and char not in escapes for char in value):
        raise ValueError("unsupported control character in Modelica string")
    return '"' + "".join(escapes.get(char, char) for char in value) + '"'


class OpenModelicaBackend:
    """Builds once per model, then re-runs the executable per test case."""

    name = "openmodelica"

    #: What this environment can observe. CANONICAL_IDENTITY is deliberately
    #: absent — OMC reports names, not DAE ids.
    capabilities = frozenset({
        Capability.OBSERVE_VARIABLE,
        Capability.OBSERVE_FAILURE,
        Capability.OBSERVE_EVENTS,
    })

    def __init__(self, libraries: list[str], t_end: float = 0.5,
                 timeout: float = 120.0, *, number_of_intervals: int = 500) -> None:
        if not math.isfinite(timeout) or timeout <= 0:
            raise ValueError("timeout must be positive and finite")
        if not math.isfinite(t_end) or t_end < 0:
            raise ValueError("t_end must be nonnegative and finite")
        if (not isinstance(number_of_intervals, int)
                or isinstance(number_of_intervals, bool) or number_of_intervals <= 0):
            raise ValueError("number_of_intervals must be a positive integer")
        self.libraries = libraries
        self.t_end = t_end
        self.timeout = timeout
        self.number_of_intervals = number_of_intervals
        self._work: tempfile.TemporaryDirectory | None = None
        self._executable: Path | None = None

    def prepare(self, model_path: str, model_name: str) -> ExecutionResult | None:
        self.close()
        if MODEL_NAME.fullmatch(model_name) is None:
            return ExecutionResult.backend_error(self.name, "invalid Modelica model name")
        self._work = tempfile.TemporaryDirectory()
        work = Path(self._work.name)
        paths = list(self.libraries)
        if model_path and not model_name.startswith(("Modelica.", "ModelicaTest.")):
            paths.insert(0, model_path)
        try:
            lines = [f"if not loadFile({_modelica_string(str(Path(path).resolve()))}) then "
                     "print(getErrorString()); exit(1); end if; getErrorString();"
                     for path in paths]
        except ValueError as error:
            return ExecutionResult.backend_error(self.name, str(error))
        lines.append(f'buildModel({model_name}, stopTime={self.t_end}, '
                     f'numberOfIntervals={self.number_of_intervals}, '
                     'fileNamePrefix="modelsan_model"); getErrorString();')
        script = work / "build.mos"
        script.write_text("\n".join(lines) + "\n")
        try:
            done = execute(["omc", str(script)], work, self.timeout, env=ENV)
        except subprocess.TimeoutExpired as error:
            return self._backend_error(f"build exceeded {self.timeout:g}s", error)
        except OSError as error:
            return self._backend_error(f"cannot build: {error}")

        candidate = work / "modelsan_model"
        if done.returncode != 0 or not candidate.is_file() or not os.access(candidate, os.X_OK):
            return self._backend_error("build did not produce an executable", done)
        self._executable = candidate
        return None

    def _backend_error(self, message: str, process=None,
                       phase: ExecutionPhase = ExecutionPhase.COMPILATION) -> ExecutionResult:
        stdout = getattr(process, "stdout", "") or ""
        stderr = getattr(process, "stderr", "") or ""
        output = stdout + stderr
        result = ExecutionResult.backend_error(self.name, message + ("\n" + output if output else ""), phase)
        result.backend_metadata = {"stdout": stdout, "stderr": stderr,
                                   "returncode": getattr(process, "returncode", None)}
        return result

    def run(self, testcase: TestCase, instrumentation: list | None = None) -> ExecutionResult:
        if self._executable is None or self._work is None:
            return ExecutionResult.backend_error(self.name, "model was not built")
        if not self._executable.is_file():
            return self._backend_error("built executable is missing", phase=ExecutionPhase.SIMULATION)
        if testcase.input_trajectory is not None or testcase.solver_options:
            return self._backend_error("input trajectories/solver overrides unsupported")

        work = Path(self._work.name)
        command = [str(self._executable), "-outputFormat=csv", "-lv", "LOG_EVENTS"]
        overrides = {**testcase.parameters, **testcase.initial_values}
        if overrides:
            command += ["-override", ",".join(f"{k}={v:g}" for k, v in overrides.items())]

        trace_path = work / f"{self._executable.name}_res.csv"
        try:
            trace_path.unlink(missing_ok=True)
            done = execute(command, work, self.timeout, env=ENV)
        except OSError as error:
            return self._backend_error(f"cannot execute: {error}", phase=ExecutionPhase.SIMULATION)
        except subprocess.TimeoutExpired as error:
            stream = ObservationStream()
            stream.add(SimulationAbort(kind=FailureKind.TIMEOUT,
                                       reason=f"exceeded {self.timeout:g}s"))
            return ExecutionResult(
                backend=self.name, status=ExecutionStatus.TIMEOUT,
                phase=ExecutionPhase.SIMULATION, observations=stream,
                failure=ExecutionFailure(kind=FailureKind.TIMEOUT,
                                         phase=ExecutionPhase.SIMULATION,
                                         message=f"exceeded {self.timeout:g}s",
                                         raw=(error.stdout or "") + (error.stderr or "")),
                backend_metadata={"stdout": error.stdout or "", "stderr": error.stderr or ""})

        if done.returncode < 0:
            return self._aborted(done)
        try:
            times, columns = self._read_trace(trace_path)
            if done.returncode == 0 and not times:
                raise ValueError("successful process produced no trace")
        except UnorderedTraceError as error:
            if done.returncode != 0:
                return self._backend_error(f"invalid trace: {error}", done, ExecutionPhase.FINALIZATION)
            return self._unordered_values(done, trace_path, error)
        except (OSError, ValueError, csv.Error) as error:
            return self._backend_error(f"invalid trace: {error}", done, ExecutionPhase.FINALIZATION)
        trace = Trace(times=times, columns=columns) if times else None
        stream = self._stream(times, columns)
        events = self._events(done.stdout + done.stderr)
        for event in events:
            stream.add(event)
        text = done.stdout + done.stderr
        metadata = {"returncode": done.returncode, "stdout": done.stdout, "stderr": done.stderr}

        if done.returncode == 0:
            stream.add(SimulationEnd(completed=True))
            return ExecutionResult(backend=self.name, status=ExecutionStatus.SUCCESS,
                                   phase=ExecutionPhase.FINALIZATION,
                                   observations=stream, trace=trace, events=events,
                                   backend_metadata=metadata)

        failure = self._failure(text, times)
        # The failure is an observation, not an absence. Without this, a
        # sanitizer would have to infer the failure from a missing trace.
        stream.add(self._observation(failure, text))
        stream.add(SimulationEnd(completed=False, message=failure.message))
        return ExecutionResult(
            backend=self.name, status=ExecutionStatus.FAILED, phase=failure.phase,
            observations=stream, trace=trace, events=events, failure=failure,
            backend_metadata=metadata,
        )

    def _unordered_values(self, done: subprocess.CompletedProcess, path: Path,
                          error: UnorderedTraceError) -> ExecutionResult:
        """Retain values without promoting rejected chronology to a trajectory."""
        try:
            raw_csv = path.read_bytes()
            csv_text = raw_csv.decode("utf-8")
        except (OSError, UnicodeError) as unreadable:
            return self._backend_error(f"cannot preserve sample evidence: {unreadable}",
                                       done, ExecutionPhase.FINALIZATION)
        samples = error.samples
        stream = ObservationStream()
        stream.add(SimulationStart())
        for index, reported_time in enumerate(samples.times):
            for name, values in samples.columns.items():
                stream.add(UnorderedVariableObservation(
                    backend=BackendAnchor(self.name, name, EntityKind.VARIABLE),
                    value=values[index], reported_time=reported_time, row_index=index))
        events = self._events(done.stdout + done.stderr)
        for event in events:
            stream.add(event)
        stream.add(SimulationEnd(completed=True))
        return ExecutionResult(backend=self.name, status=ExecutionStatus.SUCCESS,
            phase=ExecutionPhase.FINALIZATION, observations=stream, events=events,
            backend_metadata={"returncode": done.returncode, "stdout": done.stdout,
                "stderr": done.stderr, "observation_profile": "unordered-values",
                "temporal_trace": {"available": False, "reason": str(error),
                    "raw_csv_sha256": hashlib.sha256(raw_csv).hexdigest(),
                    "raw_csv": csv_text, "row_count": len(samples.times)}})

    def _aborted(self, done: subprocess.CompletedProcess) -> ExecutionResult:
        """A signal is evidence of interruption, not proof of a model defect."""
        message = f"simulator terminated by signal {-done.returncode}"
        raw = done.stdout + done.stderr
        stream = ObservationStream()
        stream.add(SimulationStart())
        stream.add(SimulationAbort(kind=FailureKind.ABORTED, reason=message, raw=raw))
        stream.add(SimulationEnd(completed=False, message=message))
        return ExecutionResult(
            backend=self.name, status=ExecutionStatus.ABORTED,
            phase=ExecutionPhase.SIMULATION, observations=stream,
            failure=ExecutionFailure(kind=FailureKind.ABORTED,
                phase=ExecutionPhase.SIMULATION, message=message, raw=raw),
            backend_metadata={"returncode": done.returncode,
                "signal": -done.returncode, "stdout": done.stdout, "stderr": done.stderr})

    def _failure(self, text: str, times: list[float]) -> ExecutionFailure:
        at_init = "at initialization" in text or "initialization" in text.lower()
        phase = ExecutionPhase.INITIALIZATION if at_init else ExecutionPhase.SIMULATION
        blamed = DIVISION_BY_ZERO.search(text)
        message = (f"division by zero in `{blamed.group(1)}`" if blamed
                   else text[-200:] or "run failed with no message")
        return ExecutionFailure(kind=classify(text), phase=phase, message=message,
                                raw=text,
                                time=times[-1] if times else None)

    def _observation(self, failure: ExecutionFailure, text: str):
        blamed = DIVISION_BY_ZERO.search(text)
        anchor = (BackendAnchor(self.name, blamed.group(1), EntityKind.VARIABLE)
                  if blamed else None)
        cls = (InitializationFailure
               if failure.phase is ExecutionPhase.INITIALIZATION else SolverFailure)
        return cls(time=failure.time, kind=failure.kind, reason=failure.message,
                   raw=failure.raw, backend=anchor)

    @staticmethod
    def _events(text: str) -> list:
        """Event firings, in order.

        OMC reports the time and whether it was a state or time event, and
        nothing about which condition was responsible. So these carry no
        anchor: EventSan reasons about spacing and density, which is exactly
        what the available evidence supports.
        """
        found = []
        for kind, when in EVENT_AT.findall(text):
            try:
                time = float(when)
                if math.isfinite(time):
                    found.append(EventTriggered(time=time, new_value=kind))
            except ValueError:
                continue
        return found

    def _stream(self, times: list[float], columns: dict) -> ObservationStream:
        stream = ObservationStream()
        stream.add(SimulationStart())
        for index, time in enumerate(times):
            for name, values in columns.items():
                anchor = BackendAnchor(self.name, name, EntityKind.VARIABLE)
                stream.add(VariableObservation(time=time, backend=anchor, value=values[index]))
        return stream

    @staticmethod
    def _read_trace(path: Path) -> tuple[list[float], dict[str, list[float]]]:
        return read_csv_trace(path)

    def close(self) -> None:
        self._executable = None
        if self._work is not None:
            self._work.cleanup()
            self._work = None
