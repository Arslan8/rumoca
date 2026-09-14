#!/usr/bin/env python3
"""Turn a corpus evaluation into the numbers a paper can defend.

Three separations this makes, because collapsing any of them produces a figure
that overstates what was found:

**Coverage from cleanliness.** A model no sanitizer could analyse is not a model
with no bugs. Every run records which components were active, so "zero findings"
is always qualified by what was actually looking.

**Static candidates from execution-confirmed findings.** SingularitySan and
InitSan read structure and over-approximate on purpose: `m*a = f` and `f = d*v`
are structurally identical and only the first is fatal at zero. Their output is
a candidate list whose oracle is execution, and reporting it as bugs is how 168
candidates would become "168 bugs" when 8 survive.

**Findings from episodes.** One singularity that collapses the timestep and then
produces a NaN is three findings and one event.
"""
from __future__ import annotations

import argparse
import collections
import json
import sys
from pathlib import Path

sys.path[:0] = ["packages/rumoca-bitcode", "packages/modelsan"]

#: Sanitizers whose output is a candidate list, not a verdict. Named explicitly
#: rather than inferred, so the distinction survives someone adding a sanitizer.
STATIC_CANDIDATE_SANITIZERS = frozenset({"singularity", "init", "discontinuity"})

#: Findings that describe the tooling rather than the model.
TOOL_SIDE_KINDS = frozenset({"backend-failure", "assertion-unreachable-by-parameters",
                             "switching-threshold", "initialization-count-mismatch"})


def is_coverage_artifact(bug: dict) -> bool:
    """A "finding" that is really a gap in one tool rather than a model defect.

    `differential` reporting acceptance-disagreement at the *declared*
    configuration means one backend could not build a model the other ran. That
    is the known Rumoca coverage gap - external objects, Fluid media, ~515
    models - surfacing as a finding. Counting it would be measuring the
    instrument and calling it a result.
    """
    return (bug["sanitizer"] == "differential"
            and bug["kind"] == "acceptance-disagreement"
            and bug.get("test_case") == "declared configuration")


DENORMAL = "2.22507e-308"


def is_denormal_probe(bug: dict) -> bool:
    """A probe at DBL_MIN, which asks about floating point, not the model."""
    return DENORMAL in str(bug.get("test_case", ""))


COSMETIC = ("animation", "defaultframe", "defaultwidth", "defaultlength",
            "diameterfraction", "widthfraction", "lengthfraction", "shapetype",
            "color", "specularcoefficient", "enableanimation")


def is_cosmetic_probe(bug: dict) -> bool:
    """Perturbing a drawing parameter breaks a picture, not a model."""
    case = str(bug.get("test_case", "")).lower()
    return any(marker in case for marker in COSMETIC)


def excluded(bug: dict) -> str | None:
    if bug["kind"] in TOOL_SIDE_KINDS:
        return "tool-side"
    if is_coverage_artifact(bug):
        return "coverage-gap"
    if is_denormal_probe(bug):
        return "denormal-probe"
    if is_cosmetic_probe(bug):
        return "cosmetic-parameter"
    return None


def load(path: Path) -> list[dict]:
    rows = []
    for line in path.read_text().splitlines():
        if line.strip():
            try:
                rows.append(json.loads(line))
            except ValueError:
                continue
    return rows


