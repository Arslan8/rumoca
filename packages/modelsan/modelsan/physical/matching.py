"""Deciding that a physical rule applies to a model variable.

This is the hard part, and the part most easily got wrong. A checker that reads
`m` as mass and `R` as resistance will be confidently wrong on any model whose
author chose different names — and Modelica authors do.

Evidence is therefore ranked, and every match records what supported it:

    1. declared quantity   MLS §4.8 `quantity="Mass"`. Semantic and authored.
    2. connector role      potential/flow on a typed connector.
    3. unit                corroboration only, never sufficient on its own.

Unit alone is explicitly not enough. `Ohm` does not imply a value must be
positive — a negative-impedance converter is a real device, and MSL's Spice3
uses `-1e40` as an "unset" sentinel on a resistance. What makes `R > 0` right is
that the *component* is passive, which the quantity plus the component's
identity expresses and the unit does not.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import IntEnum


class Confidence(IntEnum):
    """How well-founded a match is. Rules declare the minimum they accept."""

    NONE = 0
    UNIT_ONLY = 1
    """A unit matched and nothing else. Too weak to act on alone."""
    QUANTITY = 2
    """The declared `quantity` attribute matched — the author said so."""
    QUANTITY_AND_UNIT = 3
    """Both agree. The strongest signal available from bitcode today."""


@dataclass(frozen=True)
class Match:
    """Why a rule was considered applicable to a variable."""

    confidence: Confidence
    quantity: str | None = None
    unit: str | None = None
    connector_role: str | None = None

    @property
    def evidence(self) -> dict:
        return {k: v for k, v in
                {"quantity": self.quantity, "unit": self.unit,
                 "connector_role": self.connector_role,
                 "confidence": self.confidence.name}.items() if v is not None}


def match_variable(variable, quantities: frozenset[str],
                   units: frozenset[str]) -> Match:
    """Evidence that `variable` measures one of `quantities`.

    `units` corroborates but never decides: a unit match with no quantity match
    yields UNIT_ONLY, which the default rule threshold rejects.
    """
    declared = getattr(variable, "physical_quantity", None)
    unit = getattr(variable, "unit", None)
    role = getattr(variable, "quantity", None)  # connector role, if any

    quantity_hit = bool(declared and declared in quantities)
    unit_hit = bool(unit and units and unit in units)

    if quantity_hit and unit_hit:
        confidence = Confidence.QUANTITY_AND_UNIT
    elif quantity_hit:
        confidence = Confidence.QUANTITY
    elif unit_hit:
        confidence = Confidence.UNIT_ONLY
    else:
        confidence = Confidence.NONE

    return Match(confidence=confidence, quantity=declared, unit=unit,
                 connector_role=role)
