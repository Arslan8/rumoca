"""Proving that a denominator can be zero, by exhibiting an assignment.

The rule this module exists to enforce: **a parameter appearing inside a
denominator is not evidence that the denominator can vanish.** The previous
implementation reported every parameter it found under a `/`, which produced

    1 + c_b*B_N + B_N^n      "c_b can be zero"     -> 1 + B_N^n, never zero
    1 + alpha*(T - T_ref)    "alpha can be zero"   -> 1, never zero
    2*pi*fsNominal           "pi can be zero"      -> pi is a constant

Each of those is refuted by the same discipline: propose a concrete assignment,
substitute it, and evaluate. If the denominator does not come out zero, there
is no finding. Everything else here --- bounds, assertions, branch conditions
--- narrows which assignments may be proposed.
"""

from __future__ import annotations

import math
from dataclasses import dataclass, field

from ..dae import BinaryOp, Conditional, Literal, VariableRef, ops
from .constraints import Domain, Environment, shape_key

#: Below this a denominator is treated as zero. Chosen to match the guard MSL
#: itself uses (`Modelica.Constants.eps`), so a denominator a model asserts is
#: `>= eps` is not then reported as reaching zero.
EPS = 2.220446049250313e-16

#: A denominator is zero only when its terms genuinely cancel. This is a
#: floating-point tolerance, not a smallness threshold: `Ni` at its declared
#: minimum of 2.2e-14 makes `k*Ni` small, and "small" is a large quotient, not
#: a division by zero. Treating 2.2e-14 as zero reported a declaration that
#: forbids zero as if it permitted it.
RELATIVE = 0.0


@dataclass(frozen=True)
class Witness:
    """A concrete assignment that makes a denominator vanish."""

    assignment: dict[int, float]
    """variable id -> the value the witness sets."""

    residual: float
    """The denominator evaluated under the assignment. Verified near zero."""

    rationale: str
    """How the assignment was found: zero, bound, equality, or linear solve."""

    def rendered(self, names: dict[int, str]) -> str:
        return ", ".join(f"{names.get(i, i)} = {v:g}"
                         for i, v in sorted(self.assignment.items(),
                                            key=lambda kv: names.get(kv[0], "")))


class Unevaluable(Exception):
    """The expression contains something this evaluator cannot decide."""


def evaluate(expression, environment: Environment,
             assignment: dict[int, float], _depth: int = 0) -> float:
    """Numerically evaluate an expression under an assignment.

    Raises `Unevaluable` rather than guessing. A guess here would be a
    fabricated witness, which is the failure mode this whole module exists to
    prevent.
    """
    if isinstance(expression, Literal):
        if expression.kind in ("real", "integer"):
            return float(expression.value)
        raise Unevaluable(f"{expression.kind} literal")

    if isinstance(expression, VariableRef):
        variable = expression.variable
        if expression.kind == "derivative":
            raise Unevaluable("derivative")
        if variable.id in assignment:
            return assignment[variable.id]
        if variable.id in environment.values:
            return environment.values[variable.id]
        if _depth < 12:
            # A variable one equation defines in terms of others.
            definition = environment.definitions.get(variable.id)
            if definition is not None:
                return evaluate(definition, environment, assignment, _depth + 1)
            # A derived parameter: fold its binding. Without this a witness
            # stops at the symbol it names and never reaches the parameters
            # computed from it, so `T_rising = rising` stays unknown when
            # `rising` is set to zero and the branch guarded by it cannot be
            # shown unreachable.
            binding = environment.bindings.get(variable.id)
            if binding is not None:
                return evaluate(binding, environment, assignment, _depth + 1)
        raise Unevaluable(f"no value for {variable.name}")

    if isinstance(expression, BinaryOp):
        left = evaluate(expression.lhs, environment, assignment, _depth)
        right = evaluate(expression.rhs, environment, assignment, _depth)
        if expression.op == ops.ADD:
            return left + right
        if expression.op == ops.SUBTRACT:
            return left - right
        if expression.op == ops.MULTIPLY:
            return left * right
        if expression.op == ops.DIVIDE:
            if abs(right) < EPS:
                raise Unevaluable("nested division by zero")
            return left / right
        if expression.op == ops.POWER:
            try:
                return float(left ** right)
            except (OverflowError, ValueError, ZeroDivisionError):
                raise Unevaluable("power out of range")
        raise Unevaluable(f"operator {expression.op}")

    node = type(expression).__name__
    if node == "UnaryOp":
        inner = evaluate(expression.operand, environment, assignment, _depth)
        if expression.op == "negate":
            return -inner
        if expression.op == "plus":
            return inner
        raise Unevaluable(f"unary {expression.op}")

    if node == "BuiltinCall":
        return _builtin(expression, environment, assignment, _depth)

    raise Unevaluable(node)


