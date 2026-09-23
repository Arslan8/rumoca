#!/usr/bin/env python3
"""Independently exercise v2 divisor candidates in OpenModelica.

Rumoca is deliberately not used as the oracle here: it generated the
candidates.  Each OMC case extends the reported model with the exact witness as
a *source modification*, so structural parameters and parameter bindings are
retranslated.  The unmodified model is the paired baseline.

Results are conservative.  Only a clean baseline followed by a failure that
names a numerical/structural defect is confirmed.  A surviving trigger is
reported as not reproduced, and every missing/unsupported result stays
unresolved.
"""

from __future__ import annotations

import argparse
import concurrent.futures
import csv
import hashlib
import json
import os
import re
import subprocess
import tempfile
from collections import Counter, defaultdict
from dataclasses import dataclass
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
VERIFIED = ROOT / "docs/v2/verified"
BUGS = ROOT / "docs/v2/bugs"
MSL_ROOT = ROOT / "target/msl/ModelicaStandardLibrary-4.1.0"
CORPUS_ROOT = ROOT / "target/corpus/ModelicaStandardLibrary-4.1.0"
CMM_ROOT = ROOT / "target/cmm/CMM-a642c381"
EXTERNAL_SOURCES = {
    "NeuralPredatorPrey": ROOT / "examples/models/NeuralPredatorPrey.mo",
    "SwitchedRLC": ROOT / "examples/models/SwitchedRLC.mo",
    "Tank": ROOT / "examples/modelsan/Tank.mo",
}

WITNESS = re.compile(
    r"^witness\s+(.+?)\s*=\s*(-?(?:\d+(?:\.\d*)?|\.\d+)(?:[eE][+-]?\d+)?)\s*$",
    re.MULTILINE,
)
RESULT_FILE = re.compile(r'resultFile\s*=\s*"([^"]*)"')
DEFECT_PATTERNS = (
    re.compile(r"division by zero", re.IGNORECASE),
    re.compile(r"non-finite|not finite", re.IGNORECASE),
    re.compile(r"out of bounds", re.IGNORECASE),
    re.compile(r"singular", re.IGNORECASE),
    re.compile(r"\bnan\b", re.IGNORECASE),
    re.compile(r"\binf(?:inite|inity)?\b", re.IGNORECASE),
    re.compile(r"invalid root", re.IGNORECASE),
    re.compile(r"\bis not defined\b", re.IGNORECASE),
)
DOMAIN_MARKERS = (
    "protected element",
    "is protected",
    "final element",
    "cannot be modified",
    "variability mismatch",
    "has min",
    "below the lower bound",
)


@dataclass(frozen=True)
class Case:
    model: str
    parameter: str
    value: float
    witness: str
    report_ids: tuple[str, ...]

    @property
    def key(self) -> str:
        raw = f"{self.model}\0{self.witness}".encode()
        return hashlib.sha256(raw).hexdigest()[:16]

    @property
    def wrapper(self) -> str:
        return f"V2OMC_{self.key}"

    @property
    def source(self) -> str:
        value = format(self.value, ".17g")
        return (
            f"model {self.wrapper}\n"
            f"  extends {self.model}({self.parameter}={value});\n"
            f"end {self.wrapper};"
        )


def parse_cases() -> tuple[list[Case], list[dict]]:
    rows = list(csv.DictReader((VERIFIED / "index.csv").open()))
    grouped: dict[tuple[str, str, float], list[str]] = defaultdict(list)
    skipped: list[dict] = []
    for row in rows:
        # Select the original v2 static FINDING population, not the mutable
        # post-verification verdict.  This keeps reruns stable after
        # build_reports.py promotes or refutes individual reports.
        if (
            row["tier"] != "Candidate"
            or not row["id"].startswith("FINDING-")
            or row["sanitizer_kind"] not in {
                "divisor-reachable-zero",
                "divisor-zero-when-parameters-equal",
            }
        ):
            continue
        text = (BUGS / row["original"]).read_text(errors="replace")
        found = WITNESS.search(text)
        if not found:
            skipped.append({"id": row["id"], "reason": "unparsed-witness"})
            continue
        parameter, raw_value = found.groups()
        value = float(raw_value)
        witness = f"{parameter} = {raw_value}"
        if "[" in parameter:
            skipped.append({
                "id": row["id"],
                "model": row["model"],
                "witness": witness,
                "reason": "array-element-modifier-needs-specialized-wrapper",
            })
            continue
        if not (
            row["model"].startswith(("Modelica.", "ModelicaTest.", "RigidBody."))
            or row["model"] in EXTERNAL_SOURCES
        ):
            skipped.append({
                "id": row["id"],
                "model": row["model"],
                "witness": witness,
                "reason": "outside-msl-and-modelicatest",
            })
            continue
        grouped[(row["model"], parameter, value)].append(row["id"])
    cases = [
        Case(model, parameter, value, f"{parameter} = {value:g}", tuple(sorted(ids)))
        for (model, parameter, value), ids in grouped.items()
    ]
    return sorted(cases, key=lambda case: (case.model, case.witness)), skipped


