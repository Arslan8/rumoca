#!/usr/bin/env python3
"""Generate the catalog of declaration sites that permit impossible values.

Every entry is a real place in MSL where a quantity that cannot be negative is
declared without a lower bound. Each carries `file:line` so a reader can go
look, and the declared modifiers so they can see what *is* constrained.

These are sites, not independent defects. Nine hundred of them share seventeen
missing lines in `Units.mo`, and the catalog is organised to make that visible
rather than to inflate a count.
"""
from __future__ import annotations

import argparse
import collections
import json
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path

#: Quantities for which a negative value is not a physical state of affairs.
#: Signed quantities are deliberately absent: Power and Energy are legitimately
#: negative (MSL's own POWMIN = -1e8, EMIN = -1e10), Position and Voltage are
#: signed by nature, and a PressureDifference is not an AbsolutePressure.
IMPOSSIBLE_NEGATIVE = {
    "Resistance": "electrical", "Conductance": "electrical",
    "Inductance": "electrical", "Capacitance": "electrical",
    "Resistivity": "electrical", "Conductivity": "electrical",
    "Inertia": "mechanical", "MomentOfInertia": "mechanical",
    "Mass": "mechanical", "Length": "mechanical", "Area": "mechanical",
    "Volume": "mechanical", "Diameter": "mechanical", "Radius": "mechanical",
    "ThermalConductance": "thermal", "HeatCapacity": "thermal",
    "SpecificHeatCapacity": "thermal", "ThermalResistance": "thermal",
    "Density": "fluid", "DynamicViscosity": "fluid",
    "KinematicViscosity": "fluid", "AbsolutePressure": "fluid",
    "Permeance": "magnetic", "Reluctance": "magnetic",
    "Duration": "timing", "Period": "timing",
}

DECLARATION = re.compile(
    r"parameter\s+(?:Modelica\.Units\.)?(?:SI\.)?(\w+)\s+(\w+)\s*"
    r"(?:\[[^\]]*\])?\s*(\([^;)]*\))?", re.M)


@dataclass
class Site:
    quantity: str
    domain: str
    parameter: str
    file: str
    line: int
    modifiers: str
    guarded: bool

    @property
    def component(self) -> str:
        """MSL stores one class per file, so the stem names the component."""
        return Path(self.file).stem


@dataclass
class TypeGroup:
    quantity: str
    domain: str
    type_bound: str | None = None
    sites: list[Site] = field(default_factory=list)

    @property
    def exposed(self) -> list[Site]:
        return [s for s in self.sites if not s.guarded]

    @property
    def guarded(self) -> list[Site]:
        return [s for s in self.sites if s.guarded]


def type_bounds(units_mo: Path) -> dict[str, str | None]:
    """The `min` each SI type declares, if any."""
    try:
        text = units_mo.read_text(errors="replace")
    except OSError:
        return {}
    found = {}
    for match in re.finditer(
            r"\btype\s+(\w+)\s*=\s*[\w.]+\s*(?:\(([^;]*?)\))?\s*(?:\"|;)", text, re.S):
        name, mods = match.group(1), " ".join((match.group(2) or "").split())
        low = re.search(r"min\s*=\s*([^,)]+)", mods)
        found[name] = low.group(1).strip() if low else None
    return found


def scan(root: Path) -> dict[str, TypeGroup]:
    bounds = type_bounds(root / "Units.mo")
    groups: dict[str, TypeGroup] = {}
    for mo in sorted(root.rglob("*.mo")):
        try:
            text = mo.read_text(errors="replace")
        except OSError:
            continue
        relative = str(mo.relative_to(root))
        for match in DECLARATION.finditer(text):
            quantity, parameter, mods = match.group(1), match.group(2), match.group(3) or ""
            if quantity not in IMPOSSIBLE_NEGATIVE:
                continue
            # A type that bounds itself is not a site; the model is protected.
            if bounds.get(quantity):
                continue
            group = groups.setdefault(quantity, TypeGroup(
                quantity=quantity, domain=IMPOSSIBLE_NEGATIVE[quantity],
                type_bound=bounds.get(quantity)))
            group.sites.append(Site(
                quantity=quantity, domain=IMPOSSIBLE_NEGATIVE[quantity],
                parameter=parameter, file=relative,
                line=text[: match.start()].count("\n") + 1,
                modifiers=" ".join(mods.split())[:70],
                guarded="min" in mods,
            ))
    return groups


