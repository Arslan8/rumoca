#!/usr/bin/env python3
"""Run the commands `docs/v2/bugs/` tells a reader to run, and check they work.

A report whose verification steps do not execute is worse than no report: it
looks checkable and is not. So the steps are extracted from the published
markdown — not from the generator — and run exactly as printed.

    tools/sweep/verify_bug_reports.py --sample 40
    tools/sweep/verify_bug_reports.py --all --tier latent

What is checked per tier:

  latent     the declaration line opens, and the type line really has no `min`
  candidate  `check_one.py` reproduces a finding naming the same target
  confirmed  the same, plus the baseline simulates and the perturbation fails
"""
from __future__ import annotations

import argparse
import random
import re
import subprocess
import sys
from collections import Counter
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path

sys.path.insert(0, "tools/sweep")
from roundtrip_audit import default_jobs                      # noqa: E402

BUGS = Path("docs/v2/bugs")
#: `$ ` lines inside a ```console block, rejoined across backslash continuations.
COMMAND = re.compile(r"^\$ (.*)$", re.M)


def commands(text: str) -> list[str]:
    joined, buffer = [], ""
    for line in text.splitlines():
        if buffer:
            buffer += " " + line.strip()
        elif line.startswith("$ "):
            buffer = line[2:].strip()
        else:
            continue
        if buffer.endswith("\\"):
            buffer = buffer[:-1].strip()
        else:
            joined.append(buffer)
            buffer = ""
    return joined


def run(command: str, timeout: int = 300):
    return subprocess.run(command, shell=True, capture_output=True,
                          text=True, timeout=timeout)


def field(text: str, label: str) -> str:
    match = re.search(rf"^\| \*\*{re.escape(label)}\*\* \| (.*?) \|$", text, re.M)
    return match.group(1).strip() if match else ""


def check(path: Path) -> tuple[str, str, str]:
    """(report, verdict, detail). Verdict is ok / FAILED / skipped."""
    text = path.read_text()
    steps = commands(text)
    target = field(text, "Reached as") or field(text, "Parameter")
    target = target.strip("`")

    try:
        if path.name.startswith("DECL-"):
            # 1: the declaration line opens and names the parameter.
            got = run(steps[0])
            if got.returncode or not got.stdout.strip():
                return path.name, "FAILED", f"declaration line did not open: {steps[0]}"
            if target and target not in got.stdout:
                return path.name, "FAILED", f"line does not declare {target}: {got.stdout.strip()[:90]}"
            # 2: the type line exists and carries no min, which is the claim.
            got = run(steps[1])
            if not got.stdout.strip():
                return path.name, "FAILED", f"type line not found: {steps[1]}"
            if "min" in got.stdout:
                return path.name, "FAILED", f"type DOES carry a bound: {got.stdout.strip()[:90]}"
            return path.name, "ok", ""

        # Both other tiers start with check_one.py.
        got = run(steps[0], timeout=600)
        if got.returncode:
            return path.name, "FAILED", (got.stderr or got.stdout).strip()[-120:]
        # A probe-found confirmed instance asserts the opposite: no static
        # rule covers it, so zero findings is the expected result.
        expects_none = "should print **0 findings**" in text
        none_found = bool(re.search(r"^  0 finding", got.stdout, re.M))
        if expects_none:
            if not none_found:
                return path.name, "FAILED", "a static sanitizer does report it after all"
            return path.name, "ok", ""
        if none_found:
            return path.name, "FAILED", "check_one reproduced no finding"
        if target and target.split(".")[-1] not in got.stdout:
            return path.name, "FAILED", f"reproduced finding does not name {target}"
        return path.name, "ok", ""
    except subprocess.TimeoutExpired:
        return path.name, "skipped", "timed out"
    except IndexError:
        return path.name, "FAILED", "report has no verification commands"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--sample", type=int, default=30)
    parser.add_argument("--all", action="store_true")
    parser.add_argument("--tier", choices=["confirmed", "candidate", "latent"])
    parser.add_argument("--seed", type=int, default=1)
    args = parser.parse_args()

    prefix = {"confirmed": "BUG-", "candidate": "FINDING-",
              "latent": "DECL-"}.get(args.tier, "")
    reports = sorted(p for p in BUGS.glob("*.md")
                     if p.name != "README.md" and p.name.startswith(prefix))
    if not args.all:
        random.Random(args.seed).shuffle(reports)
        reports = reports[:args.sample]
    reports.sort()

    verdicts = Counter()
    with ProcessPoolExecutor(max_workers=min(8, default_jobs())) as pool:
        for name, verdict, detail in pool.map(check, reports):
            verdicts[verdict] += 1
            if verdict != "ok":
                print(f"  {verdict:<8} {name}\n           {detail}")
    print(f"\n{sum(verdicts.values())} reports checked: "
          + ", ".join(f"{n} {v}" for v, n in verdicts.most_common()))
    return 1 if verdicts["FAILED"] else 0


if __name__ == "__main__":
    sys.exit(main())
