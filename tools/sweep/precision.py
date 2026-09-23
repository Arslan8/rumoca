#!/usr/bin/env python3
"""Precision from an adjudicated stratified sample, with an interval.

Two things this does that a bare `TP/(TP+FP)` does not.

**Weights the strata.** The sample takes 30 of each kind, but the population is
8135 `physical-domain-unenforced` against 8 `divisor-zero-when-parameters-equal`.
Pooling the raw counts would let a rare kind swing the estimate by three orders
of magnitude more than its share of the findings.

**Reports an interval.** 30 draws from a stratum of 8135 gives a wide one, and a
point estimate printed without it invites a reader to believe a digit that is
not there. Wilson rather than normal-approximation, because at the ends — where
a stratum is all true positives or all false — the normal interval is nonsense.
"""
from __future__ import annotations

import json
import math
import sys
from collections import defaultdict
from pathlib import Path

VALID = {"true-positive", "false-positive", "undecidable"}


def wilson(successes: int, trials: int, z: float = 1.96) -> tuple[float, float]:
    if trials == 0:
        return (0.0, 1.0)
    p = successes / trials
    denominator = 1 + z * z / trials
    centre = (p + z * z / (2 * trials)) / denominator
    spread = z * math.sqrt(p * (1 - p) / trials + z * z / (4 * trials * trials)) / denominator
    return (max(0.0, centre - spread), min(1.0, centre + spread))


def main() -> int:
    sample = json.loads(Path(sys.argv[1]).read_text())
    strata = defaultdict(lambda: {"tp": 0, "fp": 0, "undecidable": 0,
                                  "blank": 0, "size": 0})
    for entry in sample:
        stratum = strata[entry["kind"]]
        stratum["size"] = entry["stratum_size"]
        verdict = (entry.get("verdict") or "").strip()
        if verdict == "true-positive":
            stratum["tp"] += 1
        elif verdict == "false-positive":
            stratum["fp"] += 1
        elif verdict == "undecidable":
            stratum["undecidable"] += 1
        else:
            stratum["blank"] += 1

    blank = sum(s["blank"] for s in strata.values())
    drawn = sum(s["tp"] + s["fp"] + s["undecidable"] + s["blank"] for s in strata.values())
    if blank:
        # Refused rather than estimated. An unadjudicated draw is missing data,
        # and dropping it silently biases the result toward whichever verdicts
        # were easy to reach.
        print(f"{blank} of {drawn} sampled findings are unadjudicated.")
        print("Fill every `verdict` before a precision figure means anything.")
        return 1

    print(f"{'kind':38} {'n':>4} {'TP':>4} {'FP':>4} {'?':>3}  precision (95% CI)")
    population = sum(s["size"] for s in strata.values())
    weighted = 0.0
    for kind, s in sorted(strata.items()):
        judged = s["tp"] + s["fp"]
        p = s["tp"] / judged if judged else 0.0
        low, high = wilson(s["tp"], judged)
        weighted += p * s["size"]
        print(f"{kind:38} {s['size']:>4} {s['tp']:>4} {s['fp']:>4} "
              f"{s['undecidable']:>3}  {100 * p:5.1f}%  [{100 * low:.1f}, {100 * high:.1f}]")

    print(f"\npopulation-weighted precision: {100 * weighted / population:.1f}%")
    print(f"  over {population} findings, from {drawn} adjudicated draws")
    print("  strata are weighted by population share, so the 8-member stratum")
    print("  does not count as much as the 8135-member one")
    return 0


if __name__ == "__main__":
    sys.exit(main())
