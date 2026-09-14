#!/usr/bin/env python3
"""Run the full sanitizer suite over one model, through the real pipeline.

Every earlier corpus sweep exercised `modelsan.legacy`, which is essentially a
parameter search with a crash oracle. This runs the twelve sanitizers via
`Pipeline`, so what gets measured is the architecture rather than its
predecessor.

Coverage is reported per model, not assumed. A model Rumoca cannot compile has
no canonical DAE, so the sanitizers that read model structure are skipped and
say so — otherwise a model nothing could analyse is indistinguishable from a
clean one.

One model per invocation, so the corpus can be fanned out with `xargs -P`.
"""
import json, subprocess, sys, tempfile
from pathlib import Path

sys.path[:0] = ["packages/rumoca-bitcode", "packages/modelsan"]

from modelsan.analysis import AnalysisContext
from modelsan.backends.openmodelica import OpenModelicaBackend
from modelsan.dae import load
from modelsan.findings.deduplicate import BugDatabase
from modelsan.findings.signature import attach
from modelsan.fuzz import NOMINAL, TestCase
from modelsan.instrumentation import Capability, CapabilityPlanner
from modelsan.sanitizers import DEFAULT, SanitizerRegistry

RUMOCA = "./target/debug/rumoca"
MSL_DIR = "target/msl/ModelicaStandardLibrary-4.1.0"
CORPUS = "target/corpus/ModelicaStandardLibrary-4.1.0"
MSL = f"/data/mrumoca/rumoca/{MSL_DIR}/Modelica 4.1.0/package.mo"


def libraries(model: str) -> list[str]:
    if model.startswith("ModelicaTest."):
        root = f"/data/mrumoca/rumoca/{CORPUS}"
        return [f"{root}/Modelica/package.mo", f"{root}/ModelicaTest/package.mo"]
    return [MSL]


def compile_dae(path: str, model: str, out: Path, timeout: float):
    """A canonical DAE, when Rumoca can produce one. None is a normal outcome."""
    cmd = [RUMOCA, "compile", path, "--model", model, "--emit-bitcode", str(out),
           "--source-root", MSL_DIR, "--source-root", CORPUS]
    try:
        subprocess.run(cmd, capture_output=True, timeout=timeout)
    except subprocess.TimeoutExpired:
        return None
    if not out.exists():
        return None
    try:
        return load(out)
    except Exception:
        return None


class NoModel:
    """Stands in when there is no DAE.

    Empty rather than absent so sanitizers that were *not* skipped still have
    something to iterate; the planner has already excluded the ones that would
    read structure from it.
    """
    name = ""
    variables = equations = initial_equations = expressions = events = []
    parameters = states = []


def hints_to_cases(hints, limit: int) -> list[TestCase]:
    """Turn analysis hints into concrete test cases, strongest first.

    One parameter at a time: a case that changes two things cannot attribute a
    failure to either without a minimization pass.
    """
    cases = []
    for hint in hints:
        for value in hint.values:
            cases.append(TestCase(parameters={hint.target: value},
                                  origin=f"{hint.source}:{hint.reason[:40]}"))
            if len(cases) >= limit:
                return cases
    return cases


def sweep_one(path: str, model: str, t_end: float, timeout: float,
              max_cases: int) -> dict:
    out = {"model": model, "dae": False, "status": "", "cases": 0,
           "bugs": [], "coverage": {}, "active_components": 0}

    registry = SanitizerRegistry()
    for cls in DEFAULT:
        registry.register(cls())

    with tempfile.TemporaryDirectory() as work:
        artifact = Path(work) / "m.rbc"
        dae = compile_dae(path, model, artifact, timeout)
        out["dae"] = dae is not None
        subject = dae if dae is not None else NoModel()

        backend = OpenModelicaBackend(libraries=libraries(model), t_end=t_end,
                                      timeout=timeout)
        capabilities = set(backend.capabilities)
        if dae is not None:
            capabilities.add(Capability.CANONICAL_MODEL)

        context = AnalysisContext(subject)
        plan = CapabilityPlanner(frozenset(capabilities)).plan(registry.active(), [])
        out["coverage"] = plan.skipped_sanitizers()
        out["active_components"] = sum(
            1 for s in plan.sanitizers.values() for c in s.components
            if c.support.value == "supported")

        hints = []
        for sanitizer in registry.hint_providers():
            if plan.can_run(sanitizer.name, "hints"):
                hints.extend(sanitizer.hints(subject, context))

        database = BugDatabase()
        for sanitizer in registry.static_analyzers():
            if plan.can_run(sanitizer.name, "static"):
                database.extend(attach(sanitizer.analyze(subject, context)))

        failure = backend.prepare(path, model)
        if failure is not None:
            out["status"] = "build-failed"
            backend.close()
            out["bugs"] = _bugs(database)
            return out

        baseline = backend.run(NOMINAL)
        judged = _judge(registry, plan, baseline, subject, context, NOMINAL)
        database.extend(judged)
        if not baseline.ok:
            out["status"] = "fails-nominally"
            backend.close()
            out["bugs"] = _bugs(database)
            return out

        out["status"] = "searched"
        cases = hints_to_cases(hints, max_cases)
        out["cases"] = len(cases)
        for case in cases:
            result = backend.run(case)
            if not result.informative:
                continue
            database.extend(_judge(registry, plan, result, subject, context, case))
        backend.close()

    out["bugs"] = _bugs(database)
    return out


def _judge(registry, plan, result, model, context, testcase):
    findings = []
    for sanitizer in registry.runtime_observers():
        component = "failure" if sanitizer.name == "solver" else "runtime"
        if not plan.can_run(sanitizer.name, component):
            continue
        findings.extend(sanitizer.observe(result.observations, model, context, testcase))
    findings.sort(key=lambda f: (f.time if f.time is not None else 0.0))
    return attach(findings)


def _bugs(database: BugDatabase) -> list[dict]:
    return [
        {"signature": bug.signature, "sanitizer": bug.first.sanitizer,
         "kind": bug.first.kind, "severity": bug.first.severity.value,
         "anchor": bug.first.anchor_quality.value,
         "occurrences": bug.occurrences,
         "sanitizers": sorted(bug.sanitizers),
         "test_case": bug.first.test_case.describe() if bug.first.test_case else None,
         "evidence": {k: v for k, v in list(bug.first.evidence.items())[:6]}}
        for bug in database.bugs
    ]


if __name__ == "__main__":
    import argparse
    p = argparse.ArgumentParser()
    p.add_argument("path")
    p.add_argument("model")
    p.add_argument("--t-end", type=float, default=0.5)
    p.add_argument("--timeout", type=float, default=90)
    p.add_argument("--max-cases", type=int, default=40)
    a = p.parse_args()
    try:
        print(json.dumps(sweep_one(a.path, a.model, a.t_end, a.timeout, a.max_cases)),
              flush=True)
    except Exception as error:  # a harness crash must not look like a clean model
        print(json.dumps({"model": a.model, "status": "harness-error",
                          "detail": f"{type(error).__name__}: {error}"[:200]}), flush=True)
