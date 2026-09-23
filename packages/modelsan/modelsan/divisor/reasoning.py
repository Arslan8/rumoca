"""Deciding `constraints AND path AND denominator == 0`, three ways.

The question a divide-by-zero analysis actually asks is a satisfiability
question over three conjuncts: the declared constraints, the condition under
which the division executes, and the denominator being zero. There are three
honest answers, and collapsing them to two is what produced the false positives
this module exists to remove.

``SAT``
    An assignment satisfies all three. Report it, with the assignment.
``UNSAT``
    No assignment can. Suppress it, and record the proof --- an interval that
    excludes zero, an assertion, a contradictory path.
``UNKNOWN``
    Neither could be shown. Report it as *unresolved*, never as confirmed.

The third is the one that was missing. `Trapezoid` divides by `rising` inside
``time < T_start + T_rising``, where `T_start` is a discrete variable a `when`
clause assigns. At `rising = 0` the branch is empty *if* `T_start >= startTime`,
which is true of the model and is not deducible from the artifact. Calling that
SAT reports a defect that is not there; calling it UNSAT hides one that might
be. It is UNKNOWN, and saying so costs nothing but a column in a table.
"""

from __future__ import annotations

import math
from dataclasses import dataclass, field

from ..dae import BinaryOp, Literal, VariableRef, ops
from ..intervals.interval import INF, Interval
from .constraints import Environment, shape_key
from .witness import EPS, Unevaluable, Witness, evaluate, find


@dataclass(frozen=True)
class Verdict:
    """The answer, and why."""

    status: str
    """SAT | UNSAT | UNKNOWN"""

    witness: Witness | None = None
    """The satisfying assignment, when SAT."""

    proof: str = ""
    """Why it is UNSAT, or what could not be decided when UNKNOWN."""

    denominator_range: str = ""
    """The interval the denominator was shown to lie in."""

    @property
    def is_sat(self) -> bool:
        return self.status == "SAT"


# ── interval propagation over the denominator ────────────────────────────────

_UNARY_RANGE = {
    "abs": lambda i: Interval(0.0, max(abs(i.lo), abs(i.hi))
                              if math.isfinite(i.lo) and math.isfinite(i.hi) else INF)
                     if i.spans_zero else
                     Interval(min(abs(i.lo), abs(i.hi)), max(abs(i.lo), abs(i.hi))),
    "sqrt": lambda i: Interval(math.sqrt(max(i.lo, 0.0)),
                               math.sqrt(i.hi) if math.isfinite(i.hi) else INF),
    "exp": lambda i: Interval(math.exp(i.lo) if i.lo > -700 else 0.0,
                              math.exp(i.hi) if i.hi < 700 else INF),
}


def interval_of(expression, environment: Environment,
                depth: int = 0) -> Interval:
    """The range an expression can take, given every declared constraint.

    Conservative: anything it cannot reason about widens to unknown, which can
    only turn a would-be UNSAT into an UNKNOWN. It never manufactures a bound.
    """
    if depth > 16:
        return Interval.unknown()

    if isinstance(expression, Literal):
        if expression.kind in ("real", "integer"):
            return Interval.point(float(expression.value))
        return Interval.unknown()

    if isinstance(expression, VariableRef):
        # `kind` is the *coordinate* kind — "parameter", "algebraic", "state" —
        # not a "value"/"derivative" tag. Testing it against "value" rejected
        # every plain reference, so every interval widened to unknown and no
        # UNSAT proof was ever found.
        if expression.is_derivative or expression.is_previous:
            return Interval.unknown()
        variable = expression.variable
        domain = environment.domain(variable.id)
        declared = Interval(domain.low, domain.high)
        # `assert(abs(v) >= c)` forbids an interval around zero, which a single
        # range cannot express. Narrow to the side the domain already allows;
        # where both sides remain, keep the wider range and let the magnitude
        # floor be applied by the zero test instead.
        if domain.min_magnitude > 0.0:
            if declared.lo >= 0.0:
                declared = Interval(max(declared.lo, domain.min_magnitude),
                                    declared.hi)
            elif declared.hi <= 0.0:
                declared = Interval(declared.lo,
                                    min(declared.hi, -domain.min_magnitude))
        if not domain.settable:
            value = environment.values.get(variable.id)
            if value is not None:
                return Interval.point(value)
            binding = environment.bindings.get(variable.id)
            if binding is not None:
                return interval_of(binding, environment, depth + 1)
        return declared

    if isinstance(expression, BinaryOp):
        left = interval_of(expression.lhs, environment, depth + 1)
        right = interval_of(expression.rhs, environment, depth + 1)
        if expression.op == ops.ADD:
            return left + right
        if expression.op == ops.SUBTRACT:
            return left - right
        if expression.op == ops.MULTIPLY:
            return left * right
        if expression.op == ops.DIVIDE:
            return left / right
        if expression.op == ops.POWER and right.is_point:
            return left.power(right.lo)
        return Interval.unknown()

    node = type(expression).__name__
    if node == "UnaryOp":
        inner = interval_of(expression.operand, environment, depth + 1)
        return -inner if expression.op == "negate" else inner

    if node == "BuiltinCall":
        return _builtin_interval(expression, environment, depth)

    return Interval.unknown()


