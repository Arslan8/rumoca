#!/usr/bin/env python3
"""One report per confirmed instance, because one report per fix site is not
what a developer opens.

A fix-site file says `Mass.m` permits zero. That is the root cause and it is
one edit. But `Damper.mo` instantiates three masses, and the person holding
that file needs to know *which* of them was proven to fail, at what value, and
where the declaration sits — `mass1`, `mass2` and `mass3` are three different
lines in their model.

So the two layers are kept separate and linked: the fix-site file carries the
argument, and each instance file carries the evidence for one occurrence.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(".")
BUGS = ROOT / "docs/verified bugs"

#: Parameter -> the fix-site report that explains the root cause.
ROOT_CAUSE = {
    "m": ("BUG-002-msl-zero-mass-within-declared-bound.md",
          "Modelica.Mechanics.Translational.Components.Mass",
          "`SI.Mass m(min=0)` — the bound permits the value that degenerates `m*a = f`"),
    "J": ("BUG-018-rotational-inertia-zero-within-declared-bound.md",
          "Modelica.Mechanics.Rotational.Components.Inertia",
          "`SI.Inertia J(min=0)` — the bound permits the value that degenerates `J*a = tau`"),
    "L": ("BUG-010-inductor-documents-zero-it-cannot-honour.md",
          "Modelica.Electrical.Analog.Basic.Inductor",
          "`SI.Inductance L` with no bound, documented as permitting zero"),
    "C": ("BUG-013-capacitor-zero-capacitance-topology-dependent.md",
          "Modelica.Electrical.Analog.Basic.Capacitor",
          "`SI.Capacitance C` with no bound, documented as permitting zero"),
    "l": ("BUG-014-genericfluxtube-l-unbounded-divisor.md",
          "Modelica.Magnetic.FluxTubes.Shapes.FixedShape.GenericFluxTube",
          "`SI.Length l` with no bound, used directly as a divisor"),
    "area": ("BUG-017-genericfluxtube-area-chain-divisor.md",
             "Modelica.Magnetic.FluxTubes.Shapes.FixedShape.GenericFluxTube",
             "`SI.CrossSection area` with no bound, reaching `1/G_m` two classes away"),
    "B_myMax": ("BUG-011-fluxtubes-b-mymax-unguarded-divisor.md",
                "Modelica.Magnetic.FluxTubes.Material.SoftMagnetic.BaseData",
                "`SI.MagneticFluxDensity B_myMax` with no bound, used as a divisor"),
    "ratio": ("BUG-015-idealgear-zero-ratio.md",
              "Modelica.Mechanics.Rotational.Components.IdealGear",
              "`Real ratio` unbounded; at zero the gear decouples"),
    "Vps": ("BUG-016-relational-invariant-between-two-parameters.md",
            "Modelica.Electrical.Analog.Ideal.IdealizedOpAmpLimited",
            "`Vps - Vns` is a divisor; no `min` can express a constraint between two parameters"),
    "f": ("BUG-019-invertingamp-frequency-unbounded-divisor.md",
          "Modelica.Electrical.Analog.Examples.InvertingAmp",
          "`SI.Frequency f` with no bound, reaching four divisions"),
}

FIX = {
    "m": "parameter SI.Mass m(min=Modelica.Constants.small, start=1);",
    "J": "parameter SI.Inertia J(min=Modelica.Constants.small, start=1);",
    "L": "parameter SI.Inductance L(min=Modelica.Constants.small, start=1);",
    "C": "parameter SI.Capacitance C(min=Modelica.Constants.small, start=1);",
    "l": "parameter SI.Length l(min=Modelica.Constants.small) = 0.01;",
    "area": "parameter SI.CrossSection area(min=Modelica.Constants.small) = 0.0001;",
    "B_myMax": "parameter SI.MagneticFluxDensity B_myMax(min=Modelica.Constants.eps);",
    "ratio": "parameter Real ratio(min=Modelica.Constants.eps, start=1);",
    "Vps": "assert(Vps > Vns, \"supply rails must differ\");",
    "f": "parameter SI.Frequency f(min=Modelica.Constants.eps) = 10;",
}


def model_paths() -> dict[str, str]:
    found = {}
    for line in Path("tools/sweep/ALL.list").read_text().splitlines():
        parts = line.split("\t")
        if len(parts) > 1:
            found[parts[1].strip()] = parts[0]
    return found


def declaration_site(path: str, instance: str) -> tuple[int, str]:
    r"""The line where this model declares the instance, and the text of it.

    Three shapes occur in MSL and all three are needed:

        Translational.Components.Mass mass1(      one line
        Modelica...FixedShape.GenericFluxTube     type wrapped onto its own
          genericFluxTube1(                       line, name on the next
        parameter SI.Frequency f=10               not a component at all

    `[ \t]*`, not `\s*`, wherever a line start is anchored: `\s` matches a
    newline, which let `^` anchor on an earlier blank line and reported every
    multi-line declaration one line early.
    """
    root = instance.split(".")[0]
    try:
        text = Path(path).read_text(errors="replace")
    except OSError:
        return 0, ""

    def at(match) -> tuple[int, str]:
        line = text[: match.start()].count("\n") + 1
        return line, " ".join(match.group(0).split()).rstrip("(;")

    # A component declaration, with the type possibly wrapped onto its own line.
    found = re.search(
        rf"^[ \t]*([\w.]+)[ \t\r\n]+{re.escape(root)}[ \t]*[\(;\r\n]",
        text, re.M)
    if found:
        return at(found)

    # A parameter of the model itself, which has no component to point at.
    found = re.search(
        rf"^[ \t]*parameter[ \t]+[\w.]+[ \t]+{re.escape(root)}[ \t]*[=;(]",
        text, re.M)
    if found:
        return at(found)
    return 0, ""


def render(number: int, entry: dict, paths: dict[str, str]) -> tuple[str, str]:
    model = entry["model"]
    target, value = entry["trigger"].split("=", 1)
    instance, parameter = (target.rsplit(".", 1) if "." in target else ("", target))
    base = parameter if parameter in ROOT_CAUSE else target.rsplit(".", 1)[-1]
    cause = ROOT_CAUSE.get(base)
    path = paths.get(model, "")
    line, declaration = declaration_site(path, instance or target)
    # Two roots hold the corpus and only one is the MSL tree, so the prefix is
    # stripped by locating the repository-relative form rather than assuming it.
    relative = path
    for prefix in ("target/msl/", "target/corpus/", "target/cmm/"):
        if path.startswith(prefix):
            relative = path[len(prefix):]
            break

    slug = f"{model.split('.')[-1]}-{target.replace('.', '-')}".lower()
    name = f"BUG-{number:03d}-{slug}.md"
    where = f"`{relative}:{line}`" if line else f"`{relative}`"
    root_link, root_class, root_why = cause or ("", "?", "?")

    body = f"""# BUG-{number:03d}: `{model.split('.')[-1]}.{target}` fails at `{value}`, a value its declaration permits

| | |
|---|---|
| **Model** | `{model}` |
| **File** | {where} |
| **Instance** | `{instance or "(model parameter)"}` |
| **Parameter** | `{parameter}` |
| **Trigger** | `{target} = {value}` |
| **Reach** | this trigger reproduces in {entry['reach']} model{'s' if entry['reach'] != 1 else ''} |
| **Confirmed in** | Rumoca **and** OpenModelica 1.27.0-dev |
| **Status** | Reported, not fixed |

## The instance

```modelica
// {relative}:{line}
{declaration or f"{instance}"}
```

`{instance or model.split('.')[-1]}` is an instance of `{root_class}`.

## What happens

The model simulates cleanly at its declared values in both tools. Overriding
`{target}` to `{value}` — a value nothing in the declaration excludes — makes it fail in
both:

```console
$ rumoca compile-bitcode {model.split('.')[-1].lower()}.rbc --simulate --check --param {target}={value}
```

## Root cause

{root_why}

The declaration to change is in the component, not in this model:
[{root_link.split('-')[0]}-{root_link.split('-')[1]}]({root_link}) carries the
argument and the suggested patch.

```modelica
// the fix, in {root_class.split('.')[-1]}
{FIX.get(base, "")}
```

## Why this instance has its own report

The root cause is one edit to `{root_class.split('.')[-1]}`. This file exists because
that is not the only thing a developer needs: `{relative.split('/')[-1]}` was proven to
fail at this specific instance, and a maintainer looking at that model needs to
know which of its components was exercised and at what value. Sibling instances
in the same file are reported separately for the same reason.
"""
    return name, body


def main() -> int:
    entries = json.loads(Path(sys.argv[1]).read_text())
    start = int(sys.argv[2])
    paths = model_paths()
    entries.sort(key=lambda e: (-e["reach"], e["model"], e["trigger"]))
    written = []
    for offset, entry in enumerate(entries):
        name, body = render(start + offset, entry, paths)
        (BUGS / name).write_text(body)
        written.append((start + offset, name, entry))
    print(f"wrote {len(written)} instance reports")
    for number, name, entry in written:
        print(f"  BUG-{number:03d}  {entry['model'].split('.')[-1]:28} {entry['trigger']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
