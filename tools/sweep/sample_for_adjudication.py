#!/usr/bin/env python3
"""Draw a random sample of findings for hand adjudication.

The whole-population labels cannot give a precision figure, and the reason is
selection, not sample size:

  - every true positive came from the cross-confirmation campaign, which only
    ran on findings with a single-parameter reproducible trigger;
  - every false positive came from a class rule written *after* noticing that
    class, so classes nobody noticed are labelled unjudged.

Dividing one biased subset by another produces a number with no interpretation.
`TP / (TP + FP)` over that subset was 3.2%, which says nothing about the
sanitizer and everything about which findings happened to get looked at.

A defensible figure needs a sample drawn *before* anyone looks, stratified by
finding kind so the rare kinds are estimable, with every drawn finding
adjudicated — including the ones that turn out to be tedious. This writes that
sample as a worksheet; the verdicts go back in and
`precision.py` reports the estimate with a Wilson interval.
"""
from __future__ import annotations

import collections
import json
import random
import sys
from pathlib import Path


def main() -> int:
    rows = [json.loads(l) for l in Path(sys.argv[1]).read_text().splitlines() if l.strip()]
    per_kind = int(sys.argv[2]) if len(sys.argv) > 2 else 30
    seed = int(sys.argv[3]) if len(sys.argv) > 3 else 20260915

    population = collections.defaultdict(list)
    for row in rows:
        for finding in row["findings"]:
            evidence = finding["evidence"]
            predicate = evidence.get("required", "") or ""
            target = predicate.split()[0] if predicate else evidence.get("parameter", "?")
            population[finding["kind"]].append({
                "model": row["model"], "target": target,
                "source": finding.get("source", "?"), "kind": finding["kind"],
                "severity": finding["severity"], "sanitizer": finding["sanitizer"],
                "evidence": evidence,
            })

    rng = random.Random(seed)
    sample = []
    for kind, items in sorted(population.items()):
        take = min(per_kind, len(items))
        for item in rng.sample(items, take):
            sample.append({**item, "stratum_size": len(items),
                           "verdict": "", "reason": ""})

    out = Path(sys.argv[4]) if len(sys.argv) > 4 else Path("docs/runs/data/SAMPLE.json")
    out.write_text(json.dumps(sample, indent=1))

    print(f"seed {seed}, {per_kind} per kind -> {len(sample)} findings to adjudicate")
    for kind, items in sorted(population.items()):
        print(f"  {min(per_kind, len(items)):3} of {len(items):6}  {kind}")
    print(f"\nwrote {out}")
    print("Fill each entry's \"verdict\" with true-positive | false-positive | "
          "undecidable, and \"reason\" with what settled it.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
