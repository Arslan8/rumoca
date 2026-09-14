#!/usr/bin/env python3
"""Verify OMC-backend root causes against the library source before reporting.

The sweep says "setting `J` to 0 broke 12 models". That is a candidate, not a
finding. Four things have to be checked, and each of them removed real false
positives earlier in this project:

* **Which component actually declares it.** `C(min=0)` reached 19 models, but
  the declarer is `Examples/Utilities/DirectCapacitor` — a demo helper, not
  library code. Reach overstates importance when the count is per model.
* **Is the degenerate value guarded?** `EddyCurrent` writes
  `if G > 0 then ... else V_m.re = 0`, which honours `min=0`.
* **Is the failing expression reachable at that value?** `Ramp.duration` divides
  inside a branch that is empty when `duration = 0`.
* **Is it core library or an example?** Both are real, but only one is a defect
  users inherit.
"""
import collections, json, re, sys
from pathlib import Path

MSL = Path("target/msl/ModelicaStandardLibrary-4.1.0")


def declarations(leaf: str) -> list[tuple[str, int, str]]:
    """Every `parameter <type> <leaf>(...)` in the library, with its file."""
    pattern = re.compile(
        r"parameter\s+([\w.]+)\s+" + re.escape(leaf) + r"\s*(?:\[[^\]]*\])?\s*\(([^;]*?)\)",
        re.S,
    )
    found = []
    for mo in MSL.rglob("*.mo"):
        try:
            text = mo.read_text(errors="replace")
        except OSError:
            continue
        for match in pattern.finditer(text):
            mods = " ".join(match.group(2).split())
            if "min" in mods:
                found.append((str(mo.relative_to(MSL)),
                              text[: match.start()].count("\n") + 1, mods[:80]))
    return found


def guarded(path: str, leaf: str) -> bool:
    try:
        text = (MSL / path).read_text(errors="replace")
    except OSError:
        return False
    index = text.find("equation")
    body = text[index:] if index >= 0 else text
    n = re.escape(leaf)
    return bool(re.search(r"\b" + n + r"\s*(>|>=|<>)\s*0", body)
                or re.search(r"abs\s*\(\s*" + n + r"\s*\)\s*>", body))


def is_example(path: str) -> bool:
    return "/Examples/" in path or "/Utilities/" in path


def claim_strength(tier: str, hits) -> str:
    """What the finding actually proves.

    Failing at zero when the declaration says `min=0` is the strongest claim
    available: the component wrote a bound that includes the value, and the
    value provably breaks it.

    Failing at a positive declared bound — `min=Modelica.Constants.small`, which
    is 1e-60 — is the same *kind* of contradiction but a far weaker one in
    practice. No calibration loop lands on 1e-60 by accident, and an integrator
    struggling there is closer to a numerical limit than a defect. Reported
    separately so the two are never summed.
    """
    values = {f["value"] for _, f in hits}
    if tier == "unbounded":
        return "zero-permitted-by-omission"
    if values == {0.0}:
        return "zero-permitted-by-bound"
    return "fails-at-its-own-positive-bound"


def main(sweep: str, out: str):
    rows = []
    for line in Path(sweep).read_text().splitlines():
        try:
            rows.append(json.loads(line))
        except ValueError:
            continue

    groups = collections.defaultdict(list)
    for r in rows:
        for f in r.get("findings", []):
            groups[(f["parameter"].rsplit(".", 1)[-1], f["tier"])].append((r["model"], f))

    verified, rejected, ambiguous = [], [], []
    for (leaf, tier), hits in groups.items():
        models = sorted({m for m, _ in hits})
        decls = declarations(leaf)
        if not decls:
            rejected.append({"parameter": leaf, "tier": tier, "models": len(models),
                             "reason": "no library declaration found for this leaf name"})
            continue
        unguarded = [d for d in decls if not guarded(d[0], leaf)]
        if not unguarded:
            rejected.append({"parameter": leaf, "tier": tier, "models": len(models),
                             "reason": "every declaring component guards the value"})
            continue
        core = [d for d in unguarded if not is_example(d[0])]
        # Attribution by leaf name is only sound when the library declares that
        # name once. `k` is declared by many components, so mapping a finding in
        # an OpAmps example to `Blocks/package.mo` because both spell it `k`
        # would put the wrong file in a bug report. Those are held back for
        # manual resolution rather than guessed at.
        entry = {
            "parameter": leaf,
            "tier": tier,
            "claim": claim_strength(tier, hits),
            "models": models,
            "model_count": len(models),
            "declarations": [{"file": f, "line": n, "modifiers": m}
                             for f, n, m in unguarded],
            "in_core_library": bool(core),
            "omc_blames_it": sum(1 for _, f in hits if f["blamed"]),
        }
        if len(unguarded) > 1:
            entry["reason"] = f"{len(unguarded)} components declare `{leaf}`; attribution needs the instance type"
            ambiguous.append(entry)
        else:
            verified.append(entry)

    verified.sort(key=lambda v: (not v["in_core_library"],
                                 v["tier"] != "declared-permits",
                                 -v["model_count"]))
    ambiguous.sort(key=lambda v: -v["model_count"])
    Path(out).write_text(json.dumps(
        {"verified": verified, "ambiguous": ambiguous, "rejected": rejected}, indent=1))

    core = [v for v in verified if v["in_core_library"]]
    print(f"candidates {len(groups)} -> attributed {len(verified)} "
          f"({len(core)} core library), ambiguous {len(ambiguous)}, "
          f"rejected {len(rejected)}")
    print("\n=== attributed core-library findings, strongest first ===")
    for v in sorted(core, key=lambda v: (v["claim"] != "zero-permitted-by-bound",
                                         -v["model_count"])):
        d = v["declarations"][0]
        print(f"  [{v['claim']:32}] {v['parameter']:18} {v['model_count']:3} models  "
              f"{d['file']}:{d['line']}")
    print("\n=== held back: leaf name declared by several components ===")
    for v in ambiguous[:10]:
        print(f"  {v['parameter']:18} {v['model_count']:3} models  "
              f"({len(v['declarations'])} declarers)")
    print("\n=== rejected ===")
    for r in collections.Counter(r["reason"] for r in rejected).most_common():
        print(f"  {r[1]:4}  {r[0]}")


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
