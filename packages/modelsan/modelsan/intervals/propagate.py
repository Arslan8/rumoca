"""Propagating initial equations into the environment.

An initial equation arrives as a residual: `0 = residual`. The useful shapes
are the ones where that pins a single variable, and this deliberately handles
only those:

    0 = x - 5              x = 5
    0 = x - y              x = y
    0 = x - (y + 2)        x takes y's interval, shifted
    0 = y - (x + p)        either side, whichever is a bare variable

This is not a solver. `0 = x*y - 1` with both unknown is left alone, because
guessing there is how an analysis starts inventing constraints. The brief's
§10 says the same: prioritise simple high-value forms, do not build a symbolic
solver.

Iterated to a fixed point, because one equation's conclusion is another's
input: `x = -1` then `y = x + p` needs two passes and the order in the file is
not the order of dependency.
"""

from __future__ import annotations

from ..dae import BinaryOp, ops
from ..physical.engine import constant_value
from .initial_state import InitialState, Provenance
from .interval import Interval

#: A fixed point is reached in two or three passes on real models; the cap is
#: only there so a pathological cycle terminates.
MAX_PASSES = 8


def evaluate(expression, state: InitialState) -> Interval:
    """The interval an expression can take, given the environment."""
    if expression is None:
        return Interval.unknown()

    value = constant_value(expression)
    if value is not None:
        return Interval.point(value)

    variable = getattr(expression, "variable", None)
    if variable is not None:
        if getattr(expression, "is_derivative", False):
            return Interval.unknown()   # der(x) at t=0 is not x
        return state.interval(variable.id)

    op = getattr(expression, "op", None)
    operand = getattr(expression, "operand", None)
    if op is not None and operand is not None:
        inner = evaluate(operand, state)
        if op in ("negate", "minus", "-"):
            return -inner
        if op in ("plus", "+"):
            return inner
        return Interval.unknown()

    lhs, rhs = getattr(expression, "lhs", None), getattr(expression, "rhs", None)
    if op is None or lhs is None or rhs is None:
        return Interval.unknown()
    left, right = evaluate(lhs, state), evaluate(rhs, state)
    if op == ops.ADD:
        return left + right
    if op == ops.SUBTRACT:
        return left - right
    if op == ops.MULTIPLY:
        return left * right
    if op == ops.DIVIDE:
        return left / right
    if op == ops.POWER:
        exponent = constant_value(rhs)
        return left.power(exponent) if exponent is not None else Interval.unknown()
    return Interval.unknown()


def _bare_variable(expression):
    """The variable, if the expression is just a plain reference to one."""
    variable = getattr(expression, "variable", None)
    if variable is None:
        return None
    if getattr(expression, "is_derivative", False) or getattr(expression, "is_previous", False):
        return None
    return variable


def propagate(model, state: InitialState) -> int:
    """Refine the environment from the initial equations. Returns pass count.

    Every initial equation is a residual that must be zero, so for
    `0 = a - b` the two sides share an interval and each can narrow the other.
    """
    for pass_number in range(1, MAX_PASSES + 1):
        changed = False
        for equation in model.initial_equations:
            changed |= _apply(equation, state)
        if not changed:
            return pass_number
    return MAX_PASSES


def _apply(equation, state: InitialState) -> bool:
    residual = equation.residual
    # The canonical form is `0 = lhs - rhs`, so a subtraction at the root is
    # an equality between its operands.
    if not (isinstance(residual, BinaryOp) and residual.op == ops.SUBTRACT):
        return False
    left, right = residual.lhs, residual.rhs

    changed = False
    for target, other in ((left, right), (right, left)):
        variable = _bare_variable(target)
        if variable is None:
            continue
        interval = evaluate(other, state)
        if interval.is_unknown:
            continue
        changed |= state.refine(
            variable.id, interval,
            Provenance("initial-equation", f"{variable.name} = {other!r}"[:90]))
    return changed
