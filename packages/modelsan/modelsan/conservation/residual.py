"""Normalising a balance equation into a coefficient map.

Just enough symbolic handling for conservation equations, and no more. The
brief is explicit that this must not become a computer algebra system, and the
restraint is load-bearing: a normaliser that quietly gives up on a shape it
does not understand produces `UNKNOWN`, while one that guesses produces a
confident wrong coefficient.

Supported, because these are what balance equations are made of:

    +  -  unary -            a + b - der(m)
    constant * variable      2*m_out, m_out*2
    variable / constant      q/n
    nested sums              (a + b) - (c + d)

Anything else — a product of two variables, a call, a conditional — makes the
whole equation unnormalisable, and that is reported rather than approximated.
"""

from __future__ import annotations

from dataclasses import dataclass

from ..dae import BinaryOp, ops
from ..physical.engine import constant_value

#: (variable id, is_derivative) -> coefficient
Coefficients = dict[tuple[int, bool], float]


@dataclass
class Normalised:
    """An equation as `sum(coefficient * term) + constant = 0`, or a failure."""

    coefficients: Coefficients
    constant: float = 0.0
    ok: bool = True
    reason: str = ""

    @staticmethod
    def failed(reason: str) -> "Normalised":
        return Normalised({}, 0.0, False, reason)

    def scaled(self, factor: float) -> "Normalised":
        return Normalised({k: v * factor for k, v in self.coefficients.items()},
                          self.constant * factor, self.ok, self.reason)

    def __add__(self, other: "Normalised") -> "Normalised":
        if not (self.ok and other.ok):
            return Normalised.failed(self.reason or other.reason)
        merged = dict(self.coefficients)
        for key, value in other.coefficients.items():
            merged[key] = merged.get(key, 0.0) + value
        return Normalised({k: v for k, v in merged.items() if v != 0.0},
                          self.constant + other.constant)

    def __sub__(self, other: "Normalised") -> "Normalised":
        return self + other.scaled(-1.0)

    def render(self, names: dict[int, str]) -> str:
        if not self.coefficients:
            return f"{self.constant:g} = 0" if self.constant else "0 = 0"
        parts = []
        for (variable, derivative), coefficient in sorted(
                self.coefficients.items(), key=lambda kv: kv[0]):
            name = names.get(variable, f"<{variable}>")
            if derivative:
                name = f"der({name})"
            magnitude = "" if abs(coefficient) == 1 else f"{abs(coefficient):g}*"
            parts.append(f"{'+' if coefficient > 0 else '-'} {magnitude}{name}")
        if self.constant:
            parts.append(f"{'+' if self.constant > 0 else '-'} {abs(self.constant):g}")
        body = " ".join(parts).lstrip("+ ")
        return f"{body} = 0"


def normalise(expression) -> Normalised:
    """An expression as a linear combination of variables and `der(variable)`."""
    if expression is None:
        return Normalised.failed("empty expression")

    value = constant_value(expression)
    if value is not None:
        return Normalised({}, value)

    variable = getattr(expression, "variable", None)
    if variable is not None:
        if getattr(expression, "is_previous", False):
            return Normalised.failed("pre() is not a balance term")
        derivative = bool(getattr(expression, "is_derivative", False))
        return Normalised({(variable.id, derivative): 1.0})

    op = getattr(expression, "op", None)
    operand = getattr(expression, "operand", None)
    if op is not None and operand is not None:
        inner = normalise(operand)
        if op in ("negate", "minus", "-"):
            return inner.scaled(-1.0)
        if op in ("plus", "+"):
            return inner
        return Normalised.failed(f"unary `{op}` is not linear")

    lhs, rhs = getattr(expression, "lhs", None), getattr(expression, "rhs", None)
    if op is None or lhs is None or rhs is None:
        return Normalised.failed("not a linear expression")

    if op == ops.ADD:
        return normalise(lhs) + normalise(rhs)
    if op == ops.SUBTRACT:
        return normalise(lhs) - normalise(rhs)
    if op == ops.MULTIPLY:
        # Exactly one side must be constant; `a*b` with both variable is not
        # linear and must not be approximated.
        left, right = constant_value(lhs), constant_value(rhs)
        if left is not None and right is not None:
            return Normalised({}, left * right)
        if left is not None:
            return normalise(rhs).scaled(left)
        if right is not None:
            return normalise(lhs).scaled(right)
        return Normalised.failed("product of two variables is not linear")
    if op == ops.DIVIDE:
        divisor = constant_value(rhs)
        if divisor is None or divisor == 0.0:
            return Normalised.failed("division by a non-constant")
        return normalise(lhs).scaled(1.0 / divisor)
    return Normalised.failed(f"`{op}` is not linear")


def normalise_equation(equation) -> Normalised:
    """A residual equation `0 = residual`, normalised.

    Both `a + b = der(m)` and `der(m) = a + b` reach the DAE as the same
    residual, so canonicalisation is already done by the compiler and this
    only has to linearise what it produced.
    """
    return normalise(equation.residual)
