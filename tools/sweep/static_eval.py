#!/usr/bin/env python3
"""Run the static sanitizers over a corpus. No simulation, no backend.

PhysicalSan and DivisorSan reach their conclusions from the DAE alone, so they
need only a compiled artifact — which makes a full-corpus pass cheap enough to
re-run whenever a rule changes, rather than an hour-long campaign.

It also means they cover models nothing can execute: of 827 models, ~700 build
under OpenModelica but only ~290 compile under Rumoca, and these two run on all
290 regardless of whether either tool can simulate them.
"""
from __future__ import annotations

import argparse
import collections
import concurrent.futures
import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path

sys.path[:0] = ["packages/rumoca-bitcode", "packages/modelsan"]

from modelsan.analysis import AnalysisContext            # noqa: E402
from modelsan.dae import load                            # noqa: E402
from modelsan.findings.signature import attach           # noqa: E402
from modelsan.sanitizers import DivisorSan, PhysicalSan   # noqa: E402
from modelsan.sanitizers import SanitizerRegistry         # noqa: E402

RUMOCA = "./target/debug/rumoca"
ROOTS = ["target/msl/ModelicaStandardLibrary-4.1.0",
         "target/corpus/ModelicaStandardLibrary-4.1.0",
         "target/cmm/CMM-a642c381"]


#: Evidence keys whose value is prose meant for a reader, kept unclipped.
WHOLE_TEXT = frozenset({"question", "note", "reason", "proof", "contract",
                        "premise_reason", "witness_rationale", "rule_origin",
                        "denominator", "witness", "constraints",
                        "path_condition", "matrix"})


def compile_dae(path: str, model: str, out: Path, timeout: float,
                keep_chains: bool = False):
    command = [RUMOCA, "compile", path, "--model", model, "--emit-bitcode", str(out)]
    if keep_chains:
        # Rumoca folds a derived Real parameter whose value is an exact integer:
        # `d = k * 10` with `k = 2` arrives as `d = 20`. DivisorSan then names
        # `d`, which the user cannot set, instead of `k`, which they can. The
        # flag keeps the binding as written; the model's shape is unchanged
        # because structural and Integer parameters resolve either way.
        command.append("--no-fold-parameter-bindings")
    for root in ROOTS:
        command += ["--source-root", root]
    try:
        subprocess.run(command, capture_output=True, timeout=timeout)
    except subprocess.TimeoutExpired:
        return None
    if not out.exists():
        return None
    try:
        return load(out)
    except Exception:
        return None


def evaluate(path: str, model_name: str, timeout: float,
             keep_chains: bool = False) -> dict:
    report = {"model": model_name, "status": "", "findings": []}
    with tempfile.TemporaryDirectory() as work:
        artifact = Path(work) / "m.rbc"
        dae = compile_dae(path, model_name, artifact, timeout, keep_chains)
        if dae is None:
            report["status"] = "no-dae"
            return report
        report["status"] = "analyzed"
        report["variables"] = len(dae.variables)
        # How much semantic metadata is actually present, so a quiet result can
        # be read as "nothing found" rather than "nothing to match on".
        report["with_quantity"] = sum(
            1 for v in dae.variables if getattr(v, "physical_quantity", None))

        context = AnalysisContext(dae)
        findings = []
        for sanitizer in (PhysicalSan(), DivisorSan()):
            findings.extend(sanitizer.analyze(dae, context))
        # A suppressed division leaves no finding, so the count is recorded
        # here: "we looked at 431 divisions and proved 388 of them safe" is the
        # denominator a precision figure needs, and it vanishes otherwise.
        report["divisions"] = _division_census(dae, context)
        attach(findings)
        report["findings"] = [
            {"signature": f.signature, "sanitizer": f.sanitizer, "kind": f.kind,
             "severity": f.severity.value,
             "source": str(f.source_locations[0]) if f.source_locations else "",
             # Structure is preserved rather than stringified: the per-site
             # reports are generated from this file, and `matched_by` is a
             # nested dict whose repr they would otherwise have to parse back.
             #
             # The 200-character clip that used to apply to every string cut an
             # advisory's question off mid-word: the run file *is* the report
             # source, so anything shortened here is shortened in the published
             # page. Fields whose whole content is the message are kept whole.
             "evidence": {k: (v if isinstance(v, (dict, list, int, float, bool, type(None)))
                              or k in WHOLE_TEXT
                              else str(v)[:200])
                          for k, v in f.evidence.items()}}
            for f in findings
        ]
    return report


