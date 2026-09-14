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
        # A model *is* supplied here, so CANONICAL_MODEL is available. What is
        # missing is only OBSERVE_EXPRESSION, which is what this test is about.
        capabilities={Capability.OBSERVE_VARIABLE, Capability.OBSERVE_FAILURE,
                      Capability.CANONICAL_MODEL})
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


# ── 6. Operator vocabulary matches the schema ────────────────────────────────


def test_operator_vocabulary():
    """The op names sanitizers match against must be the ones the DAE emits.

    This exists because getting it wrong is silent. Matching `"Mul"` against
    `"multiply"` makes a sanitizer find nothing and look like a clean result —
    the same false-coverage failure the capability planner prevents elsewhere,
    arriving through a different door.
    """
    print("\n== operator vocabulary ==")
    from modelsan.dae import ops
    schema = {"add", "subtract", "multiply", "divide", "power", "equal",
              "not_equal", "less", "less_equal", "greater", "greater_equal",
              "and", "or"}
    check(ops.ALL == schema, "ops.ALL matches RbcBinaryOp serialized names")
    check(ops.MULTIPLY == "multiply" and ops.DIVIDE == "divide",
          "arithmetic names are the serialized spellings, not Rust variants")
    check(ops.RELATIONS <= schema, "relations are a subset of the schema")


# ── 7. Event pathologies are distinguished, not conflated ────────────────────


def test_event_discrimination():
    """Chattering and Zeno are different defects with different fixes.

    Chattering wants a hysteresis band or a guard; Zeno wants the accumulation
    removed. Reporting them as one thing would be the mistake of treating three
    consequences of one cause as three discoveries, run in reverse.

    The first case is the calibration that matters: `CoupledClutches` fires a
    pair of events ~1e-11 apart at every clutch engagement. That is ordinary
    event iteration, and a threshold that flags it reports a stock MSL example
    as buggy.
    """
    print("\n== event discrimination ==")
    from modelsan.runtime.observations import EventTriggered
    from modelsan.sanitizers import EventSan, ZenoSan

    class Stub:
        variables = equations = initial_equations = expressions = events = []

    context = AnalysisContext(Stub())

    def stream(times):
        got = ObservationStream()
        for when in times:
            got.add(EventTriggered(time=when))
        return got

    def kinds(sanitizer, times):
        return [f.kind for f in sanitizer.observe(stream(times), Stub(), context, NOMINAL)]

    engagements = [1e-11, 0.4, 0.4 + 1e-11, 0.71, 0.83, 0.83 + 2.6e-10, 0.9]
    chatter = [0.5 + i * 1e-11 for i in range(6)]
    zeno = [1.0 - 0.5 ** i for i in range(1, 12)]
    periodic = [0.1 * i for i in range(1, 20)]

    check(kinds(EventSan(), engagements) == [],
          "ordinary event iteration is not reported as chattering")
    check(kinds(EventSan(), chatter) == ["chattering"], "real chattering is caught")
    check(kinds(ZenoSan(), chatter) == [], "chattering is not reported as Zeno")
    check(kinds(ZenoSan(), zeno) == ["zeno-accumulation"], "Zeno accumulation is caught")
    check(kinds(EventSan(), zeno) == [], "Zeno is not reported as chattering")
    check(kinds(EventSan(), periodic) == [] and kinds(ZenoSan(), periodic) == [],
          "clean periodic switching is silent")


# ── 8. Every capability a sanitizer uses is declared ─────────────────────────


def test_capabilities_are_declared():
    """A sanitizer with an undeclared component is silently never run.

    The planner only runs what `requires` names, so a `hints()` method with no
    "hints" entry is dead code that looks like a working feature.
    `SingularitySan` and `InitSan` both shipped that way and their hints — the
    highest-value ones, naming the exact parameter that collapses a block —
    never reached the fuzzer.
    """
    print("\n== declared capabilities ==")
    from modelsan.sanitizers import COMPARATIVE, DEFAULT

    problems = []
    for cls in DEFAULT + COMPARATIVE:
        sanitizer = cls()
        declared = set(getattr(sanitizer, "requires", {}) or {})
        for method, component in (("hints", "hints"), ("analyze", "static"),
                                  ("compare", "differential")):
            if hasattr(sanitizer, method) and component not in declared:
                problems.append(f"{sanitizer.name}.{method}() undeclared")
        if hasattr(sanitizer, "observe") and not (
                declared & {"runtime", "failure", "collapse"}):
            problems.append(f"{sanitizer.name}.observe() undeclared")
    check(not problems, f"every implemented capability is declared ({problems})")


# ── 9. One cause seen several ways is one episode ────────────────────────────


def test_cross_sanitizer_correlation():
    """A cascade must count as one event, not four discoveries.

    A singular block collapses the timestep and then produces a NaN. Three
    sanitizers see it and all three are right; counting three bugs would
    inflate every number an evaluation reports.

    `BugDatabase` cannot express this — a signature begins with the sanitizer
    name on purpose — so correlation is a separate step, and this pins that it
    merges transitively rather than by arrival order.
    """
    print("\n== cross-sanitizer correlation ==")
    from modelsan.findings import Severity, correlate, summarize
    from modelsan.findings.finding import Finding
    from modelsan.findings.signature import attach
    from modelsan.runtime.anchors import CanonicalAnchor, EntityKind

    case = TestCase(parameters={"m": 0.0})
    other = TestCase(parameters={"k": 1.0})
    shared = CanonicalAnchor(EntityKind.VARIABLE, 91, "mass1.a")

    findings = [
        Finding("singularity", "vanishing-coefficient", Severity.MEDIUM,
                canonical_anchors=[shared], test_case=case),
        Finding("solver", "timestep-collapse", Severity.MEDIUM,
                test_case=case, time=0.30),
        Finding("numeric", "nan", Severity.HIGH,
                canonical_anchors=[shared], test_case=case, time=0.31),
        Finding("range", "below-min", Severity.MEDIUM,
                canonical_anchors=[CanonicalAnchor(EntityKind.VARIABLE, 7, "x")],
                test_case=other, time=0.9),
    ]
    attach(findings)
    report = summarize(findings)

    check(report["episodes"] == 2, f"4 findings group into 2 episodes ({report})")
    check(report["multi_sanitizer_episodes"] == 1, "one episode spans sanitizers")

    episodes = correlate(findings)
    cascade = next(e for e in episodes if e.is_multi_sanitizer)
    check(cascade.sanitizers == ["singularity", "solver", "numeric"],
          f"the causal order is preserved ({cascade.sanitizers})")
    check(len(cascade.timeline()) == 3, "the timeline is reconstructible")
    # The step collapse has no anchor and reaches the episode only through the
    # NaN's time proximity; taking the first match instead of merging would
    # leave it stranded in its own episode.
    check(any("solver" in line for line in cascade.timeline()),
          "an unanchored finding joins via time proximity, not arrival order")

    separate = next(e for e in episodes if not e.is_multi_sanitizer)
    check(separate.test_case_description == "k=1",
          "a different test case is a different episode")


def main() -> int:
    test_failure_without_trajectory()
    test_unsupported_instrumentation()
    test_backend_only_anchor()
    test_canonical_anchor()
    test_backend_error_is_not_a_model_bug()
    test_operator_vocabulary()
    test_event_discrimination()
    test_capabilities_are_declared()
    test_cross_sanitizer_correlation()
    print(f"\n{'ALL PASS' if not FAILURES else str(len(FAILURES)) + ' FAILED'}")
    for failure in FAILURES:
        print(f"  - {failure}")
    return 1 if FAILURES else 0


if __name__ == "__main__":
    sys.exit(main())

