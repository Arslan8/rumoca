"""Adversarial native checks: mutate serialized data, bypassing the SDK helper."""
from copy import deepcopy
import os
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from rumoca_bitcode import Model
from rumoca_bitcode.compiler import invoke
from synthesize_connector_csv import synthesize


class ConnectionValidation(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(prefix="rbc-connection-check-")
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.model, _ = synthesize()

    def check(self, model=None):
        path = self.root / "mutated.rbc"
        (model or self.model).save(path)
        invoke("bitcode", "check", path, "--strict")

    def test_flow_law_cannot_be_replaced_by_zero(self):
        model = self.model
        equation = model.raw_model["connection_sets"][0]["balances"][0]["equation"]
        model.raw_model["equations"][equation]["residual"] = model.builder("corrupt").real(0)
        model.refresh()
        with self.assertRaisesRegex(ValueError, "flow.*equation|flow.*law"):
            self.check()

    def test_metadata_corruption_matrix_is_rejected_natively(self):
        def set0(m):
            return m.raw_model["connection_sets"][0]
        cases = {
            "overlap": lambda m: m.raw_model["connection_sets"].append(dict(deepcopy(set0(m)), id=2)),
            "duplicate-port": lambda m: set0(m)["connectors"].append(set0(m)["connectors"][0]),
            "unknown-port": lambda m: set0(m)["connectors"].__setitem__(0, "missing.port"),
            "empty-set": lambda m: set0(m).__setitem__("connectors", []),
            "wrong-singleton-flag": lambda m: set0(m).__setitem__("unconnected", True),
            "wrong-connected-flag": lambda m: m.raw_model["variables"][set0(m)["potentials"][0]]["connector"].__setitem__("connected", False),
            "missing-potential": lambda m: set0(m)["potentials"].pop(),
            "extra-potential": lambda m: set0(m)["potentials"].append(0),
            "duplicate-potential": lambda m: set0(m)["potentials"].append(set0(m)["potentials"][0]),
            "missing-equality": lambda m: set0(m)["potential_equations"].clear(),
            "equation-reused": lambda m: set0(m)["potential_equations"].append(set0(m)["potential_equations"][0]),
            "missing-flow-balance": lambda m: set0(m)["balances"].clear(),
            "missing-flow-equation": lambda m: set0(m)["balances"][0].pop("equation"),
            "flow-equation-out-of-bounds": lambda m: set0(m)["balances"][0].__setitem__("equation", 999999),
            "missing-flow-member": lambda m: set0(m)["balances"][0]["terms"].pop(),
            "duplicate-flow-member": lambda m: set0(m)["balances"][0]["terms"].append(set0(m)["balances"][0]["terms"][0]),
            "wrong-flow-sign": lambda m: set0(m)["balances"][0]["terms"][0].__setitem__("negated", True),
            "wrong-orientation": lambda m: m.raw_model["connectors"][0].__setitem__("orientation", "inside"),
            "wrong-quantity": lambda m: m.raw_model["connector_types"][0]["members"][0].__setitem__("quantity", "Wrong"),
            "missing-declarations": lambda m: m.raw_model["connectors"].clear(),
            "wrong-provenance": lambda m: set0(m)["provenance"]["span"].__setitem__("source", 999999),
        }
        for label, mutate in cases.items():
            with self.subTest(label=label):
                model = Model(deepcopy(self.model._document))
                mutate(model)
                model.refresh()
                with self.assertRaises(ValueError):
                    self.check(model)

    def test_each_native_entry_point_rejects_corrupted_law(self):
        model = self.model
        eq = model.raw_model["connection_sets"][0]["balances"][0]["equation"]
        model.raw_model["equations"][eq]["residual"] = model.builder("corrupt").real(0)
        model.refresh()
        for encoding in ("json", "cbor"):
            source = self.root / f"bad-{encoding}.rbc"
            model.save(source, format=encoding)
            commands = [
                ("bitcode", "check", source),
                ("bitcode", "check", source, "--strict"),
                ("compile-bitcode", source),
                ("bitcode", "lower-execution", source, "-o", self.root / "bad-exec.rbc"),
                ("bitcode", "link", f"bad={source}", "-o", self.root / "bad-link.rbc"),
            ]
            for command in commands:
                with self.subTest(command=command), self.assertRaisesRegex(ValueError, "flow.*equation"):
                    invoke(*command)
            self.assertFalse((self.root / "bad-exec.rbc").exists())
            self.assertFalse((self.root / "bad-link.rbc").exists())

    @staticmethod
    def ports(count=3, multi=False, connect=True):
        model = Model.empty("Ports")
        b = model.builder("test.ports")
        fields = [{"name": "v", "kind": "potential", "scalar_type": "real"},
                  {"name": "i", "kind": "flow", "scalar_type": "real"}]
        if multi:
            fields += [{"name": "w", "kind": "potential", "scalar_type": "real"},
                       {"name": "j", "kind": "flow", "scalar_type": "real"}]
        ty = b.add_connector_type("Port", members=fields)
        ids = [b.add_connector("p", owner=b.add_component(f"c{i}"), type_id=ty,
                               orientation="inside" if i == 1 else "outside") for i in range(count)]
        if connect:
            b.add_connection_set(ids)
        model.refresh()
        return model

    def test_valid_nary_multifield_and_singleton_boundaries(self):
        for count in (1, 2, 3, 4):
            with self.subTest(count=count):
                self.check(self.ports(count, multi=True))

    def test_member_contract_mismatch_across_distinct_types(self):
        for field, value in [("name", "different"), ("unit", "V"), ("quantity", "Voltage")]:
            with self.subTest(field=field):
                model = self.ports(2)
                raw = model.raw_model
                ty = deepcopy(raw["connector_types"][0])
                ty["id"] = 1
                ty["members"][0][field] = value
                raw["connector_types"].append(ty)
                raw["connectors"][1]["type_id"] = 1
                member = raw["connectors"][1]["members"][0]
                if field == "name":
                    member["name"] = value
                else:
                    raw["variables"][member["variable"]]["physical_quantity" if field == "quantity" else field] = value
                model.refresh()
                with self.assertRaisesRegex(ValueError, "types differ"):
                    self.check(model)

    def test_wrong_potential_equation_and_disconnected_tree(self):
        model = self.ports(3)
        eqs = model.raw_model["connection_sets"][0]["potential_equations"]
        model.raw_model["equations"][eqs[1]]["residual"] = model.raw_model["equations"][eqs[0]]["residual"]
        with self.assertRaisesRegex(ValueError, "span every port"):
            self.check(model)
        model.raw_model["equations"][eqs[0]]["residual"] = model.builder("bad").real(0)
        model.refresh()
        with self.assertRaisesRegex(ValueError, "potential equation"):
            self.check(model)

    def test_global_sign_and_non_star_tree_are_valid(self):
        model = self.ports(3)
        b = model.builder("equivalent")
        raw = model.raw_model
        group = raw["connection_sets"][0]
        ids = group["potentials"]
        # Change the spanning tree from a-b,a-c to a-b,b-c.
        raw["equations"][group["potential_equations"][1]]["residual"] = b.sub(b.ref(ids[1]), b.ref(ids[2]))
        eq = raw["equations"][group["balances"][0]["equation"]]
        eq["residual"] = b.unary("negate", eq["residual"])
        group["potentials"].reverse()
        group["balances"][0]["terms"].reverse()
        model.refresh()
        self.check(model)

    def test_unsupported_nonlinear_and_cyclic_laws_fail_closed(self):
        for kind in ("divide", "multiply", "cycle", "overflow"):
            with self.subTest(kind=kind):
                model = self.ports(2)
                b = model.builder("bad-law")
                eqid = model.raw_model["connection_sets"][0]["balances"][0]["equation"]
                eq = model.raw_model["equations"][eqid]
                if kind == "cycle":
                    node = model.raw_model["expressions"][eq["residual"]]["node"]
                    node["rhs"] = eq["residual"]
                elif kind == "overflow":
                    for _ in range(64):
                        eq["residual"] = b.add(eq["residual"], eq["residual"])
                else:
                    eq["residual"] = b.binary(kind, eq["residual"], b.real(0 if kind == "divide" else 1))
                if kind != "cycle":
                    model.refresh()
                with self.assertRaises(ValueError):
                    self.check(model)

    def test_sdk_failures_are_atomic_and_negative_ids_rejected(self):
        model = self.ports(2, connect=False)
        b = model.builder("atomic")
        before, counts = deepcopy(model._document), deepcopy(b.added)
        for ids in ([-1, 0], [0, True], [0, 9999], [0, 0]):
            with self.subTest(ids=ids), self.assertRaises(ValueError):
                b.add_connection_set(ids)
            self.assertEqual(model._document, before)
            self.assertEqual(b.added, counts)
        with patch("rumoca_bitcode.compiler.check_model", side_effect=ValueError("native refusal")):
            with self.assertRaisesRegex(ValueError, "native refusal"):
                b.add_connection_set([0, 1])
        self.assertEqual(model._document, before)
        self.assertEqual(b.added, counts)
        with patch.dict(os.environ, {"RUMOCA": str(self.root / "missing-compiler")}):
            with self.assertRaises(OSError):
                b.add_connection_set([0, 1])
        self.assertEqual(model._document, before)
        self.assertEqual(b.added, counts)

    def test_removed_set_cannot_leave_generated_boundary_behind(self):
        model = self.ports(1)
        model.raw_model["connection_sets"].clear()
        for v in model.raw_model["variables"]:
            v["connector"]["connected"] = False
        model.refresh()
        with self.assertRaisesRegex(ValueError, "unowned generated boundary"):
            self.check(model)
        builder = model.builder("rewire-closed")
        before = deepcopy(model._document)
        with self.assertRaisesRegex(ValueError, "unowned generated boundary"):
            builder.add_connection_set([0])
        self.assertEqual(model._document, before)

    def test_legacy_graph_cannot_claim_certified_wiring(self):
        model = self.ports(2)
        model.raw_model["connectors"].clear()
        model.raw_model["connector_types"].clear()
        model.refresh()
        path = self.root / "legacy.rbc"
        model.save(path)
        self.assertIn("NOT certified", invoke("bitcode", "check", path))
        with self.assertRaisesRegex(ValueError, "complete port declarations required"):
            invoke("bitcode", "check", path, "--connections")
        with self.assertRaisesRegex(ValueError, "complete port declarations required"):
            model.validate(strict=False, connections=True)

    def test_explicit_contract_check_accepts_valid_model(self):
        path = self.root / "valid.rbc"
        self.model.save(path)
        self.assertIn("connection laws checked", invoke("bitcode", "check", path, "--connections"))
        self.model.validate(connections=True)

    def test_connection_edge_metadata_must_agree_with_owned_law(self):
        model = self.ports(2)
        raw = model.raw_model
        group = raw["connection_sets"][0]
        raw["connections"].append({
            "id": 0, "left": group["potentials"][0], "right": group["potentials"][1],
            "quantity": "potential", "left_connector": group["connectors"][0],
            "right_connector": group["connectors"][1], "equation": group["potential_equations"][0],
            "provenance": deepcopy(group["provenance"]),
        })
        model.refresh()
        self.check(model)
        edge = deepcopy(raw["connections"][0])
        raw["connections"][0]["right"] = edge["left"]
        raw["connections"][0]["right_connector"] = edge["left_connector"]
        with self.assertRaisesRegex(ValueError, "self-edge"):
            self.check(model)
        raw["connections"][0] = edge
        raw["connections"][0]["right"] = raw["connectors"][1]["members"][1]["variable"]
        with self.assertRaisesRegex(ValueError, "connection edge"):
            self.check(model)

    def test_multifield_potentials_cannot_be_crosswired(self):
        model = self.ports(2, multi=True)
        raw = model.raw_model
        eqid = raw["connection_sets"][0]["potential_equations"][0]
        b = model.builder("wrong-fields")
        lhs = raw["connectors"][0]["members"][0]["variable"]
        rhs = raw["connectors"][1]["members"][2]["variable"]
        raw["equations"][eqid]["residual"] = b.sub(b.ref(lhs), b.ref(rhs))
        model.refresh()
        with self.assertRaisesRegex(ValueError, "different fields"):
            self.check(model)


if __name__ == "__main__":
    unittest.main()
