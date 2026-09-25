#!/usr/bin/env python3
"""Render the complete report ledger without treating coverage failures as misses."""
from collections import Counter
import csv
import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
LABELS = {
    "static-defect-candidate": "Static candidate",
    "explicit-nondefect": "Explicit non-defect",
    "intent-advisory": "Intent advisory",
    "unresolved-analysis": "Unresolved analysis",
    "ambiguous-site-match": "Ambiguous site match",
    "not-reported": "No matching report",
    "analyzer-error": "Analyzer error",
    "blocked-before-analysis": "Blocked before analysis",
    "declaration-only-no-executable-witness": "Declaration only",
    "outside-msl-scope": "Outside MSL scope",
}


def status(row):
    return row.get("strict_detection", row["detection"])


def clean(value):
    return str(value).replace("|", "\\|").replace("\n", " ")


def model_key(name):
    return hashlib.sha256(name.encode()).hexdigest()[:16]


def original(row):
    return f"[{row['id']}](../../v2/verified/{row['report']})"


def explanation(row, models):
    current = status(row)
    if current == "outside-msl-scope":
        return "Custom/non-MSL model; retained in accounting, excluded from MSL counts."
    if current == "declaration-only-no-executable-witness":
        return "No model/witness in the source ledger. Needs source-declaration analysis or a legal enclosing test model."
    if current == "blocked-before-analysis":
        model = models[row["model"]]
        compile_result = model.get("compile", {})
        if compile_result.get("exit") == "timeout":
            return "Fresh compilation exceeded the 20-second attempt. Coverage unmeasured, not proof of unsupported semantics."
        return "Fresh artifact unavailable: " + model["status"] + ". See the model diagnostic."
    if current == "analyzer-error":
        return "Relevant static analyzer errored or exceeded its operation budget; no clean result."
    if current == "ambiguous-site-match":
        return "Same-target findings exist, but exact source/operation/witness identity is unproven. Not counted as exact detection or as a proven miss."
    if current == "not-reported":
        other = row.get("other_sanitizer_target_findings", [])
        suffix = " Other sanitizers mention this target, but not the historical issue." if other else ""
        return "No matching finding in the original sanitizer family; inspect source bindings, guards, and contracts before inferring a miss." + suffix
    if current == "static-defect-candidate":
        if row["verdict"] == "false-positive":
            return "Candidate overlaps an independently refuted/non-defect record. Review the historical refutation before reporting a bug."
        return "Same archived source/rule or denominator and witness found statically; not an independently verified execution."
    if current == "explicit-nondefect":
        return "Analyzer explicitly explains a supported limit, inapplicable rule, guarded/unreachable witness, or generated divisor."
    if current == "intent-advisory":
        return "Intent question, not an error: no authoritative component contract establishes a defect."
    return "Analyzer cannot discharge the path/domain obligation. Needs stronger evidence, not automatic promotion."


def runtime_note(case, models):
    if not case:
        return "Not in the historically confirmed seeded-runtime cohort."
    model = models[case["model"]]
    stage = "prepare" if case["detection"] == "blocked-preparation" else "nominal"
    result = case.get("runtime") or model.get(stage) or {}
    failure = result.get("failure") or {}
    return case.get("reason") or failure.get("message") or case["detection"]


def report_csv(rows, models, runtime_cases, runtime_models):
    columns = ["id", "historical_verdict", "model", "target", "sanitizer_kind", "strict_result",
               "target_level_result", "exact_kind_present", "matching", "why_or_next_step",
               "historical_review", "original_report", "model_evidence", "seeded_runtime_result",
               "seeded_runtime_witness", "seeded_runtime_reason", "seeded_runtime_case_key"]
    with (HERE / "all-reports.csv").open("w", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=columns)
        writer.writeheader()
        for row in rows:
            case = runtime_cases.get(row["id"], {})
            writer.writerow(dict(zip(columns, [row["id"], row["verdict"], row["model"], row["target"],
                row["sanitizer_kind"], status(row), row["detection"], row.get("exact_kind_present", ""),
                row.get("operation_match", "not-applicable"), explanation(row, models),
                "docs/v2/verified/" + row["report"], "docs/v2/bugs/" + row["original"],
                row.get("model_evidence", ""), case.get("detection", "not-in-seeded-cohort"),
                case.get("witness", ""), runtime_note(case, runtime_models), case.get("case_key", "")])))


def report_page(name, title, rows, models, runtime_cases):
    seeded = any(r["id"] in runtime_cases for r in rows)
    lines = [f"# {title}", "", "[Overview](README.md) · [All rows as CSV](all-reports.csv)", "",
             f"{len(rows)} historical report instances, not unique bugs. Current findings do not replace the historical adjudication.", "",
             "An exact static candidate is not a runtime confirmation. Ambiguous matches are deliberately not credited as exact detections.", "",
             "| Historical report | Model / target | Current strict result | Why / next step |" + (" Seeded runtime |" if seeded else ""),
             "|---|---|---|---|" + ("---|" if seeded else "")]
    for row in rows:
        model = row["model"]
        location = f"[{clean(model)}](models.md#model-{model_key(model)})" if model in models else clean(model or "Declaration only")
        case = runtime_cases.get(row["id"], {})
        runtime = f" [{case.get('detection', 'not-in-seeded-cohort')}](runtime.md)<br>`{clean(case.get('witness', ''))}` |" if seeded else ""
        lines.append(f"| {original(row)} | {location}<br>`{clean(row['target'])}` | {LABELS[status(row)]} | {clean(explanation(row, models))} |" + runtime)
    (HERE / name).write_text("\n".join(lines) + "\n")


