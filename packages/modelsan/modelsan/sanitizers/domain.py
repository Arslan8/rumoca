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
from ..findings.finding import Finding, Severity, SourceLocation
from ..fuzz.hints import FuzzHint
from ..fuzz.testcase import TestCase
from ..instrumentation.request import InstrumentationRequest, RequestKind
from ..runtime.observations import ExpressionObservation, ObservationStream

DIVISION_OPS = frozenset({"Div", "div", "/"})

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

    def requests(self, model, context: AnalysisContext) -> list[InstrumentationRequest]:
        """Ask for each constrained operand to be observed.

        Without this the sanitizer can only reason about what is statically
        reachable; with it, it can say the divisor *was* zero at t=0.31.
        """
        return [
            InstrumentationRequest(
                kind=RequestKind.OBSERVE_EXPRESSION,
                expression_id=site.operand.id,
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
        reported: set[int] = set()
        findings = []

        for observation in stream.of(ExpressionObservation):
            site = by_expression.get(observation.expression_id)
            if site is None or observation.expression_id in reported:
                continue
            if site.admits(observation.value):
                continue
            reported.add(observation.expression_id)
            findings.append(Finding(
                sanitizer=self.name,
                kind=f"{site.operation}-out-of-domain",
                severity=Severity.HIGH,
                expression_ids=[site.operand.id],
                variable_ids=[v.id for v in site.operand.variables()],
                source_locations=_location(site.operand),
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
    provenance = getattr(expression, "provenance", None)
    span = getattr(provenance, "span", None) if provenance else None
    if span is None:
        return []
    return [SourceLocation(file=getattr(span, "source_name", "") or "?",
                           line=getattr(span, "line", 0) or 0,
                           column=getattr(span, "column", 0) or 0)]
