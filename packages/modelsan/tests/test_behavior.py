"""Positive/negative controls and evidence boundaries for behavioral contracts."""
import math
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[3]
sys.path[:0] = [str(ROOT/'packages/modelsan'), str(ROOT/'packages/rumoca-bitcode')]

from modelsan.contracts.trace import Cardinality, Equality, PeriodicPulse, SampleDelay, from_dict
from modelsan.findings.signature import attach
from modelsan.fuzz.testcase import NOMINAL
from modelsan.pipeline import RunOutcome
from modelsan.runtime.anchors import BackendAnchor
from modelsan.runtime.observations import (
    ObservationStream, SimulationAbort, SimulationEnd,
    UnorderedVariableObservation, VariableObservation,
)
from modelsan.sanitizers.behavior import BehaviorSan
from modelsan.sanitizers.numeric import NumericSan

ORIGIN = dict(contract_id='documented-property', origin='test component API')


def stream(times, columns, complete=True):
    result = ObservationStream()
    for name, values in columns.items():
        for time, value in zip(times, values):
            result.add(VariableObservation(time=time, value=value,
                       backend=BackendAnchor('test-backend', name)))
    result.add(SimulationEnd(completed=complete))
    return result


def observe(contract, observations):
    return BehaviorSan([contract]).observe(observations, None, None, NOMINAL)


