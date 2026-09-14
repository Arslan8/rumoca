#!/usr/bin/env python3
"""Regression tests for the invariants that make finding counts interpretable.

Each of these exists because the alternative failure is silent. A sanitizer that
cannot observe an execution and a model that is clean both produce zero
findings; if the architecture cannot tell them apart, no evaluation built on it
means anything.

Run: python3 packages/modelsan/tests/test_architecture.py
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path[:0] = [str(ROOT / "packages/rumoca-bitcode"), str(ROOT / "packages/modelsan")]

from modelsan.analysis import AnalysisContext                       # noqa: E402
from modelsan.backends.base import (                                # noqa: E402
    ExecutionResult, ExecutionStatus, Trace,
)
from modelsan.findings import BugDatabase                           # noqa: E402
from modelsan.findings.signature import compute                     # noqa: E402
from modelsan.fuzz import NOMINAL, TestCase                         # noqa: E402
from modelsan.instrumentation import Capability, Support            # noqa: E402
from modelsan.pipeline import Pipeline                              # noqa: E402
from modelsan.reporting import JSONReporter                         # noqa: E402
from modelsan.runtime.anchors import (                              # noqa: E402
    AnchorQuality, BackendAnchor, CanonicalAnchor, EntityKind,
)
from modelsan.runtime.failures import (                             # noqa: E402
    ExecutionFailure, ExecutionPhase, FailureKind,
)
from modelsan.runtime.observations import (                         # noqa: E402
    InitializationFailure, ObservationStream, SimulationEnd, VariableObservation,
)
from modelsan.sanitizers import (                                   # noqa: E402
    DomainSan, NumericSan, RangeSan, SanitizerRegistry, SolverSan,
)

FAILURES: list[str] = []


def check(condition: bool, label: str) -> None:
    print(f"{'PASS' if condition else 'FAIL'}  {label}")
    if not condition:
        FAILURES.append(label)


# ── Doubles ──────────────────────────────────────────────────────────────────


class FakeVariable:
    """Minimal stand-in for a DAE variable view, with declared bounds."""

    def __init__(self, id, name, minimum=None, maximum=None, parameter=False):
        self.id, self.name = id, name
        self.minimum = type("L", (), {"value": minimum})() if minimum is not None else None
        self.maximum = type("L", (), {"value": maximum})() if maximum is not None else None
        self.is_parameter = parameter
        self.source = None
        # The traversal walks every attribute expression; a double has to carry
        # the same surface or it tests the double rather than the code.
        self.binding = None
        self.start = None


class FakeModel:
    def __init__(self, variables):
        self.variables = variables
        self.equations = []
        self.initial_equations = []
        self.expressions = []


class FakeBackend:
    """Returns whatever result the test wants, always as an ExecutionResult."""

    name = "fake"

    def __init__(self, result, capabilities, build_error=None):
        self._result, self.capabilities = result, frozenset(capabilities)
        self._build_error = build_error

    def prepare(self, model_path, model_name):
        return self._build_error

    def run(self, testcase, instrumentation=None):
        return self._result


# ── 1. A failed execution is still an execution result ───────────────────────


def test_failure_without_trajectory():
    print("\n== failure without trajectory ==")
    stream = ObservationStream()
    stream.add(InitializationFailure(
        kind=FailureKind.DIVISION_BY_ZERO,
        reason="division by zero in `mass1.m`",
        raw="LOG_ASSERT | debug | division by zero ... divisor b expression is: mass1.m",
        backend=BackendAnchor("fake", "mass1.m", EntityKind.VARIABLE)))
    stream.add(SimulationEnd(completed=False))
    result = ExecutionResult(
        backend="fake", status=ExecutionStatus.FAILED,
        phase=ExecutionPhase.INITIALIZATION, trace=None, observations=stream,
        failure=ExecutionFailure(kind=FailureKind.DIVISION_BY_ZERO,
                                 phase=ExecutionPhase.INITIALIZATION,
                                 message="division by zero in `mass1.m`",
                                 raw="LOG_ASSERT | debug | division by zero"))

    check(result is not None and result.trace is None,
          "result exists even though there is no trajectory")
    check(result.failure is not None and result.failure.kind is FailureKind.DIVISION_BY_ZERO,
          "failure is classified")
    check("division by zero" in result.failure.raw,
          "raw backend message is preserved for later reclassification")
    check(result.informative, "a model failure is informative about the model")

    model = FakeModel([FakeVariable(0, "mass1.m", minimum=0.0, parameter=True)])
    context = AnalysisContext(model)

    solver = SolverSan().observe(stream, model, context, NOMINAL)
    check(len(solver) == 1, "SolverSan fires with no trajectory")
    check(solver[0].kind == "initialization-failure",
          "phase is part of the kind, not collapsed into t=0")

    # The other two must not crash, and must find nothing rather than erroring.
    check(NumericSan().observe(stream, model, context, NOMINAL) == [],
          "NumericSan does not crash without a trajectory")
    check(RangeSan().observe(stream, model, context, NOMINAL) == [],
          "RangeSan does not crash without a trajectory")


# ── 2. Unsupported instrumentation is explicit, never silent ─────────────────


def test_unsupported_instrumentation():
    print("\n== unsupported instrumentation ==")
    registry = SanitizerRegistry()
    for sanitizer in (DomainSan(), NumericSan(), RangeSan(), SolverSan()):
        registry.register(sanitizer)

    model = FakeModel([FakeVariable(0, "x")])
    backend = FakeBackend(
        ExecutionResult(backend="fake", status=ExecutionStatus.SUCCESS,
                        trace=Trace(times=[0.0], columns={"x": [1.0]})),
        capabilities={Capability.OBSERVE_VARIABLE, Capability.OBSERVE_FAILURE})
    outcome = Pipeline(registry, backend).run(model, "", "M", [])

    coverage = outcome.coverage
    check("domain.runtime" in coverage, "DomainSan runtime marked unsupported")
    check("observe_expression" in coverage.get("domain.runtime", ""),
          "the reason names the missing capability")
    check(outcome.plan.sanitizers["domain"].support is Support.PARTIAL,
          "DomainSan is PARTIAL, not globally disabled")
    check(outcome.plan.can_run("range", "runtime"), "RangeSan runtime is supported")
    check(outcome.executed >= 1, "execution continues despite unsupported capability")


# ── 3. Backend-only anchors: keep the bug, do not invent identity ────────────


def test_backend_only_anchor():
    print("\n== backend-only anchor ==")
    model = FakeModel([FakeVariable(7, "pump.medium.X", minimum=0.0)])
    context = AnalysisContext(model)

    stream = ObservationStream()
    stream.add(VariableObservation(
        time=1.0, value=-0.13,
        backend=BackendAnchor("openmodelica", "pump.medium.X", EntityKind.VARIABLE)))

    findings = RangeSan().observe(stream, model, context, NOMINAL)
    check(len(findings) == 1, "RangeSan still reports a violation without a DAE id")

    finding = findings[0]
    check(finding.canonical_anchors == [], "no canonical anchor is manufactured")
    check(finding.backend_anchors[0].name == "pump.medium.X", "backend anchor preserved")
    check(finding.anchor_quality is AnchorQuality.BACKEND_ONLY, "anchor quality is honest")
    check("openmodelica" in compute(finding),
          "signature is namespaced by backend, not passed off as canonical")

    database = BugDatabase()
    finding.signature = compute(finding)
    database.add(finding)
    check(len(database) == 1, "deduplication works on backend-anchored findings")
    payload = JSONReporter().summarize(database, "M")
    check(json.loads(json.dumps(payload))["unique_bugs"] == 1,
          "backend-anchored findings serialize")


# ── 4. Canonical anchors resolve to exact DAE entities ───────────────────────


def test_canonical_anchor():
    print("\n== canonical anchor ==")
    model = FakeModel([FakeVariable(91, "tank.level", minimum=0.0)])
    context = AnalysisContext(model)

    stream = ObservationStream()
    stream.add(VariableObservation(
        time=2.0, value=-1.5,
        canonical=CanonicalAnchor(EntityKind.VARIABLE, 91, "tank.level")))

    findings = RangeSan().observe(stream, model, context, NOMINAL)
    check(len(findings) == 1, "RangeSan reports a canonically anchored violation")

    finding = findings[0]
    check(finding.canonical_anchors[0].dae_id == 91, "the DAE id is preserved exactly")
    check(finding.anchor_quality is AnchorQuality.CANONICAL, "anchor quality is canonical")
    check("var:91" in compute(finding), "signature is built from the DAE id")

    backend_version = RangeSan().observe(
        _named_stream("tank.level", -1.5), model, context, NOMINAL)[0]
    check(compute(finding) != compute(backend_version),
          "canonical and backend signatures are not interchangeable")


def _named_stream(name: str, value: float) -> ObservationStream:
    stream = ObservationStream()
    stream.add(VariableObservation(
        time=2.0, value=value,
        backend=BackendAnchor("openmodelica", name, EntityKind.VARIABLE)))
    return stream


# ── 5. A backend error is not a model failure ────────────────────────────────


def test_backend_error_is_not_a_model_bug():
    print("\n== backend error vs model failure ==")
    error = ExecutionResult.backend_error("fake", "could not build model")
    check(not error.informative, "a build failure says nothing about the model")
    check(error.status is ExecutionStatus.BACKEND_ERROR, "status distinguishes it")

    registry = SanitizerRegistry()
    registry.register(SolverSan())
    backend = FakeBackend(None, {Capability.OBSERVE_FAILURE}, build_error=error)
    outcome = Pipeline(registry, backend).run(FakeModel([]), "", "M", [])
    check(outcome.note.startswith("backend could not build"),
          "the outcome records that the tool, not the model, failed")


def main() -> int:
    test_failure_without_trajectory()
    test_unsupported_instrumentation()
    test_backend_only_anchor()
    test_canonical_anchor()
    test_backend_error_is_not_a_model_bug()
    print(f"\n{'ALL PASS' if not FAILURES else str(len(FAILURES)) + ' FAILED'}")
    for failure in FAILURES:
        print(f"  - {failure}")
    return 1 if FAILURES else 0


if __name__ == "__main__":
    sys.exit(main())
