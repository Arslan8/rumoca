#!/usr/bin/env python3
"""Group OMC-backend findings by root cause and rank them by strength.

One defect in a shared component shows up once per example model that uses it —
`Inertia J(min=0)` produced findings in four unrelated Clocked examples. Counting
model instances overstates how much is wrong; counting distinct
(component, parameter) pairs is the number that means something.
"""
import collections, json, re, sys
from pathlib import Path

# `load.J` -> `J`; `genericFluxTube.material.B_myMax` -> `B_myMax`
LEAF = re.compile(r"([^.]+)$")


def leaf(name: str) -> str:
    found = LEAF.search(name)
    return found.group(1) if found else name


def main(path: str, out: str | None):
    rows = []
    for line in Path(path).read_text().splitlines():
        try:
            rows.append(json.loads(line))
        except ValueError:
            continue

    status = collections.Counter(r["status"] for r in rows)
    searched = [r for r in rows if r["status"] == "searched"]
    findings = [(r["model"], f) for r in rows for f in r.get("findings", [])]

    # A root cause is the parameter's own leaf name plus the tier: the same leaf
    # reached through different instance paths is one defect in one component.
    groups = collections.defaultdict(list)
    for model, f in findings:
        groups[(leaf(f["parameter"]), f["tier"])].append((model, f))

    print("=== corpus ===")
    for k, n in status.most_common():
        print(f"  {n:5}  {k}")
    print(f"  {len(rows):5}  total")
    trials = sum(r.get("trials", 0) for r in searched)
    print(f"\nsearched {len(searched)} models, {trials} trials, "
          f"{len(findings)} failing (parameter, model) pairs")
    print(f"distinct root causes: {len(groups)}\n")

    ranked = sorted(groups.items(), key=lambda kv: (kv[0][1] != "declared-permits",
                                                    -len(kv[1])))
    print("=== root causes, strongest first ===")
    for (name, tier), hits in ranked:
        models = sorted({m for m, _ in hits})
        blamed = sum(1 for _, f in hits if f["blamed"])
        mins = {f["declared_min"] for _, f in hits}
        print(f"  [{tier:16}] {name:24} {len(models):3} models  "
              f"min={sorted(m for m in mins if m is not None) or 'none'}"
              f"  omc-blames-it={blamed}")
        for m in models[:3]:
            print(f"        {m}")
        if len(models) > 3:
            print(f"        ... {len(models) - 3} more")

    if out:
        Path(out).write_text(json.dumps({
            "status": dict(status),
            "root_causes": [
                {"parameter": name, "tier": tier,
                 "models": sorted({m for m, _ in hits}),
                 "declared_min": sorted({f["declared_min"] for _, f in hits
                                         if f["declared_min"] is not None}),
                 "example_detail": hits[0][1]["detail"][:200]}
                for (name, tier), hits in ranked
            ],
        }, indent=1))


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2] if len(sys.argv) > 2 else None)
