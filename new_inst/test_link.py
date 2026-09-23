"""Native linker and SDK regression tests; requires the current RUMOCA binary."""
from copy import deepcopy
import json
import math
from pathlib import Path
import tempfile
import unittest

from rumoca_bitcode import Model
from rumoca_bitcode.compiler import invoke
from rumoca_bitcode.execution import lower
from synthesize_connector_csv import synthesize, instrument_all_connectors


def decay(rate=1.0, initial=2.0):
    model = Model.empty("Decay")
    b = model.builder("test.link")
    x = b.add_state("x", initial, causality="output")
    k = b.add_parameter("k", rate)
    b.add_derivative_equation(x, b.sub(b.real(0), b.mul(b.ref(k), b.ref(x))))
    model.refresh()
    return model


class LinkAcceptance(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(prefix="rbc-link-test-")
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)

    def run_model(self, model, label):
        p = lower(model)
        artifact = self.root / f"{label}.rbc"
        p.save(artifact)
        result = self.root / f"{label}.json"
        invoke("bitcode", "run", artifact, "--trace-root", self.root / label,
               "--stop", "1", "--publish-interval", "0.1", "--result", result)
        return json.loads(result.read_text())

    def test_linked_odes_match_analytic_and_separate_native_runs(self):
        a, b = decay(1, 2), decay(3, 7)
        snapshots = deepcopy([a._document, b._document])
        linked = Model.link({"left": a, "right": b}, name="TwoDecays")
        self.assertEqual([a._document, b._document], snapshots)
        self.assertEqual([v.name for v in linked.states], ["left.x", "right.x"])
        result = self.run_model(linked, "combined")
        for ns, model, initial, rate in [("left", a, 2, 1), ("right", b, 7, 3)]:
            standalone = self.run_model(model, ns)
            values = result["data"][result["names"].index(f"{ns}.x")]
            reference = standalone["data"][standalone["names"].index("x")]
            self.assertEqual(len(values), 11)
            for i, (value, expected) in enumerate(zip(values, reference)):
                self.assertAlmostEqual(value, expected, delta=1e-7)
                self.assertAlmostEqual(value, initial * math.exp(-rate * i / 10), delta=1e-7)

    def test_same_module_twice_and_deterministic_json_cbor_cli(self):
        model = decay()
        a, b = self.root / "a.json", self.root / "b.rbc"
        model.save(a)
        model.save(b)
        result = Model.link({"a": a, "b": b})
        again = Model.link({"a": model, "b": model})
        self.assertEqual(result._document, again._document)
        output = self.root / "combined.json"
        invoke("bitcode", "link", f"a={a}", f"b={b}", "-o", output, "--format", "json")
        self.assertEqual(Model.load(output)._document, again._document)
        invoke("bitcode", "check", output, "--strict")
        invoke("compile-bitcode", output)

    def test_nested_link_keeps_namespaces_and_sources(self):
        original = decay()
        inner = Model.link({"a": original, "b": original})
        result = Model.link({"system": inner, "c": original})
        self.assertEqual([v.name for v in result.states], ["system.a.x", "system.b.x", "c.x"])
        self.assertEqual(len(result.sources), 3 * len(original.sources))
        result.validate()

    def test_rejects_duplicates_invalid_input_and_overwriting_any_output(self):
        source = self.root / "a.rbc"
        decay().save(source)
        before = source.read_bytes()
        with self.assertRaisesRegex(ValueError, "create new output"):
            invoke("bitcode", "link", f"a={source}", "-o", source)
        self.assertEqual(source.read_bytes(), before)
        output = self.root / "bad.rbc"
        with self.assertRaisesRegex(ValueError, "unique simple identifier"):
            invoke("bitcode", "link", f"a={source}", f"a={source}", "-o", output)
        self.assertFalse(output.exists())
        for namespace in ["", "../x", "a.b", "a=b", "1x"]:
            with self.assertRaises(ValueError):
                Model.link({namespace: source})
        broken = decay()
        broken.raw_model["variables"][0]["start"] = 999999
        with self.assertRaises(ValueError):
            Model.link({"broken": broken})
        with self.assertRaises(ValueError):
            Model.link({})

    def test_executable_requires_explicit_discard_and_new_lowering(self):
        source = self.root / "execution.rbc"
        lower(decay()).save(source)
        before = source.read_bytes()
        with self.assertRaisesRegex(ValueError, "explicitly discard execution"):
            Model.link({"a": source, "b": decay()})
        linked = Model.link({"a": source, "b": decay()}, discard_execution=True)
        self.assertIsNone(linked._document.get("execution"))
        self.assertEqual(source.read_bytes(), before)
        self.run_model(linked, "relowered")

    def test_closed_thermal_systems_keep_all_equations_and_instrumentation_targets(self):
        thermal, _ = synthesize()
        linked = Model.link({"a": thermal, "b": thermal})
        self.assertEqual(len(linked.equations), 2 * len(thermal.equations))
        self.assertEqual(len(linked.connectors), 8)
        self.assertEqual(len(linked.raw_model["connection_sets"]), 4)
        for left, right in zip(thermal.raw_model["connection_sets"], linked.raw_model["connection_sets"][2:]):
            self.assertEqual(right["potential_equations"], [n + len(thermal.equations) for n in left["potential_equations"]])
            self.assertEqual(right["connectors"], ["b." + p for p in left["connectors"]])
        p = lower(linked)
        instrument_all_connectors(p, linked)
        output = self.root / "thermal.rbc"
        p.save(output)
        traces = self.root / "thermal"
        invoke("bitcode", "run", output, "--trace-root", traces, "--stop", "0.2")
        self.assertEqual(len(list(traces.glob("*.csv"))), 8)
        b = linked.builder("test.closed")
        with self.assertRaisesRegex(ValueError, "overlapping finalized"):
            b.add_connection_set([0, 4])

    def test_open_ports_can_be_explicitly_connected_after_linking(self):
        def body(temperature):
            model = Model.empty("Body")
            b = model.builder("test.open-port")
            ty = b.add_connector_type("HeatPort", members=[
                {"name": "T", "scalar_type": "real", "kind": "potential", "unit": "K"},
                {"name": "Q", "scalar_type": "real", "kind": "flow", "unit": "W"},
            ])
            owner = b.add_component("body", type_name="Body")
            x = b.add_state("T", temperature, owner=owner, causality="output")
            port = b.add_connector("port", owner=owner, type_id=ty)
            b.add_equation(b.sub(b.ref(b.member(port, "T")), b.ref(x)))
            b.add_derivative_equation(x, b.ref(b.member(port, "Q")))
            model.refresh()
            return model
        # Link an intentionally open body and a closed temperature source whose
        # port remains open. Wiring adds the two missing connection equations.
        source = Model.empty("Source")
        b = source.builder("test.source")
        ty = b.add_connector_type("HeatPort", members=[
            {"name": "T", "scalar_type": "real", "kind": "potential", "unit": "K"},
            {"name": "Q", "scalar_type": "real", "kind": "flow", "unit": "W"},
        ])
        owner = b.add_component("source", type_name="Source")
        port = b.add_connector("port", owner=owner, type_id=ty)
        b.add_equation(b.sub(b.ref(b.member(port, "T")), b.real(300)))
        source.refresh()
        linked = Model.link({"body": body(300), "source": source})
        b = linked.builder("test.wire")
        b.add_connection_set([0, 1])
        linked.refresh()
        linked.validate()
        self.assertEqual(len(linked.equations), 5)

    def test_incompatible_port_contracts_rejected_without_mutation(self):
        thermal, _ = synthesize()
        other = deepcopy(thermal._document)
        other["model"]["connector_types"][0]["members"][0]["quantity"] = "DifferentQuantity"
        for port in other["model"]["connectors"]:
            other["model"]["variables"][port["members"][0]["variable"]]["physical_quantity"] = "DifferentQuantity"
        linked = Model.link({"a": thermal, "b": Model(other)})
        builder = linked.builder("test.bad-wire")
        before = deepcopy(linked._document)
        with self.assertRaisesRegex(ValueError, "types differ"):
            builder.add_connection_set([0, 4])
        self.assertEqual(before, linked._document)

    def test_modelica_compiled_artifact_links_and_reconstructs(self):
        source = Path(__file__).parent / "link_fixtures" / "Decay.mo"
        artifact = self.root / "compiled.rbc"
        invoke("compile", source, "--model", "LinkDecay", "--emit-bitcode", artifact)
        linked = Model.link({"first": artifact, "second": artifact}, name="CompiledPair")
        linked.validate()
        result = self.run_model(linked, "compiled-pair")
        for name in ("first.x", "second.x"):
            data = result["data"][result["names"].index(name)]
            self.assertAlmostEqual(data[-1], 2 * math.exp(-1), delta=1e-7)


if __name__ == "__main__":
    unittest.main()
