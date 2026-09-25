#!/usr/bin/env python3
"""Reduce full per-command evidence into the checked-in recall table."""
import argparse
import hashlib
import json
from pathlib import Path
import re


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("evidence", type=Path)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    full = json.loads(args.evidence.read_text())
    summary = {k: v for k, v in full.items() if k != "cases"}
    summary.update({"evidence_file": str(args.evidence),
                    "evidence_sha256": hashlib.sha256(args.evidence.read_bytes()).hexdigest(),
                    "scope": "7 exact witness variants in 5 existing independent LLM root-cause reports; not all MSL",
                    "counts": {}, "cases": []})
    for case in full["cases"]:
        analysis = case["analysis"]
        witness = f"{case['parameter']} = 0"
        matching = [f for f in analysis["static_findings"]
                    if f.get("evidence", {}).get("witness") == witness]
        confirmed = [f for f in matching if f["severity"] == "high"
                     and f["evidence"].get("verdict") == "SAT"]
        nominal = analysis.get("nominal", analysis.get("prepare_failure", {}))
        trial = analysis.get("witness", {})
        paired = nominal.get("status") == "success" and trial.get("status") == "failed"
        domains = [f for f in trial.get("findings", [])
                   if f["sanitizer"] == "domain" and f["severity"] == "high"]
        row = {"report": case["report"], "variant": case["variant"],
               "nominal_model": case["nominal_model"], "trigger_model": case["trigger_model"],
               "witness": witness, "nominal_compile_ok": case["nominal_compile"]["returncode"] == 0,
               "static_detected_exact_witness": bool(confirmed),
               "matching_static_findings": matching,
               "exact_witness_hints": [h for h in analysis["hints"]
                                       if h["target"] == case["parameter"] and 0 in h["values"]],
               "nominal_runtime_status": nominal.get("status", "not-run"),
               "nominal_runtime_failure": nominal.get("failure"),
               "runtime_witness_status": trial.get("status", "not-run"),
               "runtime_witness_failure": trial.get("failure"),
               "runtime_paired_failure": paired,
               "runtime_paired_exact_domain_evidence": paired and bool(domains),
               "runtime_findings": trial.get("findings", []),
               "native_domain_diagnostics": trial.get("metadata", {}).get("domain_diagnostics", {}),
               "target_variable": analysis["target_variable"],
               "source_trigger_compile_ok": case["trigger_compile"]["returncode"] == 0,
               "source_trigger_compiler_stderr": re.sub(r"\x1b\[[0-9;]*m", "", case["trigger_compile"]["stderr"]),
               "omc_successful_nominal_failed_trigger": case["omc"]["successful_simulations"] == 1
                    and len(case["omc"]["result_files"]) == 2
                    and bool(case["omc"]["result_files"][0]) and not case["omc"]["result_files"][1],
               "omc_stdout_file": case["omc"]["stdout_file"],
               "analysis_errors": analysis["analysis_errors"],
               "full_evidence": str(Path(case["nominal_compile"]["artifact"]).parent / "result.json")}
        # Native solver records are large and unrelated to exact domain recall.
        row["native_domain_diagnostics"].pop("solver", None)
        summary["cases"].append(row)
    cases = summary["cases"]
    summary["counts"] = {"variants": len(cases), "reports": len({c["report"] for c in cases}),
        "nominal_compiles": sum(c["nominal_compile_ok"] for c in cases),
        "static_exact_witness_detected": sum(c["static_detected_exact_witness"] for c in cases),
        "static_roots_detected": len({c["report"] for c in cases if c["static_detected_exact_witness"]}),
        "exact_witness_hint_present": sum(bool(c["exact_witness_hints"]) for c in cases),
        "clean_nominal_runtime": sum(c["nominal_runtime_status"] == "success" for c in cases),
        "paired_runtime_failure": sum(c["runtime_paired_failure"] for c in cases),
        "paired_runtime_exact_domain": sum(c["runtime_paired_exact_domain_evidence"] for c in cases),
        "exact_source_trigger_rejected_by_compiler": sum(not c["source_trigger_compile_ok"] for c in cases),
        "omc_pairs_confirmed": sum(c["omc_successful_nominal_failed_trigger"] for c in cases)}
    args.output.write_text(json.dumps(summary, indent=2) + "\n")
    print(json.dumps(summary["counts"], indent=2))


if __name__ == "__main__":
    main()
