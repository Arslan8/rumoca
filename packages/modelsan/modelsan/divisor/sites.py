"""Where a division is, what protects it, and whether the source wrote it.

Three questions decide whether a division site is worth reporting at all,
before any witness is sought:

**Did the source write it?** `L*der(i) = v` contains no division. The canonical
DAE may still contain `der(i) = v/L`, because solving for the derivative is
what a solver needs --- but a division the compiler introduced is not evidence
that the source contract is wrong, and reporting it as one blames the modeller
for the translation. The artifact records this directly: every object carries
whether it is `source` or `generated`, and generated objects carry the lowering
that produced them.

**Is it guarded?** A division under `if x > 0 then a/x else b` cannot divide by
zero, and one preceded by `assert(d >= eps)` is protected by the model's own
statement. Both are recorded, not silently dropped: a reader wants to know that
a guard was found, and a guard that turns out to be insufficient is itself
interesting.

**Under what path?** A division inside a branch executes only when that branch
is taken. `Ramp` divides by `duration`, and at `duration = 0` the model takes
the step branch instead --- so the witness that zeroes the denominator also
makes the division unreachable.
"""

from __future__ import annotations

import math
from dataclasses import dataclass, field

from ..dae import BinaryOp, Conditional, ops
from .constraints import Environment, shape_key


@dataclass(frozen=True)
class Site:
    """One division, with everything known about its context."""

    division: object
    numerator: object
    denominator: object
    owner: object

    generated: bool
    """True when the compiler introduced this division rather than the source."""

    generation: str | None
    """The lowering that produced it, when generated."""

    guards: tuple[str, ...] = ()
    """Branch conditions that must hold for this division to be evaluated."""

    branch_conditions: tuple[tuple[object, bool], ...] = ()
    """Each enclosing condition and whether this division is on its true side."""

    asserted: bool = False
    """The model asserts this denominator is bounded away from zero."""

    @property
    def span(self):
        return self.division.provenance.span


def _conditional_paths(node, condition_stack):
    """Yield (subexpression, path conditions) over a conditional tree."""
    if isinstance(node, Conditional):
        for condition, value in node.branches:
            yield from _conditional_paths(condition, condition_stack)
            yield from _conditional_paths(
                value, condition_stack + [(condition, True)])
        yield from _conditional_paths(
            node.fallback,
            condition_stack + [(c, False) for c, _ in node.branches])
        return
    yield node, condition_stack
    for child in node.children():
        yield from _conditional_paths(child, condition_stack)


def collect(model, environment: Environment) -> list[Site]:
    """Every division in the model, with its context."""
    from ..dae.traversal import root_expressions

    # Roots only. Walking every node would visit a nested `if` a second time as
    # a root of its own, and the division inside it would then be recorded with
    # only part of its path condition — which is how a guarded division came to
    # be reported as unguarded.
    seen: set[int] = set()
    sites: list[Site] = []
    for owner, root in root_expressions(model):
        for node, stack in _conditional_paths(root, []):
            if not (isinstance(node, BinaryOp) and node.op == ops.DIVIDE):
                continue
            if node.id in seen:
                continue
            seen.add(node.id)
            sites.append(_site(node, owner, stack, environment))
    return sites


def _site(division, owner, stack, environment: Environment) -> Site:
    provenance = division.provenance
    guards = tuple(
        f"{'' if taken else 'not '}({condition!r})" for condition, taken in stack)
    return Site(
        division=division,
        numerator=division.lhs,
        denominator=division.rhs,
        owner=owner,
        generated=provenance.is_generated,
        generation=provenance.generation,
        guards=guards,
        branch_conditions=tuple(stack),
        asserted=shape_key(division.rhs) in environment.guarded_shapes,
    )


def guard_excludes(site: Site, assignment: dict[int, float],
                   environment: Environment) -> str | None:
    """Whether the witness makes this division unreachable.

    Two ways a path can be closed, and both occur in MSL:

    *The guard decides numerically.* Every quantity in it has a value under the
    witness, and the branch is simply not taken.

    *The guard becomes contradictory.* `Ramp` divides by `duration` inside
    ``time < startTime + duration``, nested in the ``else`` of
    ``time < startTime``. At `duration = 0` the path requires
    ``time >= startTime`` and ``time < startTime`` at once. Nothing evaluates,
    because `time` is free — but the interval it would have to lie in is
    empty, and the division is unreachable for that reason.

    Returns the guard responsible, or None. An undecidable guard returns None:
    a guard we cannot read must not silently suppress a finding.
    """
    for condition, taken in site.branch_conditions:
        decided = _truth(condition, environment, assignment)
        if decided is not None and decided is not taken:
            return f"{'' if taken else 'not '}({condition!r})"

    empty = _infeasible(site.branch_conditions, environment, assignment)
    if empty is not None:
        return empty
    return None


