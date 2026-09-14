"""DiscontinuitySan — the thresholds a model switches on.

1. Bug class    behaviour that is wrong *at* or immediately around a switching
                threshold: a branch that divides by something only zero at the
                boundary, a `noEvent` that hides a discontinuity from the
                integrator, a guard whose two sides disagree at the crossing.
2. Overlap      it shares oracles with DomainSan and SolverSan; what it
                contributes is *where to look*. A threshold is a measure-zero
                set that random search never lands on.
3. Signal       static: a conditional whose branch condition compares against a
                value a search can set.
4. Needs        DAE conditional expressions. No instrumentation.
5. Transform    no.
6. Fuzzing      its entire purpose. c-eps, c, c+eps around every threshold.
7. Signature    the DAE expression id of the conditional.
"""

from __future__ import annotations

from ..analysis.context import AnalysisContext
from ..dae import BinaryOp, Conditional, Literal
from ..dae.traversal import walk_expressions
from ..findings.finding import Finding, Severity
from ..fuzz.hints import FuzzHint
from ..instrumentation.capability import Capability
from .base import is_cosmetic
from ..runtime.anchors import CanonicalAnchor, EntityKind

from ..dae import ops

RELATIONS = ops.RELATIONS

#: Small enough to sit inside any physical tolerance, large enough to survive
#: double rounding at unit scale.
EPSILON = 1e-9


def _numeric(literal) -> float | None:
    """A literal's value as a float, or None when it is not numeric.

    A relation can compare against a String or an enumeration — `mode == Mode.Off`
    is a switching condition too. Those are real thresholds but not ones a
    numeric fuzzer can place itself on, and calling `float()` on them crashed
    the harness on 34 of the first 201 corpus models.
    """
    value = getattr(literal, "value", None)
    if isinstance(value, bool) or value is None:
        return None
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


class DiscontinuitySan:
    name = "discontinuity"

    requires = {"hints": frozenset({Capability.CANONICAL_MODEL}),
                "static": frozenset({Capability.CANONICAL_MODEL})}

    def _thresholds(self, model):
        """(conditional, parameter, threshold) for every switch a search can move.

        Only relations of the form `p <op> literal` are used. A relation
        between two computed quantities is a real threshold too, but not one a
        parameter fuzzer can place itself on, so offering a hint for it would
        be noise.
        """
        found = []
        for _, node in walk_expressions(model):
            if not isinstance(node, Conditional):
                continue
            for condition, _value in getattr(node, "branches", []):
                if not isinstance(condition, BinaryOp) or condition.op not in RELATIONS:
                    continue
                for left, right in ((condition.lhs, condition.rhs),
                                    (condition.rhs, condition.lhs)):
                    if not isinstance(right, Literal):
                        continue
                    threshold = _numeric(right)
                    if threshold is None:
                        continue  # a String or enumeration literal is not a threshold
                    reads = left.variables()
                    if len(reads) == 1 and reads[0].is_parameter:
                        found.append((node, reads[0], threshold))
        return found

    def hints(self, model, context: AnalysisContext) -> list[FuzzHint]:
        found = []
        for node, parameter, threshold in self._thresholds(model):
            if is_cosmetic(parameter.name):
                continue
            scale = max(abs(threshold), 1.0)
            found.append(FuzzHint(
                target=parameter.name,
                values=(threshold - EPSILON * scale, threshold,
                        threshold + EPSILON * scale),
                reason=f"switching threshold of a conditional (expression {node.id})",
                source=self.name,
                expression_ids=(node.id,),
                variable_ids=(parameter.id,),
            ))
        return found

    def analyze(self, model, context: AnalysisContext) -> list[Finding]:
        """Report thresholds found, as coverage information rather than defects.

        A threshold is not a bug. Recording them lets an evaluation say how much
        of a model's switching behaviour the search actually visited, which is
        the difference between "no bug here" and "never looked".
        """
        found = []
        for node, parameter, threshold in self._thresholds(model):
            found.append(Finding(
                sanitizer=self.name,
                kind="switching-threshold",
                severity=Severity.INFO,
                canonical_anchors=[CanonicalAnchor(EntityKind.EXPRESSION, node.id)],
                evidence={"parameter": parameter.name, "threshold": threshold},
            ))
        return found
