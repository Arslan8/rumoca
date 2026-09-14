"""SingularitySan — structure that cannot be solved, found before it is run.

1. Bug class    an algebraic block that loses rank for a reachable parameter
                value: a coefficient that vanishes, a block that is not square.
                This is the *cause* behind a large share of what SolverSan
                reports as a generic failure.
2. Overlap      substantial by design, and in the useful direction. SolverSan
                says the run failed; this says which block, which equations,
                and which parameter made it singular. When both fire the
                deduplicator keeps one bug, and this one carries the
                explanation.
3. Signal       static and structural: a parameter that is the sole coefficient
                of a state derivative, or a block whose equation and variable
                counts disagree. No Jacobian, no symbolic determinant — those
                do not scale to MSL-sized systems.
4. Needs        the shared dependency graph and block decomposition. Nothing at
                runtime, which is what lets it run on models no backend can
                execute.
5. Transform    no.
6. Fuzzing      strong hints: it names the exact parameter whose vanishing
                collapses a block, which is the highest-value single value to
                try in the whole model.
7. Signature    the block's equation ids, plus the implicated parameter.

**Deliberately an over-approximation.** `m*a = f` and `f = d*v` are structurally
identical residuals and only the first is fatal at zero; which it is depends on
the variable the equation is matched to, and bitcode does not carry BLT
information. So this is a candidate generator whose oracle is execution — the
same division of labour that took 147 candidates down to 7 confirmed.
"""

from __future__ import annotations

from dataclasses import dataclass

from ..analysis.blocks import AlgebraicBlock
from ..analysis.context import AnalysisContext
from ..dae import BinaryOp
from ..findings.finding import Finding, Severity, SourceLocation
from ..fuzz.hints import FuzzHint
from ..runtime.anchors import CanonicalAnchor, EntityKind

from ..dae import ops

MULTIPLY = frozenset({ops.MULTIPLY})


@dataclass(frozen=True)
class VanishingCoefficient:
    """A parameter multiplying a derivative, which zero would remove."""

    parameter: object
    equation: object
    declared_min: float | None


def _literal(expression):
    return getattr(expression, "value", None) if expression is not None else None


class SingularitySan:
    name = "singularity"

    #: Purely structural. Declaring no runtime requirement is what lets the
    #: planner run this on models nothing can execute.
    requires = {"static": frozenset()}

    @staticmethod
    def _derivative_refs(expression) -> set[int]:
        """Variable ids read as `der(...)` inside one expression.

        `Expression.variables()` returns `Variable`, which does not know
        whether it was read as a value or a derivative — that lives on the
        `VariableRef` node. Walking is the only way to tell them apart, and
        conflating them makes every index-1 system look algebraic.
        """
        from ..dae import VariableRef
        return {node.variable.id for node in expression.walk()
                if isinstance(node, VariableRef) and node.is_derivative}

    @staticmethod
    def _derivative_aliases(model) -> set[int]:
        """Algebraic variables defined as `x = der(y)`.

        MSL almost never writes `m*der(v) = f`. It writes `a = der(v)` and then
        `m*a = f`, so a check that only recognises a literal `der(...)` operand
        misses the entire Mass/Inertia family — which is most of what this
        sanitizer exists to find. One level of resolution covers the idiom.
        """
        aliases = set()
        for equation in model.equations:
            derivative_ids = SingularitySan._derivative_refs(equation.residual)
            if len(derivative_ids) != 1:
                continue
            plain = [v for v in equation.residual.variables()
                     if not v.is_parameter and v.id not in derivative_ids]
            # `x - der(y)`: one derivative, one plain unknown, nothing else.
            if len(plain) == 1:
                aliases.add(plain[0].id)
        return aliases

    def _vanishing(self, model) -> list[VanishingCoefficient]:
        aliases = self._derivative_aliases(model)
        found = []
        for equation in model.equations:
            for node in equation.residual.walk():
                if not isinstance(node, BinaryOp) or node.op not in MULTIPLY:
                    continue
                for coefficient, other in ((node.lhs, node.rhs), (node.rhs, node.lhs)):
                    reads = coefficient.variables()
                    if len(reads) != 1 or not reads[0].is_parameter:
                        continue
                    derivative_ids = SingularitySan._derivative_refs(other)
                    touches_state = bool(derivative_ids) or any(
                        v.id in aliases for v in other.variables())
                    if not touches_state:
                        continue
                    found.append(VanishingCoefficient(
                        parameter=reads[0], equation=equation,
                        declared_min=_literal(reads[0].minimum)))
        return found

    def analyze(self, model, context: AnalysisContext) -> list[Finding]:
        findings: list[Finding] = []

        for risk in self._vanishing(model):
            permitted = risk.declared_min is None or risk.declared_min <= 0.0
            findings.append(Finding(
                sanitizer=self.name,
                kind="vanishing-coefficient" if permitted
                     else "vanishing-coefficient-excluded-by-bound",
                # Only a risk when the declaration actually admits zero. Where
                # a positive bound excludes it, the model has already defended
                # itself and this is informational.
                severity=Severity.MEDIUM if permitted else Severity.INFO,
                canonical_anchors=[
                    CanonicalAnchor(EntityKind.PARAMETER, risk.parameter.id,
                                    risk.parameter.name),
                    CanonicalAnchor(EntityKind.EQUATION, risk.equation.id),
                ],
                source_locations=_location(risk.parameter),
                evidence={
                    "parameter": risk.parameter.name,
                    "declared_min": risk.declared_min,
                    "shape": "parameter multiplies a derivative; zero removes "
                             "the equation's only determination of that state",
                },
            ))

        for block in context.blocks:
            if block.is_square or not block.is_loop:
                continue
            findings.append(Finding(
                sanitizer=self.name,
                kind="non-square-block",
                severity=Severity.MEDIUM,
                canonical_anchors=[CanonicalAnchor(EntityKind.EQUATION, e)
                                   for e in block.equation_ids[:8]],
                evidence={"block": block.block_id,
                          "equations": len(block.equation_ids),
                          "variables": len(block.variable_ids)},
            ))
        return findings

    def hints(self, model, context: AnalysisContext) -> list[FuzzHint]:
        """Zero for every parameter whose vanishing would collapse a block."""
        return [
            FuzzHint(
                target=risk.parameter.name,
                values=(0.0,),
                reason="sole coefficient of a derivative; zero removes the "
                       "equation that determines that state",
                source=self.name,
                variable_ids=(risk.parameter.id,),
            )
            for risk in self._vanishing(model)
            if risk.declared_min is None or risk.declared_min <= 0.0
        ]


def _location(variable) -> list[SourceLocation]:
    source = getattr(variable, "source", None)
    span = getattr(source, "span", None) if source else None
    if span is None:
        return []
    return [SourceLocation(file=getattr(span, "source_name", "") or "?",
                           line=getattr(span, "line", 0) or 0)]
