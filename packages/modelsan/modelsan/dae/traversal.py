"""Shared traversal helpers over DAE expressions.

These are used by several sanitizers, so they live once here rather than being
re-implemented per sanitizer. They return DAE objects, never copies.
"""

from __future__ import annotations

from typing import Iterator

from rumoca_bitcode import BinaryOp, Expression, Model

from . import ops


def walk_expressions(model: Model) -> Iterator[tuple[object, Expression]]:
    """Every expression the model evaluates, with the owner it belongs to.

    The owner matters for findings: an expression id alone says *what* is wrong,
    the owner says which equation or variable attribute will fail because of it.
    """
    for equation in model.equations:
        for node in equation.residual.walk():
            yield equation, node
    for equation in model.initial_equations:
        for node in equation.residual.walk():
            yield equation, node
    for variable in model.variables:
        for attribute in (variable.binding, variable.start,
                          variable.minimum, variable.maximum):
            if attribute is None:
                continue
            for node in attribute.walk():
                yield variable, node


def expression_by_id(model: Model, expression_id: int) -> Expression | None:
    """Resolve a DAE expression id back to its node.

    Findings carry ids rather than objects so they can be serialized and
    compared across runs; this is how a reporter or a minimizer gets back to the
    expression itself.
    """
    expressions = model.expressions
    if 0 <= expression_id < len(expressions):
        return expressions[expression_id]
    return None


def denominators(model: Model) -> Iterator[tuple[object, Expression]]:
    """Every expression that appears as a divisor.

    Division is the one unsafe operation whose operand position matters: `a/b`
    is only dangerous in `b`. Sanitizers that care about reachable zeros need
    the divisor specifically, not both operands.
    """
    for owner, node in walk_expressions(model):
        if isinstance(node, BinaryOp) and node.op == ops.DIVIDE:
            yield owner, node.rhs


def equations_reading(model: Model, variable_id: int) -> list:
    """Equations whose residual reads a given variable.

    Uses the `reads` set the exporter computed from the compiler's own
    incidence proof, rather than re-deriving incidence by walking expressions —
    the two can disagree for array and record coordinates, and the compiler's is
    the authority.
    """
    found = []
    for equation in model.equations:
        if any(v.id == variable_id for v in equation.residual.variables()):
            found.append(equation)
    return found
