#!/usr/bin/env python3
"""Cross-confirm the pipeline evaluation's findings in the second tool.

The evaluation produces findings; this decides which of them are statements
about a *model* rather than about one tool. Every earlier round of this project
lost most candidates here — 147 to 7, then 168 to 8 — so running it is not
optional bookkeeping, it is the step that makes a count defensible.

A finding is confirmed when the trigger reproduces in the other tool on a model
whose declared configuration both tools run cleanly. It is excluded when the
other tool survives the trigger, and single-tool when no model of that finding
gives the other tool a clean baseline to judge from.

`single-tool` is the absence of a verdict, not a verdict of innocence.
"""
from __future__ import annotations

import argparse
import collections
import json
import re
import subprocess
import sys
import tempfile
from pathlib import Path

RUMOCA = "./target/debug/rumoca"
ROOTS = ["target/msl/ModelicaStandardLibrary-4.1.0",
         "target/corpus/ModelicaStandardLibrary-4.1.0"]
FAIL_MARKERS = ("simulation-failure", "DAE structural", "below-min", "above-max")

# `mass1.m=0` from the finding's recorded test case.
ASSIGNMENT = re.compile(r"^([\w.\[\]]+)=(-?[\d.eE+-]+)$")


def parse_case(description: str) -> tuple[str, float] | None:
    """The single assignment a finding was triggered by, if it was one.

    Multi-parameter cases are skipped: confirming one would need the same
    minimization the search deliberately avoids by moving one value at a time.
    """
    if not description or description == "declared configuration":
        return None
    parts = [p.strip() for p in description.split(",")]
    if len(parts) != 1:
        return None
    found = ASSIGNMENT.match(parts[0])
    if not found:
        return None
    try:
        return found.group(1), float(found.group(2))
    except ValueError:
        return None


_COMPILED: dict[str, Path | None] = {}
_BASELINE: dict[str, str] = {}
_COMPLETE: dict[str, bool] = {}


def exported_completely(artifact: Path) -> bool:
    """Whether the artifact represents the whole model.

    Bitcode v1 cannot carry every expression - functions, records and general
    arrays are marked `Unsupported` rather than dropped silently. A model with
    any of those is a *different* model from the one the other tool ran, and
    its surviving a trigger says nothing about whether the trigger is benign.

    This check exists because omitting it produced wrong verdicts: the three
    highest-reach findings excluded in a first pass -
    `HeatingNPN_NORGate`, `HeatingRectifier`, `EddyCurrentBrake` - carry 44, 12
    and 11 unsupported expressions respectively. "Rumoca survived" there meant
    "Rumoca never evaluated the equation in question".
    """
    key = str(artifact)
    if key in _COMPLETE:
        return _COMPLETE[key]
    try:
        sys.path[:0] = ["packages/rumoca-bitcode"]
        from rumoca_bitcode import Model, Unsupported
        model = Model.load(artifact)
        complete = not any(isinstance(e, Unsupported) for e in model.expressions)
    except Exception:
        complete = False
    _COMPLETE[key] = complete
    return complete


def compile_model(path: str, model: str, cache: Path, timeout: float) -> Path | None:
    """Compile once per model; findings overlap heavily across models."""
    if model in _COMPILED:
        return _COMPILED[model]
    artifact = cache / f"{abs(hash(model)):x}.rbc"
    command = [RUMOCA, "compile", path, "--model", model,
               "--emit-bitcode", str(artifact)]
    for root in ROOTS:
        command += ["--source-root", root]
    try:
        subprocess.run(command, capture_output=True, timeout=timeout)
    except subprocess.TimeoutExpired:
        _COMPILED[model] = None
        return None
    _COMPILED[model] = artifact if artifact.exists() else None
    return _COMPILED[model]


def simulate(artifact: Path, override: tuple[str, float] | None,
             timeout: float) -> str:
    command = [RUMOCA, "compile-bitcode", str(artifact), "--simulate", "--check",
               "--t-end", "0.5"]
    if override:
        command += ["--param", f"{override[0]}={override[1]:g}"]
    try:
        done = subprocess.run(command, capture_output=True, text=True, timeout=timeout)
    except subprocess.TimeoutExpired:
        return "timeout"
    text = done.stdout + done.stderr
    if "not a tunable parameter" in text:
        return "no-such-parameter"
    return "fail" if any(m in text for m in FAIL_MARKERS) else "clean"


