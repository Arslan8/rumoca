"""Saved-program experiment configuration must not erase executable edits."""
from copy import deepcopy
import math
from pathlib import Path
import tempfile
import unittest

from rumoca_bitcode import Model
from rumoca_bitcode.execution import lower
from modelsan.backends.rumoca import RumocaBackend
from modelsan.backends.base import ExecutionStatus
from modelsan.fuzz.testcase import NOMINAL, TestCase as Case
from test_current_bitcode import decay, user_logger, RUMOCA


class Configuration(unittest.TestCase):
    def setUp(self):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        self.path = Path(tmp.name) / "saved.rbc"
        self.backend = RumocaBackend(RUMOCA, t_end=.2, timeout=10)
        self.addCleanup(self.backend.close)

    def prepare(self, program):
        program.save(self.path)
        self.assertIsNone(self.backend.prepare_from_artifact(self.path))

    def test_parameters_and_starts_are_per_run(self):
        self.prepare(lower(decay()))
        before = self.path.read_bytes()
        result = self.backend.run(Case(parameters={"k": 2.}, initial_values={"x": 3.}))
        self.assertTrue(result.ok, result.failure)
        self.assertAlmostEqual(result.trace.columns["x"][0], 3.)
        self.assertAlmostEqual(result.trace.final_state["x"], 3 * math.exp(-.4), delta=1e-7)
        nominal = self.backend.run(NOMINAL)
        self.assertTrue(nominal.ok, nominal.failure)
        self.assertAlmostEqual(nominal.trace.final_state["x"], 2 * math.exp(-.2), delta=1e-7)
        self.assertEqual(self.path.read_bytes(), before)

    def test_overrides_preserve_numerical_edits_and_user_effects(self):
        program = lower(decay())
        program.numerical["derivatives"][0]["instructions"] = [
            {"op": "const", "dst": 0, "value": -3.}, {"op": "store_output", "src": 0}]
        user_logger(program)
        self.prepare(program)
        result = self.backend.run(Case(parameters={"k": 2.}, initial_values={"x": 3.}))
        self.assertTrue(result.ok, result.failure)
        self.assertAlmostEqual(result.trace.final_state["x"], 2.4, delta=1e-7)
        self.assertTrue((Path(result.backend_metadata["trace_root"]) / "user.csv").exists())

    def test_invalid_overrides_are_not_model_bugs(self):
        self.prepare(lower(decay()))
        for case in [Case(parameters={"x": 2}), Case(parameters={"k": float("nan")}),
                     Case(initial_values={"k": 3}), Case(initial_values={"x": float("inf")})]:
            result = self.backend.run(case)
            self.assertEqual(result.status, ExecutionStatus.BACKEND_ERROR, result.failure)
            self.assertFalse(result.informative)

    def test_dependent_parameter_cannot_silently_keep_frozen_value(self):
        model = decay()
        b = model.builder("dependent")
        q = b.add_parameter("q", 2.)
        # Compiler-folded binding retains its semantic dependency contract.
        model.raw_model["variables"][q]["contract"] = {
            "variability": "parameter", "binding_depends_on": [b.variable("k")]}
        b.finish()
        self.prepare(lower(model))
        result = self.backend.run(Case(parameters={"k": 2.}))
        self.assertEqual(result.status, ExecutionStatus.BACKEND_ERROR)
        self.assertIn("dependent", result.failure.message)

    def test_explicit_replay_fills_missing_observations_and_preserves_recipes(self):
        program = lower(decay(), observe=[1])  # Only parameter k; state x is missing.
        user_logger(program)
        original = deepcopy(program.raw)
        program.save(self.path)
        self.assertIsNotNone(self.backend.prepare_from_artifact(self.path))
        self.backend.replay = {"test.user-logging": lambda p, m: user_logger(p)}
        self.assertIsNone(self.backend.prepare_from_artifact(self.path))
        result = self.backend.run(NOMINAL)
        self.assertTrue(result.ok, result.failure)
        self.assertIn("x", result.trace.columns)
        self.assertTrue((Path(result.backend_metadata["trace_root"]) / "user.csv").exists())
        self.assertEqual(Model.load(self.path)._document["execution"]["numerical"], original["numerical"])

    def test_missing_replay_implementation_is_refused(self):
        program = lower(decay(), observe=[1])
        user_logger(program)
        program.save(self.path)
        self.backend.replay = {}
        failure = self.backend.prepare_from_artifact(self.path)
        self.assertEqual(failure.status, ExecutionStatus.BACKEND_ERROR)
        self.assertIn("no compatible replay", failure.failure.message)

    def test_explicit_initialization_owner_is_not_discarded(self):
        program = lower(decay())
        program.numerical["initialization"] = [{"output": 0, "target": 0, "instructions": [
            {"op": "load_y", "dst": 0, "index": 0},
            {"op": "const", "dst": 1, "value": 2.},
            {"op": "binary", "dst": 2, "operator": "Sub", "lhs": 0, "rhs": 1},
            {"op": "store_output", "src": 2}]}]
        program.numerical["initial_blocks"] = [{"rows": [0], "unknowns": [0]}]
        self.prepare(program)
        result = self.backend.run(Case(initial_values={"x": 4.}))
        self.assertEqual(result.status, ExecutionStatus.BACKEND_ERROR)
        self.assertIn("explicit initialization owner", result.failure.message)

    def test_structural_parameter_and_duplicate_cli_override_are_refused(self):
        from rumoca_bitcode.compiler import invoke
        model = decay()
        model.raw_model["variables"][1]["tunable"] = False
        self.prepare(lower(model))
        result = self.backend.run(Case(parameters={"k": 2.}))
        self.assertEqual(result.status, ExecutionStatus.BACKEND_ERROR)
        with self.assertRaisesRegex(ValueError, "duplicate override"):
            invoke("bitcode", "run", self.path, "--trace-root", self.path.parent / "trace",
                   "--initial", "x=2", "--initial", "x=3", executable=RUMOCA)
