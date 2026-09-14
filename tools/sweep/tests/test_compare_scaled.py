#!/usr/bin/env python3
"""Calibration for the trajectory-divergence detector.

A differential detector is only worth its output if it separates solver noise
from a wrong answer. These cases pin both directions: the ones that must stay
quiet, and the ones that must fire. Run with `python3 tools/sweep/tests/test_compare_scaled.py`.
"""
import importlib.util
import math
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path[:0] = [str(ROOT / "packages/rumoca-bitcode"), str(ROOT / "packages/modelsan")]

spec = importlib.util.spec_from_file_location("td", ROOT / "tools/sweep/trajdiff.py")
td = importlib.util.module_from_spec(spec)
spec.loader.exec_module(td)

from modelsan.differential import OmcResult

TIMES = [i * 0.1 for i in range(11)]
BASE = [math.exp(-t) for t in TIMES]


def verdict(other, rtol=0.05):
    omc = OmcResult(accepted=True, trajectory={"x": other}, times=TIMES)
    found = td.compare_scaled(["x"], TIMES, [BASE], omc, rtol=rtol, atol=1e-6)
    return found[0].kind if found else "agree"


CASES = [
    # Must stay quiet: two integrators at their own default tolerances.
    ("identical", list(BASE), "agree"),
    ("0.1% solver noise", [v * 1.001 for v in BASE], "agree"),
    ("2% noise, under threshold", [v * 1.02 for v in BASE], "agree"),
    # The false positive that motivated scaling by signal range: a small
    # absolute offset on a quantity decaying to zero is a huge *relative* one.
    ("decaying-tail offset", [v + 1e-4 for v in BASE], "agree"),
    # Must fire.
    ("20% error", [v * 1.20 for v in BASE], "trajectory-divergence"),
    ("wrong sign", [-v for v in BASE], "trajectory-divergence"),
    ("NaN in one tool", [float("nan")] * 11, "nan-disagreement"),
]


def main():
    failures = 0
    for label, other, expected in CASES:
        got = verdict(other)
        ok = got == expected
        failures += not ok
        print(f"{'PASS' if ok else 'FAIL'}  {label:32} expected={expected:24} got={got}")
    print(f"\n{len(CASES) - failures}/{len(CASES)} passed")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
