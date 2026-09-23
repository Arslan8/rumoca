#!/usr/bin/env python3
"""Decide a divisor finding by executing the witness it names.

The older adjudicator always set the parameter to zero, which was right while
every finding claimed "this parameter can be zero". A finding now carries a
*witness*: a complete assignment, which may set one knob to zero, may set two
knobs equal, and may name a value that is neither. Judging it means applying
that assignment and no other.

    baseline clean, witness applied -> fails   true-positive
    baseline clean, witness applied -> clean   false-positive for this model
    baseline not clean                         undecidable, nothing to attribute

The baseline requirement is not a formality. A model that does not run at its
declared values cannot tell us anything about a parameter, and recording that
as a false positive would credit the tool for a judgement it did not make.
"""
from __future__ import annotations

import concurrent.futures
import json
import re
import subprocess
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, "tools/sweep")
from static_eval import ROOTS, RUMOCA, default_jobs           # noqa: E402

FAIL = ("simulation-failure", "DAE structural", "below-min", "above-max")
#: Kinds that assert a defect. The guarded kinds are not judged: they say the
#: division is protected, and executing them would test the guard, not the claim.
JUDGED = {"divisor-reachable-zero", "divisor-zero-when-parameters-equal"}


def paths() -> dict[str, str]:
    found = {}
    for line in Path("tools/sweep/ALL.list").read_text().splitlines():
        parts = line.split("\t")
        if len(parts) > 1:
            found[parts[1].strip()] = parts[0]
    return found


def parse_witness(text: str) -> list[tuple[str, float]]:
    """`a = 1, b = -15` -> [("a", 1.0), ("b", -15.0)]."""
    out = []
    for part in text.split(","):
        match = re.match(r"\s*([\w.\[\]]+)\s*=\s*(-?[\d.eE+-]+)\s*$", part)
        if match:
            try:
                out.append((match.group(1), float(match.group(2))))
            except ValueError:
                continue
    return out


def simulate(artifact: Path, overrides: list[tuple[str, float]]) -> str:
    command = [RUMOCA, "compile-bitcode", str(artifact), "--simulate", "--check",
               "--t-end", "0.5"]
    for name, value in overrides:
        command += ["--param", f"{name}={value:g}"]
    try:
        done = subprocess.run(command, capture_output=True, text=True, timeout=120)
    except subprocess.TimeoutExpired:
        return "timeout"
    text = done.stdout + done.stderr
    if "not a tunable parameter" in text:
        return "no-such-parameter"
    return "fail" if any(marker in text for marker in FAIL) else "clean"


def judge(job):
    model, witness_text, path = job
    overrides = parse_witness(witness_text)
    if not overrides:
        return (model, witness_text, "undecidable", "the witness names no value")

    with tempfile.TemporaryDirectory() as work:
        artifact = Path(work) / "m.rbc"
        command = [RUMOCA, "compile", path, "--model", model,
                   "--emit-bitcode", str(artifact), "--no-fold-parameter-bindings"]
        for root in ROOTS:
            command += ["--source-root", root]
        try:
            subprocess.run(command, capture_output=True, timeout=180)
        except subprocess.TimeoutExpired:
            return (model, witness_text, "undecidable", "compile timed out")
        if not artifact.exists():
            return (model, witness_text, "undecidable",
                    "this tool cannot compile the model")

        if simulate(artifact, []) != "clean":
            return (model, witness_text, "undecidable",
                    "baseline is not clean; nothing can be attributed")
        verdict = simulate(artifact, overrides)
        if verdict == "no-such-parameter":
            return (model, witness_text, "undecidable",
                    "the witness names something this artifact cannot override")
        if verdict == "fail":
            return (model, witness_text, "true-positive",
                    "baseline clean, and the model fails under the witness")
        return (model, witness_text, "false-positive",
                f"baseline clean and the model still runs under the witness "
                f"({verdict})")


def main() -> int:
    sample = json.loads(Path(sys.argv[1]).read_text())
    where = paths()
    jobs, index = [], {}
    for position, entry in enumerate(sample):
        if entry["kind"] not in JUDGED or entry.get("verdict"):
            continue
        path = where.get(entry["model"])
        if path is None:
            continue
        witness = entry["evidence"].get("witness", "")
        key = (entry["model"], witness)
        if key in index:
            continue
        index[key] = position
        jobs.append((entry["model"], witness, path))

    workers = min(8, default_jobs())
    print(f"judging {len(jobs)} witnesses on {workers} workers")
    with concurrent.futures.ProcessPoolExecutor(max_workers=workers) as pool:
        for model, witness, verdict, reason in pool.map(judge, jobs):
            entry = sample[index[(model, witness)]]
            entry["verdict"], entry["reason"] = verdict, reason
            print(f"  {verdict:15} {model.split('.')[-1]:30} {witness[:40]}")

    Path(sys.argv[1]).write_text(json.dumps(sample, indent=1))
    decided = sum(1 for e in sample if e.get("verdict"))
    print(f"\n{decided}/{len(sample)} of the sample now has a verdict")
    return 0


if __name__ == "__main__":
    sys.exit(main())
