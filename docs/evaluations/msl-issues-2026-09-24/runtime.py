#!/usr/bin/env python3
"""Seeded current-backend evaluation of every historically confirmed MSL report.

This is an evaluation harness, not a replacement sanitizer or a new source-bug
adjudicator. It consumes the sibling fresh static campaign, never recompiles
source variants, and preserves source/runtime configuration boundaries.
"""
from __future__ import annotations

import argparse
from collections import Counter, defaultdict
import hashlib
import json
import math
import os
from pathlib import Path
import re
import resource
import shutil
import signal
import subprocess
import sys
import time

ROOT = Path(__file__).resolve().parents[3]
HERE = Path(__file__).resolve().parent
OUT = ROOT / "target/msl-issue-evaluation-20260924/runtime"
CORPUS = OUT.parent / "corpus"
LEDGER = ROOT / "docs/v2/verified/index.json"
SOURCE = ROOT / "docs/v2/verified/omc-source-verification.json"
PHYSICAL = ROOT / "docs/v2/verified/omc-physical-verification.json"
TIMEOUT = 12
MODEL_TIMEOUT = 180
STOP = 0.02
sys.path[:0] = [str(ROOT / "packages/rumoca-bitcode"), str(ROOT / "packages/modelsan")]


def key(value):
    return hashlib.sha256(value.encode()).hexdigest()[:16]


