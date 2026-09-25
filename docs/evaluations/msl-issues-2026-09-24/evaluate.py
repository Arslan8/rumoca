#!/usr/bin/env python3
"""Current-checkout detectability audit, not a new ground-truth adjudicator.

Retains every historical report ID. Fresh artifacts, bounded isolated model
workers, no production code changes, and no compiler failure counted as a hit.
"""
from __future__ import annotations
import argparse
from concurrent.futures import ThreadPoolExecutor, as_completed
import hashlib
import json
import os
from pathlib import Path
import resource
import signal
import subprocess
import sys
import time
import uuid

from matching import score, summarize

ROOT = Path(__file__).resolve().parents[3]
OUT = ROOT / "target/msl-issue-evaluation-20260924/corpus"
LEDGER = ROOT / "docs/v2/verified/index.json"
sys.path[:0] = [str(ROOT / "packages/rumoca-bitcode"), str(ROOT / "packages/modelsan"), str(ROOT / "tools/sweep")]


def write(path, value, compact=False):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=None if compact else 2,
                              separators=(",", ":") if compact else None, default=str) + "\n")


def key(model):
    return hashlib.sha256(model.encode()).hexdigest()[:16]


def bounded(command, seconds, log):
    started = time.monotonic()
    with log.open("w") as output:
        child = subprocess.Popen(command, cwd=ROOT, stdout=output, stderr=subprocess.STDOUT,
                                 start_new_session=True)
        try:
            code = child.wait(timeout=seconds)
        except subprocess.TimeoutExpired:
            os.killpg(child.pid, signal.SIGKILL)
            child.wait()
            code = "timeout"
    return {"command": list(map(str, command)), "exit": code,
            "elapsed": round(time.monotonic() - started, 3),
            "diagnostic": log.read_text(errors="replace")[-6000:]}


def alarm(_signum, _frame):
    raise TimeoutError("analysis exceeded 20-second budget")


def static_worker(model):
    from check_one import locate
    from rumoca_bitcode import Model
    from modelsan.analysis import AnalysisContext
    from modelsan.sanitizers import DEFAULT, DimensionSan, InitStaticSan, NetworkSan, StructureSan
    from modelsan.reporting.json import _plain
    directory = OUT / key(model)
    directory.mkdir(parents=True, exist_ok=True)
    result = {"model": model, "status": "started", "analyses": {}, "findings": [], "hints": []}
    campaign_path = OUT / "campaign.json"
    if campaign_path.exists():
        result["campaign_id"] = json.loads(campaign_path.read_text())["id"]
    destination = directory / "static.json"
    write(destination, result)
    source = locate(model)
    if source is None:
        result["status"] = "source-not-located"
        write(destination, result)
        return
    artifact = directory / "model.rbc"
    command = [str(ROOT / "target/debug/rumoca"), "compile", source, "--model", model,
               "--emit-bitcode", str(artifact), "--no-fold-parameter-bindings",
               "--source-root", "target/msl/ModelicaStandardLibrary-4.1.0",
               "--source-root", "target/corpus/ModelicaStandardLibrary-4.1.0"]
    result["compile"] = bounded(command, 20, directory / "compile.log")
    if result["compile"]["exit"] != 0 or not artifact.exists():
        result["status"] = "compile-blocked"
        write(destination, result)
        return
    result["artifact_sha256"] = hashlib.sha256(artifact.read_bytes()).hexdigest()
    try:
        dae = Model.load(artifact)
        context = AnalysisContext(dae)
    except Exception as error:
        result.update(status="artifact-load-error", error=f"{type(error).__name__}: {error}")
        write(destination, result)
        return
    result["status"] = "analyzing"
    result["variables"] = len(dae.variables)
    signal.signal(signal.SIGALRM, alarm)
    for cls in DEFAULT + (DimensionSan, InitStaticSan, NetworkSan, StructureSan):
        sanitizer = cls()
        for operation in ("analyze", "hints"):
            if not hasattr(sanitizer, operation):
                continue
            label = f"{sanitizer.name}.{operation}"
            write(destination, result)
            signal.setitimer(signal.ITIMER_REAL, 20)
            try:
                values = getattr(sanitizer, operation)(dae, context)
                result["findings" if operation == "analyze" else "hints"].extend(_plain(v) for v in values)
                result["analyses"][label] = {"status": "ok", "count": len(values)}
            except Exception as error:
                result["analyses"][label] = {"status": "error", "error": f"{type(error).__name__}: {error}"}
            finally:
                signal.setitimer(signal.ITIMER_REAL, 0)
    result["status"] = "analyzed"
    write(destination, result)


def run_model(model):
    directory = OUT / key(model)
    directory.mkdir(parents=True, exist_ok=True)
    command = [sys.executable, str(Path(__file__).resolve()), "--worker", model]
    outcome = bounded(command, 180, directory / "worker.log")
    path = directory / "static.json"
    result = json.loads(path.read_text()) if path.exists() else {"model": model, "status": "worker-error"}
    result["worker"] = outcome
    if outcome["exit"] != 0:
        result["status"] = "worker-" + str(outcome["exit"])
    write(path, result)
    return result


