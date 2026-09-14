"""Rumoca behind the Backend contract.

This backend is what makes canonical identity available. It executes the same
artifact the analyses read, so every observation it produces can name the exact
DAE entity it came from — where OpenModelica can only report the name it happens
to use. That is the difference between a finding anchored to the model and one
anchored to a tool's vocabulary.

It is also the second implementation DifferentialSan needs. With one backend
there is nothing to differ from.
"""

from __future__ import annotations

import csv
import json
import re
import subprocess
import tempfile
from pathlib import Path

from ..dae import load, save
from ..fuzz.testcase import TestCase
from ..instrumentation.capability import Capability
from ..runtime.anchors import CanonicalAnchor, EntityKind
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

# Ordered; first match wins.
CLASSIFIERS = (
    (re.compile(r"non-finite|NaN|inf", re.I), FailureKind.NON_FINITE_VALUE),
    (re.compile(r"structurally singular|singular", re.I), FailureKind.SINGULAR_SYSTEM),
    (re.compile(r"did not converge|projection", re.I),
     FailureKind.NONLINEAR_SOLVER_FAILURE),
    (re.compile(r"step size", re.I), FailureKind.STEP_SIZE_TOO_SMALL),
    (re.compile(r"division", re.I), FailureKind.DIVISION_BY_ZERO),
)


def classify(text: str) -> FailureKind:
    for pattern, kind in CLASSIFIERS:
        if pattern.search(text):
            return kind
    return FailureKind.UNKNOWN


