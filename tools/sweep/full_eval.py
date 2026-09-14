#!/usr/bin/env python3
"""Evaluate every sanitizer on one model. The complete campaign, per model.

Earlier corpus runs were partial in two ways that mattered: they exercised
`modelsan.legacy` rather than the pipeline, and they ran only the sanitizers
that judge a single execution. This runs all twelve, across both backends.

What each model gets, and why some get less:

  Rumoca compiles it      canonical DAE -> structure-reading sanitizers run,
                          observations carry DAE ids, and there are two
                          backends so DifferentialSan has something to compare
  Rumoca cannot           OpenModelica only. Structure-reading sanitizers are
                          skipped *with a reason*, so the model is not confused
                          with a clean one

Coverage is therefore reported per model rather than assumed, which is the only
way a finding count means anything.

One model per invocation, to be fanned out with `xargs -P`.
"""
from __future__ import annotations

import json
import subprocess
import sys
import tempfile
from pathlib import Path

sys.path[:0] = ["packages/rumoca-bitcode", "packages/modelsan"]

from modelsan.analysis import AnalysisContext
from modelsan.backends import OpenModelicaBackend, RumocaBackend
from modelsan.dae import load
from modelsan.findings.deduplicate import BugDatabase
from modelsan.findings.signature import attach
from modelsan.fuzz import NOMINAL, TestCase
from modelsan.instrumentation import Capability, CapabilityPlanner
from modelsan.sanitizers import COMPARATIVE, DEFAULT, SanitizerRegistry

RUMOCA = "./target/debug/rumoca"
MSL_DIR = "target/msl/ModelicaStandardLibrary-4.1.0"
CORPUS_DIR = "target/corpus/ModelicaStandardLibrary-4.1.0"
MSL = f"/data/mrumoca/rumoca/{MSL_DIR}/Modelica 4.1.0/package.mo"


def libraries(model: str) -> list[str]:
    if model.startswith("ModelicaTest."):
        root = f"/data/mrumoca/rumoca/{CORPUS_DIR}"
        return [f"{root}/Modelica/package.mo", f"{root}/ModelicaTest/package.mo"]
    return [MSL]


class NoModel:
    """Stands in when Rumoca cannot compile the model.

    Empty rather than absent so the sanitizers that were *not* skipped still
    have something to iterate. The planner has already excluded everything that
    would read structure from it.
    """

    name = ""
    variables = equations = initial_equations = expressions = events = []
    parameters = states = []


def compile_dae(path: str, model: str, out: Path, timeout: float):
    command = [RUMOCA, "compile", path, "--model", model, "--emit-bitcode", str(out),
               "--source-root", MSL_DIR, "--source-root", CORPUS_DIR]
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


def cases_from_hints(hints, limit: int) -> list[TestCase]:
    """Concrete cases from analysis hints, one parameter at a time.

    Changing two things at once makes a failure unattributable without a
    separate minimization pass, so each case moves exactly one.
    """
    cases, seen = [], set()
    for hint in hints:
        for value in hint.values:
            # A hint whose value is not finite cannot be handed to a solver;
            # dropping it here keeps a bad hint from failing the whole model.
            if value is None or value != value or abs(value) == float("inf"):
                continue
            key = (hint.target, value)
            if key in seen:
                continue
            seen.add(key)
            cases.append(TestCase(parameters={hint.target: value},
                                  origin=f"{hint.source}:{hint.reason[:50]}"))
            if len(cases) >= limit:
                return cases
    return cases


def judge(registry, plan, result, model, context, testcase) -> list:
    """Every runtime observer the plan permits, over one execution."""
    findings = []
    for sanitizer in registry.runtime_observers():
        component = "failure" if sanitizer.name == "solver" else "runtime"
        if not plan.can_run(sanitizer.name, component):
            continue
        findings.extend(sanitizer.observe(result.observations, model, context, testcase))
    findings.sort(key=lambda f: (f.time if f.time is not None else 0.0))
    return attach(findings)


