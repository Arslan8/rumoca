"""Explicit native source execution with backend-name observations.

This profile runs Rumoca's existing source simulation entry point. It neither
imports nor executes an editable bitcode artifact, and does not silently replace
RumocaBackend. A separately compiled model cannot supply canonical identities
for these observations. Parameter/start overrides and expression instrumentation
are deliberately rejected until this entry point can honor them.
"""
from __future__ import annotations

import csv
import hashlib
import math
import os
import re
import shutil
import subprocess
import tempfile
from pathlib import Path

from ..instrumentation.capability import Capability
from ..runtime.anchors import BackendAnchor, EntityKind
from ..runtime.failures import ExecutionFailure, ExecutionPhase, FailureKind
from ..runtime.observations import (
    ObservationStream, SimulationEnd, SimulationStart, SolverFailure,
    VariableObservation,
)
from .base import ExecutionResult, ExecutionStatus, Trace
from .csv_trace import read_csv_trace
from .process import execute
from .compile_diagnostics import proven_model_failure
from .rumoca import classify


def _digest(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


class RumocaSourceBackend:
    """Nominal source simulation, selected explicitly by the caller.

    Timeout bounds the entire compile-and-simulate subprocess group. Because the
    CLI does not export a machine-readable live phase, a watchdog expiration is
    a coverage error; it is never presented as a proven solver/model timeout.
    """

    name = "rumoca-source"
    capabilities = frozenset({Capability.OBSERVE_VARIABLE, Capability.OBSERVE_FAILURE})

    def __init__(self, executable="./target/debug/rumoca", t_end=1.0, timeout=90.0,
                 *, source_roots=(), cache_dir=None, dt=0.0025, solver="rk-like",
                 freeze_parameters=False):
        for label, value in (("timeout", timeout), ("dt", dt), ("t_end", t_end)):
            if not math.isfinite(value) or value < 0 or (label != "t_end" and value == 0):
                raise ValueError(f"{label} must be finite and {'nonnegative' if label == 't_end' else 'positive'}")
        if solver not in {"auto", "bdf", "rk-like"}:
            raise ValueError("unsupported native source solver")
        candidate = shutil.which(str(executable))
        self.executable = str(Path(candidate or executable).resolve())
        self.t_end, self.timeout, self.dt, self.solver = t_end, timeout, dt, solver
        self.freeze_parameters = bool(freeze_parameters)
        self.source_roots = tuple(str(Path(root).resolve()) for root in source_roots)
        self.cache_dir = str(Path(cache_dir).resolve()) if cache_dir is not None else None
        self._work = None
        self._source = None
        self._model_name = ""
        self._metadata = {}
        self._run_index = 0

    def prepare(self, model_path: str, model_name: str):
        self.close()
        source = Path(model_path).resolve()
        if source.suffix.lower() != ".mo" or not source.is_file() or not model_name.strip():
            return ExecutionResult.backend_error(self.name, "expected a Modelica source file and model name")
        if not Path(self.executable).is_file() or not os.access(self.executable, os.X_OK):
            return ExecutionResult.backend_error(self.name, "native Rumoca executable is unavailable")
        if any(not Path(root).exists() for root in self.source_roots):
            return ExecutionResult.backend_error(self.name, "a requested source root is unavailable")
        try:
            self._metadata = {
                "profile": "native-source", "source": str(source), "model": model_name,
                "source_sha256": _digest(source), "executable": self.executable,
                "executable_sha256": _digest(Path(self.executable)),
                "source_roots": list(self.source_roots), "solver": self.solver,
                "start_time": 0.0, "stop_time": self.t_end, "output_interval": self.dt,
                "identity": "backend-only", "dependency_digests": "not recorded",
                "modelica_path": os.environ.get("MODELICAPATH", ""),
                "parameter_policy": "frozen" if self.freeze_parameters else "declared",
            }
            self._work = tempfile.TemporaryDirectory(prefix="modelsan-rumoca-source-")
        except OSError as error:
            self.close()
            return ExecutionResult.backend_error(self.name, str(error))
        self._source, self._model_name = source, model_name
        return None

    def run(self, testcase, instrumentation=None):
        if self._work is None or self._source is None:
            return ExecutionResult.backend_error(self.name, "source model was not prepared")
        if (testcase.parameters or testcase.initial_values or testcase.solver_options
                or testcase.input_trajectory is not None):
            return self._error("native source profile does not support test-case overrides")
        if any(r.capability not in self.capabilities or r.anchor is not None
               for r in instrumentation or ()):
            return self._error("requested instrumentation is unavailable in native source profile")
        self._run_index += 1
        work = Path(self._work.name)
        destination = work / f"trace-{self._run_index}.csv"
        command = self._command(destination)
        try:
            if not self._unchanged():
                return self._error("source or executable changed after prepare; prepare again")
            done = execute(command, work, self.timeout, env={**os.environ, "RAYON_NUM_THREADS": "4"})
            if not self._unchanged():
                return self._error("source or executable changed during execution; evidence discarded")
        except subprocess.TimeoutExpired as error:
            return self._error(f"native compile/simulation exceeded {self.timeout:g}s; phase unknown",
                               timeout_seconds=self.timeout, raw_output=_timeout_output(error))
        except (OSError, ValueError) as error:
            return self._error(str(error))
        metadata = {**self._metadata, "command": command, "returncode": done.returncode}
        if done.returncode < 0:
            return self._error(f"native process terminated by signal {-done.returncode}; phase unknown",
                               returncode=done.returncode, stdout=done.stdout, stderr=done.stderr)
        if done.returncode:
            try:
                proved = proven_model_failure(destination.with_suffix('.diagnostics.json'), self.name)
            except (OSError, ValueError) as error:
                return self._error(f"invalid compiler diagnostic evidence: {error}")
            if proved is not None:
                proved.backend_metadata.update(metadata)
                return proved
            return self._failure(done.stdout + done.stderr, metadata)
        return self._success(destination, metadata)

    def _unchanged(self):
        return (_digest(self._source) == self._metadata["source_sha256"]
                and _digest(Path(self.executable)) == self._metadata["executable_sha256"])

    def _command(self, destination):
        command = [self.executable, "sim", str(self._source), "--model", self._model_name,
                   "--solver", self.solver, "--t-end", str(self.t_end), "--dt", str(self.dt),
                   "--output", str(destination),
                   "--diagnostics-json", str(destination.with_suffix('.diagnostics.json'))]
        for root in self.source_roots:
            command += ["--source-root", root]
        if self.freeze_parameters:
            command += ["--freeze-parameters"]
        cache = self.cache_dir or str(Path(self._work.name) / "cache")
        return command + ["--cache-dir", cache]

    def _success(self, path, metadata):
        try:
            times, columns = read_csv_trace(path)
            if not times or not columns:
                raise ValueError("successful native execution produced no usable variable trace")
        except (OSError, ValueError, csv.Error) as error:
            result = self._error(f"invalid native trace: {error}")
            result.backend_metadata = metadata
            return result
        stream = ObservationStream()
        stream.add(SimulationStart(time=times[0]))
        for index, time in enumerate(times):
            for name, values in columns.items():
                stream.add(VariableObservation(time=time, value=values[index],
                    backend=BackendAnchor(self.name, name, EntityKind.VARIABLE)))
        stream.add(SimulationEnd(time=times[-1], completed=True))
        return ExecutionResult(backend=self.name, status=ExecutionStatus.SUCCESS,
            phase=ExecutionPhase.FINALIZATION, observations=stream,
            trace=Trace(times=times, columns=columns), backend_metadata=metadata)

    def _failure(self, text, metadata):
        # SPEC_0008 / native SimulationDiagnosticError: EX001 is solver runtime;
        # ED/EL/ES and EX002/EX003 are compiler/preparation/override refusals.
        clean = re.sub(r"\x1b\[[0-9;]*m", "", text)
        marker = "[EX001]"
        if marker not in clean:
            result = self._error(clean.strip() or "native source process failed without diagnostics")
            result.backend_metadata = metadata
            return result
        message = clean.rsplit(marker, 1)[1].strip()
        kind = FailureKind.ASSERTION_VIOLATED if "Modelica assert failed" in message else classify(message)
        failure = ExecutionFailure(kind=kind, phase=ExecutionPhase.SIMULATION,
                                   message=message[:200], raw=message)
        stream = ObservationStream()
        stream.add(SolverFailure(kind=kind, reason=failure.message, raw=message))
        stream.add(SimulationEnd(completed=False, message=failure.message))
        return ExecutionResult(backend=self.name, status=ExecutionStatus.FAILED,
            phase=failure.phase, observations=stream, failure=failure, backend_metadata=metadata)

    def _error(self, message, **metadata):
        result = ExecutionResult.backend_error(self.name, message)
        result.backend_metadata = {**self._metadata, **metadata}
        return result

    def close(self):
        if self._work is not None:
            self._work.cleanup()
        self._work, self._source = None, None
        self._model_name, self._metadata, self._run_index = "", {}, 0


def _timeout_output(error):
    return "".join(value.decode(errors="replace") if isinstance(value, bytes) else value or ""
                   for value in (error.stdout, error.stderr))
