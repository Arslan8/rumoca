"""DimensionSan — an equation that adds quantities of different dimensions.

1. Bug class    `a + b` where `a` is a length and `b` a time. Unambiguous: no
                physical argument decides it, the exponent vectors differ.
2. Overlap      none. Every other sanitizer here reasons about *values*; this
                reasons about the units MSL already declares and never looks at
                a number.
3. Signal       static: the dimensions of two operands of `+`, `-`, or a
                relation disagree.
4. Needs        the DAE and its `unit` attributes. Nothing at runtime.
5. Transform    no.
6. Fuzzing      none — there is no value to perturb.
7. Signature    the expression plus the two dimensions.

**Conservative by construction**, because this project's own precision data says
a claim is only worth making when the source settles it:

- an unparseable unit yields *no claim*, never a guess;
- a literal adopts the dimension of what it is added to, so `1 - eps` and
  `v/v_nominal + 1` are silent;
- a variable with no declared unit is unknown, not dimensionless.

The remaining claims are the ones where MSL states both dimensions and they
differ.
"""

from __future__ import annotations

from ..analysis.context import AnalysisContext
from ..dae import BinaryOp, ops
from ..dae.traversal import walk_expressions
from ..findings.finding import Finding, Severity
from ..findings.location import locate
from ..instrumentation.capability import Capability
from ..runtime.anchors import CanonicalAnchor, EntityKind
from ..units.dimension import Dimension, parse

#: For differentiating: `der(x)` has the dimension of `x` per second.
SECOND = parse("s")

#: Operators whose operands must share a dimension.
ADDITIVE = frozenset({ops.ADD, ops.SUBTRACT})
#: `ops.RELATIONS` is the schema-pinned set; naming the members here would let
#: the two drift, which is how an earlier sanitizer silently matched nothing.
RELATIONAL = ops.RELATIONS


def dimension_of(expression) -> Dimension | None:
    """The dimension of an expression, or None where it cannot be settled.

    None is not "dimensionless" — it is "no claim", and it propagates, so one
    unknown operand silences the whole subtree rather than producing a
    confident answer from an incomplete one.
    """
    if expression is None:
        return None

    variable = getattr(expression, "variable", None)
    if variable is not None:
        base = parse(getattr(variable, "unit", None))
        if base is None:
            return None
        # `der(x)` is x per second. Missing this made every state equation in
        # the corpus look inconsistent: `L.L * der(L.i)` is henry times
        # amperes-per-second, which is volts, and reads as webers without it.
        if getattr(expression, "is_derivative", False):
            return base / SECOND
        return base

    # A literal takes its dimension from context; on its own it makes no claim.
    if getattr(expression, "value", None) is not None:
        return None

    op = getattr(expression, "op", None)
    operand = getattr(expression, "operand", None)
    if op is not None and operand is not None:
        return dimension_of(operand)

    lhs, rhs = getattr(expression, "lhs", None), getattr(expression, "rhs", None)
    if op is None or lhs is None or rhs is None:
        return None
    left, right = dimension_of(lhs), dimension_of(rhs)

    if op == ops.MULTIPLY:
        return left * right if left and right else None
    if op == ops.DIVIDE:
        return left / right if left and right else None
    if op in ADDITIVE or op in RELATIONAL:
        # A literal on one side adopts the other's dimension, which is what
        # makes `v/v_nominal + 1` silent instead of a finding.
        return left or right
    return None


class DimensionSan:
    name = "dimension"

    requires = {"static": frozenset({Capability.CANONICAL_MODEL})}

    def analyze(self, model, context: AnalysisContext) -> list[Finding]:
        findings, seen = [], set()
        for _owner, node in walk_expressions(model):
            if not isinstance(node, BinaryOp):
                continue
            if node.op not in ADDITIVE and node.op not in RELATIONAL:
                continue
            left, right = dimension_of(node.lhs), dimension_of(node.rhs)
            if left is None or right is None or left == right:
                continue
            key = (str(left), str(right), repr(node)[:120])
            if key in seen:
                continue
            seen.add(key)

            variables = node.variables()
            findings.append(Finding(
                sanitizer=self.name,
                kind="dimension-mismatch",
                severity=Severity.HIGH,
                canonical_anchors=[CanonicalAnchor(EntityKind.EXPRESSION, node.id)]
                + [CanonicalAnchor(EntityKind.VARIABLE, v.id, v.name)
                   for v in variables[:4]],
                source_locations=locate(node),
                evidence={
                    "expression": repr(node)[:160],
                    "operator": node.op,
                    "left": str(left),
                    "right": str(right),
                    "units": ", ".join(
                        f"{v.name}[{v.unit}]" for v in variables[:6] if v.unit),
                    "note": "the two sides of this operation have different SI "
                            "dimensions, which no choice of values can reconcile",
                },
            ))
        return findings