class RumocaBackend:
    """Simulates a canonical DAE artifact directly."""

    name = "rumoca"

    #: The only backend that can supply CANONICAL_IDENTITY, because it runs the
    #: same artifact the analyses read.
    capabilities = frozenset({
        Capability.OBSERVE_VARIABLE,
        Capability.OBSERVE_FAILURE,
        Capability.CANONICAL_IDENTITY,
    })

    def __init__(self, executable: str = "./target/debug/rumoca",
                 t_end: float = 0.5, timeout: float = 90.0) -> None:
        self.executable = executable
        self.t_end = t_end
        self.timeout = timeout
        self._work: tempfile.TemporaryDirectory | None = None
        self._artifact: Path | None = None
        self._ids: dict[str, int] = {}

    def prepare_from_artifact(self, artifact: Path) -> ExecutionResult | None:
        """Instrument an existing artifact so its variables are observable.

        `--simulate --trace-out` reports only declared trace points, and a
        freshly compiled artifact declares none. Adding one per variable is a
        pure observation change: no equation, variable or parameter is touched,
        so what runs is what was analysed.
        """
        self._work = tempfile.TemporaryDirectory()
        work = Path(self._work.name)
        try:
            model = load(artifact)
        except Exception as error:
            return ExecutionResult.backend_error(self.name, f"cannot load: {error}")

        self._ids = {v.name: v.id for v in model.variables}
        added = 0
        for variable in model.variables:
            if variable.is_parameter:
                continue  # constant over the run; a column per sample says nothing
            try:
                model.add_trace_point(variable, label=variable.name,
                                      added_by="modelsan.RumocaBackend")
                added += 1
            except Exception:
                continue
        if not added:
            return ExecutionResult.backend_error(self.name, "no traceable variables")

        self._artifact = work / "traced.rbc"
        try:
            save(model, self._artifact)
        except Exception as error:
            return ExecutionResult.backend_error(self.name, f"cannot save: {error}")
        return None

    def prepare(self, model_path: str, model_name: str) -> ExecutionResult | None:
        """Compile Modelica source, then instrument the result."""
        self._work = tempfile.TemporaryDirectory()
        work = Path(self._work.name)
        raw = work / "m.rbc"
        command = [self.executable, "compile", model_path, "--model", model_name,
                   "--emit-bitcode", str(raw),
                   "--source-root", "target/msl/ModelicaStandardLibrary-4.1.0",
                   "--source-root", "target/corpus/ModelicaStandardLibrary-4.1.0"]
        try:
            done = subprocess.run(command, capture_output=True, text=True,
                                  timeout=max(self.timeout, 180))
        except subprocess.TimeoutExpired:
            return ExecutionResult.backend_error(self.name, "compile timed out")
        if not raw.exists():
            return ExecutionResult.backend_error(
                self.name, (done.stdout + done.stderr).strip()[-300:])
        return self.prepare_from_artifact(raw)

    def run(self, testcase: TestCase, instrumentation: list | None = None) -> ExecutionResult:
        if self._artifact is None or self._work is None:
            return ExecutionResult.backend_error(self.name, "model was not prepared")
        work = Path(self._work.name)
        trace_csv = work / "trace.csv"
        if trace_csv.exists():
            trace_csv.unlink()

        # `--check` and `--trace-out` are mutually exclusive in Rumoca, and the
        # trace is the right choice: `--check` reports non-finite values and
        # bound breaches, which is exactly what NumericSan and RangeSan do from
        # observations. Letting the backend do it would move a sanitizer's
        # judgement inside the execution boundary and hide it from the planner.
        command = [self.executable, "compile-bitcode", str(self._artifact),
                   "--simulate", "--t-end", str(self.t_end),
                   "--trace-out", str(trace_csv)]
        for name, value in {**testcase.parameters, **testcase.initial_values}.items():
            command += ["--param", f"{name}={value:g}"]

        try:
            done = subprocess.run(command, capture_output=True, text=True,
                                  timeout=self.timeout)
        except subprocess.TimeoutExpired:
            stream = ObservationStream()
            stream.add(SimulationAbort(kind=FailureKind.TIMEOUT,
                                       reason=f"exceeded {self.timeout:g}s"))
            return ExecutionResult(backend=self.name, status=ExecutionStatus.TIMEOUT,
                                   observations=stream,
                                   failure=ExecutionFailure(
                                       kind=FailureKind.TIMEOUT,
                                       phase=ExecutionPhase.SIMULATION,
                                       message=f"exceeded {self.timeout:g}s"))

        times, columns = self._read_trace(trace_csv)
        trace = Trace(times=times, columns=columns) if times else None
        stream = self._stream(times, columns)
        text = " ".join((done.stdout + done.stderr).split())

        # `--param` naming a parameter the artifact does not expose is a harness
        # error, not a model failure: reporting it as one blames the model for a
        # badly formed question.
        if "not a tunable parameter" in text:
            return ExecutionResult.backend_error(
                self.name, "parameter not tunable in this artifact",
                phase=ExecutionPhase.INITIALIZATION)

        if done.returncode == 0:
            stream.add(SimulationEnd(completed=True))
            return ExecutionResult(backend=self.name, status=ExecutionStatus.SUCCESS,
                                   phase=ExecutionPhase.FINALIZATION,
                                   observations=stream, trace=trace)

        violations = self._violations(done.stdout)
        detail = violations[0] if violations else text[-200:]
        at_init = "structural" in detail.lower() or "initial" in detail.lower()
        phase = ExecutionPhase.INITIALIZATION if at_init else ExecutionPhase.SIMULATION
        # Classify from the whole output, not the truncated summary: the
        # phrase that identifies the failure is often earlier than the last
        # 200 characters.
        failure = ExecutionFailure(kind=classify(text) if classify(text)
                                   is not FailureKind.UNKNOWN else classify(detail),
                                   phase=phase,
                                   message=detail[:200], raw=text[-2000:])
        cls = InitializationFailure if at_init else SolverFailure
        stream.add(cls(kind=failure.kind, reason=failure.message, raw=failure.raw))
        stream.add(SimulationEnd(completed=False, message=failure.message))
        return ExecutionResult(backend=self.name, status=ExecutionStatus.FAILED,
                               phase=phase, observations=stream, trace=trace,
                               failure=failure)

    @staticmethod
    def _violations(stdout: str) -> list[str]:
        """`--check` emits machine-readable JSON; parse that, not the prose."""
        start = stdout.find("[")
        if start < 0:
            return []
        try:
            entries = json.loads(stdout[start:stdout.rfind("]") + 1])
        except (ValueError, TypeError):
            return []
        return [str(e.get("detail", e.get("kind", ""))) for e in entries
                if isinstance(e, dict)]

    def _stream(self, times: list[float], columns: dict) -> ObservationStream:
        stream = ObservationStream()
        stream.add(SimulationStart())
        for name, values in columns.items():
            dae_id = self._ids.get(name)
            # Anchored canonically only where the id is genuinely known.
            anchor = (CanonicalAnchor(EntityKind.VARIABLE, dae_id, name)
                      if dae_id is not None else None)
            for index, value in enumerate(values):
                if index >= len(times):
                    break
                stream.add(VariableObservation(time=times[index], canonical=anchor,
                                               value=value))
        return stream

    @staticmethod
    def _read_trace(path: Path) -> tuple[list[float], dict[str, list[float]]]:
        """Rumoca writes long format: time, trace_id, ..., variable, ..., value."""
        if not path.exists():
            return [], {}
        series: dict[str, dict[float, float]] = {}
        with path.open(errors="replace") as handle:
            for row in csv.DictReader(handle):
                try:
                    when, value = float(row["time"]), float(row["value"])
                except (KeyError, ValueError, TypeError):
                    continue
                series.setdefault(row.get("variable", "?"), {})[when] = value
        if not series:
            return [], {}
        times = sorted(next(iter(series.values())))
        return times, {name: [points.get(t, float("nan")) for t in times]
                       for name, points in series.items()}

    def close(self) -> None:
        if self._work is not None:
            self._work.cleanup()
            self._work = None
