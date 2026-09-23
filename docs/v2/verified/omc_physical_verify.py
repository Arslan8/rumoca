#!/usr/bin/env python3
"""Exercise v2 physical-policy candidates with source-instantiated OMC cases.

This complements ``omc_source_verify.py``.  It tests whether the value claimed
to be admitted by a declaration is in fact accepted after full Modelica
translation: zero for ``physical-bound-permits-zero`` and -1 for
``physical-domain-unenforced``.  Execution alone cannot establish the intended
physical contract, so the outcome names deliberately distinguish an admitted
witness from a numerical failure and from an illegal modification.
"""

from __future__ import annotations

import argparse
import concurrent.futures
import csv
import json
import subprocess
from collections import Counter, defaultdict
from pathlib import Path

from omc_source_verify import Case, VERIFIED, run_model


KINDS = {
    "physical-bound-permits-zero": 0.0,
    "physical-domain-unenforced": -1.0,
}


def parse_cases() -> tuple[list[Case], list[dict]]:
    rows = list(csv.DictReader((VERIFIED / "index.csv").open()))
    prior_result = VERIFIED / "omc-physical-verification.json"
    selected_ids: set[str] | None = None
    if prior_result.exists():
        data = json.loads(prior_result.read_text())
        selected_ids = {
            report_id
            for result in data.get("results", [])
            for report_id in result["report_ids"]
        } | {item["id"] for item in data.get("skipped", [])}
    cases: list[Case] = []
    skipped: list[dict] = []
    for row in rows:
        if row["sanitizer_kind"] not in KINDS:
            continue
        # The first pass selected the still-unverified physical candidates
        # after source-semantic adjudication. Preserve that recorded cohort on
        # later reruns, even though build_reports.py may have changed verdicts.
        if selected_ids is not None and row["id"] not in selected_ids:
            continue
        if selected_ids is None and row["verdict"] != "candidate":
            continue
        target = row["target"]
        if not row["model"].startswith(("Modelica.", "ModelicaTest.")):
            skipped.append({"id": row["id"], "reason": "outside-msl-and-modelicatest"})
            continue
        if "[" in target:
            skipped.append({
                "id": row["id"],
                "model": row["model"],
                "target": target,
                "reason": "array-element-modifier-needs-specialized-wrapper",
            })
            continue
        value = KINDS[row["sanitizer_kind"]]
        cases.append(Case(
            model=row["model"],
            parameter=target,
            value=value,
            witness=f"{target} = {value:g}",
            report_ids=(row["id"],),
        ))
    return sorted(cases, key=lambda case: (case.model, case.witness)), skipped


def physical_outcome(row: dict) -> str:
    outcome = row["outcome"]
    diagnostic = row.get("diagnostic", "").lower()
    if outcome == "not-reproduced-by-omc" and "assertion has been violated" in diagnostic:
        return "witness-admitted-with-warning"
    if outcome == "unresolved-trigger-failed-other" and "argument of log" in diagnostic:
        return "witness-causes-omc-numerical-failure"
    return {
        "confirmed-by-omc": "witness-causes-omc-numerical-failure",
        "not-reproduced-by-omc": "witness-executes-cleanly",
    }.get(outcome, outcome)


def write_summary(path: Path, result: dict) -> None:
    lines = [
        "# OpenModelica physical-witness execution",
        "",
        "Each case modifies the reported parameter in Modelica source before "
        "translation and compares it with the unmodified model. Zero tests a "
        "reported permissive lower bound; -1 tests a reported missing domain bound.",
        "",
        "| Outcome | Reports |",
        "|---|---:|",
    ]
    for outcome, count in sorted(result["report_counts"].items()):
        lines.append(f"| `{outcome}` | {count} |")
    lines += [
        "",
        f"Unsupported cases: **{len(result['skipped'])} reports**.",
        "",
        "A clean negative/zero execution proves that the value is admitted, but "
        "does not by itself prove what the physical contract ought to be. A "
        "numerical failure is behavioral evidence only when the unmodified "
        "baseline is clean. Physical intent still requires the reviewed source "
        "contract recorded in the per-report audit.",
        "",
        "[Raw JSON evidence](omc-physical-verification.json) · [v2 verification index](README.md)",
        "",
    ]
    path.write_text("\n".join(lines))


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--jobs", type=int, default=4)
    parser.add_argument("--timeout", type=int, default=240)
    parser.add_argument("--out", default=str(VERIFIED / "omc-physical-verification.json"))
    args = parser.parse_args()

    cases, skipped = parse_cases()
    by_model: dict[str, list[Case]] = defaultdict(list)
    for case in cases:
        by_model[case.model].append(case)

    results: list[dict] = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=args.jobs) as pool:
        pending = {
            pool.submit(run_model, model, model_cases, args.timeout): model
            for model, model_cases in by_model.items()
        }
        for completed, future in enumerate(concurrent.futures.as_completed(pending), 1):
            model = pending[future]
            try:
                rows = future.result()
            except Exception as error:
                rows = [{
                    "case_key": case.key,
                    "model": case.model,
                    "witness": case.witness,
                    "wrapper": case.source,
                    "report_ids": list(case.report_ids),
                    "outcome": "unresolved-harness-error",
                    "baseline": "unknown",
                    "baseline_diagnostic": "",
                    "trigger": "unknown",
                    "diagnostic": repr(error),
                } for case in by_model[model]]
            for row in rows:
                row["outcome"] = physical_outcome(row)
            results.extend(rows)
            print(
                f"{completed}/{len(by_model)} {model} "
                f"{dict(Counter(row['outcome'] for row in rows))}",
                flush=True,
            )

    results.sort(key=lambda row: (row["model"], row["witness"]))
    counts = Counter(row["outcome"] for row in results)
    result = {
        "method": "source-instantiated paired OpenModelica physical-witness execution",
        "msl_version": "4.1.0",
        "omc_version": subprocess.run(
            ["omc", "--version"], capture_output=True, text=True
        ).stdout.strip(),
        "candidate_report_count": len(results),
        "report_counts": dict(counts),
        "skipped": sorted(skipped, key=lambda row: row["id"]),
        "results": results,
    }
    out = Path(args.out)
    out.write_text(json.dumps(result, indent=2) + "\n")
    write_summary(out.with_name("omc-physical-verification.md"), result)
    print(json.dumps({"report_counts": dict(counts), "skipped": len(skipped)}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
