"""Native, fresh-process acceptance tests (requires built rumoca via RUMOCA).

Run: PYTHONPATH=packages/rumoca-bitcode:new_inst RUMOCA=target/debug/rumoca
     python3 -m unittest discover -s new_inst -p test_execution.py -v
"""
from copy import deepcopy
import csv
import json
import os
from pathlib import Path
import subprocess
import tempfile
import unittest

from rumoca_bitcode import Model
from rumoca_bitcode.compiler import compiler, invoke
from rumoca_bitcode.execution import Program, lower
from synthesize_connector_csv import synthesize, scale_conductor_equation, instrument_all_connectors
from check_thermal_csv import verify


class ExecutionAcceptance(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        model, handles = synthesize()
        cls.base = deepcopy(model._document)
        cls.handles = handles

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(prefix="rbc-execution-test-")
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.model = Model(deepcopy(self.base))

    def program(self, scale=2):
        scale_conductor_equation(self.model, self.handles, scale)
        observed = [m.variable_id for c in self.model.connectors for m in c.members]
        return lower(self.model, observe=observed)

    def run_program(self, p, label="run"):
        artifact = self.root / f"{label}.rbc"
        p.save(artifact)
        # Only a native CLI process reads the artifact; no Python pass module.
        result = self.root / f"{label}.json"
        invoke("bitcode", "run", artifact, "--execution", "require", "--trace-root", self.root / label, "--result", result)
        return json.loads(result.read_text())

    def test_scales_fresh_process_and_neutrality(self):
        for scale in (1, 2):
            with self.subTest(scale=scale):
                p = self.program(scale)
                baseline = self.run_program(p, f"baseline-{scale}")
                instrument_all_connectors(p, self.model)
                logged = self.run_program(p, f"logged-{scale}")
                self.assertEqual(baseline, logged)
                self.assertEqual(verify(self.root / f"logged-{scale}", scale)["total_rows"], 204)

    def test_stale_builder_rewrite_and_explicit_replay(self):
        p = self.program(1)
        instrument_all_connectors(p, self.model)
        scale_conductor_equation(self.model, self.handles, 2)
        with self.assertRaisesRegex(ValueError, "stale execution"):
            p.validate()
        with self.assertRaisesRegex(ValueError, "no compatible replay"):
            p.relower()
        fresh = p.relower(replay={"example.connector-csv": instrument_all_connectors})
        self.run_program(fresh)
        verify(self.root / "run", 2)

    def test_raw_mutation_stale_at_native_boundary(self):
        p = self.program()
        artifact = self.root / "raw.json"
        p.save(artifact)
        document = Model.load(artifact)
        document.raw_model["variables"][0]["unit"] = "changed"
        document.save(artifact)
        with self.assertRaisesRegex(ValueError, "stale execution"):
            invoke("bitcode", "check-execution", artifact)
        with self.assertRaisesRegex(ValueError, "stale execution"):
            invoke("bitcode", "run", artifact, "--trace-root", self.root / "forbidden")
        self.assertFalse((self.root / "forbidden").exists())

    def test_duplicate_pass_rejected(self):
        p = self.program()
        instrument_all_connectors(p, self.model)
        with self.assertRaisesRegex(ValueError, "duplicate execution pass"):
            instrument_all_connectors(p, self.model)

    def test_default_observation_includes_static_parameters(self):
        p = lower(self.model)
        self.assertEqual(len(p.numerical["observations"]), 13)
        p.validate()

    def test_effect_order_and_csv_quoting(self):
        p = self.program()
        b = p.builder("test.ordered-effects")
        sink = b.declare_csv_sink(key="ordered", filename="ordered.csv", columns=['value,"quoted"'], column_types=["real"], metadata={})
        with b.before_return(p.function("run_start")) as ir:
            ir.emit("csv.open", sink=sink)
        with b.before_return(p.function("publish")) as ir:
            for n in (2.0, 1.0):
                value = ir.emit("compute", arguments=[], instructions=[{"op": "const", "dst": 0, "value": n}, {"op": "store_output", "src": 0}])
                ir.emit("csv.write_row", sink=sink, values=[value])
        with b.before_return(p.function("run_finish")) as ir:
            ir.emit("csv.close", sink=sink)
        self.run_program(p)
        with (self.root / "run" / "ordered.csv").open(newline="") as stream:
            rows = list(csv.reader(stream))
        self.assertEqual(rows[0], ['value,"quoted"'])
        self.assertEqual([float(row[0]) for row in rows[1:]], [2.0, 1.0] * 51)

    def test_unsupported_shapes_and_connector_metadata_rejected(self):
        b = self.model.builder("test.unsupported")
        with self.assertRaisesRegex(ValueError, "unsupported-feature"):
            b.add_connector_type("ArrayPort", members=[{"name": "x", "scalar_type": "real", "kind": "flow", "shape": [2]}])
        self.model.raw_model["connectors"][0]["members"][0]["variable"] = 999999
        with self.assertRaisesRegex(ValueError, "connector"):
            self.model.validate()

    def test_invalid_operations_types_and_lifecycles(self):
        p = self.program()
        instrument_all_connectors(p, self.model)
        original = deepcopy(p.raw)
        mutations = [
            lambda: p.function("run_start").append({"op": "snapshot.time", "result": "illegal"}),
            lambda: p.function("publish").append({"op": "assert", "condition": "undefined", "message": "bad"}),
            lambda: p.function("publish").append({"op": "compute", "result": "bad", "arguments": ["v2"], "instructions": [{"op": "load_y", "dst": 0, "index": 0}, {"op": "store_output", "src": 0}]}),
            lambda: p.numerical["derivatives"][0]["instructions"].append({"op": "binary", "dst": 999, "operator": "Add", "lhs": 999, "rhs": 998}),
            lambda: p.function("run_finish").clear(),
            lambda: p.raw["sinks"][0].update(filename="../escape.csv"),
            lambda: p.function("publish").append({"op": "unknown.operation"}),
        ]
        for mutate in mutations:
            p.raw = deepcopy(original)
            mutate()
            with self.assertRaises(ValueError):
                p.validate()

    def test_backend_and_no_overwrite(self):
        p = self.program()
        path = self.root / "artifact.rbc"
        p.save(path)
        with self.assertRaisesRegex(ValueError, "unsupported execution mode/backend"):
            invoke("bitcode", "run", path, "--backend", "other", "--trace-root", self.root / "no")
        self.run_program(p)
        with self.assertRaisesRegex(ValueError, "trace directory must be new"):
            invoke("bitcode", "run", path, "--trace-root", self.root / "run")
        with self.assertRaisesRegex(ValueError, "discard executable edits"):
            invoke("compile-bitcode", path)

    def test_failed_initialization_no_valid_rows(self):
        p = self.program()
        instrument_all_connectors(p, self.model)
        p.numerical["initialization"][0]["instructions"] = [
            {"op": "const", "dst": 0, "value": 1.0}, {"op": "store_output", "src": 0}]
        artifact = self.root / "failure.rbc"
        p.save(artifact)
        with self.assertRaisesRegex(ValueError, "execution-failure"):
            invoke("bitcode", "run", artifact, "--trace-root", self.root / "failed")
        for path in (self.root / "failed").glob("*.csv"):
            self.assertEqual(len(path.read_text().splitlines()), 1)

    def test_execution_edit_is_not_silently_relowered(self):
        p = self.program()
        instrument_all_connectors(p, self.model)
        # Change an ordinary saved derivative program, not the equations.
        p.numerical["derivatives"][0]["instructions"] = [
            {"op": "const", "dst": 0, "value": 0.0}, {"op": "store_output", "src": 0}]
        result = self.run_program(p)
        hot = result["data"][result["names"].index("hot.T")]
        self.assertTrue(all(abs(v - 350) < 1e-8 for v in hot))

    def test_computation_call_branch_assert_and_signed_alias(self):
        p = self.program()
        instrument_all_connectors(p, self.model)
        b = p.builder("test.check")
        helper = p.add_function("publish:check")
        with b.before_return(helper) as ir:
            t = ir.emit("snapshot.time")
            nonnegative = ir.emit("compute", arguments=[t], instructions=[
                {"op": "load_y", "dst": 0, "index": 0}, {"op": "const", "dst": 1, "value": 0},
                {"op": "compare", "dst": 2, "operator": "Ge", "lhs": 0, "rhs": 1}, {"op": "store_output", "src": 2}])
            ir.emit("if", condition=nonnegative, then_body=[], else_body=[{"op": "assert", "condition": nonnegative, "message": "negative time"}])
        with b.before_return(p.function("publish")) as ir:
            ir.emit("call", function="publish:check")
        # Public reconstruction supports signed aliases through canonical ops.
        observation = next(o for o in p.numerical["observations"] if o["name"] == "hot.port.Q_flow")
        peer = next(o for o in p.numerical["observations"] if o["name"] == "link.a.Q_flow")
        observation["instructions"] = deepcopy(peer["instructions"][:-1]) + [
            {"op": "unary", "operator": "Neg", "src": 0, "dst": 1}, {"op": "store_output", "src": 1}]
        self.run_program(p)
        verify(self.root / "run")

    def test_missing_replay_target_rejected(self):
        p = self.program()
        instrument_all_connectors(p, self.model)
        p.numerical["observations"][0]["variable_id"] = 999999
        with self.assertRaisesRegex(ValueError, "unknown observation variable"):
            p.relower(replay={"example.connector-csv": instrument_all_connectors})

    def test_three_way_connection_one_flow_sum(self):
        model = Model.empty("Nary")
        b = model.builder("test.nary")
        t = b.add_connector_type("Port", members=[{"name": "v", "scalar_type": "real", "kind": "potential"}, {"name": "i", "scalar_type": "real", "kind": "flow"}])
        ports = [b.add_connector("p", owner=b.add_component(n), type_id=t) for n in ("a", "b", "c")]
        b.add_connection_set(ports)
        model.refresh()
        model.validate()
        self.assertEqual(len(model.equations), 3)
        self.assertEqual(len(model.raw_model["connection_sets"][0]["balances"]), 1)
        self.assertEqual(len(model.raw_model["connection_sets"][0]["balances"][0]["terms"]), 3)

    def test_state_equation_removal_is_atomic_and_reindexes(self):
        model = Model.empty("Removal")
        b = model.builder("test.add")
        a, z = b.add_state("a", 1), b.add_state("z", 2)
        ea = b.add_derivative_equation(a, b.unary("negate", b.ref(a)))
        b.add_derivative_equation(z, b.unary("negate", b.ref(z)))
        model.refresh()
        before = deepcopy(model.raw_model)
        with self.assertRaisesRegex(ValueError, "still referenced"):
            b.remove(variables=[a])
        self.assertEqual(before, model.raw_model)
        mapping = b.remove(variables=[a], equations=[ea])
        self.assertEqual(mapping["variables"], {z: 0})
        self.assertEqual([v.name for v in model.states], ["z"])
        self.assertEqual(len(model.equations), 1)
        model.validate()


if __name__ == "__main__":
    unittest.main()