_UNARY_BUILTINS = {
    "sqrt": math.sqrt, "abs": abs, "exp": math.exp, "log": math.log,
    "log10": math.log10, "sin": math.sin, "cos": math.cos, "tan": math.tan,
    "asin": math.asin, "acos": math.acos, "atan": math.atan,
    "sinh": math.sinh, "cosh": math.cosh, "tanh": math.tanh,
    "ceil": math.ceil, "floor": math.floor,
}


def _builtin(expression, environment, assignment, _depth=0) -> float:
    name = expression.name
    arguments = [evaluate(a, environment, assignment, _depth)
                 for a in expression.arguments]
    try:
        if name in _UNARY_BUILTINS and len(arguments) == 1:
            return float(_UNARY_BUILTINS[name](arguments[0]))
        if name == "min":
            return float(min(arguments))
        if name == "max":
            return float(max(arguments))
        if name == "atan2" and len(arguments) == 2:
            return math.atan2(*arguments)
        if name == "sign" and len(arguments) == 1:
            return float((arguments[0] > 0) - (arguments[0] < 0))
    except (ValueError, OverflowError):
        raise Unevaluable(f"{name} out of domain")
    raise Unevaluable(f"builtin {name}")


def _is_zero(expression, residual: float, scale: float) -> bool:
    """Whether the denominator is zero under the witness.

    Exact zero, or --- only for a sum or a difference --- a cancellation small
    against the terms being combined. Nothing else may be approximately zero,
    and two rounds of this analysis went wrong by allowing it to:

    * `V_flowLaminar` at its declared minimum of 2.2e-308 is the smallest value
      the declaration *permits*. Small is a large quotient, not a division by
      zero.
    * `max(eps*oneOhm, abs(R))` is the idiom MSL uses to hold a denominator
      away from zero. At `R = 0` it returns `eps`, which is the guard working,
      and a tolerance of `EPS * scale` accepted it as zero by a hair.

    Only an addition or a subtraction can cancel. A product, a power, a `max`
    or a bare parameter is zero when it is zero.
    """
    if not math.isfinite(residual):
        return False
    if residual == 0.0:
        return True
    cancellable = (isinstance(expression, BinaryOp)
                   and expression.op in (ops.ADD, ops.SUBTRACT))
    return cancellable and abs(residual) <= 1e-12 * scale


def _scale(expression, environment, assignment) -> float:
    """The magnitude of the largest term, for a relative zero test.

    No floor. Seeding this list with 1.0 — which it was — makes the tolerance
    at least `EPS`, so any denominator below 2.2e-16 counts as zero. MSL bounds
    quantities away from zero with `Modelica.Constants.small` = 2.2e-308, and
    those declarations were being read as permitting the zero they forbid.
    """
    magnitudes = []
    for node in expression.walk():
        if isinstance(node, (Literal, VariableRef)):
            try:
                magnitudes.append(abs(evaluate(node, environment, assignment)))
            except Unevaluable:
                continue
    return max(magnitudes) if magnitudes else 0.0