def confirm(signature: str, occurrences: list[tuple[str, str, str]],
            paths: dict[str, str], cache: Path, timeout: float,
            max_models: int) -> dict:
    """Try several of a finding's models before deciding.

    A component defect need not break every circuit that uses it — zero
    capacitance is fatal in ChuaCircuit and harmless in CauerLowPassAnalog — so
    confirming from one topology is wrong in both directions.
    """
    judged = 0
    for model, description, _ in occurrences:
        if judged >= max_models:
            break
        trigger = parse_case(description)
        if trigger is None:
            continue
        path = paths.get(model)
        if not path:
            continue
        artifact = compile_model(path, model, cache, timeout)
        if artifact is None:
            continue
        if not exported_completely(artifact):
            continue  # a partial export cannot exclude anything
        if model not in _BASELINE:
            _BASELINE[model] = simulate(artifact, None, timeout)
        if _BASELINE[model] != "clean":
            continue  # the other tool cannot judge this model
        verdict = simulate(artifact, trigger, timeout)
        if verdict == "no-such-parameter":
            continue
        judged += 1
        if verdict == "fail":
            return {"verdict": "confirmed", "via": model,
                    "trigger": f"{trigger[0]}={trigger[1]:g}", "judged": judged}
    # `excluded` requires that a *complete* export of some model ran cleanly at
    # its declared values and survived the trigger. Anything less is the absence
    # of a verdict, not a verdict of innocence.
    return {"verdict": "excluded" if judged else "single-tool",
            "via": None, "trigger": None, "judged": judged}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("results")
    parser.add_argument("--list", default="tools/sweep/ALL.list")
    parser.add_argument("--out", required=True)
    parser.add_argument("--timeout", type=float, default=120)
    parser.add_argument("--max-models", type=int, default=4)
    parser.add_argument("--limit", type=int, default=10 ** 9)
    args = parser.parse_args()

    sys.path[:0] = ["tools/sweep"]
    from analyze_eval import STATIC_CANDIDATE_SANITIZERS, excluded

    paths = {}
    for line in Path(args.list).read_text().splitlines():
        parts = line.split("\t")
        if len(parts) > 1:
            paths[parts[1].strip()] = parts[0]

    grouped: dict[str, list] = collections.defaultdict(list)
    meta: dict[str, dict] = {}
    for line in Path(args.results).read_text().splitlines():
        if not line.strip():
            continue
        try:
            row = json.loads(line)
        except ValueError:
            continue
        for bug in row.get("bugs", []):
            if bug["sanitizer"] in STATIC_CANDIDATE_SANITIZERS or excluded(bug):
                continue
            if parse_case(bug.get("test_case") or "") is None:
                continue  # nothing reproducible to re-run
            grouped[bug["signature"]].append(
                (row["model"], bug.get("test_case"), bug["kind"]))
            meta.setdefault(bug["signature"], bug)

    signatures = sorted(grouped, key=lambda s: -len(grouped[s]))[: args.limit]
    counts = collections.Counter()
    results = []
    with tempfile.TemporaryDirectory() as work:
        cache = Path(work)
        for index, signature in enumerate(signatures, 1):
            outcome = confirm(signature, grouped[signature], paths, cache,
                              args.timeout, args.max_models)
            counts[outcome["verdict"]] += 1
            bug = meta[signature]
            results.append({**outcome, "signature": signature,
                            "sanitizer": bug["sanitizer"], "kind": bug["kind"],
                            "models": len(grouped[signature]),
                            "example": grouped[signature][0][0]})
            mark = {"confirmed": "OK ", "excluded": "XX ",
                    "single-tool": ".. "}[outcome["verdict"]]
            print(f"{mark}{bug['sanitizer']:12} {bug['kind']:26} "
                  f"{len(grouped[signature]):3} models  {grouped[signature][0][1]}",
                  flush=True)
            if index % 25 == 0:
                print(f"    -- {index}/{len(signatures)}  {dict(counts)}", flush=True)

    Path(args.out).write_text(json.dumps(
        {"counts": dict(counts), "results": results}, indent=1))
    print("\n" + json.dumps(dict(counts), indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main())
