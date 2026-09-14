"""AssertSan — the model's own stated invariants, used as targets.

1. Bug class    a condition the *author* wrote down as must-hold, violated by a
                reachable configuration. Unlike every other sanitizer this one
                does not supply its own notion of wrong: the model already said
                what wrong means.
2. Overlap      none at the oracle level. SolverSan sees an assertion firing as
                a generic failure; AssertSan knows which assertion, what it
                claimed, and which parameters can reach it.
3. Signal       static: the assertion's condition depends on parameters a
                search can set. runtime: the assertion fires.
4. Needs        DAE events of kind `assert`, and their condition expressions.
                Runtime: OBSERVE_FAILURE, which every backend has.
5. Transform    no.
6. Fuzzing      this is its main value. An assertion is a labelled target with
                a known dependency set, so hints go straight at the parameters
                that can reach it rather than at the whole parameter space.
7. Signature    the DAE event id of the assertion.
"""

from __future__ import annotations

from ..analysis.context import AnalysisContext
from ..findings.finding import Finding, Severity, SourceLocation
from ..fuzz.hints import FuzzHint
from ..fuzz.testcase import TestCase
from ..instrumentation.capability import Capability
from .base import is_cosmetic
from ..runtime.anchors import CanonicalAnchor, EntityKind
from ..runtime.failures import FailureKind
from ..runtime.observations import ExecutionFailureObservation, ObservationStream


def assertions(model) -> list:
    """Every `assert(...)` the DAE carries as an event action."""
    return [event for event in model.events if event.kind == "assert"]


class AssertSan:
    name = "assert"

    requires = {
        "hints": frozenset({Capability.CANONICAL_MODEL}),
        "static": frozenset({Capability.CANONICAL_MODEL}),
        "runtime": frozenset({Capability.OBSERVE_FAILURE}),
    }

    def hints(self, model, context: AnalysisContext) -> list[FuzzHint]:
        """Values that could carry an assertion's condition toward violation.

        The condition is not solved — that would need a constraint solver and
        would still be defeated by nonlinearity. Instead every parameter the
        condition transitively depends on is offered with boundary values,
        which is enough to make the search look in the right place.
        """
        found: list[FuzzHint] = []
        graph = context.parameters
        for event in assertions(model):
            condition = getattr(event, "condition", None) or getattr(event, "value", None)
            if condition is None:
                continue
            reads = {v for v in condition.variables() if v.is_parameter}
            # A derived parameter is not settable; what a fuzzer can move is
            # whatever the derived value depends on.
            for parameter in list(reads):
                for source_id in graph.depends_on.get(parameter.id, set()):
                    resolved = context.variable(source_id)
                    if resolved is not None:
                        reads.add(resolved)
            for parameter in reads:
                if is_cosmetic(parameter.name):
                    continue
                found.append(FuzzHint(
                    target=parameter.name,
                    values=(0.0, -1.0, 1.0),
                    reason=f"reaches the condition of an assertion (event {event.id})",
                    source=self.name,
                    variable_ids=(parameter.id,),
                ))
        return found

    def observe(self, stream: ObservationStream, model, context: AnalysisContext,
                testcase: TestCase) -> list[Finding]:
        """Report an assertion that actually fired.

        Distinguished from a generic solver failure because an assertion is the
        author's own invariant: violating it is a statement about the model that
        needs no interpretation from us.
        """
        found = []
        for observation in stream.of(ExecutionFailureObservation):
            if observation.kind is not FailureKind.ASSERTION_VIOLATED:
                continue
            found.append(Finding(
                sanitizer=self.name,
                kind="assertion-violated",
                severity=Severity.HIGH,
                backend_anchors=[observation.backend] if observation.backend else [],
                phase=observation.phase,
                time=observation.time,
                test_case=testcase,
                evidence={"reason": observation.reason, "raw": observation.raw[:300]},
            ))
        return found

    def analyze(self, model, context: AnalysisContext) -> list[Finding]:
        """Assertions whose condition no parameter can influence.

        Not a defect in itself, but worth surfacing: such an assertion can only
        be reached through state, so parameter fuzzing will never exercise it
        and its coverage has to come from somewhere else.
        """
        found = []
        for event in assertions(model):
            condition = getattr(event, "condition", None) or getattr(event, "value", None)
            if condition is None:
                continue
            if any(v.is_parameter for v in condition.variables()):
                continue
            found.append(Finding(
                sanitizer=self.name,
                kind="assertion-unreachable-by-parameters",
                severity=Severity.INFO,
                canonical_anchors=[CanonicalAnchor(EntityKind.EVENT, event.id)],
                source_locations=_location(event),
                evidence={"note": "no parameter reaches this condition; "
                                  "parameter fuzzing cannot exercise it"},
            ))
        return found


def _location(event) -> list[SourceLocation]:
    source = getattr(event, "source", None)
    span = getattr(source, "span", None) if source else None
    if span is None:
        return []
    return [SourceLocation(file=getattr(span, "source_name", "") or "?",
                           line=getattr(span, "line", 0) or 0)]