def report(rows: list[dict]) -> dict:
    status = collections.Counter(r["status"] for r in rows)
    searched = [r for r in rows if r["status"] == "searched"]
    with_dae = [r for r in rows if r.get("dae")]
    both = [r for r in rows if len(r.get("backends", [])) >= 2]

    findings = [(r["model"], b) for r in rows for b in r.get("bugs", [])]
    rejected = collections.Counter()
    kept = []
    for model, bug in findings:
        reason = excluded(bug)
        if reason:
            rejected[reason] += 1
        else:
            kept.append((model, bug))

    execution = [(m, b) for m, b in kept
                 if b["sanitizer"] not in STATIC_CANDIDATE_SANITIZERS]
    candidates = [(m, b) for m, b in kept
                  if b["sanitizer"] in STATIC_CANDIDATE_SANITIZERS]

    def per_sanitizer(items):
        return dict(collections.Counter(b["sanitizer"] for _, b in items).most_common())

    # Distinct defects, not occurrences: one component defect reached through
    # thirty models is one signature.
    execution_signatures = {b["signature"] for _, b in execution}
    candidate_signatures = {b["signature"] for _, b in candidates}

    models_with_execution_finding = {m for m, _ in execution}

    return {
        "corpus": {
            "models": len(rows),
            "status": dict(status.most_common()),
            "with_canonical_dae": len(with_dae),
            "with_two_backends": len(both),
            "searched": len(searched),
        },
        "coverage": {
            "components_active": dict(collections.Counter(
                r.get("active_components", 0) for r in rows).most_common()),
            "most_common_skips": dict(collections.Counter(
                reason for r in rows
                for reason in (r.get("coverage") or {}).values()).most_common(6)),
            "total_cases_executed": sum(r.get("cases", 0) for r in searched),
            "total_hints": sum(r.get("hints", 0) for r in searched),
        },
        "execution_confirmed": {
            "findings": len(execution),
            "distinct_signatures": len(execution_signatures),
            "models_affected": len(models_with_execution_finding),
            "per_sanitizer": per_sanitizer(execution),
            "by_anchor": dict(collections.Counter(
                b["anchor"] for _, b in execution).most_common()),
        },
        "excluded": dict(rejected.most_common()),
        "static_candidates": {
            "findings": len(candidates),
            "distinct_signatures": len(candidate_signatures),
            "per_sanitizer": per_sanitizer(candidates),
            "note": "over-approximations whose oracle is execution; not bugs",
        },
    }


def top_signatures(rows: list[dict], limit: int) -> list[dict]:
    """Execution-confirmed defects by how many models reach them."""
    grouped: dict[str, dict] = {}
    for row in rows:
        for bug in row.get("bugs", []):
            if bug["sanitizer"] in STATIC_CANDIDATE_SANITIZERS or excluded(bug):
                continue
            entry = grouped.setdefault(bug["signature"], {
                "signature": bug["signature"], "sanitizer": bug["sanitizer"],
                "kind": bug["kind"], "anchor": bug["anchor"], "models": set(),
                "example_case": bug.get("test_case"),
            })
            entry["models"].add(row["model"])
    ranked = sorted(grouped.values(), key=lambda e: -len(e["models"]))[:limit]
    for entry in ranked:
        entry["model_count"] = len(entry["models"])
        entry["models"] = sorted(entry["models"])[:5]
    return ranked


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("results")
    parser.add_argument("--out")
    parser.add_argument("--top", type=int, default=15)
    args = parser.parse_args()

    rows = load(Path(args.results))
    summary = report(rows)
    summary["top_execution_confirmed"] = top_signatures(rows, args.top)

    corpus, coverage = summary["corpus"], summary["coverage"]
    print("=== corpus ===")
    for key, value in corpus["status"].items():
        print(f"  {value:5}  {key}")
    print(f"  {corpus['models']:5}  total")
    print(f"\n  canonical DAE available : {corpus['with_canonical_dae']}")
    print(f"  two backends available  : {corpus['with_two_backends']}")
    print(f"  hints generated         : {coverage['total_hints']}")
    print(f"  test cases executed     : {coverage['total_cases_executed']}")

    print("\n=== coverage (components active per model) ===")
    for count, models in sorted(coverage["components_active"].items(), reverse=True):
        print(f"  {models:5} models at {count} components")
    print("  most common skips:")
    for reason, count in coverage["most_common_skips"].items():
        print(f"    {count:5}  {reason}")

    print("\n=== excluded before counting ===")
    for reason, count in summary["excluded"].items():
        print(f"  {count:5}  {reason}")

    execution = summary["execution_confirmed"]
    print("\n=== execution-confirmed findings ===")
    print(f"  findings {execution['findings']}   distinct {execution['distinct_signatures']}"
          f"   models affected {execution['models_affected']}")
    for name, count in execution["per_sanitizer"].items():
        print(f"    {count:5}  {name}")
    print(f"  anchors: {execution['by_anchor']}")

    static = summary["static_candidates"]
    print(f"\n=== static candidates (NOT bugs) ===")
    print(f"  findings {static['findings']}   distinct {static['distinct_signatures']}")
    for name, count in static["per_sanitizer"].items():
        print(f"    {count:5}  {name}")

    print("\n=== top execution-confirmed defects by reach ===")
    for entry in summary["top_execution_confirmed"]:
        print(f"  {entry['model_count']:4} models  [{entry['sanitizer']}] {entry['kind']}"
              f"  ({entry['anchor']})  {entry['example_case']}")

    if args.out:
        Path(args.out).write_text(json.dumps(summary, indent=1, default=str))
        print(f"\nwrote {args.out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
