"""DomainSan — operations evaluated outside their mathematical domain.

1. Bug class    an operation whose operand leaves the domain where it is
                defined: division by zero, sqrt/log of a negative, asin/acos
                outside [-1, 1], a fractional power of a negative base.
2. Overlap      NumericSan sees the *consequence* (a NaN some variable now
                holds). DomainSan names the operation that produced it, which
                is the difference between "x is NaN" and "this divisor reached
                zero". Both may fire on one defect; deduplication decides.
3. Signal       static: the operand's reachable range includes the forbidden
                value. runtime: the instrumented operand actually enters it.
4. Needs        DAE expressions and declared bounds; runtime values of operands.
5. Transform    yes, to observe an operand that is not otherwise a variable.
6. Fuzzing      strong. It knows precisely which value is interesting — the
                edge of the domain — for a named parameter.
7. Signature    expression id of the operation plus the operation itself.
"""

from __future__ import annotations

from dataclasses import dataclass

from ..analysis.context import AnalysisContext
from ..dae import BinaryOp, BuiltinCall, Expression
from ..findings.location import locate
from ..findings.finding import Finding, Severity, SourceLocation
from ..fuzz.hints import FuzzHint
from ..fuzz.testcase import TestCase
from ..instrumentation.capability import Capability
from .base import is_cosmetic
from ..instrumentation.request import InstrumentationRequest
from ..runtime.anchors import CanonicalAnchor, EntityKind
from ..runtime.observations import ExpressionObservation, ObservationStream

from ..dae import ops

DIVISION_OPS = frozenset({ops.DIVIDE})

# operand must be > 0, >= 0, or within [-1, 1]
POSITIVE = frozenset({"log", "log10", "log2"})
NON_NEGATIVE = frozenset({"sqrt"})
UNIT_INTERVAL = frozenset({"asin", "acos"})


@dataclass(frozen=True)
class DomainSite:
    """One operation with a restricted domain, and the operand that must obey it."""

    operation: str
    operand: Expression
    owner: object
    requirement: str

    def admits(self, value: float) -> bool:
        if self.requirement == "nonzero":
            return value != 0.0
        if self.requirement == "positive":
            return value > 0.0
        if self.requirement == "non-negative":
            return value >= 0.0
        if self.requirement == "unit-interval":
            return -1.0 <= value <= 1.0
        return True

    def forbidden_probes(self) -> tuple[float, ...]:
        """Values at or just past the edge of the domain."""
        return {
            "nonzero": (0.0,),
            "positive": (0.0, -1.0),
            "non-negative": (-1.0,),
            "unit-interval": (1.5, -1.5),
        }.get(self.requirement, ())


def sites(model) -> list[DomainSite]:
    """Every restricted operation in the model, with its constrained operand."""
    from ..dae.traversal import walk_expressions

    found = []
    for owner, node in walk_expressions(model):
        if isinstance(node, BinaryOp) and node.op in DIVISION_OPS:
            found.append(DomainSite("division", node.rhs, owner, "nonzero"))
        elif isinstance(node, BuiltinCall) and node.arguments:
            name = node.name
            requirement = (
                "positive" if name in POSITIVE else
                "non-negative" if name in NON_NEGATIVE else
                "unit-interval" if name in UNIT_INTERVAL else None
            )
            if requirement:
                found.append(DomainSite(name, node.arguments[0], owner, requirement))
    return found


class DomainSan:
    """Static candidate generation, instrumentation, hints, and runtime checking."""

    name = "domain"

    #: The split matters. Hints need nothing and always work; the runtime check
    #: needs an observed sub-expression, which no current backend provides. The
    #: planner reports the runtime half as skipped rather than letting it look
    #: like a clean result.
    requires = {
        "hints": frozenset({Capability.CANONICAL_MODEL}),
        "runtime": frozenset({Capability.OBSERVE_EXPRESSION,
                              Capability.CANONICAL_MODEL}),
    }

    def requests(self, model, context: AnalysisContext) -> list[InstrumentationRequest]:
        """Ask for each constrained operand to be observed.

        Without this the sanitizer can only reason about what is statically
        reachable; with it, it can say the divisor *was* zero at t=0.31.
        """
        return [
            InstrumentationRequest(
                capability=Capability.OBSERVE_EXPRESSION,
                anchor=CanonicalAnchor(EntityKind.EXPRESSION, site.operand.id),
                label=f"{site.operation}:{site.requirement}",
                requested_by=self.name,
            )
            for site in sites(model)
        ]

    def hints(self, model, context: AnalysisContext) -> list[FuzzHint]:
        """Values that would push each operand out of its domain.

        Only emitted when the operand is a single parameter: those are the ones
        a fuzzer can actually set. An operand that is a computed expression
        needs the search to reach it indirectly, which is a different problem.
        """
        found = []
        for site in sites(model):
            reads = site.operand.variables()
            if len(reads) != 1 or not reads[0].is_parameter:
                continue
            parameter = reads[0]
            if is_cosmetic(parameter.name):
                continue
            found.append(FuzzHint(
                target=parameter.name,
                values=site.forbidden_probes(),
                reason=f"operand of {site.operation}, which requires {site.requirement}",
                source=self.name,
                expression_ids=(site.operand.id,),
                variable_ids=(parameter.id,),
            ))
        return found

    def observe(self, stream: ObservationStream, model, context: AnalysisContext,
                testcase: TestCase) -> list[Finding]:
        """Report the first time each operand leaves its domain.

        First time only: an operand that goes to zero usually stays there, and
        one finding per sample would bury the result.
        """
        by_expression = {site.operand.id: site for site in sites(model)}
        # Expression observations are always canonically anchored: an
        # instrumentation request names a DAE expression, so anything answering
        # one knows which.
        reported: set[int] = set()
        findings = []

        for observation in stream.of(ExpressionObservation):
            if observation.canonical is None:
                continue
            expression_id = observation.canonical.dae_id
            site = by_expression.get(expression_id)
            if site is None or expression_id in reported:
                continue
            if site.admits(observation.value):
                continue
            reported.add(expression_id)
            findings.append(Finding(
                sanitizer=self.name,
                kind=f"{site.operation}-out-of-domain",
                severity=Severity.HIGH,
                canonical_anchors=[CanonicalAnchor(EntityKind.EXPRESSION,
                                                   site.operand.id)],
                source_locations=_location(site.operand),
                phase=observation.phase,
                time=observation.time,
                test_case=testcase,
                evidence={
                    "operation": site.operation,
                    "requirement": site.requirement,
                    "operand_value": observation.value,
                },
            ))
        return findings


def _location(expression: Expression) -> list[SourceLocation]:
    """An expression's site, with the column — a divisor is mid-line."""
    found = locate(getattr(expression, "provenance", None))
    if not found:
        return []
    span = getattr(getattr(expression, "provenance", None), "span", None)
    return [SourceLocation(file=found[0].file, line=found[0].line,
                           column=getattr(span, "column", 0) or 0)]
