#!/usr/bin/env python3
"""Decide the divisor strata of a sample by execution.

For a divisor finding the oracle really is execution: the claim is "this
parameter reaches a denominator and nothing excludes zero", and whether zero
actually breaks the model depends on topology a static pass cannot see. A
vanishing divisor in a branch nothing reads is harmless.

    baseline clean, override fails  -> true-positive
    baseline clean, override clean  -> false-positive for this model
    baseline not clean              -> undecidable, the tool cannot judge it

Deliberately *not* used for the physical strata. A negative mass that simulates
cleanly is still a negative mass; there the oracle is physics and the
component's own documentation, which no amount of running settles.
"""
from __future__ import annotations

import concurrent.futures
import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path

RUMOCA = "./target/debug/rumoca"
ROOTS = ["target/msl/ModelicaStandardLibrary-4.1.0",
         "target/corpus/ModelicaStandardLibrary-4.1.0", "target/cmm/CMM-a642c381"]
#: Kinds whose claim execution can actually settle.
#:
#: `physical-bound-permits-zero` belongs here for the same reason the divisor
#: kinds do: the claim is that `min=0` admits a value the component cannot
#: honour, and whether it can is a property of its equations.
#: `Mass.m(min=0)` degenerates `m*a = f` and fails; `IdealSwitch.Ron(final
#: min=0)` is a closed switch at its ideal value and runs.
#:
#: Deliberately excludes the other physical kinds. A negative resistance that
#: simulates cleanly is still outside the declared physical domain; there the
#: oracle is the source, not the solver.
EXECUTION_KINDS = {"divisor-reachable-zero", "divisor-zero-when-parameters-equal",
                   "physical-bound-permits-zero"}
FAIL = ("simulation-failure", "DAE structural", "below-min", "above-max")


def paths() -> dict[str, str]:
    found = {}
    for line in Path("tools/sweep/ALL.list").read_text().splitlines():
        parts = line.split("\t")
        if len(parts) > 1:
            found[parts[1].strip()] = parts[0]
    return found


def simulate(artifact: Path, override: tuple[str, float] | None) -> str:
    command = [RUMOCA, "compile-bitcode", str(artifact), "--simulate", "--check",
               "--t-end", "0.5"]
    if override:
        command += ["--param", f"{override[0]}={override[1]:g}"]
    try:
        done = subprocess.run(command, capture_output=True, text=True, timeout=120)
    except subprocess.TimeoutExpired:
        return "timeout"
    text = done.stdout + done.stderr
    if "not a tunable parameter" in text:
        return "no-such-parameter"
    return "fail" if any(marker in text for marker in FAIL) else "clean"


def judge(job):
    model, target, path = job
    with tempfile.TemporaryDirectory() as work:
        artifact = Path(work) / "m.rbc"
        command = [RUMOCA, "compile", path, "--model", model,
                   "--emit-bitcode", str(artifact)]
        for root in ROOTS:
            command += ["--source-root", root]
        try:
            subprocess.run(command, capture_output=True, timeout=180)
        except subprocess.TimeoutExpired:
            return (model, target, "undecidable", "compile timed out")
        if not artifact.exists():
            return (model, target, "undecidable", "this tool cannot compile the model")

        baseline = simulate(artifact, None)
        if baseline != "clean":
            return (model, target, "undecidable",
                    f"baseline is not clean ({baseline}); the tool cannot judge it")
        verdict = simulate(artifact, (target, 0.0))
        if verdict == "no-such-parameter":
            return (model, target, "undecidable", "not tunable in this artifact")
        if verdict == "fail":
            return (model, target, "true-positive",
                    "baseline clean, and the model fails at zero — the declared "
                    "bound admits a value the component cannot honour")
        return (model, target, "false-positive",
                f"baseline clean and the model still runs at zero ({verdict}); "
                "the value the declaration permits is one the component handles")


def main() -> int:
    sample = json.loads(Path(sys.argv[1]).read_text())
    where = paths()
    jobs, index = [], {}
    for position, entry in enumerate(sample):
        if entry["kind"] not in EXECUTION_KINDS or entry.get("verdict"):
            continue
        path = where.get(entry["model"])
        if not path:
            entry["verdict"] = "undecidable"
            entry["reason"] = "model not in the corpus list"
            continue
        jobs.append((entry["model"], entry["target"], path))
        index[(entry["model"], entry["target"])] = position

    workers = max(1, min(16, (os.cpu_count() or 4) - 2))
    with concurrent.futures.ProcessPoolExecutor(max_workers=workers) as pool:
        for model, target, verdict, reason in pool.map(judge, jobs):
            entry = sample[index[(model, target)]]
            entry["verdict"], entry["reason"] = verdict, reason
            print(f"  {verdict:15} {model.split('.')[-1]:28} {target}")

    Path(sys.argv[1]).write_text(json.dumps(sample, indent=1))
    decided = sum(1 for e in sample if e.get("verdict"))
    print(f"\n{decided}/{len(sample)} of the sample now has a verdict")
    return 0


if __name__ == "__main__":
    sys.exit(main())
