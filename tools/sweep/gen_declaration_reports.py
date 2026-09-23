#!/usr/bin/env python3
"""One report per catalogued declaration site.

`docs/findings/catalog/by-type/` holds these as tables, which is right for
seeing that `SI.Resistance` has 281 unbounded declarations against 43 guarded
ones. It is wrong for acting on any single one: a table row cannot be linked
to, assigned, or closed.

So each exposed declaration also gets a file. They are the *weakest* tier of
evidence in this project and the files say so — a declaration that permits a
physically impossible value is a latent hazard, not an observed failure, and
911 of them share 17 missing lines in `Units.mo`.
"""
from __future__ import annotations

import collections
import re
import sys
from pathlib import Path

CATALOG = Path("docs/findings/catalog/by-type")
OUT = Path("docs/declaration-sites")
ROW = re.compile(r"^\| `([^`]+)` \| (\d+) \| `([^`]+)` \| `?([^|]*?)`? \|$")

#: Why a negative value is not a physical state of affairs, per quantity.
WHY = {
    "resistance": "a resistance below zero makes a passive element a source",
    "conductance": "the reciprocal of a resistance; negative means generation",
    "inductance": "stored energy is L*i^2/2, which a negative L makes negative",
    "capacitance": "stored energy is C*v^2/2, which a negative C makes negative",
    "inertia": "J*a = tau determines angular acceleration only for J > 0",
    "length": "a negative length is not a geometry",
    "area": "a negative cross-section is not a geometry",
    "volume": "a negative volume is not a geometry",
    "permeance": "the magnetic analogue of conductance",
    "reluctance": "the magnetic analogue of resistance",
    "resistivity": "a material property that is non-negative by definition",
    "conductivity": "a material property that is non-negative by definition",
    "heatcapacity": "a negative heat capacity makes heating cool the body",
    "specificheatcapacity": "a negative heat capacity makes heating cool the body",
    "thermalconductance": "negative thermal conductance moves heat up a gradient",
    "thermalresistance": "negative thermal resistance moves heat up a gradient",
    "duration": "a negative duration runs time backwards",
    "period": "a negative period is not a period",
}


