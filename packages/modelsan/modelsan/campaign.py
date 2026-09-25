"""Run a declared behavioral campaign through the normal ModelSan pipeline."""
from __future__ import annotations

from dataclasses import asdict, is_dataclass
from enum import Enum
import hashlib
import json
import math
from pathlib import Path

from .backends.base import ExecutionStatus
from .runtime.failures import ExecutionPhase
from .contracts.trace import from_dict
from .pipeline import Pipeline
from .sanitizers import BehaviorSan, NumericSan, SanitizerRegistry, SolverSan


def plain(value):
    if is_dataclass(value):
        return plain(asdict(value))
    if isinstance(value, Enum):
        return value.value
    if isinstance(value, dict):
        return {str(k): plain(v) for k, v in value.items()}
    if isinstance(value, (list, tuple)):
        return [plain(v) for v in value]
    if isinstance(value, float) and not math.isfinite(value):
        return str(value)
    return value


def _status(outcome, findings):
    result = outcome.results[-1] if outcome.results else None
    if result is None or result.status is ExecutionStatus.BACKEND_ERROR:
        return 'blocked'
    if result.status in (ExecutionStatus.TIMEOUT, ExecutionStatus.ABORTED):
        return 'inconclusive'
    if result.status is ExecutionStatus.FAILED:
        if result.phase is ExecutionPhase.COMPILATION:
            return 'model-rejected'
        return 'execution-failed'
    if any(f.kind == 'contract-violation' for f in findings):
        return 'violated'
    if any(f.kind == 'contract-unobserved' for f in findings):
        return 'unobserved'
    if any(f.severity.value == 'high' for f in findings):
        return 'violation'
    return 'no-violation-observed'


def load_campaign(path):
    path = Path(path).resolve()
    data = json.loads(path.read_text())
    if data.get('schema') != 1 or not isinstance(data.get('cases'), list) or not data['cases']:
        raise ValueError('campaign requires schema=1 and nonempty cases')
    source = (path.parent/data['source']).resolve()
    if not source.is_file():
        raise ValueError(f'campaign source is unavailable: {source}')
    seen, cases = set(), []
    for item in data['cases']:
        name = item['model']
        if not isinstance(name, str) or not name.strip() or name in seen:
            raise ValueError('campaign model names must be nonempty and unique')
        if not isinstance(item.get('contracts'), list):
            raise ValueError('each case must declare its contracts (possibly empty)')
        contracts = [from_dict(c) for c in item['contracts']]
        BehaviorSan(contracts)  # Validate all cases before any execution starts.
        cases.append((name, contracts))
        seen.add(name)
    return source, cases


def run_case(backend, source, name, contracts):
    registry = SanitizerRegistry()
    for sanitizer in (BehaviorSan(contracts), NumericSan(), SolverSan()):
        registry.register(sanitizer)
    try:
        outcome = Pipeline(registry, backend).run(None, str(source), name)
        findings = [f for bug in outcome.database.bugs for f in bug.findings]
        return dict(model=name, backend=backend.name, status=_status(outcome, findings),
            contracts=[plain(c) for c in contracts], findings=plain(findings),
            coverage=outcome.coverage, note=outcome.note,
            executions=[dict(status=r.status.value, phase=r.phase.value,
                failure=plain(r.failure), metadata=plain(r.backend_metadata),
                trace=plain(r.trace)) for r in outcome.results])
    finally:
        backend.close()


def run_campaign(path, backend_factory, output=None, progress=None, provenance=None):
    source, cases = load_campaign(path)
    report = dict(schema=1, campaign=str(Path(path).resolve()), source=str(source),
        campaign_sha256=hashlib.sha256(Path(path).read_bytes()).hexdigest(),
        source_sha256=hashlib.sha256(source.read_bytes()).hexdigest(),
        provenance=provenance or {}, cases=[])
    for name, contracts in cases:
        if progress:
            progress(name)
        report['cases'].append(run_case(backend_factory(), source, name, contracts))
        if output:
            Path(output).write_text(json.dumps(report, indent=2, allow_nan=False)+'\n')
    return report