def _division_census(dae, context) -> dict:
    """How many divisions there are, and how each was decided."""
    from collections import Counter

    from modelsan.divisor import build, classify, collect
    try:
        environment = build(dae)
        verdicts = Counter(classify(site, environment).status
                           for site in collect(dae, environment))
    except Exception as error:                      # never lose the row
        return {"error": f"{type(error).__name__}: {error}"[:120]}
    return {"total": sum(verdicts.values()), **dict(verdicts)}


#: Resident set of one `rumoca compile` over MSL, measured at ~1.5 GB.
WORKER_MEMORY_GB = 1.8


def default_jobs() -> int:
    """Workers, bounded by memory as well as by cores.

    Sizing on `cpu_count()` alone drove this machine to 35 GB resident across 24
    workers and got a sibling process killed for low memory. Each worker holds a
    whole compile of MSL, so memory is the binding constraint well before cores
    are, and a sweep that gets its neighbours OOM-killed is not faster.

    Half of *available* memory, not total: the rest of the machine is doing
    something too.
    """
    by_cores = max(1, (os.cpu_count() or 4) - 2)
    try:
        available_kb = next(
            int(line.split()[1])
            for line in Path("/proc/meminfo").read_text().splitlines()
            if line.startswith("MemAvailable:")
        )
        by_memory = max(1, int((available_kb / 1024 / 1024) * 0.5 / WORKER_MEMORY_GB))
    except Exception:
        by_memory = 4  # unknown memory is a reason for caution, not optimism
    return max(1, min(by_cores, by_memory, 24))


def _evaluate_job(job):
    """One model, in a worker. Never raises: a crash must not lose the batch.

    A worker that dies takes its result with it, and a sweep that reports 846
    of 847 rows without saying which one vanished is worse than one that
    records the failure.
    """
    path, model, timeout, keep_chains = job
    try:
        return evaluate(path, model, timeout, keep_chains)
    except Exception as error:
        return {"model": model, "status": "harness-error",
                "detail": f"{type(error).__name__}: {error}"[:160],
                "findings": []}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--list", required=True)
    parser.add_argument("--out", required=True)
    parser.add_argument("--timeout", type=float, default=120)
    parser.add_argument("--limit", type=int, default=10 ** 9)
    parser.add_argument("--jobs", type=int, default=default_jobs(),
                        help="worker processes (default: whichever of cores and "
                             "free memory allows fewer)")
    parser.add_argument("--keep-parameter-chains", action="store_true",
                        help="compile with --no-fold-parameter-bindings so a "
                             "derived parameter still names what it derives from")
    args = parser.parse_args()

    jobs = []
    for line in Path(args.list).read_text().splitlines():
        parts = line.split("\t")
        if len(parts) > 1:
            jobs.append((parts[0], parts[1].strip()))
    jobs = jobs[: args.limit]

    out = Path(args.out)
    status = collections.Counter()

    # One model per worker. The jobs are independent — each compiles its own
    # artifact into its own temp directory and shares nothing — so this is
    # embarrassingly parallel, and running it serially on a 32-core machine
    # turned a four-minute sweep into seventy-five.
    #
    # `executor.map` rather than `as_completed`: it yields in input order, so
    # two runs of the same list produce byte-comparable output and a partial
    # file is a prefix of the whole. It also streams, so memory stays flat
    # rather than buffering 847 reports.
    with out.open("w") as handle:
        with concurrent.futures.ProcessPoolExecutor(max_workers=args.jobs) as pool:
            reports = pool.map(
                _evaluate_job,
                ((path, model, args.timeout, args.keep_parameter_chains)
                 for path, model in jobs),
                chunksize=1,
            )
            for index, report in enumerate(reports, 1):
                status[report["status"]] += 1
                handle.write(json.dumps(report) + "\n")
                handle.flush()
                if index % 100 == 0:
                    print(f"  {index}/{len(jobs)}  {dict(status)}", flush=True)

    print(json.dumps(dict(status), indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main())
