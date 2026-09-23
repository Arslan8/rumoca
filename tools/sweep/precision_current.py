#!/usr/bin/env python3
"""Precision on the *current* run, reusing what is still valid from the old one.

A precision figure belongs to the run it was measured on. When a compiler fix
changes what the sanitizers can see, the old sample cannot simply be requoted —
but nor does it all have to be thrown away, and throwing it away would mean
re-adjudicating hundreds of draws that nothing has changed about.

So the population is split three ways per stratum:

  unchanged        same population, same draws        reuse the verdicts
  carried over     draws that survive into this run   still a valid SRS of the
                                                      subset they survive into
  new              never eligible for the old draw    must be adjudicated

Restricting a simple random sample to a subset leaves a simple random sample of
that subset, which is why the carried-over draws stay usable. The new part has
no sample at all, so it is adjudicated exhaustively and enters as a census with
no sampling error.

    tools/sweep/precision_current.py
    tools/sweep/precision_current.py --run other.jsonl --new other_sample.json
"""
from __future__ import annotations

import argparse
import json
import math
from collections import Counter
from pathlib import Path

BASELINE = Path("docs/runs/data/STATIC_FINAL.jsonl")
CURRENT = Path("docs/runs/data/STATIC_WITH_FAMILIES_AND_CALLS.jsonl")
SAMPLE = Path("docs/runs/data/SAMPLE.json")
NEW_SAMPLE = Path("docs/runs/data/SAMPLE_NEW_DIVISORS.json")


def wilson(successes: int, trials: int, z: float = 1.96) -> tuple[float, float]:
    if trials == 0:
        return (0.0, 1.0)
    p = successes / trials
    denominator = 1 + z * z / trials
    centre = (p + z * z / (2 * trials)) / denominator
    spread = z * math.sqrt(p * (1 - p) / trials
                           + z * z / (4 * trials * trials)) / denominator
    return (max(0.0, centre - spread), min(1.0, centre + spread))


def target_of(evidence: dict) -> str:
    if evidence.get("parameter"):
        return str(evidence["parameter"])
    for key in ("required", "where"):
        text = str(evidence.get(key, "")).split()
        if text:
            return text[0]
    return ""


def occurrences(path: Path) -> Counter:
    """(model, kind, target) -> how many findings share it."""
    found = Counter()
    for line in path.read_text().splitlines():
        row = json.loads(line)
        for finding in row.get("findings", []):
            found[(row["model"], finding["kind"],
                   target_of(finding["evidence"]))] += 1
    return found


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--run", type=Path, default=CURRENT)
    parser.add_argument("--baseline", type=Path, default=BASELINE)
    parser.add_argument("--sample", type=Path, default=SAMPLE)
    parser.add_argument("--new", type=Path, default=NEW_SAMPLE)
    args = parser.parse_args()

    old, current = occurrences(args.baseline), occurrences(args.run)
    sizes = Counter()
    for (_, kind, _), count in current.items():
        sizes[kind] += count

    sample = json.loads(args.sample.read_text())
    alive = [e for e in sample
             if (e["model"], e["kind"], e["target"]) in current]
    withdrawn = len(sample) - len(alive)
    census = json.loads(args.new.read_text()) if args.new.exists() else []
    census_by_kind: dict[str, list] = {}
    for entry in census:
        census_by_kind.setdefault(entry["kind"], []).append(entry)

    blank = [e for e in alive + census if not (e.get("verdict") or "").strip()]
    if blank:
        print(f"{len(blank)} draws are unadjudicated; a figure would be a guess.")
        return 1

    print(f"{'stratum':<36}{'pop':>6}{'n':>5}{'TP':>4}{'FP':>4}{'?':>4}"
          f"  precision      95% CI")
    print("-" * 92)

    total = sum(sizes.values())
    weighted = low_total = high_total = 0.0
    notes = []
    for kind in sorted(sizes):
        drawn = [e for e in alive if e["kind"] == kind]
        counts = Counter(e["verdict"] for e in drawn)
        judged = counts["true-positive"] + counts["false-positive"]
        sampled_p = counts["true-positive"] / judged if judged else 0.0
        low, high = wilson(counts["true-positive"], judged)

        fresh = census_by_kind.get(kind, [])
        if fresh:
            # This stratum has a part the old sample could never have reached.
            carried = sum(n for key, n in current.items()
                          if key[1] == kind and key in old)
            new_count = sizes[kind] - carried
            fresh_counts = Counter(e["verdict"] for e in fresh)
            fresh_judged = (fresh_counts["true-positive"]
                            + fresh_counts["false-positive"])
            fresh_p = (fresh_counts["true-positive"] / fresh_judged
                       if fresh_judged else 0.0)
            blend = lambda value: (carried * value + new_count * fresh_p) / sizes[kind]
            p, low, high = blend(sampled_p), blend(low), blend(high)
            counts += fresh_counts
            drawn = drawn + fresh
            notes.append(f"  {kind}: {carried} carried over estimated from "
                         f"{len(drawn) - len(fresh)} draws ({sampled_p * 100:.1f}%), "
                         f"{new_count} new adjudicated exhaustively "
                         f"({fresh_p * 100:.1f}%)")
        else:
            p = sampled_p

        weighted += sizes[kind] * p
        low_total += sizes[kind] * low
        high_total += sizes[kind] * high
        print(f"{kind:<36}{sizes[kind]:>6}{len(drawn):>5}"
              f"{counts['true-positive']:>4}{counts['false-positive']:>4}"
              f"{counts['undecidable']:>4}"
              f"  {p * 100:>6.1f}%   [{low * 100:>5.1f}, {high * 100:>5.1f}]")

    print("-" * 92)
    print(f"{'TOTAL':<36}{total:>6}"
          f"  {weighted / total * 100:>36.1f}%"
          f"   [{low_total / total * 100:.1f}, {high_total / total * 100:.1f}]")
    if notes:
        print("\nstrata combining a sample with a census:")
        print("\n".join(notes))
    if withdrawn:
        print(f"\n{withdrawn} of {len(sample)} original draws no longer appear "
              f"in this run and were dropped. Restricting a simple random "
              f"sample to a subset leaves a simple random sample of that "
              f"subset, so the survivors stay usable.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