def model_page(rows, models):
    lines = ["# Per-model analysis and blockers", "", "[Overview](README.md) · [Full model evidence](model-results.json)", "",
             "All 255 original Modelica/ModelicaTest models remain visible. Compiler failures and timeouts are coverage blockers, not MSL bug detections.", "",
             "| Model | Fresh artifact/static status | Reports | Exact static candidates | Ambiguous matches |",
             "|---|---|---:|---:|---:|"]
    grouped = {name: [r for r in rows if r["model"] == name] for name in models}
    for name, model in sorted(models.items()):
        group = grouped[name]
        lines.append(f"| [{clean(name)}](#model-{model_key(name)}) | {model['status']} | {len(group)} | "
                     f"{sum(r.get('exact_candidate', False) for r in group)} | {sum(status(r) == 'ambiguous-site-match' for r in group)} |")
    for name, model in sorted(models.items()):
        lines.extend(["", f'<a id="model-{model_key(name)}"></a>', "", f"## {name}", "",
                      f"Status: `{model['status']}`. Report IDs: " + ", ".join(r["id"] for r in grouped[name]) + ".", ""])
        compilation = model.get("compile", {})
        if compilation:
            lines.append(f"Fresh compile: exit `{compilation.get('exit')}`, {compilation.get('elapsed')} seconds.")
        errors = {k: v for k, v in model.get("analyses", {}).items() if v.get("status") != "ok"}
        if errors:
            lines.extend(["", "Analyzer failures:", "", "```json", json.dumps(errors, indent=2), "```"])
        if model["status"] != "analyzed":
            diagnostic = compilation.get("diagnostic") or model.get("error") or model.get("worker", {}).get("diagnostic")
            lines.extend(["", "```text", diagnostic or "No diagnostic was emitted; worker/status fields record the boundary.", "```"])
        else:
            counts = Counter(f["sanitizer"] for f in model.get("findings", []))
            lines.extend(["", "All static finding counts (including advisories/non-defects; not bug counts): `" +
                          json.dumps(dict(sorted(counts.items()))) + "`."])
    (HERE / "models.md").write_text("\n".join(lines) + "\n")


def summary(rows, models):
    executable = [r for r in rows if r["model"] in models]
    kinds = sorted({status(r) for r in executable})
    verdicts = ["confirmed", "false-positive", "unresolved", "advisory", "candidate"]
    lines = ["# Complete-corpus static results", "", "[Overview](README.md) · [Per-model diagnostics](models.md)", "",
             f"{len(executable)} executable report instances across {len(models)} models. Counts below are conservative **historical-operation matches**, not unique-root-cause recall.", "",
             "| Historical verdict | Total | " + " | ".join(LABELS[k] for k in kinds) + " |",
             "|---|---:|" + "---:|" * len(kinds)]
    for verdict in verdicts:
        selected = [r for r in executable if r["verdict"] == verdict]
        counts = Counter(status(r) for r in selected)
        lines.append(f"| {verdict} | {len(selected)} | " + " | ".join(str(counts[k]) for k in kinds) + " |")
    lines.extend(["", "An ambiguous match usually means the old report lacks sufficient operation/witness identity, or the new witness differs. It is neither a demonstrated miss nor an exact hit.", "",
                  "## Current target-level output (weaker, not used as exact detection)", "",
                  "| Historical verdict | Current output | Reports |", "|---|---|---:|"])
    for (verdict, detection), count in sorted(Counter((r["verdict"], r["detection"]) for r in executable).items()):
        lines.append(f"| {verdict} | {LABELS[detection]} | {count} |")
    lines.extend(["", "## Analyzer health", "", "| Component | Failed operations |", "|---|---:|"])
    errors = Counter(k for model in models.values() for k, v in model.get("analyses", {}).items() if v["status"] != "ok")
    lines.extend(f"| {k} | {v} |" for k, v in sorted(errors.items()))
    if not errors:
        lines.append("| No recorded analyzer errors | 0 |")
    lines.extend(["", "These are not precision/recall estimates for all MSL defects. The ledger mostly originated from these same detector families; unresolved/advisory rows are not labeled positives. See the independent benchmark separately."])
    (HERE / "static-summary.md").write_text("\n".join(lines) + "\n")


def main():
    data = json.loads((HERE / "corpus-results.json").read_text())
    rows = data["reports"]
    models = {r["model"]: r for r in json.loads((HERE / "model-results.json").read_text())}
    runtime = json.loads((HERE / "runtime-results.json").read_text())
    runtime_cases = {identifier: case for case in runtime["cases"] for identifier in case["report_ids"]}
    runtime_models = {model["model"]: model for model in runtime["models"]}
    assert len(rows) == 6440 and len({r["id"] for r in rows}) == 6440
    assert len(models) == 255
    assert sum(r["model"] in models for r in rows) == 5476
    report_csv(rows, models, runtime_cases, runtime_models)
    for verdict in ("confirmed", "false-positive", "unresolved", "advisory", "candidate"):
        selected = [r for r in rows if r["model"] in models and r["verdict"] == verdict]
        report_page(verdict + ".md", f"Historical {verdict} reports: current detection", selected, models, runtime_cases)
    report_page("declarations.md", "Declaration-only entries", [r for r in rows if not r["model"]], models, runtime_cases)
    report_page("out-of-scope.md", "Custom-model entries (not MSL)", [r for r in rows if r["model"] and r["model"] not in models], models, runtime_cases)
    model_page(rows, models)
    summary(rows, models)


if __name__ == "__main__":
    main()
