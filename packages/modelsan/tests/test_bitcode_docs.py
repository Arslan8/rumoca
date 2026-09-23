"""The format's documentation is a build product, not an intention.

`SPEC_RUMOCA_BITCODE.md` is a good narrative that stopped tracking the schema:
51 of 56 types had never appeared in it by name, and six fields of `RbcModel`
were absent. Nothing kept it honest, so it stayed current for exactly as long
as somebody remembered.

These tests make the drift a failure instead.
"""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]


def check(condition: bool, label: str) -> None:
    print(f"  {'ok  ' if condition else 'FAIL'} {label}")
    assert condition, label


def test_the_type_reference_is_current():
    print("\n== the generated reference matches schema.rs ==")
    finished = subprocess.run(
        [sys.executable, "tools/bitcode/gen_reference.py", "--check"],
        capture_output=True, text=True, cwd=ROOT)
    check(finished.returncode == 0,
          f"run tools/bitcode/gen_reference.py — {finished.stderr.strip()[:120]}")


def test_every_model_table_is_in_the_reference():
    print("\n== no field of RbcModel is undocumented ==")
    import re

    schema = (ROOT / "crates/rumoca-bitcode/src/schema.rs").read_text()
    reference = (ROOT / "docs/bitcode-reference.md").read_text()
    body = re.search(r"pub struct RbcModel \{(.*?)\n\}", schema, re.S).group(1)
    fields = re.findall(r"pub (\w+):", body)
    missing = [name for name in fields if f"`{name}`" not in reference]
    check(not missing, f"every RbcModel field is listed (missing {missing})")


def test_the_extension_checklist_names_every_place_a_field_must_reach():
    print("\n== the seven places, and why the compiler finds only six ==")
    guide = (ROOT / "docs/dev-guide/extending-the-bitcode.md").read_text()
    for place in ("schema.rs", "export.rs", "import.rs", "text.rs",
                  "validate.rs", "packages/rumoca-bitcode/"):
        check(place in guide, f"{place} is in the checklist")
    check("coverage.py" in guide,
          "and the check that answers what the others cannot")


def test_the_spec_states_the_computational_power():
    print("\n== the property every analysis depends on is written down ==")
    spec = (ROOT / "docs/SPEC_RUMOCA_BITCODE.md").read_text()
    check("Computational power" in spec, "the section exists")
    check("not Turing complete" in spec, "and says which way it falls")
    check("undecidable" in spec,
          "and distinguishes the IR from the system it denotes")
    for hole in ("External", "ElidedModelica", "Unsupported"):
        check(hole in spec, f"the {hole} hole is named")