def quoted(value: str) -> str:
    """A Modelica string literal; JSON escaping is compatible here."""
    return json.dumps(value)


def mos_for(model: str, cases: list[Case]) -> str:
    if model.startswith("ModelicaTest."):
        loads = [
            f"loadFile({quoted(str(CORPUS_ROOT / 'Modelica/package.mo'))});",
            f"loadFile({quoted(str(CORPUS_ROOT / 'ModelicaTest/package.mo'))});",
        ]
    elif model.startswith("Modelica."):
        loads = [
            f"setModelicaPath({quoted(str(MSL_ROOT))} + \":\" + getModelicaPath());",
            'loadModel(Modelica, {"4.1.0"});',
        ]
    elif model.startswith("RigidBody."):
        loads = [
            f"setModelicaPath({quoted(str(CMM_ROOT))} + \":\" + {quoted(str(MSL_ROOT))} + \":\" + getModelicaPath());",
            "loadModel(LieGroups);",
            "loadModel(RigidBody);",
        ]
    else:
        loads = [f"loadFile({quoted(str(EXTERNAL_SOURCES[model]))});"]
    version_expr = "getVersion(Modelica)" if model.startswith(("Modelica.", "ModelicaTest.")) else "getVersion()"
    lines = loads + [f'print("@@VERSION " + {version_expr} + "\\n");']
    for case in cases:
        lines.append(f"loadString({quoted(case.source)});")
        lines.append("getErrorString();")
    lines += [
        'print("@@BASE_START\\n");',
        f'simulate({model}, stopTime=0.02, numberOfIntervals=2, fileNamePrefix="base");',
        "getErrorString();",
        'print("@@BASE_END\\n");',
    ]
    for case in cases:
        lines += [
            f'print("@@TRIGGER_START {case.key}\\n");',
            f'simulate({case.wrapper}, stopTime=0.02, numberOfIntervals=2, fileNamePrefix="t_{case.key}");',
            "getErrorString();",
            f'print("@@TRIGGER_END {case.key}\\n");',
        ]
    return "\n".join(lines) + "\n"


def between(text: str, start: str, end: str) -> str:
    _, marker, tail = text.partition(start)
    if not marker:
        return ""
    body, marker, _ = tail.partition(end)
    return body if marker else tail


def succeeded(chunk: str) -> bool:
    return any(match for match in RESULT_FILE.findall(chunk))


def compact(chunk: str, limit: int = 1600) -> str:
    lines = [line.strip() for line in chunk.splitlines() if line.strip()]
    useful = [
        line for line in lines
        if any(word in line.lower() for word in (
            "error", "assert", "division", "non-finite", "singular",
            "protected", "bounds", "failed", "nan", "inf",
        ))
    ]
    value = "\n".join(useful[-12:] if useful else lines[-8:])
    return value[-limit:]


def has_defect_diagnostic(chunk: str) -> bool:
    return any(pattern.search(chunk) for pattern in DEFECT_PATTERNS)


def decoded_timeout_stream(value: str | bytes | None) -> str:
    if value is None:
        return ""
    return value.decode(errors="replace") if isinstance(value, bytes) else value


