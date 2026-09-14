#!/usr/bin/env python3
"""Verify OMC-backend findings, attributing each to the class that declares it.

Supersedes verify_causes.py, which grouped by the parameter's leaf name. That
was unsound: 14 components declare `k` and 26 declare `Goff`, so a finding in an
OpAmps example was being pinned on `Blocks/package.mo` because both spell it
`k`. Attribution now comes from the model's own component structure.

The funnel, in order:

1. Resolve the declaring class for every (model, parameter path).
2. Group by (declaring class, parameter) — one defect, however many models.
3. Find the declaration in that class's source and read its bounds.
4. Drop anything the class guards (`if p > 0 then ... else ...`).
5. Separate core library from Examples/Utilities, and separate what the finding
   proves: zero permitted by a written bound, zero permitted by omission, or
   failure at the component's own positive bound.
"""
import collections, json, re, sys
from pathlib import Path

sys.path[:0] = ["tools/sweep"]
from resolve_types import declaring_classes

MSL = Path("target/msl/ModelicaStandardLibrary-4.1.0/Modelica 4.1.0")
CORPUS = Path("target/corpus/ModelicaStandardLibrary-4.1.0")


def class_file(name: str) -> Path | None:
    """MSL stores one class per file under a directory per package."""
    if name.startswith("Modelica."):
        base, parts = MSL, name.split(".")[1:]
    elif name.startswith("ModelicaTest."):
        base, parts = CORPUS / "ModelicaTest", name.split(".")[1:]
    else:
        return None
    direct = base.joinpath(*parts).with_suffix(".mo")
    if direct.exists():
        return direct
    package = base.joinpath(*parts) / "package.mo"
    return package if package.exists() else None


def declaration(path: Path, leaf: str) -> tuple[int, str] | None:
    try:
        text = path.read_text(errors="replace")
    except OSError:
        return None
    pattern = re.compile(
        r"parameter\s+[\w.]+\s+" + re.escape(leaf)
        + r"\s*(?:\[[^\]]*\])?\s*(\([^;]*?\))?\s*(?:=|\"|;)", re.S)
    found = pattern.search(text)
    if not found:
        return None
    return text[: found.start()].count("\n") + 1, " ".join((found.group(1) or "").split())


UNITS = MSL / "Units.mo"
_TYPE_CACHE: dict[str, str] = {}


def type_bounds(type_name: str) -> str | None:
    """The modifiers an SI type declares, e.g. `Capacitance` -> `min=0`.

    Most MSL components declare no bound of their own; the bound arrives with
    the type. `SI.Capacitance` is `Real(..., min=0)`, so `Capacitor C` permits
    zero without `Capacitor.mo` saying so anywhere. A report that claims the
    component declared it would be wrong, and would send a maintainer to the
    wrong file.
    """
    leaf = type_name.rsplit(".", 1)[-1]
    if leaf in _TYPE_CACHE:
        return _TYPE_CACHE[leaf] or None
    try:
        text = UNITS.read_text(errors="replace")
    except OSError:
        return None
    # Three spellings: `type X = Real(mods);`, `type X = Base(mods);`, and a
    # plain alias `type X = Base;`. Temperature is the last kind, so requiring
    # parentheses lost every bound the thermal types carry.
    found = re.search(
        r"\btype\s+" + re.escape(leaf) + r"\s*=\s*([\w.]+)\s*(?:\(([^;]*?)\))?\s*(?:\"|;)",
        text, re.S)
    if not found:
        _TYPE_CACHE[leaf] = ""
        return None
    base, mods = found.group(1), " ".join((found.group(2) or "").split())
    if "min" not in mods and base not in ("Real", "Integer", "Boolean", "String"):
        inherited = type_bounds(base)  # e.g. SelfInductance = Inductance(min=0)
        mods = inherited or mods
    _TYPE_CACHE[leaf] = mods
    return mods or None


def declared_type(path: Path, leaf: str) -> str | None:
    try:
        text = path.read_text(errors="replace")
    except OSError:
        return None
    found = re.search(r"parameter\s+([\w.]+)\s+" + re.escape(leaf) + r"\b", text)
    return found.group(1) if found else None


def guarded(path: Path, leaf: str) -> bool:
    try:
        text = path.read_text(errors="replace")
    except OSError:
        return False
    index = text.find("equation")
    body = text[index:] if index >= 0 else text
    n = re.escape(leaf)
    return bool(re.search(r"\b" + n + r"\s*(>|>=|<>)\s*0", body)
                or re.search(r"abs\s*\(\s*" + n + r"\s*\)\s*>", body))


