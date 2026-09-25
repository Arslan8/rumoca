"""Public SDK edits preserve clock ownership and String conversion operands."""
from copy import deepcopy
from pathlib import Path
import tempfile
import unittest

from rumoca_bitcode import BitcodeError, Model, StringConversion, VERSION
from rumoca_bitcode.builder import operands_of, with_operands


class ClockTransport(unittest.TestCase):
    def model(self):
        model = Model.empty("ClockTransport")
        builder = model.builder("test.clock-transport")
        value = builder.real(1.25)
        length, justified, digits = builder.integer(8), builder.boolean(True), builder.integer(6)
        string = builder.add_expression({"kind": "string_conversion", "value": value,
            "format": {"kind": "options", "minimum_length": length,
                "left_justified": justified, "significant_digits": digits}},
            value_type=builder.scalar_type("string"))
        target = builder.add_discrete("held")
        provenance = deepcopy(model.raw_model["variables"][target]["declaration"])
        model.raw_model["clocks"] = [{"id": 0, "node": {"kind": "periodic",
            "period": {"numerator": "1", "denominator": "20"},
            "phase": {"numerator": "-5", "denominator": "4"},
            "anchor": "simulation_start"}, "provenance": provenance}]
        model.raw_model["clock_ownerships"] = [{"variable": target, "clock": 0,
            "sampled": True, "provenance": provenance}]
        model.refresh()
        return model, string

    def test_sdk_children_and_rewrite_include_all_string_operands(self):
        model, string = self.model()
        expression = model.expressions[string]
        self.assertIsInstance(expression, StringConversion)
        self.assertEqual([child.id for child in expression.children()], [0, 1, 2, 3])
        node = model.raw_model["expressions"][string]["node"]
        self.assertEqual(set(operands_of(node)), {0, 1, 2, 3})
        replacement = with_operands(node, {0: 10, 1: 11, 2: 12, 3: 13})
        self.assertEqual(set(operands_of(replacement)), {10, 11, 12, 13})
        self.assertEqual(set(operands_of(node)), {0, 1, 2, 3})

    def test_sdk_json_cbor_edits_preserve_clock_semantics(self):
        model, _ = self.model()
        snapshot = deepcopy(model.raw_model)
        self.assertEqual(snapshot["summary"]["clocks"], 1)
        self.assertEqual(snapshot["summary"]["clock_ownerships"], 1)
        with tempfile.TemporaryDirectory() as directory:
            for suffix in ["json", "rbc"]:
                path = Path(directory)/f"model.{suffix}"
                model.save(path)
                loaded = Model.load(path)
                loaded.builder("test.add").real(9)
                loaded.refresh()
                loaded.save(path)
                again = Model.load(path)
                for table in ["clocks", "clock_ownerships"]:
                    self.assertEqual(again.raw_model[table], snapshot[table])

    def test_sdk_rejects_superseded_version(self):
        self.assertEqual(VERSION, 2)
        model, _ = self.model()
        old = deepcopy(model._document)
        old["bitcode_version"] = 1
        with self.assertRaises(BitcodeError):
            Model(old)


if __name__ == "__main__":
    unittest.main()