def run_model(model: str, cases: list[Case], timeout: int) -> list[dict]:
    with tempfile.TemporaryDirectory(prefix="v2-omc-") as raw_work:
        work = Path(raw_work)
        script = work / "verify.mos"
        script.write_text(mos_for(model, cases))
        try:
            done = subprocess.run(
                ["omc", str(script)],
                cwd=work,
                capture_output=True,
                text=True,
                timeout=timeout,
                env={**os.environ, "CC": "gcc"},
            )
            output = done.stdout + done.stderr
        except subprocess.TimeoutExpired as expired:
            output = decoded_timeout_stream(expired.stdout) + decoded_timeout_stream(expired.stderr)
            return [{
                "case_key": case.key,
                "model": case.model,
                "witness": case.witness,
                "wrapper": case.source,
                "report_ids": list(case.report_ids),
                "outcome": "unresolved-timeout",
                "baseline": "unknown",
                "baseline_diagnostic": "",
                "trigger": "unknown",
                "diagnostic": compact(output),
            } for case in cases]

    base_chunk = between(output, "@@BASE_START\n", "@@BASE_END\n")
    base_ok = succeeded(base_chunk)
    rows = []
    for case in cases:
        trigger_chunk = between(
            output,
            f"@@TRIGGER_START {case.key}\n",
            f"@@TRIGGER_END {case.key}\n",
        )
        trigger_ok = succeeded(trigger_chunk)
        low = trigger_chunk.lower()
        if trigger_chunk and any(marker in low for marker in DOMAIN_MARKERS):
            # An inadmissible source modification refutes the report's exact
            # witness even when the containing model has no executable
            # baseline of its own.
            outcome = "refuted-illegal-witness"
        elif not base_chunk:
            outcome = "unresolved-no-baseline-result"
        elif not base_ok:
            outcome = "unresolved-baseline-fails"
        elif trigger_ok:
            outcome = "not-reproduced-by-omc"
        elif not trigger_chunk:
            outcome = "unresolved-no-trigger-result"
        elif has_defect_diagnostic(trigger_chunk):
            outcome = "confirmed-by-omc"
        else:
            outcome = "unresolved-trigger-failed-other"
        rows.append({
            "case_key": case.key,
            "model": case.model,
            "witness": case.witness,
            "wrapper": case.source,
            "report_ids": list(case.report_ids),
            "outcome": outcome,
            "baseline": "clean" if base_ok else "failed",
            "baseline_diagnostic": compact(base_chunk if base_chunk else output),
            "trigger": "clean" if trigger_ok else "failed",
            "diagnostic": compact(trigger_chunk if trigger_chunk else output),
        })
    return rows


def write_summary(path: Path, result: dict) -> None:
    counts = result["report_counts"]
    case_counts = result["case_counts"]
    lines = [
        "# OpenModelica source-instantiated verification",
        "",
        "Rumoca generated the candidates; OpenModelica is the independent verifier. "
        "Every attempted trigger is encoded in a generated subclass before translation, "
        "and is compared with the unmodified model.",
        "",
        "| Outcome | Unique model/witness cases | v2 report instances |",
        "|---|---:|---:|",
    ]
    for outcome in sorted(set(case_counts) | set(counts)):
        lines.append(f"| `{outcome}` | {case_counts.get(outcome, 0)} | {counts.get(outcome, 0)} |")
    lines += [
        "",
        f"Array/scope cases not attempted: **{len(result['skipped'])} report instances**.",
        "",
        "Only `confirmed-by-omc` is positive execution evidence. `not-reproduced-by-omc` "
        "must not remain labelled a true positive without stronger path evidence. Baseline "
        "failures, timeouts and harness gaps are unresolved.",
        "",
        "[Raw JSON evidence](omc-source-verification.json) · [v2 verification index](README.md)",
        "",
    ]
    path.write_text("\n".join(lines))


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--jobs", type=int, default=4)
    parser.add_argument("--timeout", type=int, default=180)
    parser.add_argument("--limit-models", type=int, default=0)
    parser.add_argument("--out", default=str(VERIFIED / "omc-source-verification.json"))
    args = parser.parse_args()

    cases, skipped = parse_cases()
    by_model: dict[str, list[Case]] = defaultdict(list)
    for case in cases:
        by_model[case.model].append(case)
    models = sorted(by_model)
    if args.limit_models:
        models = models[: args.limit_models]
        selected = set(models)
        skipped += [
            {"id": report_id, "model": case.model, "witness": case.witness, "reason": "limit-models"}
            for case in cases if case.model not in selected for report_id in case.report_ids
        ]

    results: list[dict] = []
    completed = 0
    with concurrent.futures.ThreadPoolExecutor(max_workers=args.jobs) as pool:
        pending = {
            pool.submit(run_model, model, by_model[model], args.timeout): model
            for model in models
        }
        for future in concurrent.futures.as_completed(pending):
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
            results.extend(rows)
            completed += 1
            print(f"{completed}/{len(models)} {model} " + str(dict(Counter(row['outcome'] for row in rows))), flush=True)

    results.sort(key=lambda row: (row["model"], row["witness"]))
    case_counts = Counter(row["outcome"] for row in results)
    report_counts = Counter()
    for row in results:
        report_counts[row["outcome"]] += len(row["report_ids"])
    result = {
        "method": "source-instantiated paired OpenModelica execution",
        "msl_version": "4.1.0",
        "omc_version": subprocess.run(["omc", "--version"], capture_output=True, text=True).stdout.strip(),
        "candidate_case_count": len(results),
        "candidate_report_count": sum(len(row["report_ids"]) for row in results),
        "case_counts": dict(case_counts),
        "report_counts": dict(report_counts),
        "skipped": sorted(skipped, key=lambda row: row["id"]),
        "results": results,
    }
    out = Path(args.out)
    out.write_text(json.dumps(result, indent=2) + "\n")
    write_summary(out.with_name("omc-source-verification.md"), result)
    print(json.dumps({"case_counts": dict(case_counts), "report_counts": dict(report_counts), "skipped": len(skipped)}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
