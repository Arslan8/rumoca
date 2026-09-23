"""Comparing the balance a component implements against the one it owes.

Both sides are coefficient maps, so the comparison is exact and the diagnostic
falls out of it: a key present in the contract and absent from the equation is
a **missing term**; a key whose coefficients differ is a **mis-scaled term**.

Scale-invariant, because `a + b - der(m) = 0` and `2a + 2b - 2der(m) = 0` are
the same balance. Comparing raw coefficients would report the second as three
violations.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from .contract import Contract, Verdict
from .residual import Coefficients, Normalised

#: Coefficients are small integers scaled by a common factor; this tolerance
#: only absorbs float division like `1/3 + 1/3 + 1/3`.
TOLERANCE = 1e-9


@dataclass
class Comparison:
    verdict: Verdict
    missing: list[str] = field(default_factory=list)
    extra: list[str] = field(default_factory=list)
    mis_scaled: list[tuple[str, float, float]] = field(default_factory=list)
    reason: str = ""
    observed: str = ""
    expected: str = ""


def _normalise_scale(coefficients: Coefficients) -> Coefficients:
    """Divide through by the first coefficient so scale does not matter."""
    if not coefficients:
        return {}
    pivot = coefficients[sorted(coefficients)[0]]
    if pivot == 0:
        return dict(coefficients)
    return {k: v / pivot for k, v in coefficients.items()}


def compare(contract: Contract, observed: Normalised,
            names: dict[int, str]) -> Comparison:
    """Does the equation implement the contract?"""
    if not observed.ok:
        return Comparison(Verdict.UNKNOWN,
                          reason=f"the equation is not linear: {observed.reason}")
    expected = {k: float(v) for k, v in contract.expected.items()}
    if not expected:
        return Comparison(Verdict.UNKNOWN, reason="the contract states no terms")

    # Align scale on a key both sides share; without one they are not
    # comparable and saying so beats inventing a correspondence.
    shared = set(expected) & set(observed.coefficients)
    if not shared:
        return Comparison(
            Verdict.UNKNOWN,
            reason="the equation and the contract share no term",
            observed=observed.render(names))
    pivot = sorted(shared)[0]
    scale = expected[pivot] / observed.coefficients[pivot]
    scaled = {k: v * scale for k, v in observed.coefficients.items()}

    def label(key) -> str:
        variable, derivative = key
        name = names.get(variable, f"<{variable}>")
        return f"der({name})" if derivative else name

    missing = [label(k) for k in expected if k not in scaled]
    extra = [label(k) for k in scaled if k not in expected]
    mis_scaled = [
        (label(k), expected[k], scaled[k])
        for k in set(expected) & set(scaled)
        if abs(expected[k] - scaled[k]) > TOLERANCE
    ]

    rendered_expected = " ".join(
        f"{'+' if v > 0 else '-'} {label(k)}" for k, v in sorted(expected.items())
    ).lstrip("+ ") + " = 0"

    if not missing and not extra and not mis_scaled:
        return Comparison(Verdict.PROVEN_CONSERVED,
                          observed=observed.render(names),
                          expected=rendered_expected)

    # An excluded term's absence is documented, not a defect.
    missing = [m for m in missing
               if not any(x in m for x in contract.excluded)]
    if not missing and not extra and not mis_scaled:
        return Comparison(Verdict.PROVEN_CONSERVED,
                          reason="the only absent terms are explicitly excluded",
                          observed=observed.render(names),
                          expected=rendered_expected)

    return Comparison(Verdict.PROVEN_VIOLATION, missing=missing, extra=extra,
                      mis_scaled=mis_scaled,
                      observed=observed.render(names),
                      expected=rendered_expected)