def candidates(denominator, environment: Environment) -> list[tuple[dict, str]]:
    """Assignments worth trying, cheapest and most likely first.

    Deliberately a small, explainable set rather than a solver. Every candidate
    is verified by evaluation afterwards, so an unhelpful proposal costs a
    numeric evaluation and nothing else; a proposal this list cannot express
    means no finding, which is the safe direction.
    """
    settable = _knobs(denominator, environment)
    proposals: list[tuple[dict, str]] = []

    # 1. One knob to zero. The classic direct and product-factor cases.
    for variable in settable:
        if environment.domain(variable.id).admits_zero:
            proposals.append(({variable.id: 0.0}, "set to zero"))

    # 2. One knob to a declared extreme. Catches a denominator that vanishes
    #    at a bound rather than at zero.
    for variable in settable:
        domain = environment.domain(variable.id)
        for limit, label in ((domain.low, "at its declared minimum"),
                             (domain.high, "at its declared maximum")):
            if math.isfinite(limit) and limit != 0.0:
                proposals.append(({variable.id: limit}, label))

    # 3. Equality between two knobs: `a - b` is zero when they are equal, and
    #    no `min` on either can express that. The witness is the equality, not
    #    a zero.
    if isinstance(denominator, BinaryOp) and denominator.op == ops.SUBTRACT:
        left = _knobs(denominator.lhs, environment)
        right = _knobs(denominator.rhs, environment)
        if len(left) == 1 and len(right) == 1:
            a, b = left[0], right[0]
            for source, target in ((a, b), (b, a)):
                domain = environment.domain(source.id)
                value = environment.values.get(target.id)
                if domain.settable and value is not None and domain.admits(value):
                    proposals.append(
                        ({source.id: value},
                         f"set equal to {target.name}"))

    # 4. Solve for one knob, treating the rest as declared. This is what
    #    decides `1 + alpha*(T - T_ref)`: it is linear in alpha, and the
    #    solution alpha = -1/(T - T_ref) either exists inside the domain or
    #    does not.
    for variable in settable:
        solved = _solve_linear(denominator, variable, environment)
        if solved is None:
            continue
        domain = environment.domain(variable.id)
        if domain.admits(solved):
            proposals.append(({variable.id: solved},
                              "the value that solves the denominator to zero"))
    return proposals


def _knobs(denominator, environment: Environment) -> list:
    """Variables a witness may assign, including through definitions.

    `p_s/(vps - vns)` divides by two variables, neither of which a user sets.
    Both are defined by `vps = Vps` and `vns = Vns`, so the knobs are the
    supply-voltage parameters and the witness is an assignment to those.
    """
    found, seen = [], set()

    def visit(expression, depth: int) -> None:
        for variable in expression.variables():
            if variable.id in seen:
                continue
            seen.add(variable.id)
            if environment.domain(variable.id).settable:
                found.append(variable)
                continue
            definition = environment.definitions.get(variable.id)
            if definition is not None and depth < 8:
                visit(definition, depth + 1)

    visit(denominator, 0)
    return found


def _solve_linear(denominator, variable, environment: Environment) -> float | None:
    """Solve `D(v) = 0` for `v`, if `D` is linear in `v`.

    Two evaluations determine a line. If the denominator is not linear in `v`
    the third evaluation disagrees and we decline, rather than returning a
    root of the secant that is not a root of `D`.
    """
    def at(value: float) -> float | None:
        try:
            return evaluate(denominator, environment, {variable.id: value})
        except Unevaluable:
            return None

    zero, one = at(0.0), at(1.0)
    if zero is None or one is None:
        return None
    slope = one - zero
    if abs(slope) < EPS:
        return None
    root = -zero / slope
    if not math.isfinite(root):
        return None
    # Confirm linearity: a linear D must also agree at 2.
    two = at(2.0)
    if two is None or abs(two - (zero + 2 * slope)) > 1e-9 * max(1.0, abs(two)):
        return None
    return root


def find(denominator, environment: Environment) -> Witness | None:
    """A verified assignment making `denominator` zero, or None.

    None means *no evidence*, not *proved safe*: an assignment may exist that
    this search does not express. Reporting only what is verified is the whole
    point, and the cost is recall.
    """
    for assignment, rationale in candidates(denominator, environment):
        try:
            residual = evaluate(denominator, environment, assignment)
        except Unevaluable:
            continue
        if _is_zero(denominator, residual,
                    _scale(denominator, environment, assignment)):
            return Witness(assignment=dict(assignment), residual=residual,
                           rationale=rationale)
    return None


def baseline(denominator, environment: Environment) -> float | None:
    """The denominator at the model's declared values, or None if unknown.

    A denominator that is *already* zero at the declared configuration is not a
    latent hazard, it is a broken model --- and far more often it means the
    evaluator is missing a value, which is why this is reported rather than
    treated as a finding.
    """
    try:
        return evaluate(denominator, environment, {})
    except Unevaluable:
        return None