def write_catalog(groups: dict[str, TypeGroup], out: Path, confirmed: list[dict]) -> None:
    out.mkdir(parents=True, exist_ok=True)
    ordered = sorted(groups.values(), key=lambda g: -len(g.exposed))
    total_exposed = sum(len(g.exposed) for g in ordered)
    total_guarded = sum(len(g.guarded) for g in ordered)

    index = [
        "# Catalog: declaration sites permitting physically impossible values",
        "",
        "Every entry is a place in MSL 4.1.0 where a quantity that cannot be",
        "negative is declared without a lower bound, with `file:line` so it can be",
        "checked directly.",
        "",
        "**These are sites, not independent defects.** All of them trace to",
        f"**{len(ordered)} SI type definitions** in `Units.mo` that declare no `min`.",
        "Fixing those fixes every site below, which is why the count to quote is the",
        "number of types, not the number of lines.",
        "",
        f"- **{len(ordered)}** SI types with no lower bound on an impossible-negative quantity",
        f"- **{total_exposed}** declarations that inherit one and add no bound of their own",
        f"- **{total_guarded}** declarations that do add their own bound (already safe)",
        "",
        "The guarded column is the evidence that the omissions are omissions: the same",
        "library, for the same quantity, sometimes writes the bound and sometimes does",
        "not.",
        "",
        "## By type",
        "",
        "| Quantity | Domain | Exposed | Guarded | Detail |",
        "|---|---|---|---|---|",
    ]
    for group in ordered:
        if not group.exposed:
            continue
        slug = group.quantity.lower()
        index.append(f"| `SI.{group.quantity}` | {group.domain} | "
                     f"**{len(group.exposed)}** | {len(group.guarded)} | "
                     f"[sites](by-type/{slug}.md) |")

    if confirmed:
        index += [
            "",
            "## Execution-confirmed defects",
            "",
            "Sites where a permitted value provably breaks the model in two",
            "independent tools. These are defects, not merely sites.",
            "",
            "| Component | Parameter | Models |",
            "|---|---|---|",
        ]
        for entry in confirmed:
            index.append(f"| `{entry['component']}` | `{entry['parameter']}` | "
                         f"{entry['models']} |")

    (out / "README.md").write_text("\n".join(index) + "\n")

    per_type = out / "by-type"
    per_type.mkdir(exist_ok=True)
    for group in ordered:
        if not group.exposed:
            continue
        lines = [
            f"# `SI.{group.quantity}` — {len(group.exposed)} unbounded declarations",
            "",
            f"Domain: {group.domain}",
            "",
            f"`Units.mo` declares `type {group.quantity}` with **no `min`**, so every",
            "declaration below accepts a negative value.",
            "",
            "## Exposed",
            "",
            "| File | Line | Parameter | Declared modifiers |",
            "|---|---|---|---|",
        ]
        for site in sorted(group.exposed, key=lambda s: (s.file, s.line)):
            mods = site.modifiers.replace("|", r"\|") or "—"
            lines.append(f"| `{site.file}` | {site.line} | `{site.parameter}` | `{mods}` |")
        if group.guarded:
            lines += [
                "",
                "## Guarded — these add their own bound",
                "",
                "Same library, same quantity, bound written. This is why the exposed",
                "cases read as omissions rather than as a deliberate choice.",
                "",
                "| File | Line | Parameter | Declared modifiers |",
                "|---|---|---|---|",
            ]
            for site in sorted(group.guarded, key=lambda s: (s.file, s.line)):
                mods = site.modifiers.replace("|", r"\|")
                lines.append(f"| `{site.file}` | {site.line} | `{site.parameter}` | `{mods}` |")
        (per_type / f"{group.quantity.lower()}.md").write_text("\n".join(lines) + "\n")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--msl", default="target/msl/ModelicaStandardLibrary-4.1.0/Modelica 4.1.0")
    parser.add_argument("--out", default="docs/findings/catalog")
    parser.add_argument("--confirmed", help="JSON from confirm_eval.py")
    args = parser.parse_args()

    groups = scan(Path(args.msl))
    confirmed = []
    if args.confirmed and Path(args.confirmed).exists():
        data = json.loads(Path(args.confirmed).read_text())
        seen = {}
        for row in data.get("results", []):
            if row.get("verdict") != "confirmed" or not row.get("trigger"):
                continue
            parameter = row["trigger"].split("=")[0].rsplit(".", 1)[-1]
            seen.setdefault((row.get("via", ""), parameter),
                            {"component": row.get("via", ""),
                             "parameter": parameter, "models": row.get("models", 1)})
        confirmed = sorted(seen.values(), key=lambda e: -e["models"])

    write_catalog(groups, Path(args.out), confirmed)
    exposed = sum(len(g.exposed) for g in groups.values())
    print(f"{len(groups)} types, {exposed} exposed declarations -> {args.out}")
    for group in sorted(groups.values(), key=lambda g: -len(g.exposed))[:8]:
        print(f"  {len(group.exposed):4} exposed / {len(group.guarded):3} guarded  "
              f"SI.{group.quantity}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
