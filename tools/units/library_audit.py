#!/usr/bin/env python3
"""Audit a Modelica library's *type declarations* for unit/quantity defects.

`QuantitySan` reads a compiled model, so it only ever sees the quantities some
model happens to instantiate. The largest recurring unit defects in MSL are not
in models at all — they are in `Modelica/Units.mo`, in type declarations that
may have no user yet. `Units.LogarithmicDecrement` has been wrong since it was
written; no model has to use it for the declaration to be wrong.

So this reads the declarations directly. Three checks, each one an open
upstream issue pattern:

    quantity-maps-to-two-dimensions   one quantity, dimensionally different
                                      units  (#4062, #4088)
    quantity-non-si-unit              one quantity, an SI unit and a non-SI
                                      one of the same dimension  (#3158)
    unit-without-quantity             a unit and nothing saying what it
                                      measures  (#4086, #4085)

MLS §4.8 makes `quantity` the semantic identity of what is measured, which is
what licenses the first two: the map quantity → dimension must be a function,
so two declarations that disagree prove a defect between them even when nothing
here knows which one to correct.

    tools/units/library_audit.py
    tools/units/library_audit.py --units "path/to/Units.mo" --json out.json
"""
from __future__ import annotations

import argparse
import collections
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path[:0] = [str(ROOT / "packages" / "modelsan"),
                str(ROOT / "packages" / "rumoca-bitcode")]

from modelsan.sanitizers.quantity import is_si_coherent   # noqa: E402
from modelsan.units.dimension import parse                # noqa: E402

DEFAULT_UNITS = (ROOT / "target/msl/ModelicaStandardLibrary-4.1.0"
                 / "Modelica 4.1.0" / "Units.mo")

#: `type Name = Real ( ... );` — the only declaration form that carries the
#: attributes this audit reads. A narrow pattern with one owner, like the
#: bitcode reference generator: anything it cannot read is reported as
#: unparsed rather than silently skipped.
DECLARATION = re.compile(r'type\s+(\w+)\s*=\s*Real\s*\((.*?)\)\s*;', re.S)


def declarations(source: str):
    """Every `(name, quantity, unit)` a Units file declares."""
    for match in DECLARATION.finditer(source):
        name, body = match.group(1), match.group(2)
        quantity = re.search(r'quantity\s*=\s*"([^"]*)"', body)
        unit = re.search(r'(?<!display)(?<!display_)\bunit\s*=\s*"([^"]*)"', body)
        yield (name,
               quantity.group(1) if quantity else None,
               unit.group(1) if unit else None)


def audit(source: str) -> list[dict]:
    entries = list(declarations(source))
    by_quantity: dict[str, dict[str, list[str]]] = collections.defaultdict(
        lambda: collections.defaultdict(list))
    findings = []

    for name, quantity, unit in entries:
        if quantity and unit:
            by_quantity[quantity][unit].append(name)
        elif unit and not quantity:
            dimension = parse(unit)
            # A dimensionless value with no quantity risks nothing, exactly as
            # in the per-model check; `PerUnit` is reported, `Stress` matters.
            findings.append({
                "check": "unit-without-quantity",
                "severity": "low" if dimension and dimension.dimensionless
                            else "medium",
                "type": name,
                "unit": unit,
                "dimension": str(dimension) if dimension else None,
                "note": "the declaration states a unit and nothing states what "
                        "is measured, so no rule keyed on quantity can apply",
            })

    for quantity, units in sorted(by_quantity.items()):
        if len(units) < 2:
            continue
        dimensions = {u: parse(u) for u in units}
        known = {u: d for u, d in dimensions.items() if d is not None}
        if len(known) < 2:
            continue
        if len({str(d) for d in known.values()}) > 1:
            findings.append({
                "check": "quantity-maps-to-two-dimensions",
                "severity": "high",
                "quantity": quantity,
                "units": {u: str(d) for u, d in sorted(known.items())},
                "types": {u: units[u] for u in sorted(known)},
                "note": "one quantity is declared with units of different SI "
                        "dimension; at most one of them can be right",
            })
            continue
        coherent = sorted(u for u in units if is_si_coherent(u))
        other = sorted(u for u in units if not is_si_coherent(u))
        if coherent and other:
            findings.append({
                "check": "quantity-non-si-unit",
                "severity": "low",
                "quantity": quantity,
                "si_unit": coherent,
                "non_si": {u: units[u] for u in other},
                "note": "the same quantity is declared in its SI unit and in a "
                        "non-SI unit of the same dimension",
            })
    return findings


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--units", default=str(DEFAULT_UNITS))
    parser.add_argument("--json", default="")
    parser.add_argument("--fail-on", default="",
                        help="exit nonzero when a check of this severity fires")
    args = parser.parse_args()

    path = Path(args.units)
    if not path.is_file():
        print(f"no Units file at {path}", file=sys.stderr)
        return 2
    source = path.read_text()
    findings = audit(source)
    total = len(list(declarations(source)))

    order = {"high": 0, "medium": 1, "low": 2}
    findings.sort(key=lambda f: (order.get(f["severity"], 3), f["check"]))
    counts = collections.Counter(f["check"] for f in findings)
    print(f"{path.name}: {total} type declarations, {len(findings)} finding(s)")
    for check, n in counts.most_common():
        print(f"   {n:4d}  {check}")
    print()
    for finding in findings:
        head = finding.get("quantity") or finding.get("type")
        print(f"  [{finding['severity']:6}] {finding['check']}  {head}")
        for key in ("units", "types", "si_unit", "non_si", "unit", "dimension"):
            if key in finding and finding[key]:
                print(f"            {key}: {finding[key]}")
    if args.json:
        Path(args.json).write_text(json.dumps(
            {"source": str(path), "declarations": total,
             "findings": findings}, indent=1) + "\n")
    if args.fail_on:
        return 1 if any(f["severity"] == args.fail_on for f in findings) else 0
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