class BehaviorTests(unittest.TestCase):
    def test_unordered_values_establish_cardinality_but_never_timing(self):
        data = ObservationStream()
        for index, (time, value) in enumerate([(0,0), (10,1), (2,2), (1,3), (5,4)]):
            for name in ['q', 'u']:
                data.add(UnorderedVariableObservation(value=value, reported_time=time,
                    row_index=index, backend=BackendAnchor('test-backend', name)))
        data.add(SimulationEnd(completed=True))
        contract = Cardinality(actual='q', maximum=4, **ORIGIN)
        finding = observe(contract, data)[0]
        self.assertEqual(finding.kind, 'contract-violation')
        self.assertEqual(finding.evidence['observed_count_lower_bound'], 5)
        self.assertEqual(finding.evidence['sample_order'], 'unordered')
        self.assertIsNone(finding.time)
        self.assertEqual(finding.evidence['reported_time'], 5)
        self.assertEqual(observe(Cardinality(actual='q', maximum=5, **ORIGIN), data), [])
        for temporal in [Equality(actual='q', expected='u', **ORIGIN),
                         PeriodicPulse(actual='q', period=1, start=0, **ORIGIN),
                         SampleDelay(actual='q', input='u', period=1, **ORIGIN)]:
            self.assertEqual(observe(temporal, data)[0].kind, 'contract-unobserved')

    def test_unordered_samples_still_require_complete_valid_provenance(self):
        contract = Cardinality(actual='q', maximum=1, **ORIGIN)
        for override in [dict(reported_time=math.nan), dict(row_index=-1), dict(time=2)]:
            fields = dict(value=1, reported_time=0, row_index=0,
                          backend=BackendAnchor('test-backend', 'q'))
            fields.update(override)
            data = ObservationStream([UnorderedVariableObservation(**fields),
                                      SimulationEnd(completed=True)])
            self.assertEqual(observe(contract, data)[0].kind, 'contract-unobserved')
        data = ObservationStream([UnorderedVariableObservation(value=1, reported_time=0,
            row_index=0, backend=BackendAnchor('test-backend', 'q')),
            SimulationEnd(completed=False)])
        self.assertEqual(observe(contract, data)[0].kind, 'contract-unobserved')

    def test_numeric_finding_from_unordered_values_has_no_invented_time(self):
        data = ObservationStream([UnorderedVariableObservation(value=math.inf,
            reported_time=2, row_index=4, backend=BackendAnchor('test-backend', 'q')),
            SimulationEnd(completed=True)])
        finding = NumericSan().observe(data, None, None, NOMINAL)[0]
        self.assertEqual(finding.kind, 'inf')
        self.assertIsNone(finding.time)
        self.assertEqual(finding.evidence['sample_order'], 'unordered')
        self.assertEqual(finding.evidence['row_index'], 4)

    def test_equality_and_backend_provenance(self):
        contract = Equality(actual='temperature', expected='original', **ORIGIN)
        self.assertEqual(observe(contract, stream([0, 1], {'temperature':[300,301], 'original':[300,301]})), [])
        found = observe(contract, stream([0, 1], {'temperature':[327,328], 'original':[300,301]}))
        self.assertEqual(found[0].kind, 'contract-violation')
        self.assertEqual(found[0].evidence['expected'], 300)
        self.assertEqual(found[0].evidence['origin'], ORIGIN['origin'])
        self.assertFalse(found[0].canonical_anchors)
        self.assertEqual(found[0].backend_anchors[0].backend, 'test-backend')

    def test_unsynchronized_events_are_not_compared_by_index(self):
        contract = Equality(actual='a', expected='b', **ORIGIN)
        data = stream([0, 1], {'a':[1,2], 'b':[1,2]})
        data.observations[2].time = .1
        self.assertEqual(observe(contract, data)[0].kind, 'contract-unobserved')

    def test_empty_truncated_and_nonfinite_evidence_is_unobserved(self):
        contract = Equality(actual='a', expected='b', **ORIGIN)
        cases = [stream([], {}), stream([0], {'a':[1],'b':[1]}, False),
                 stream([0], {'a':[1]}), stream([0], {'a':[math.nan],'b':[1]}),
                 stream([1,0], {'a':[1,2],'b':[1,2]})]
        for data in cases:
            with self.subTest(data=data):
                finding = observe(contract, data)[0]
                self.assertEqual(finding.kind, 'contract-unobserved')
                self.assertFalse(finding.evidence['detection'])

    def test_period_equivalent_pulse_starts(self):
        for start in [-.25, -1.25]:
            contract = PeriodicPulse(actual='pulse', period=1, start=start, **ORIGIN)
            self.assertEqual(observe(contract, stream([.1,.3,.9], {'pulse':[1,0,1]})), [])
        found = observe(contract, stream([.1,.3,.9], {'pulse':[0,0,1]}))
        self.assertEqual(found[0].evidence['expected'], 1)

    def test_pulse_event_sides_do_not_create_false_positive(self):
        contract = PeriodicPulse(actual='pulse', period=1, start=0, **ORIGIN)
        self.assertEqual(observe(contract, stream([0,0,.1,.5,.5,.6], {'pulse':[0,1,1,1,0,0]})), [])
        self.assertEqual(observe(contract, stream([0,.5,1], {'pulse':[1,0,1]}))[0].kind, 'contract-unobserved')

    def test_pulse_before_start(self):
        contract = PeriodicPulse(actual='pulse', period=1, start=2, **ORIGIN)
        self.assertEqual(observe(contract, stream([.1,.6], {'pulse':[0,0]})), [])
        self.assertEqual(observe(contract, stream([.1,.6], {'pulse':[1,0]}))[0].kind, 'contract-violation')

    def test_previous_sample_delay_not_current_sample(self):
        contract = SampleDelay(actual='y', input='u', period=.05, **ORIGIN)
        times = [0,.025,.05,.075,.1,.125,.15,.175]
        source = [math.sin(2*math.pi*t) for t in times]
        delayed = [0,0,0,0,source[2],source[2],source[4],source[4]]
        current = [source[2*(i//2)] for i in range(len(times))]
        self.assertEqual(observe(contract, stream(times, {'u':source,'y':delayed})), [])
        self.assertEqual(observe(contract, stream(times, {'u':source,'y':current}))[0].kind, 'contract-violation')

    def test_delay_missing_sample_or_discontinuous_input(self):
        contract = SampleDelay(actual='y', input='u', period=1, **ORIGIN)
        for data in [stream([.5,1.5], {'u':[0,1], 'y':[0,0]}),
                     stream([0,0,.5,1.5], {'u':[0,1,1,2], 'y':[0,0,0,1]})]:
            self.assertEqual(observe(contract, data)[0].kind, 'contract-unobserved')

    def test_cardinality_with_roundoff_and_extra_level(self):
        contract = Cardinality(actual='q', maximum=4, **ORIGIN)
        self.assertEqual(observe(contract, stream([0,1,2,3,4], {'q':[-1,-.5,0,.5,.5+1e-10]})), [])
        found = observe(contract, stream([0,1,2,3,4], {'q':[-1,-.5,0,.5,1]}))
        self.assertEqual(found[0].evidence['observed_count_lower_bound'], 5)

    def test_cardinality_accepts_jitter_on_both_sides_of_one_level(self):
        contract = Cardinality(actual='q', maximum=1, atol=.1, rtol=0, **ORIGIN)
        self.assertEqual(observe(contract, stream([0,1], {'q':[-.09,.09]})), [])
        self.assertEqual(observe(contract, stream([0,1], {'q':[-.11,.11]}))[0].kind, 'contract-violation')

    def test_multiple_lifecycles_and_rows_after_end_are_not_merged(self):
        contract = Cardinality(actual='q', maximum=1, **ORIGIN)
        for extra in [SimulationEnd(completed=True),
                      VariableObservation(time=2, value=2, backend=BackendAnchor('test-backend','q'))]:
            data = stream([0], {'q':[1]})
            data.add(extra)
            self.assertEqual(observe(contract, data)[0].kind, 'contract-unobserved')

    def test_aborted_execution_cannot_claim_completed_behavior(self):
        data = stream([0,1], {'q':[0,1]})
        data.observations.insert(-1, SimulationAbort())
        contract = Cardinality(actual='q', maximum=1, **ORIGIN)
        self.assertEqual(observe(contract, data)[0].kind, 'contract-unobserved')

    def test_overflow_in_derived_schedule_is_unobserved(self):
        contract = PeriodicPulse(actual='q', period=1, start=-1e308, **ORIGIN)
        self.assertEqual(observe(contract, stream([1e308], {'q':[1]}))[0].kind, 'contract-unobserved')
        contract = SampleDelay(actual='q', input='u', period=1e-300, **ORIGIN)
        self.assertEqual(observe(contract, stream([1e308], {'q':[1],'u':[1]}))[0].kind, 'contract-unobserved')

    def test_contract_ids_prevent_distinct_properties_collapsing(self):
        observations = stream([0], {'a':[5], 'b':[1], 'c':[2]})
        contracts = [Equality(actual='a', expected='b', contract_id='one', origin='API'),
                     Equality(actual='a', expected='c', contract_id='two', origin='API')]
        found = attach(BehaviorSan(contracts).observe(observations, None, None, NOMINAL))
        self.assertNotEqual(found[0].signature, found[1].signature)

    def test_missing_contract_observations_enter_coverage(self):
        contract = Cardinality(actual='q', maximum=4, **ORIGIN)
        outcome = RunOutcome('example')
        outcome.database.extend(attach(observe(contract, stream([], {}))))
        self.assertIn('behavior.contract.documented-property', outcome.coverage)

    def test_configuration_rejects_invalid_or_unknown_rules(self):
        with self.assertRaises(ValueError):
            from_dict(dict(kind='arbitrary_python', **ORIGIN))
        for arguments in [dict(period=0, start=0), dict(period=1, start=math.inf),
                          dict(period=1, start=0, duty=2)]:
            with self.assertRaises(ValueError):
                PeriodicPulse(actual='p', **arguments, **ORIGIN)
        with self.assertRaises(ValueError):
            Equality(actual='a', expected='b', rtol=-1, **ORIGIN)
        contract = Cardinality(actual='q', maximum=4, **ORIGIN)
        with self.assertRaises(ValueError):
            BehaviorSan([contract,contract])


if __name__ == '__main__':
    unittest.main()