def write(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(json.dumps(value, indent=2, default=str) + "\n")
    temporary.replace(path)


def read(path):
    try:
        return json.loads(path.read_text())
    except (FileNotFoundError, json.JSONDecodeError):
        return None


def parameters(witness):
    result = {}
    for part in witness.split(","):
        name, value = (piece.strip() for piece in part.split("=", 1))
        if not re.fullmatch(r"[A-Za-z_]\w*(?:\.\w+|\[\d+\])*", name):
            raise ValueError(f"unsupported witness name: {name}")
        number = float(value)
        if not math.isfinite(number) or name in result:
            raise ValueError(f"invalid witness: {witness}")
        result[name] = number
    return result


def catalog():
    ledger = {r["id"]: r for r in json.loads(LEDGER.read_text())
              if r["verdict"] == "confirmed"
              and r["model"].startswith(("Modelica.", "ModelicaTest."))}
    cases = {}

    def add(model, witness, identifiers, source, historical, operation="division"):
        identifiers = sorted(set(identifiers) & ledger.keys())
        if not identifiers:
            return
        overrides = parameters(witness)
        identity = model + "\0" + json.dumps(overrides, sort_keys=True)
        case = cases.setdefault(key(identity), {
            "case_key": key(identity), "model": model, "parameters": overrides,
            "witness": witness, "report_ids": [], "historical_sources": [],
            "expected_operations": []})
        case["report_ids"] = sorted(set(case["report_ids"] + identifiers))
        case["historical_sources"].append({"path": source, **historical})
        case["expected_operations"] = sorted(set(case["expected_operations"] + [operation]))

    for path in (SOURCE, PHYSICAL):
        for row in json.loads(path.read_text())["results"]:
            if row["outcome"] not in {"confirmed-by-omc", "witness-causes-omc-numerical-failure"}:
                continue
            operation = "log" if path == PHYSICAL and "Argument of log(" in row["diagnostic"] else "division"
            add(row["model"], row["witness"], row["report_ids"], str(path.relative_to(ROOT)),
                {"case_key": row["case_key"], "outcome": row["outcome"],
                 "operation_basis": "source-denominator claim" if path == SOURCE else "independent diagnostic"},
                operation)
    for identifier, row in ledger.items():
        if not identifier.startswith("BUG-"):
            continue
        # The exact reviewed equality is -15, not the old incorrect zero probe.
        value = -15 if identifier == "BUG-024" else 0
        add(row["model"], f"{row['target']} = {value}", [identifier],
            "docs/v2/verified/" + row["report"],
            {"outcome": "inherited-source-execution-review", "qualification": row["reason"]})
    covered = {identifier for case in cases.values() for identifier in case["report_ids"]}
    if covered != ledger.keys():
        raise ValueError(f"unaccounted confirmed IDs: {sorted(ledger.keys() - covered)}")
    return sorted(cases.values(), key=lambda c: (c["model"], c["case_key"]))


class Commands:
    """Record actual backend commands without changing their return semantics."""

    def __init__(self, directory):
        self.directory = directory
        self.original = subprocess.run
        self.calls = []
        self.stage = "prepare"

    def __enter__(self):
        subprocess.run = self.run
        return self

    def __exit__(self, *_):
        subprocess.run = self.original

    def run(self, command, *args, **kwargs):
        index = len(self.calls)
        started = time.monotonic()
        entry = {"argv": list(map(str, command)), "stage": self.stage,
                 "timeout_seconds": kwargs.get("timeout")}
        self.calls.append(entry)
        try:
            result = self.original(command, *args, **kwargs)
            entry.update(exit=result.returncode, stdout=result.stdout, stderr=result.stderr)
            return result
        except subprocess.TimeoutExpired as error:
            entry.update(exit="timeout", stdout=error.stdout, stderr=error.stderr)
            raise
        finally:
            entry["seconds"] = round(time.monotonic() - started, 3)
            write(self.directory / f"command-{index:03}.json", entry)


def configuration(model, case):
    """Conservatively preserve the equivalence boundary of a scalar override."""
    by_name = {v.name: v for v in model.variables}
    changed, metadata, reasons = set(), [], []
    for name in case["parameters"]:
        variable = by_name.get(name)
        if variable is None:
            reasons.append(f"{name}: no exact canonical variable (array/member mapping not guessed)")
            continue
        contract = variable.contract
        changed.add(variable.id)
        metadata.append({"name": name, "id": variable.id, "role": variable.role,
                         "scalar_count": variable.scalar_count, "tunable": variable.tunable,
                         "contract": str(contract)})
        if not variable.is_parameter or not variable.tunable or variable.scalar_count != 1:
            reasons.append(f"{name}: not a retained scalar tunable parameter; source retranslation needed")
        if contract is None:
            reasons.append(f"{name}: declaration contract unavailable")
        elif contract.is_final or contract.is_protected or contract.structural:
            reasons.append(f"{name}: final/protected/structural declaration requires a legal source-level witness")
    # Contract dependencies survive constant folding. A missing expression edge
    # is evidence that post-translation storage mutation may leave a stale value.
    pending = set(changed)
    while pending:
        added = set()
        for variable in model.variables:
            contract = variable.contract
            edges = set(contract.binding_depends_on) if contract else set()
            if variable.id in changed or not edges & pending:
                continue
            retained = {v.id for v in variable.binding.variables()} if variable.binding else set()
            if not edges & pending <= retained:
                reasons.append(f"{variable.name}: folded dependent binding; requires source retranslation")
            if model.has_execution:
                reasons.append(f"{variable.name}: saved execution dependent binding requires explicit replay")
            added.add(variable.id)
        added -= changed
        changed.update(added)
        pending = added
    return {"eligible": not reasons, "reasons": sorted(set(reasons)), "targets": metadata,
            "scope": "eligible for runtime probe only; tunable metadata does not prove source-recompile equivalence"}


def timeout_handler(_signum, _frame):
    raise TimeoutError("runtime observer exceeded 10-second evaluation budget")


def judge(result, observers, model, context, testcase):
    from modelsan.reporting.json import _plain
    findings, errors = [], []
    for observer in observers:
        signal.setitimer(signal.ITIMER_REAL, 10)
        try:
            findings.extend(_plain(f) for f in observer.observe(
                result.observations, model, context, testcase))
        except Exception as error:
            errors.append({"sanitizer": observer.name, "error": f"{type(error).__name__}: {error}"})
        finally:
            signal.setitimer(signal.ITIMER_REAL, 0)
    return findings, errors


def result_record(result, observers, model, context, testcase, backend, directory):
    from modelsan.reporting.json import _plain
    findings, errors = judge(result, observers, model, context, testcase)
    evidence = directory / "native"
    evidence.mkdir(parents=True, exist_ok=True)
    if backend._work is not None:
        work = Path(backend._work.name)
        paths = [work / "trace.csv", work / f"domain-{backend._run_index}.json"]
        paths += list((work / f"execution-run-{backend._run_index}").glob("*"))
        for path in paths:
            if path.is_file():
                shutil.copy2(path, evidence / path.name)
    output = {"status": result.status.value, "phase": result.phase.value,
              "failure": _plain(result.failure), "findings": findings, "observer_errors": errors,
              "trace_samples": len(result.trace) if result.trace else 0,
              "observation_counts": dict(Counter(type(o).__name__ for o in result.observations)),
              "backend_metadata": _plain(result.backend_metadata),
              "native_evidence": str(evidence.relative_to(ROOT))}
    write(directory / "result.json", output)
    return output


def classify(case, result):
    if result["status"] == "backend-error":
        return "blocked-backend-or-configuration"
    evidence = result["backend_metadata"].get("domain_diagnostics", {})
    expected = set(case["expected_operations"])
    exact = [f for f in result["findings"] if f["sanitizer"] == "domain"
             and f["kind"].endswith("-out-of-domain")
             and f["evidence"].get("operation") in expected]
    if exact:
        return "seeded-operation-signal"
    started = bool(result["trace_samples"] or evidence.get("faults")
                   or evidence.get("solver", {}).get("records"))
    if result["status"] != "success":
        return "symptom-only" if started else "failure-before-native-observation"
    if any(f["sanitizer"] in {"numeric", "range", "physical", "assert"}
           and f["severity"] in {"medium", "high"} for f in result["findings"]):
        return "other-runtime-signal"
    if evidence.get("unobserved_evaluations") or evidence.get("truncated"):
        return "not-reproduced-partial-observability"
    return "not-reproduced-in-bounded-run"


def fill_unrun(output, cases, detection, reason):
    completed = {row["case_key"] for row in output["cases"]}
    for case in cases:
        if case["case_key"] not in completed:
            output["cases"].append({**case, "detection": detection, "reason": reason})


def model_worker(model_name):
    from modelsan.analysis.context import AnalysisContext
    from modelsan.backends.rumoca import RumocaBackend
    from modelsan.fuzz.testcase import NOMINAL, TestCase
    from modelsan.instrumentation.planner import CapabilityPlanner
    from modelsan.sanitizers import DEFAULT
    from rumoca_bitcode import Model
    cases = [c for c in catalog() if c["model"] == model_name]
    directory = OUT / key(model_name)
    directory.mkdir(parents=True, exist_ok=True)
    path = directory / "model.json"
    output = {"model": model_name, "status": "started", "cases": []}
    write(path, output)
    static = read(CORPUS / key(model_name) / "static.json")
    output["static_status"] = static["status"]
    output["static_evidence"] = str((CORPUS / key(model_name) / "static.json").relative_to(ROOT))
    artifact = CORPUS / key(model_name) / "model.rbc"
    if static["status"] != "analyzed":
        fill_unrun(output, cases, "blocked-compiler-or-static-artifact", static["status"])
        output["status"] = "completed"
        write(path, output)
        return
    output["artifact_sha256"] = hashlib.sha256(artifact.read_bytes()).hexdigest()
    output["static_artifact_sha256"] = static.get("artifact_sha256")
    if output["artifact_sha256"] != output["static_artifact_sha256"]:
        fill_unrun(output, cases, "blocked-artifact-provenance", "artifact digest differs from completed static result")
        output["status"] = "completed"
        write(path, output)
        return
    output["harness_sha256"] = hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    model = Model.load(artifact)
    context = AnalysisContext(model)
    observers = [cls() for cls in DEFAULT if hasattr(cls, "observe")]
    backend = RumocaBackend(str(ROOT / "target/debug/rumoca"), t_end=STOP, timeout=TIMEOUT)
    signal.signal(signal.SIGALRM, timeout_handler)
    with Commands(directory) as commands:
        try:
            failure = backend.prepare_from_artifact(artifact)
            output["coverage"] = CapabilityPlanner(backend.capabilities).plan(observers, []).skipped_sanitizers()
            if failure is not None:
                output["prepare"] = result_record(failure, observers, model, context, NOMINAL,
                                                   backend, directory / "prepare")
                fill_unrun(output, cases, "blocked-preparation", str(failure.failure))
            else:
                commands.stage = "nominal"
                nominal = backend.run(NOMINAL)
                output["nominal"] = result_record(nominal, observers, model, context, NOMINAL,
                                                   backend, directory / "nominal")
                write(path, output)
                if nominal.ok:
                    run_cases(cases, output, model, context, observers, backend, commands, directory)
                else:
                    fill_unrun(output, cases, "blocked-nominal-baseline", str(nominal.failure))
        finally:
            output["commands"] = [str(p.relative_to(ROOT)) for p in sorted(directory.glob("command-*.json"))]
            output["status"] = "completed"
            write(path, output)
            backend.close()


def run_cases(cases, output, model, context, observers, backend, commands, directory):
    from modelsan.fuzz.testcase import TestCase
    for case in cases:
        eligibility = configuration(model, case)
        row = {**case, "configuration": eligibility}
        if not eligibility["eligible"]:
            row.update(detection="blocked-source-configuration-equivalence",
                       reason="; ".join(eligibility["reasons"]))
        else:
            commands.stage = case["case_key"]
            testcase = TestCase(parameters=case["parameters"], origin="historical-confirmed-witness")
            result = backend.run(testcase)
            row["runtime"] = result_record(result, observers, model, context, testcase, backend,
                                             directory / case["case_key"])
            row["detection"] = classify(case, row["runtime"])
            row["site_attribution"] = "backend instruction only; no canonical source-site identity"
        output["cases"].append(row)
        write(directory / "model.json", output)


def launch(model):
    directory = OUT / key(model)
    directory.mkdir(parents=True, exist_ok=True)
    argv = [sys.executable, str(Path(__file__).resolve()), "--worker", model]
    started = time.monotonic()
    with (directory / "worker.log").open("w") as log:
        child = subprocess.Popen(argv, cwd=ROOT, stdout=log, stderr=subprocess.STDOUT,
                                 start_new_session=True)
        try:
            code = child.wait(timeout=MODEL_TIMEOUT)
        except subprocess.TimeoutExpired:
            os.killpg(child.pid, signal.SIGKILL)
            child.wait()
            code = "timeout"
    output = read(directory / "model.json") or {"model": model, "cases": []}
    output["worker"] = {"argv": argv, "exit": code,
                        "seconds": round(time.monotonic() - started, 3)}
    fill_unrun(output, [c for c in catalog() if c["model"] == model],
               "blocked-runtime-worker", f"worker exit: {code}")
    output["status"] = "completed" if code == 0 else "worker-failed"
    write(directory / "model.json", output)
    return output


DIAGNOSTIC_PATTERNS = {
    "non-dense-domain-ids": r"domains entry at position \d+ declares id \d+, expected",
    "missing-domain-reference": r"references domain \d+, which does not exist",
    "unknown-imported-coordinate": r"coordinate names an unknown variable",
    "unsupported-string-conversion": r"string_conversion",
    "unsupported-delay-coordinate": r"coordinate kind delay",
    "unsupported-clocked-conditions": r"clocked conditions are not supported",
    "missing-requested-observation-columns": r"missing requested columns|missing requested variable|requested.*(?:column|observation).*unavailable",
    "missing-input-value": r"input .*neither a checked default nor a runtime",
    "structural-proof-or-index-reduction": r"DAE structural proof failed|index reduction would",
    "nonfinite-parameter-or-runtime-values": r"numeric evaluation produced a non-finite result",
    "native-scalar-domain-violation": r"divi(?:de|sion) by zero|zero denominator",
    "native-projection-nonconvergence": r"projection.*did.*not.*converge",
    "native-nonfinite-derivative": r"non-finite derivative",
    "native-timeout": r"exceeded 12s|timed out|TimeoutExpired",
}


def diagnostics(models, rows):
    """Retain full failed-stage command output in the durable, committed JSON."""
    rows_by_model = defaultdict(list)
    for row in rows:
        rows_by_model[row["model"]].append(row)
    documents, families = [], defaultdict(lambda: {"models": set(), "report_ids": set(), "documents": []})
    for model in models:
        commands = [read(ROOT / name) for name in model.get("commands", [])]
        model_rows = rows_by_model[model["model"]]
        stages = [(stage, model.get(stage), [i for row in model_rows for i in row["report_ids"]])
                  for stage in ("prepare", "nominal")]
        stages += [(row["case_key"], row.get("runtime"), row["report_ids"]) for row in model_rows]
        for stage, result, identifiers in stages:
            if result is None or result["status"] == "success":
                continue
            records = [c for c in commands if c and c["stage"] == stage]
            failure = result.get("failure") or {}
            raw = failure.get("raw") or failure.get("message", "")
            full = raw + "\n" + "\n".join(str(c.get("stderr") or "") for c in records)
            matched = [name for name, pattern in DIAGNOSTIC_PATTERNS.items()
                       if re.search(pattern, full, re.I | re.S)]
            if result.get("backend_metadata", {}).get("domain_diagnostics", {}).get("faults"):
                matched = sorted(set(matched + ["native-scalar-domain-violation"]))
            matched = matched or ["other-native-diagnostic"]
            identity = key(model["model"] + "\0" + stage)
            documents.append({"id": identity, "model": model["model"], "stage": stage,
                "report_ids": identifiers, "families": matched, "failure": failure,
                "commands": records, "diagnostic_sha256": hashlib.sha256(full.encode()).hexdigest()})
            for family in matched:
                families[family]["models"].add(model["model"])
                families[family]["report_ids"].update(identifiers)
                families[family]["documents"].append(identity)
    counts = {name: {"model_count": len(data["models"]), "report_count": len(data["report_ids"]),
                    "examples": sorted(data["models"])[:3], "document_ids": data["documents"]}
              for name, data in sorted(families.items())}
    counts.setdefault("missing-requested-observation-columns", {
        "model_count": 0, "report_count": 0, "examples": [], "document_ids": []})
    return documents, counts


def check_boundaries():
    """Two read-only controls separate exported validation from simulation import."""
    results = []
    for model in ("Modelica.Electrical.Analog.Examples.Lines.CompareLineTrunks",
                  "Modelica.Electrical.Analog.Examples.CompareTransformers"):
        artifact = CORPUS / key(model) / "model.rbc"
        argv = [str(ROOT / "target/debug/rumoca"), "bitcode", "check", str(artifact), "--strict"]
        run = subprocess.run(argv, capture_output=True, text=True, timeout=TIMEOUT)
        results.append({"model": model, "artifact": str(artifact.relative_to(ROOT)),
            "artifact_sha256": hashlib.sha256(artifact.read_bytes()).hexdigest(), "argv": argv,
            "exit": run.returncode, "stdout": run.stdout, "stderr": run.stderr,
            "stderr_sha256": hashlib.sha256(run.stderr.encode()).hexdigest()})
    write(OUT / "artifact-boundaries.json", results)


def collect(cases, reason="runtime campaign not complete"):
    campaign = (read(HERE / "corpus-results.json") or {}).get("campaign", {})
    by_model = defaultdict(list)
    for case in cases:
        by_model[case["model"]].append(case)
    models, rows = [], []
    for model, model_cases in sorted(by_model.items()):
        result = read(OUT / key(model) / "model.json") or {"model": model, "cases": []}
        fill_unrun(result, model_cases, "not-run", reason)
        static = read(CORPUS / key(model) / "static.json") or {}
        if result.get("artifact_sha256"):
            result["final_static_digest_matches"] = result["artifact_sha256"] == static.get("artifact_sha256")
            directory = CORPUS / key(model)
            result["static_campaign_freshness"] = bool(
                model in campaign.get("models", [])
                and (directory / "static.json").stat().st_mtime >= campaign.get("started_epoch", float("inf"))
                and (directory / "worker.log").stat().st_mtime >= campaign.get("started_epoch", float("inf")))
            if campaign.get("validation") == "run-id":
                result["static_campaign_freshness"] &= static.get("campaign_id") == campaign.get("id")
        models.append({k: v for k, v in result.items() if k != "cases"})
        for row in result["cases"]:
            if "runtime" in row:
                # Rescore preserved executions; this never launches another run.
                row["detection"] = classify(row, row["runtime"])
                nominal = result.get("nominal", {}).get("backend_metadata", {}).get("domain_diagnostics", {})
                trial = row["runtime"]["backend_metadata"].get("domain_diagnostics", {})
                before = {(f["program_sha1"], f["instruction_index"]) for f in nominal.get("faults", [])}
                after = {(f["program_sha1"], f["instruction_index"]) for f in trial.get("faults", [])}
                row["domain_fault_comparison"] = {"nominal_fault_sites": len(before),
                    "witness_fault_sites": len(after), "additional_backend_sites": len(after - before),
                    "shared_backend_sites": len(after & before),
                    "limitation": "backend program hashes may change between lowered configurations"}
            if result.get("artifact_sha256") and not (result["final_static_digest_matches"]
                                                       and result["static_campaign_freshness"]):
                row["uncredited_detection"] = row["detection"]
                row["detection"] = "blocked-artifact-provenance"
            rows.append(row)
    counts = Counter(r["detection"] for r in rows)
    report_counts = Counter()
    for row in rows:
        report_counts[row["detection"]] += len(row["report_ids"])
    evidence_documents, diagnostic_counts = diagnostics(models, rows)
    result = {"method": "seeded runtime evaluation, historical independent ground truth not rerun",
              "revision": subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip(),
              "working_tree_dirty": True, "source_sha256": hashlib.sha256(SOURCE.read_bytes()).hexdigest(),
              "ledger_sha256": hashlib.sha256(LEDGER.read_bytes()).hexdigest(),
              "native_binary_sha256": hashlib.sha256((ROOT / "target/debug/rumoca").read_bytes()).hexdigest(),
              "scoring_harness_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
              "static_campaign": {k: v for k, v in campaign.items() if k != "models"},
              "budgets": {"stop_time": STOP, "native_command_timeout": TIMEOUT,
                          "model_worker_timeout": MODEL_TIMEOUT, "workers": 1},
              "case_count": len(rows), "report_count": sum(report_counts.values()),
              "model_count": len(models), "case_counts": dict(sorted(counts.items())),
              "report_counts": dict(sorted(report_counts.items())), "models": models, "cases": rows,
              "diagnostic_families": diagnostic_counts, "diagnostic_documents": evidence_documents,
              "original_artifact_boundary_controls": read(OUT / "artifact-boundaries.json") or []}
    write(HERE / "runtime-results.json", result)
    return result


def report(result):
    """A navigable generated index; the JSON retains full diagnostics and IDs."""
    lines = [
        "# Seeded runtime evaluation of confirmed MSL reports", "",
        "[Machine-readable results and complete diagnostics](runtime-results.json) · [Driver](runtime.py)", "",
        f"This evaluation accounts for **{result['report_count']} historically confirmed report IDs**, "
        f"deduplicated into **{result['case_count']} exact parameter configurations across {result['model_count']} models**. "
        "The scope is `Modelica.*` and `ModelicaTest.*`, including the inherited BUG reports and two physical-witness reports. "
        "These are instances, not independent root causes. No confirmed report in this scope was silently omitted.", "",
        "This is **seeded detectability**, not autonomous discovery and not a new verification that every historical verdict is correct. "
        "Known witnesses were supplied from the independent historical OpenModelica/source review; OpenModelica was not rerun. "
        "A positive native operation signal identifies a reached instruction, not the exact historical source expression. "
        "Tunable metadata is only permission to attempt a scalar runtime probe, not proof that a source retranslation has identical semantics.", "",
        "## Outcomes", "", "| Outcome | Exact cases | Report IDs |", "|---|---:|---:|"]
    for outcome, count in result["case_counts"].items():
        lines.append(f"| `{outcome}` | {count} | {result['report_counts'][outcome]} |")
    lines += ["",
        "`seeded-operation-signal` requires a successful nominal run followed by a failed witness run with a native "
        "domain finding of the expected operation class. Source-site rediscovery is **not** claimed. "
        "`failure-before-native-observation` preserves the generic SolverSan signal but has no reached-operation telemetry. "
        "Preparation, baseline, artifact, configuration and compiler failures are coverage blockers, never sanitizer hits. "
        "A short non-reproduction would not prove safety.", "",
        "## Why cases could not be checked or attributed", "",
        "Families overlap: one artifact can have both invalid domain IDs and unsupported operations. "
        "Counts below are unique models/report IDs per family, **not additive**. Full failed-stage stdout/stderr, "
        "commands, normalized failures and SHA-256 digests are embedded in `diagnostic_documents` in the JSON, "
        "so the evidence does not depend only on untracked target logs.", "",
        "| Diagnostic family | Models | Report IDs | Representative model |", "|---|---:|---:|---|"]
    for family, counts in result["diagnostic_families"].items():
        example = counts["examples"][0] if counts["examples"] else "None reached in this cohort"
        lines.append(f"| `{family}` | {counts['model_count']} | {counts['report_count']} | `{example}` |")
    lines += ["", "### Ownership controls", "",
        "Two original, **uninstrumented** exported artifacts were checked separately. CompareLineTrunks already fails "
        "native strict validation because the exported domain IDs are not dense; trace instrumentation is therefore "
        "not the first observed divergence in that example. CompareTransformers passes strict validation, but simulation "
        "import later rejects an unknown variable coordinate. These establish exporter/checker/importer boundaries for "
        "triage, not an unproven instruction to renumber arbitrary IDs or weaken validation. The exact controls and their "
        "artifact/output digests are embedded under `original_artifact_boundary_controls`.", "",
        "The exact pre-observation nonfinite diagnostic is emitted by "
        "`crates/rumoca-eval-dae/src/numeric.rs::require_finite`. That owner evaluates checked parameter/constant/input "
        "expressions. Its `NumericEvaluationError` carries a source span, but the current failure path exposes only the "
        "generic message instead of the operation/operand. This is distinct from the newly instrumented Solve scalar runtime.", "",
        "## Implementation priorities indicated by this run", "",
        "1. Repair the earliest exporter/checker/importer contract divergence for domain IDs and variable coordinates; "
        "do not count or bypass rejected artifacts. This unlocks more real models than adding another numeric heuristic.",
        "2. Carry typed operation, operand and source provenance through parameter/binding evaluation failures. "
        "Keep the existing generic failure signal while enabling specific attribution before the first solver sample.",
        "3. Complete array observation mapping and the explicitly rejected delay, string-conversion and clocked profiles. "
        "Preserve refused constructs as coverage failures until implemented.",
        "4. Add legal source-configuration generation/retranslation for structural and folded-dependent witnesses, "
        "with nominal/witness controls. Never treat arbitrary post-translation storage changes as equivalent source modifiers.",
        "5. Correlate native operation identities back to canonical/source identities and retain trial-versus-accepted "
        "execution context; the current backend fingerprints cannot prove original-site recall.",
        "6. Wire hint generation into a bounded current-API campaign and repair the missing advertised CLI. "
        "The present `Pipeline.run` executes only supplied testcases; this report deliberately uses historical seeds.", "",
        "## Method and reproduction", "",
        f"Revision: `{result['revision']}` plus the dirty working tree. Fresh sibling static artifacts were compiled with "
        "`--no-fold-parameter-bindings`. Artifact SHA-256 values bind each runtime result to its static input. "
        "Only current DEFAULT runtime observers are invoked here; the separate static campaign covers the optional static analyzers.", "",
        "One worker; one nominal run per prepared model; simulation stop time 0.02 s (matching the historical paired OMC "
        "test), 12-second native command limits, 10 seconds per observer, 180-second per-model process-group watchdog, "
        "and a 30-minute overall campaign cap. No source variant recompilation, retry, alternate solver, or relaxed validation "
        "was used. Unsupported configurations and models without a clean nominal run do not run witness probes.", "",
        "```sh",
        "CARGO_BUILD_JOBS=4 RUST_TEST_THREADS=4 RAYON_NUM_THREADS=4 \\",
        "  python3 docs/evaluations/msl-issues-2026-09-24/runtime.py",
        "python3 docs/evaluations/msl-issues-2026-09-24/runtime.py --check-boundaries",
        "# Re-score retained evidence without running simulations:",
        "python3 docs/evaluations/msl-issues-2026-09-24/runtime.py --collect",
        "```", "",
        "The driver waits for completed sibling static artifacts; InvertingAmp is deferred until the full fresh static "
        "ledger is published to avoid the initial smoke artifact. `--collect` applies the final conservative labels and "
        "records nominal/witness fault-site overlap without replaying any run. Raw native traces, command logs and per-model "
        "results remain under `target/msl-issue-evaluation-20260924/runtime/`.", "",
        "## Every seeded case", "", "| Model | Exact witness | Outcome | Historical reports |",
        "|---|---|---|---|"]
    for row in result["cases"]:
        reports = ", ".join(f"[{i}](../../v2/verified/confirmed/{i}.md)" for i in row["report_ids"])
        lines.append(f"| `{row['model']}` | `{row['witness']}` | `{row['detection']}` | {reports} |")
    (HERE / "runtime.md").write_text("\n".join(lines) + "\n")


def static_complete():
    result = read(HERE / "corpus-results.json")
    return bool(result and result.get("models") and all(
        r["status"] not in {"not-run", "started", "analyzing"} for r in result["models"]))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--worker")
    parser.add_argument("--collect", action="store_true")
    parser.add_argument("--catalog-only", action="store_true")
    parser.add_argument("--check-boundaries", action="store_true")
    parser.add_argument("--budget-seconds", type=float, default=1800)
    args = parser.parse_args()
    os.chdir(ROOT)
    if args.worker:
        resource.setrlimit(resource.RLIMIT_AS, (6 * 1024**3, 6 * 1024**3))
        model_worker(args.worker)
        return
    cases = catalog()
    if args.check_boundaries:
        check_boundaries()
        return
    if args.catalog_only:
        print(json.dumps({"cases": len(cases), "models": len({c['model'] for c in cases}),
                          "reports": sum(len(c['report_ids']) for c in cases)}, indent=2))
        return
    if args.collect:
        result = collect(cases)
        report(result)
        print(json.dumps(result["case_counts"], indent=2))
        return
    pending = sorted({case["model"] for case in cases})
    started, completed = time.monotonic(), 0
    while pending and time.monotonic() - started < args.budget_seconds:
        ready = []
        for model in pending:
            if model.endswith(".InvertingAmp") and not static_complete():
                continue  # Defer the earlier smoke artifact until fresh sweep completes.
            static = read(CORPUS / key(model) / "static.json")
            if static and "worker" in static and static["status"] not in {"started", "analyzing"}:
                ready.append(model)
        if not ready:
            time.sleep(2)
            continue
        for model in ready:
            result = launch(model)
            completed += 1
            pending.remove(model)
            counts = dict(Counter(row["detection"] for row in result["cases"]))
            print(f"{completed}/{completed + len(pending)} {model} {counts}", flush=True)
            collect(cases)
            if time.monotonic() - started >= args.budget_seconds:
                break
    reason = "overall runtime campaign budget reached" if pending else "complete"
    result = collect(cases, reason)
    report(result)
    print(json.dumps({"reason": reason, "case_counts": result["case_counts"],
                      "report_counts": result["report_counts"]}, indent=2), flush=True)


if __name__ == "__main__":
    main()