def evaluate(path: str, model_name: str, t_end: float, timeout: float,
             max_cases: int) -> dict:
    report = {"model": model_name, "dae": False, "status": "", "cases": 0,
              "backends": [], "active_components": 0, "coverage": {},
              "bugs": [], "hints": 0}

    registry = SanitizerRegistry()
    for cls in DEFAULT + COMPARATIVE:
        registry.register(cls())

    database = BugDatabase()
    with tempfile.TemporaryDirectory() as work:
        artifact = Path(work) / "m.rbc"
        dae = compile_dae(path, model_name, artifact, timeout)
        report["dae"] = dae is not None
        subject = dae if dae is not None else NoModel()
        context = AnalysisContext(subject)

        backends: dict[str, object] = {}
        omc = OpenModelicaBackend(libraries=libraries(model_name), t_end=t_end,
                                  timeout=timeout)
        if omc.prepare(path, model_name) is None:
            backends["openmodelica"] = omc
        if dae is not None:
            rumoca = RumocaBackend(t_end=t_end, timeout=timeout)
            if rumoca.prepare_from_artifact(artifact) is None:
                backends["rumoca"] = rumoca
        report["backends"] = sorted(backends)

        # Capabilities are the union of what the available backends provide,
        # plus whether a canonical model exists at all.
        capabilities: set = set()
        for backend in backends.values():
            capabilities |= set(backend.capabilities)
        if dae is not None:
            capabilities.add(Capability.CANONICAL_MODEL)
        plan = CapabilityPlanner(frozenset(capabilities)).plan(registry.active(), [])
        report["coverage"] = plan.skipped_sanitizers()
        report["active_components"] = sum(
            1 for s in plan.sanitizers.values() for c in s.components
            if c.support.value == "supported")

        if not backends:
            report["status"] = "no-backend"
            return _finish(report, database)

        for sanitizer in registry.static_analyzers():
            if plan.can_run(sanitizer.name, "static"):
                database.extend(attach(sanitizer.analyze(subject, context)))

        hints = []
        for sanitizer in registry.hint_providers():
            if plan.can_run(sanitizer.name, "hints"):
                hints.extend(sanitizer.hints(subject, context))
        report["hints"] = len(hints)

        primary = backends.get("openmodelica") or next(iter(backends.values()))
        baseline = primary.run(NOMINAL)
        database.extend(judge(registry, plan, baseline, subject, context, NOMINAL))

        if not baseline.ok:
            # Without a clean baseline nothing can be attributed to a case; the
            # baseline failure is itself already reported above.
            report["status"] = "fails-nominally"
            return _finish(report, database, backends)

        report["status"] = "searched"
        cases = cases_from_hints(hints, max_cases)
        report["cases"] = len(cases)

        for case in cases:
            result = primary.run(case)
            if result.informative:
                database.extend(judge(registry, plan, result, subject, context, case))

        # Comparative oracles: several results for one case rather than one.
        for sanitizer in registry.differential_oracles():
            if not plan.can_run(sanitizer.name, "differential"):
                continue
            if sanitizer.name == "determinism":
                repeats = {f"{primary.name}#1": primary.run(NOMINAL),
                           f"{primary.name}#2": primary.run(NOMINAL)}
                database.extend(attach(
                    sanitizer.compare(repeats, subject, NOMINAL)))
            elif len(backends) >= 2:
                across = {name: backend.run(NOMINAL)
                          for name, backend in backends.items()}
                database.extend(attach(
                    sanitizer.compare(across, subject, NOMINAL)))

        return _finish(report, database, backends)


def _finish(report: dict, database: BugDatabase, backends: dict | None = None) -> dict:
    for backend in (backends or {}).values():
        try:
            backend.close()
        except Exception:
            pass
    report["bugs"] = [
        {"signature": bug.signature, "sanitizer": bug.first.sanitizer,
         "kind": bug.first.kind, "severity": bug.first.severity.value,
         "anchor": bug.first.anchor_quality.value,
         "occurrences": bug.occurrences, "sanitizers": sorted(bug.sanitizers),
         "test_case": bug.first.test_case.describe() if bug.first.test_case else None,
         "evidence": {k: str(v)[:120] for k, v in list(bug.first.evidence.items())[:6]}}
        for bug in database.bugs
    ]
    report["overlap"] = len(database.overlap())
    return report


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("path")
    parser.add_argument("model")
    parser.add_argument("--t-end", type=float, default=0.5)
    parser.add_argument("--timeout", type=float, default=60)
    parser.add_argument("--max-cases", type=int, default=30)
    args = parser.parse_args()
    try:
        print(json.dumps(evaluate(args.path, args.model, args.t_end,
                                  args.timeout, args.max_cases)), flush=True)
    except Exception as error:
        # A harness crash must never be indistinguishable from a clean model.
        print(json.dumps({"model": args.model, "status": "harness-error",
                          "detail": f"{type(error).__name__}: {error}"[:200],
                          "bugs": []}), flush=True)
