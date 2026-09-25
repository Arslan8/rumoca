"""Domain evidence must come from reached native operations, not guessed zeros."""
from pathlib import Path
import tempfile
import unittest

from rumoca_bitcode.execution import lower
from modelsan.analysis.context import AnalysisContext
from modelsan.backends.rumoca import RumocaBackend
from modelsan.findings.finding import Severity
from modelsan.fuzz.testcase import NOMINAL, TestCase as Case
from modelsan.runtime.observations import ExpressionObservation
from modelsan.sanitizers.domain import DomainSan
from test_current_bitcode import decay, RUMOCA


class NativeDomain(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.path = Path(self.tmp.name) / "program.rbc"
        self.model = decay()
        self.backend = RumocaBackend(RUMOCA, t_end=.2)
        self.addCleanup(self.backend.close)

    def run_program(self, instructions, case=NOMINAL):
        program = lower(self.model)
        program.numerical["derivatives"][0]["instructions"] = instructions
        program.save(self.path)
        original = self.path.read_bytes()
        self.assertIsNone(self.backend.prepare_from_artifact(self.path))
        result = self.backend.run(case)
        self.assertEqual(original, self.path.read_bytes())
        findings = DomainSan().observe(result.observations, self.model,
                                       AnalysisContext(self.model), case)
        return result, findings

    def reciprocal(self):
        return [{"op": "const", "dst": 0, "value": 1.},
                {"op": "load_p", "dst": 1, "index": 0},
                {"op": "binary", "dst": 2, "operator": "Div", "lhs": 0, "rhs": 1}]

    def test_zero_denominator_is_recorded_before_first_physical_sample(self):
        result, findings = self.run_program(self.reciprocal() + [{"op": "store_output", "src": 2}],
                                            Case(parameters={"k": 0.}))
        self.assertFalse(result.ok)
        self.assertIsNone(result.trace)
        self.assertEqual([f.kind for f in findings], ["division-out-of-domain"])
        self.assertEqual(findings[0].evidence["operand_value"], 0.)
        self.assertEqual(findings[0].canonical_anchors, [])
        self.assertTrue(findings[0].backend_anchors)
        self.assertEqual(findings[0].evidence["coordinates"], "internal-evaluation")

    def test_zero_on_an_inactive_branch_is_not_a_violation(self):
        code = self.reciprocal() + [
            {"op": "const", "dst": 3, "value": 0.},
            {"op": "compare", "dst": 4, "operator": "Ne", "lhs": 1, "rhs": 3},
            {"op": "select", "dst": 5, "cond": 4, "if_true": 2, "if_false": 3},
            {"op": "store_output", "src": 5}]
        result, findings = self.run_program(code, Case(parameters={"k": 0.}))
        self.assertTrue(result.ok, result.failure)
        self.assertEqual(findings, [])
        self.assertEqual(result.trace.final_state["x"], 2.)
        self.assertEqual(result.backend_metadata["domain_diagnostics"]["faults"], [])

    def test_nonzero_denominator_is_not_a_violation(self):
        result, findings = self.run_program(self.reciprocal() + [{"op": "store_output", "src": 2}])
        self.assertTrue(result.ok, result.failure)
        self.assertAlmostEqual(result.trace.final_state["x"], 2.2)
        self.assertEqual(findings, [])

    def test_recovered_internal_evaluation_is_informational(self):
        code = self.reciprocal() + [
            {"op": "compare", "dst": 3, "operator": "Gt", "lhs": 2, "rhs": 0},
            {"op": "select", "dst": 4, "cond": 3, "if_true": 0, "if_false": 1},
            {"op": "store_output", "src": 4}]
        result, findings = self.run_program(code, Case(parameters={"k": 0.}))
        self.assertTrue(result.ok, result.failure)
        self.assertEqual([f.kind for f in findings], ["division-domain-trial"])
        self.assertEqual(findings[0].severity, Severity.INFO)

    def test_scope_is_reset_between_failed_and_successful_runs(self):
        code = self.reciprocal() + [{"op": "store_output", "src": 2}]
        result, _ = self.run_program(code, Case(parameters={"k": 0.}))
        self.assertFalse(result.ok)
        result = self.backend.run(NOMINAL)
        self.assertTrue(result.ok, result.failure)
        self.assertEqual(list(result.observations.of(ExpressionObservation)), [])
        self.assertEqual(result.backend_metadata["domain_diagnostics"]["faults"], [])

    def test_sqrt_negative_argument_is_reported(self):
        result, findings = self.run_program([
            {"op": "const", "dst": 0, "value": -1.},
            {"op": "unary", "dst": 1, "operator": "Sqrt", "src": 0},
            {"op": "store_output", "src": 1}])
        self.assertFalse(result.ok)
        self.assertEqual([f.kind for f in findings], ["sqrt-out-of-domain"])

    def test_equation_input_uses_the_same_native_diagnostics(self):
        from rumoca_bitcode import Model
        model = Model.empty("Reciprocal")
        b = model.builder("test")
        x, p = b.add_state("x", 2.), b.add_parameter("p", 1.)
        model.raw_model["variables"][p]["tunable"] = True
        b.add_derivative_equation(x, b.div(b.real(1.), b.ref(p)))
        b.finish()
        model.save(self.path)
        self.assertIsNone(self.backend.prepare_from_artifact(self.path))
        result = self.backend.run(Case(parameters={"p": 0.}))
        self.assertFalse(result.ok)
        findings = DomainSan().observe(result.observations, model, AnalysisContext(model), NOMINAL)
        self.assertEqual([f.kind for f in findings], ["division-out-of-domain"])

    def test_diagnostics_preserve_ordinary_native_trajectory(self):
        import json
        from rumoca_bitcode.compiler import invoke
        program = lower(self.model)
        program.save(self.path)
        ordinary = Path(self.tmp.name) / "ordinary.json"
        invoke("bitcode", "run", self.path, "--stop", ".2",
               "--trace-root", Path(self.tmp.name) / "ordinary-traces", "--result", ordinary,
               executable=RUMOCA)
        self.assertIsNone(self.backend.prepare_from_artifact(self.path))
        observed = self.backend.run(NOMINAL)
        self.assertTrue(observed.ok, observed.failure)
        payload = json.loads(ordinary.read_text())
        self.assertEqual(observed.trace.times, payload["times"])
        for actual, expected in zip(observed.trace.columns["x"], payload["data"][0]):
            self.assertAlmostEqual(actual, expected, places=12)
