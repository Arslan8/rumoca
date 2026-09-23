"""Shared traversal helpers over DAE expressions.

These are used by several sanitizers, so they live once here rather than being
re-implemented per sanitizer. They return DAE objects, never copies.
"""

from __future__ import annotations

from typing import Iterator

from rumoca_bitcode import BinaryOp, Expression, Model

from . import ops


def root_expressions(model: Model) -> Iterator[tuple[object, Expression]]:
    """Every *top-level* expression, with the owner that evaluates it.

    `walk_expressions` yields every node, which is what a pass wants when it is
    looking for a shape. It is the wrong thing when a pass needs the context a
    node sits in: an inner `if` arrives both as a child of its parent and as a
    root of its own, so a division inside it is visited twice — once with its
    full path condition and once with only part of it. DivisorSan reported the
    second as unguarded.
    """
    for equation in model.equations:
        yield equation, equation.residual
    for equation in model.initial_equations:
        yield equation, equation.residual
    for families in (getattr(model, "equation_families", ()) or (),
                     getattr(model, "initial_equation_families", ()) or ()):
        for family in families:
            for body in family.bodies:
                yield family, body
    for equation in getattr(model, "discrete_real_equations", ()) or ():
        yield equation, equation.residual
    for variable in model.variables:
        for attribute in (variable.binding, variable.start,
                          variable.minimum, variable.maximum):
            if attribute is not None:
                yield variable, attribute


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
    # Array and `for` equations. Their bodies were invisible here for as long
    # as the compiler dropped families from the artifact (TOOLBUG-014), so
    # every expression inside a `for` loop — every division, every unit, every
    # bound — went unchecked by every pass built on this traversal.
    for families in (getattr(model, "equation_families", ()) or (),
                     getattr(model, "initial_equation_families", ()) or ()):
        for family in families:
            for body in family.bodies:
                for node in body.walk():
                    yield family, node
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
    for family in getattr(model, "equation_families", ()) or ():
        if any(v.id == variable_id
               for body in family.bodies for v in body.variables()):
            found.append(family)
    return found