def claim(hits) -> str:
    """Use the claim the probe recorded, not one re-derived from the value.

    The sweep knows why it tried a value; re-deriving it here from the number
    alone cannot distinguish a negative probe from a positive declared bound,
    and silently filed every negative finding under the wrong heading.
    """
    recorded = [f.get("claim") for _, f in hits if f.get("claim")]
    if recorded:
        # Strongest claim present wins: one model where the bound explicitly
        # admits the value is a better statement than several where it is
        # merely unbounded.
        order = ["zero-permitted-by-bound", "fails-at-its-own-positive-bound",
                 "fails-at-its-own-upper-bound", "negative-permitted-by-omission",
                 "zero-permitted-by-omission"]
        for kind in order:
            if kind in recorded:
                return kind
        return recorded[0]

    values = {f["value"] for _, f in hits}
    tiers = {f["tier"] for _, f in hits}
    if values == {0.0}:
        return ("zero-permitted-by-bound" if "declared-permits" in tiers
                else "zero-permitted-by-omission")
    return "fails-at-its-own-positive-bound"


def main(sweep: str, out: str):
    rows = []
    for line in Path(sweep).read_text().splitlines():
        try:
            rows.append(json.loads(line))
        except ValueError:
            continue

    pairs = sorted({(r["model"], f["parameter"])
                    for r in rows for f in r.get("findings", [])})
    print(f"resolving declaring class for {len(pairs)} (model, parameter) pairs...",
          flush=True)
    owners = declaring_classes(list(pairs))

    groups = collections.defaultdict(list)
    for r in rows:
        for f in r.get("findings", []):
            owner = owners.get((r["model"], f["parameter"]), r["model"])
            groups[(owner, f["parameter"].rsplit(".", 1)[-1])].append((r["model"], f))

    verified, dropped = [], []
    for (owner, leaf), hits in groups.items():
        models = sorted({m for m, _ in hits})
        source = class_file(owner)
        if source is None:
            dropped.append({"class": owner, "parameter": leaf,
                            "models": len(models), "reason": "class source not found"})
            continue
        decl = declaration(source, leaf)
        if decl is None:
            dropped.append({"class": owner, "parameter": leaf, "models": len(models),
                            "reason": "parameter not declared in the resolved class"})
            continue
        if guarded(source, leaf):
            dropped.append({"class": owner, "parameter": leaf, "models": len(models),
                            "reason": "the class guards the degenerate value"})
            continue
        line, mods = decl
        type_name = declared_type(source, leaf)
        inherited = None if "min" in mods else (
            type_bounds(type_name) if type_name else None)
        bound_from = "component" if "min" in mods else (
            f"type {type_name}" if inherited and "min" in inherited else "nothing")
        relative = str(source.relative_to(MSL.parent if owner.startswith("Modelica.")
                                          else CORPUS.parent))
        verified.append({
            "class": owner, "parameter": leaf, "claim": claim(hits),
            "file": relative, "line": line, "modifiers": mods,
            "declared_type": type_name, "type_modifiers": inherited,
            "bound_declared_by": bound_from,
            "models": models, "model_count": len(models),
            "core_library": "/Examples/" not in relative and "/Utilities/" not in relative,
            "omc_blames_it": sum(1 for _, f in hits if f["blamed"]),
        })

    order = {"zero-permitted-by-bound": 0, "fails-at-its-own-positive-bound": 1,
             "fails-at-its-own-upper-bound": 2, "negative-permitted-by-omission": 3,
             "zero-permitted-by-omission": 4}
    verified.sort(key=lambda v: (not v["core_library"], order.get(v["claim"], 9),
                                 -v["model_count"]))
    Path(out).write_text(json.dumps({"verified": verified, "dropped": dropped}, indent=1))

    core = [v for v in verified if v["core_library"]]
    print(f"\ncandidates {len(groups)} -> verified {len(verified)} "
          f"({len(core)} core library), dropped {len(dropped)}\n")
    print("=== core-library findings, strongest first ===")
    for v in core:
        print(f"  [{v['claim']:31}] {v['class'].split('.',1)[1]:52} {v['parameter']:16}"
              f" {v['model_count']:3} models")
        origin = v["bound_declared_by"]
        detail = v["modifiers"] if origin == "component" else (v["type_modifiers"] or "")
        print(f"        {v['file']}:{v['line']}   bound from {origin}"
              f"{('  [' + detail + ']') if detail else ''}")
    print("\n=== dropped ===")
    for reason, n in collections.Counter(d["reason"] for d in dropped).most_common():
        print(f"  {n:4}  {reason}")


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