def declaration_filename(number: int, entry: dict, stem: str) -> str:
    """`DECL-0001-resistance-resistor-R.md`.

    The id keeps its case so it reads the same in a filename, a link and a
    conversation; only the descriptive tail is normalised.
    """
    tail = f"{entry['quantity']}-{stem}-{entry['parameter']}".lower()
    tail = re.sub(r"[^a-z0-9]+", "-", tail).strip("-")[:70]
    return f"DECL-{number:04d}-{tail}.md"


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    for stale in OUT.glob("DECL-*.md"):
        stale.unlink()

    entries = []
    for page in sorted(CATALOG.glob("*.md")):
        quantity = page.stem
        text = page.read_text()
        exposed_block = text.split("## Guarded")[0]
        for line in exposed_block.splitlines():
            found = ROW.match(line.strip())
            if not found:
                continue
            entries.append({
                "quantity": quantity, "file": found.group(1),
                "line": int(found.group(2)), "parameter": found.group(3),
                "modifiers": found.group(4).strip(),
            })

    entries.sort(key=lambda e: (e["quantity"], e["file"], e["line"]))
    for number, entry in enumerate(entries, 1):
        stem = Path(entry["file"]).stem
        name = declaration_filename(number, entry, stem)
        why = WHY.get(entry["quantity"], "physically non-negative")
        mods = entry["modifiers"] if entry["modifiers"] not in ("", "—") else "none"
        # Spice3 encodes "the user did not set this" as -1e40, which is a
        # documented workaround for Modelica having no optional parameter, not
        # an oversight. Saying so here stops a reader filing it.
        caveat = ""
        if entry["file"].endswith("Spice3.mo"):
            caveat = ("\n> **Read the sentinel study first.** `Spice3.mo` encodes "
                      "an unset parameter as `-1e40`\n> and tests against it before "
                      "use (`Spice3.mo:157`). If this declaration carries that\n> "
                      "default, the negative value is deliberate and this is not a "
                      "defect — see\n> [sentinel-parameters.md]"
                      "(../findings/sentinel-parameters.md).\n")
        (OUT / name).write_text(f"""# DECL-{number:04d}: `{entry['parameter']}` declared without a lower bound

| | |
|---|---|
| **Declaration** | `Modelica 4.1.0/{entry['file']}:{entry['line']}` |
| **Parameter** | `{entry['parameter']}` |
| **Quantity** | `SI.{entry['quantity'].capitalize()}` |
| **Declared modifiers** | {mods} |
| **Status** | **latent — a permitted value, not an observed failure** |
{caveat}
## What is wrong

`SI.{entry['quantity'].capitalize()}` declares no `min` in `Units.mo`, and this
declaration adds none of its own. It therefore accepts a negative value, and
{why}.

## What this is not

Nothing has been observed failing here. This is a declaration that *permits* an
impossible value, which is the weakest of the three tiers this project reports:

| Tier | Evidence | Where |
|---|---|---|
| confirmed | fails in two independent tools | [`INSTANCES.md`](../verified%20bugs/INSTANCES.md) |
| candidate | static analysis reached it | [`site-reports/`](../site-reports/README.md) |
| **latent** | **the declaration permits it** | **here** |

## The fix is not here

This site and {len(entries) - 1} others inherit from **17 type definitions** in
`Units.mo` that declare no `min`. Adding the bound to the type fixes every site
that inherits it, and is one edit rather than {len(entries)}:

```modelica
// Units.mo
type {entry['quantity'].capitalize()} = Real (
    final quantity="{entry['quantity'].capitalize()}",
    final unit="...",
    min=0);
```

Bounding this one declaration instead is correct but local:

```modelica
// {entry['file']}:{entry['line']}
parameter SI.{entry['quantity'].capitalize()} {entry['parameter']}(min=0) = ...;
```

See [si-type-bounds.md](../findings/si-type-bounds.md) for why the type is the
right place, and [`catalog/`](../findings/catalog/README.md) for the same data
grouped by type.
""")

    by_quantity = collections.Counter(e["quantity"] for e in entries)
    lines = [
        "# Declaration sites",
        "",
        f"**{len(entries)} files**, one per MSL 4.1.0 declaration that accepts a",
        "physically impossible value.",
        "",
        "These are the **weakest** tier of evidence here. Nothing has been observed",
        "failing at any of them; each is a declaration that permits a value it",
        "should not. They are individually addressable because a table row cannot",
        "be linked to or closed, and grouped below because **17 missing lines in",
        f"`Units.mo` account for all {len(entries)}**.",
        "",
        "Quote the 17 as the defect count. These are its blast radius.",
        "",
        "| Quantity | Sites | |",
        "|---|---|---|",
    ]
    for quantity, count in by_quantity.most_common():
        lines.append(f"| `SI.{quantity.capitalize()}` | {count} | "
                     f"[by type](../findings/catalog/by-type/{quantity}.md) |")
    lines += ["", "## All sites", "",
              "| ID | Parameter | Declaration |", "|---|---|---|"]
    for number, entry in enumerate(entries, 1):
        stem = Path(entry["file"]).stem
        name = declaration_filename(number, entry, stem)
        lines.append(f"| [DECL-{number:04d}]({name}) | `{entry['parameter']}` | "
                     f"`{entry['file']}:{entry['line']}` |")
    lines += ["", "## Regenerating", "",
              "```bash", "python3 tools/sweep/gen_declaration_reports.py", "```", ""]
    (OUT / "README.md").write_text("\n".join(lines))

    print(f"wrote {len(entries)} declaration reports")
    for quantity, count in by_quantity.most_common(6):
        print(f"  {count:5}  SI.{quantity.capitalize()}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
