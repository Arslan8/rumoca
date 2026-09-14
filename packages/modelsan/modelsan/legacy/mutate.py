"""Model-aware parameter-space exploration.

Random floating-point values are a poor way to break a physical model. The
values that break them are the ones sitting exactly on a boundary: zero, the
declared `min`, one epsilon past `max`, or a value that makes two previously
independent parameters equal.

So the generator is ordered by how likely a value is to expose something, and a
search stops at the first failure it finds.
"""

from __future__ import annotations

import math
from dataclasses import dataclass

EPSILON = 1e-12
"""Small enough to sit on a boundary, large enough to survive double rounding."""


@dataclass(frozen=True)
class Candidate:
    """One parameter configuration to try."""

    assignment: dict[str, float]
    rationale: str

    def as_args(self) -> list[str]:
        return [f"--param={name}={value!r}" for name, value in self.assignment.items()]

    def __str__(self) -> str:
        body = ", ".join(f"{name} = {value:g}" for name, value in self.assignment.items())
        return f"{body}   [{self.rationale}]"


def boundary_values(parameter) -> list[tuple[float, str]]:
    """Values worth trying for one parameter, most suspicious first.

    Declared `min`/`max` are used when they are literal. A bound that is itself
    an expression is skipped rather than guessed at, because evaluating it here
    would duplicate the compiler's evaluator less correctly.
    """
    values: list[tuple[float, str]] = []

    def literal(expression):
        """A numeric literal, or nothing.

        A parameter may be a String or an enumeration, and a bound may be an
        expression rather than a literal. Neither is something to coerce: a
        non-numeric value has no boundary to sit on.
        """
        if expression is None:
            return None
        value = getattr(expression, "value", None)
        if isinstance(value, bool) or not isinstance(value, (int, float)):
            return None
        return float(value)

    minimum = literal(parameter.minimum)
    maximum = literal(parameter.maximum)
    default = literal(parameter.binding)

    # Zero first: it is the single most common trigger, because it is the
    # denominator value, the singular stiffness and the empty area all at once.
    values.append((0.0, "zero"))
    values.append((-1.0, "negative"))
    values.append((EPSILON, "epsilon above zero"))
    values.append((-EPSILON, "epsilon below zero"))

    if minimum is not None:
        values.append((float(minimum), "declared min"))
        values.append((float(minimum) - EPSILON, "epsilon below declared min"))
    if maximum is not None:
        values.append((float(maximum), "declared max"))
        values.append((float(maximum) + EPSILON, "epsilon above declared max"))
    if default is not None:
        values.append((-float(default), "negated default"))

    # Drop values the declaration forbids. A user cannot legally set a
    # parameter outside its own `min`/`max`, so a "failure" there is not a
    # finding — it is ModelSan breaking a rule the model already stated.
    # The `min - epsilon` / `max + epsilon` probes are the deliberate exception:
    # they test whether the bound is actually enforced.
    def permitted(value: float, why: str) -> bool:
        if "declared" in why:
            return True
        if minimum is not None and value < float(minimum):
            return False
        if maximum is not None and value > float(maximum):
            return False
        return True

    # Deduplicate while preserving order, so the most suspicious value wins its
    # rationale.
    seen: set[float] = set()
    unique = []
    for value, why in values:
        key = round(value, 15)
        if key in seen or not math.isfinite(value) or not permitted(value, why):
            continue
        seen.add(key)
        unique.append((value, why))
    return unique


def single_parameter_candidates(parameters) -> list[Candidate]:
    """Vary one parameter at a time."""
    candidates = []
    for parameter in parameters:
        for value, why in boundary_values(parameter):
            candidates.append(Candidate({parameter.name: value}, f"{parameter.name} = {why}"))
    return candidates


def equality_candidates(parameters) -> list[Candidate]:
    """Make pairs of parameters equal.

    Singularities cluster here: a system that is solvable while `a != b` often
    loses rank exactly when they coincide, and no single-parameter sweep finds
    that.
    """
    candidates = []
    for i, first in enumerate(parameters):
        for second in parameters[i + 1 :]:
            for value, why in ((1.0, "both = 1"), (0.0, "both = 0")):
                candidates.append(
                    Candidate(
                        {first.name: value, second.name: value},
                        f"{first.name} == {second.name} ({why})",
                    )
                )
    return candidates


def candidates(parameters, *, include_equalities: bool = True) -> list[Candidate]:
    """The full ordered search space.

    Single-parameter boundaries come first because they are cheaper to explain:
    a report naming one parameter is easier to act on than one naming two.
    """
    out = single_parameter_candidates(parameters)
    if include_equalities:
        out.extend(equality_candidates(parameters))
    return out


def minimize(assignment: dict[str, float], still_fails) -> dict[str, float]:
    """Shrink a failing configuration to the smallest one that still fails.

    Drops one override at a time and keeps the drop if the failure survives.
    A report naming one parameter is worth far more than one naming six, and
    this is the difference between them.
    """
    minimal = dict(assignment)
    for name in list(minimal):
        trial = {key: value for key, value in minimal.items() if key != name}
        if trial and still_fails(trial):
            minimal = trial
    return minimal