def collect(campaign):
    ledger = json.loads(LEDGER.read_text())
    rows, models = [], {}
    for row in ledger:
        name = row["model"]
        if not name.startswith(("Modelica.", "ModelicaTest.")):
            rows.append({**row, "detection": "declaration-only-no-executable-witness" if not name else "outside-msl-scope"})
            continue
        if name not in models:
            path = OUT / key(name) / "static.json"
            models[name] = json.loads(path.read_text()) if path.exists() else {"status": "not-run"}
            result = models[name]
            # A partial --model run must not borrow another run's checkpoints.
            eligible = name in campaign["models"] and path.exists()
            fresh = eligible and path.stat().st_mtime >= campaign["started_epoch"]
            if campaign["validation"] == "run-id":
                fresh = fresh and result.get("campaign_id") == campaign["id"]
            else:
                worker_log = path.parent / "worker.log"
                fresh = fresh and worker_log.exists() and worker_log.stat().st_mtime >= campaign["started_epoch"]
            if not fresh:
                models[name] = {"status": "outside-requested-run-or-stale-checkpoint"}
            elif "worker" not in result or result["status"] in ("started", "analyzing"):
                models[name] = {"status": "incomplete-worker"}
        rows.append(score(row, models[name]))
    destination = Path(__file__).parent
    write(destination / "model-results.json", [
        {"model": name, **result} for name, result in sorted(models.items())], compact=True)
    retained = {"id", "verdict", "group", "sanitizer_kind", "model", "target", "declaration",
                "original", "report", "omc_outcome"}
    ledger_keys = set(ledger[0])
    rows = [{k: v for k, v in row.items() if k not in ledger_keys or k in retained} for row in rows]
    write(destination / "corpus-results.json", {
        "method": "all latest-ledger reports; conservative source/operation/witness matching; target-only matches remain ambiguous",
        "ledger_sha256": hashlib.sha256(LEDGER.read_bytes()).hexdigest(),
        "campaign": campaign,
        "revision": subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip(),
        "working_tree_dirty": True, "summary": summarize(rows), "reports": rows,
        "models": [{"model": name, "status": result["status"],
                    "compile": result.get("compile"), "analyses": result.get("analyses", {})}
                   for name, result in sorted(models.items())]}, compact=True)


def manifest():
    """Record exact local inputs; HEAD alone does not identify this dirty tree."""
    selected = ["target/debug/rumoca", "docs/v2/verified/index.json",
                "docs/v2/verified/omc-source-verification.json", "tools/sweep/ALL.list"]
    paths = set(selected)
    paths.update(str(p.relative_to(ROOT)) for p in Path(__file__).parent.glob("*.py"))
    dirty = subprocess.check_output(
        ["git", "ls-files", "-z", "--modified", "--others", "--exclude-standard", "--", "crates", "packages", "Cargo.lock"],
        cwd=ROOT).decode().split("\0")
    paths.update(p for p in dirty if p.endswith((".rs", ".toml", ".py")) or p == "Cargo.lock")
    for prefix in ("packages/modelsan/modelsan", "packages/rumoca-bitcode/rumoca_bitcode"):
        paths.update(str(p.relative_to(ROOT)) for p in (ROOT / prefix).rglob("*.py"))
    # Pin both actual library roots, including the test library in corpus/.
    for prefix in ("target/msl/ModelicaStandardLibrary-4.1.0", "target/corpus/ModelicaStandardLibrary-4.1.0"):
        paths.update(str(p.relative_to(ROOT)) for p in (ROOT / prefix).rglob("*.mo"))
    hashes = {p: hashlib.sha256((ROOT / p).read_bytes()).hexdigest()
              for p in sorted(paths) if (ROOT / p).is_file()}
    write(Path(__file__).parent / "input-manifest.json", {
        "date": "2026-09-24", "msl": "4.1.0", "rumoca_version": "0.10.0",
        "revision": subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip(),
        "git_status": subprocess.check_output(["git", "status", "--short"], cwd=ROOT, text=True),
        "note": "Current built binary plus uncommitted Python sources; not a clean-commit measurement.",
        "sha256": hashes,
        "limits": {"compile_seconds": 20, "static_operation_seconds": 20,
                   "model_worker_seconds": 180, "model_workers": 3, "worker_address_space_gib": 8}})


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--worker")
    parser.add_argument("--model", action="append")
    parser.add_argument("--collect", action="store_true")
    parser.add_argument("--collect-since", type=float,
                        help="Adopt the completed initial audit by requiring both checkpoint and worker-log freshness after this epoch")
    args = parser.parse_args()
    os.chdir(ROOT)
    if args.worker:
        resource.setrlimit(resource.RLIMIT_AS, (8 * 1024**3, 8 * 1024**3))
        static_worker(args.worker)
        return
    if args.collect:
        if args.collect_since is not None:
            campaign = {"id": "initial-audit-adopted-with-timestamp-validation",
                        "started_epoch": args.collect_since, "validation": "timestamp",
                        "models": sorted({r["model"] for r in json.loads(LEDGER.read_text())
                                          if r["model"].startswith(("Modelica.", "ModelicaTest."))})}
            write(OUT / "campaign.json", campaign)
        else:
            campaign = json.loads((OUT / "campaign.json").read_text())
        collect(campaign)
        manifest()
        return
    ledger = json.loads(LEDGER.read_text())
    models = args.model or sorted({r["model"] for r in ledger if r["model"].startswith(("Modelica.", "ModelicaTest."))})
    campaign = {"id": str(uuid.uuid4()), "started_epoch": time.time(), "validation": "run-id", "models": models}
    write(OUT / "campaign.json", campaign)
    with ThreadPoolExecutor(max_workers=3) as pool:
        futures = {pool.submit(run_model, model): model for model in models}
        for i, future in enumerate(as_completed(futures), 1):
            result = future.result()
            print(f"{i}/{len(models)} {result['status']} {result['model']}", flush=True)
    collect(campaign)
    manifest()


if __name__ == "__main__":
    main()