def _infeasible(branch_conditions, environment: Environment,
                assignment: dict[int, float]) -> str | None:
    """Whether the path conditions leave no room for a free quantity.

    Only the shape that occurs: relations comparing one free symbol against an
    expression the witness makes numeric. Accumulating those gives an interval
    per symbol, and an empty interval means the path is closed.
    """
    bounds: dict[str, list] = {}
    for condition, taken in branch_conditions:
        for atom, polarity in _atoms(condition, taken):
            constraint = _one_sided(atom, polarity, environment, assignment)
            if constraint is None:
                continue
            symbol, low, high = constraint
            entry = bounds.setdefault(symbol, [-math.inf, math.inf, None, None])
            if low is not None and low[0] >= entry[0]:
                entry[0], entry[2] = low[0], low[1]
            if high is not None and high[0] <= entry[1]:
                entry[1], entry[3] = high[0], high[1]

    for symbol, (low, high, low_strict, high_strict) in bounds.items():
        if low > high:
            return f"{symbol} must be both >= {low:g} and <= {high:g}"
        if low == high and (low_strict or high_strict):
            return f"{symbol} must be both > {low:g} and < {high:g}"
    return None


def _atoms(condition, taken: bool):
    """Break a path condition into the atomic relations it definitely implies.

    De Morgan, and only in the direction that is sound. Taking the true side of
    `A and B` implies both; taking the *false* side of `A or B` implies neither
    holds, so it implies both negations. The other two combinations imply a
    disjunction, which constrains nothing definite and is dropped.

    Without this, a guard written as `if A or B or C then 0 else ...` --- which
    is how `Trapezoid` writes its "before the signal starts" case --- yields no
    bound at all, and the branch containing the division cannot be shown
    unreachable.
    """
    node = condition
    while type(node).__name__ == "UnaryOp" and node.op == "not":
        node, taken = node.operand, not taken

    op = getattr(node, "op", None)
    if op == "and" and taken:
        yield from _atoms(node.lhs, True)
        yield from _atoms(node.rhs, True)
        return
    if op == "or" and not taken:
        yield from _atoms(node.lhs, False)
        yield from _atoms(node.rhs, False)
        return
    if op in ("and", "or"):
        return          # a disjunction: nothing definite follows
    yield node, taken


def _one_sided(condition, taken: bool, environment: Environment,
               assignment: dict[int, float]):
    """`(symbol, (low, strict) | None, (high, strict) | None)` for one guard."""
    from .witness import Unevaluable, evaluate

    if not isinstance(condition, BinaryOp) or condition.op not in ops.RELATIONS:
        return None
    op = condition.op
    if not taken:
        op = {"less": "greater_equal", "less_equal": "greater",
              "greater": "less_equal", "greater_equal": "less",
              "equal": "not_equal", "not_equal": "equal"}.get(op)
        if op is None:
            return None

    for free, other, flip in ((condition.lhs, condition.rhs, False),
                              (condition.rhs, condition.lhs, True)):
        symbol = _free_symbol(free, environment, assignment)
        if symbol is None:
            continue
        try:
            limit = evaluate(other, environment, assignment)
        except Unevaluable:
            continue
        comparison = op if not flip else {
            "less": "greater", "less_equal": "greater_equal",
            "greater": "less", "greater_equal": "less_equal"}.get(op, op)
        if comparison == "less":
            return symbol, None, (limit, True)
        if comparison == "less_equal":
            return symbol, None, (limit, False)
        if comparison == "greater":
            return symbol, (limit, True), None
        if comparison == "greater_equal":
            return symbol, (limit, False), None
    return None


def _free_symbol(expression, environment: Environment,
                 assignment: dict[int, float]) -> str | None:
    """A name for a quantity the witness does not fix, or None.

    `time` is the case that matters: it is not a variable, it has no value,
    and a path condition on it is exactly what closes the Ramp branch.
    """
    from .witness import Unevaluable, evaluate

    if type(expression).__name__ == "TimeRef":
        return "time"
    try:
        evaluate(expression, environment, assignment)
    except Unevaluable:
        variables = expression.variables()
        if len(variables) == 1 and repr(expression) == variables[0].name:
            return variables[0].name
        return None
    return None


def _truth(condition, environment: Environment,
           assignment: dict[int, float]) -> bool | None:
    from .witness import Unevaluable, evaluate

    if not isinstance(condition, BinaryOp):
        return None
    if condition.op not in ops.RELATIONS:
        return None
    try:
        left = evaluate(condition.lhs, environment, assignment)
        right = evaluate(condition.rhs, environment, assignment)
    except Unevaluable:
        return None
    return {
        "less": left < right, "less_equal": left <= right,
        "greater": left > right, "greater_equal": left >= right,
        "equal": left == right, "not_equal": left != right,
    }.get(condition.op)