def _builtin_interval(expression, environment: Environment,
                      depth: int) -> Interval:
    """The range of a built-in call.

    `max` and `min` are the ones that matter. MSL holds a denominator away from
    zero by writing `max(eps*oneOhm, abs(R))`, and an analysis that cannot see
    a lower bound through `max` reports that guard as the hazard it prevents.
    """
    arguments = [interval_of(a, environment, depth + 1)
                 for a in expression.arguments]
    if not arguments:
        return Interval.unknown()

    if expression.name == "max":
        return Interval(max(a.lo for a in arguments),
                        max(a.hi for a in arguments))
    if expression.name == "min":
        return Interval(min(a.lo for a in arguments),
                        min(a.hi for a in arguments))
    if len(arguments) == 1 and expression.name in _UNARY_RANGE:
        try:
            return _UNARY_RANGE[expression.name](arguments[0])
        except (ValueError, OverflowError):
            return Interval.unknown()
    return Interval.unknown()


# ── path feasibility ─────────────────────────────────────────────────────────

def path_status(site, assignment: dict, environment: Environment) -> tuple[str, str]:
    """Whether the division still executes under `assignment`.

    Returns (SAT | UNSAT | UNKNOWN, explanation). UNKNOWN is returned when a
    guard mentions something the artifact does not determine --- a discrete
    variable a `when` clause assigns, most often --- because a guard we cannot
    read must not be assumed either way.
    """
    from .sites import _atoms, _truth, _infeasible

    if not site.branch_conditions:
        return "SAT", "the division is not inside any branch"

    empty = _infeasible(site.branch_conditions, environment, assignment)
    if empty is not None:
        return "UNSAT", f"the path conditions cannot hold together: {empty}"

    undecided = []
    for condition, taken in site.branch_conditions:
        for atom, polarity in _atoms(condition, taken):
            decided = _truth(atom, environment, assignment)
            if decided is None:
                undecided.append(repr(atom)[:90])
            elif decided is not polarity:
                return "UNSAT", (f"the guard {'' if polarity else 'not '}"
                                 f"({repr(atom)[:90]}) is false under the witness")
    if undecided:
        return "UNKNOWN", ("the path depends on quantities the artifact does not "
                           "determine: " + "; ".join(sorted(set(undecided))[:3]))
    return "SAT", "every guard still holds under the witness"


# ── the decision ─────────────────────────────────────────────────────────────

def classify(site, environment: Environment) -> Verdict:
    """Decide `constraints AND path AND denominator == 0` for one division."""
    denominator = site.denominator

    # 1. The model's own assertion. Strongest and cheapest.
    if shape_key(denominator) in environment.guarded_shapes:
        return Verdict("UNSAT", proof=(
            "the model asserts this denominator is bounded away from zero, so "
            "zero is outside its declared domain"))

    # 2. Interval propagation. Proves the `max(eps, abs(R))` family outright.
    span = interval_of(denominator, environment)
    rendered = f"[{span.lo:g}, {span.hi:g}]"
    if not span.is_empty and not span.contains(0.0):
        return Verdict("UNSAT", proof=(
            f"every value the declarations permit puts the denominator in "
            f"{rendered}, which excludes zero"), denominator_range=rendered)

    # 3. Search for a satisfying assignment.
    witness = find(denominator, environment)
    if witness is None:
        return Verdict("UNKNOWN", proof=(
            "no assignment this search can express drives the denominator to "
            "zero, and interval propagation could not prove that none exists"),
            denominator_range=rendered)

    # 4. The path must still be taken under that assignment.
    status, why = path_status(site, witness.assignment, environment)
    if status == "UNSAT":
        return Verdict("UNSAT", witness=witness, proof=why,
                       denominator_range=rendered)
    if status == "UNKNOWN":
        return Verdict("UNKNOWN", witness=witness, proof=why,
                       denominator_range=rendered)
    return Verdict("SAT", witness=witness, proof=why, denominator_range=rendered)
