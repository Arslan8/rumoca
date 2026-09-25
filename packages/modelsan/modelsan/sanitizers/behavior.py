"""BehaviorSan checks explicit, reusable trace contracts with provenance."""
from __future__ import annotations

from ..contracts.trace import Signals, Unavailable
from ..findings.finding import Finding, Severity
from ..instrumentation.capability import Capability


class BehaviorSan:
    name = 'behavior'
    requires = {'runtime': frozenset({Capability.OBSERVE_VARIABLE})}

    def __init__(self, contracts):
        self.contracts = tuple(contracts)
        ids = [contract.contract_id for contract in self.contracts]
        if len(set(ids)) != len(ids):
            raise ValueError('behavioral contract ids must be unique')

    def observe(self, stream, model, context, testcase):
        signals = Signals(stream)
        findings = []
        for contract in self.contracts:
            evidence = dict(contract_id=contract.contract_id, origin=contract.origin,
                            contract_type=type(contract).__name__, atol=contract.atol,
                            rtol=contract.rtol, authority='explicit contract')
            try:
                verdict = contract.evaluate(signals)
            except Unavailable as error:
                findings.append(Finding(self.name, 'contract-unobserved', Severity.INFO,
                    test_case=testcase, evidence={**evidence, 'reason': str(error),
                    'detection': False, 'note': 'coverage gap, not a model defect'}))
                continue
            if verdict.witness is None:
                continue
            rows = signals.rows.get(contract.actual, [])
            anchor = rows[0] if rows else None
            findings.append(Finding(self.name, 'contract-violation', Severity.HIGH,
                canonical_anchors=[anchor.canonical] if anchor and anchor.canonical else [],
                backend_anchors=[anchor.backend] if anchor and anchor.backend else [],
                time=verdict.witness.get('time'), test_case=testcase,
                evidence={**evidence, **verdict.witness, 'checked_samples': verdict.checked,
                          'detection': True}))
        return findings
