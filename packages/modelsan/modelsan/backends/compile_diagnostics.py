"""Only typed, source-backed compiler proofs can establish a model defect.

An unsupported construct, an arbitrary compile error, or prose resembling a
bounds failure never earns model-detection credit.
"""
from __future__ import annotations

import json
from pathlib import Path

from .base import ExecutionResult, ExecutionStatus
from ..runtime.failures import ExecutionFailure, ExecutionPhase, FailureKind
from ..runtime.observations import CompilationFailure, ObservationStream


def source_labels(diagnostic):
    """Resolved source coordinates, never a guessed filename or synthetic span."""
    return [label for label in diagnostic.get('labels', [])
            if isinstance(label, dict) and isinstance(label.get('file'), str)
            and label['file'] and type(label.get('line')) is int and label['line'] > 0
            and type(label.get('column')) is int and label['column'] > 0]


def proven_model_failure(path: Path, backend: str):
    if not path.is_file():
        return None
    report = json.loads(path.read_text())
    if not isinstance(report, dict) or report.get('schema') != 1:
        raise ValueError('unsupported compiler diagnostic report')
    diagnostics = report.get('diagnostics')
    if not isinstance(diagnostics, list):
        raise ValueError('compiler report has no diagnostic list')
    if report.get('status') != 'failed':
        return None
    matches = [d for d in diagnostics if isinstance(d, dict) and d.get('code') == 'EF032']
    if not matches:
        return None
    stream = ObservationStream()
    for diagnostic in matches:
        message = diagnostic.get('message')
        labels = diagnostic.get('labels')
        if (not isinstance(message, str) or not message
                or not isinstance(labels, list) or not source_labels(diagnostic)):
            raise ValueError('constant bounds proof is missing source evidence')
        stream.add(CompilationFailure(kind=FailureKind.ARRAY_BOUNDS, reason=message,
            raw=message, diagnostic=diagnostic))
    first = stream.observations[0]
    return ExecutionResult(backend, ExecutionStatus.FAILED,
        phase=ExecutionPhase.COMPILATION, observations=stream,
        failure=ExecutionFailure(FailureKind.ARRAY_BOUNDS, ExecutionPhase.COMPILATION,
                                 first.reason, first.raw),
        backend_metadata={'compiler_diagnostics': report, 'proof_stage':'constant-evaluation'})
