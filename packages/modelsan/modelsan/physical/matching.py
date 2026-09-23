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
from enum import Enum, IntEnum


class Premise(str, Enum):
    """Whether the rule's premise --- that this object *is* the component the
    rule is about --- was established, refuted, or never settled.

    An SI quantity says what kind of value something is. It does not say what
    the component is for: `SI.Resistance` describes a passive resistor, an
    active negative impedance, a linearised incremental model, an optimisation
    variable and a fault-injection input alike. The predicate `R > 0` and the
    authority for applying it *here* are two separate facts, and conflating
    them is what let a quantity match report a stock MSL example as a defect.

    The three states are carried through the invariant and into the published
    finding, not collapsed into a severity, so a later stage cannot turn an
    advisory back into an error.
    """

    ESTABLISHED = "established"
    """A component contract, a delegated one, or a user assumption applies."""

    REFUTED = "refuted"
    """An authoritative contract permits the value. Not a violation."""

    UNKNOWN = "unknown"
    """Only quantity, unit or a generic heuristic matched. Ask, do not assert."""


class Authority(IntEnum):
    """What supplied the premise. Higher cannot be contradicted by lower.

    The same ordering the binder uses, for the same reason: it ranks *who is
    entitled to say*, not how reliable the signal looked.
    """

    NONE = 0
    NAME_HEURISTIC = 1
    QUANTITY_OR_UNIT = 2
    COMPONENT_CONTRACT = 3
    USER_ASSUMPTION = 4
    SOURCE_BOUND = 5
    SOURCE_ARITHMETIC = 6
    """An active denominator that becomes zero. No physical assumption waives
    this one."""


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
    semantic_role: str | None = None
    """The bound role that established the premise, when one did. Its presence
    is the difference between "this measures a resistance" and "this *is* a
    passive resistance", which is the difference the whole binding layer
    exists to draw."""

    binding_source: str | None = None
    """Which authority supplied that role: user, component-type, connector."""

    binding_evidence: dict | None = None

    premise: Premise = Premise.UNKNOWN
    """Whether the rule's premise holds here. See [`Premise`]."""

    authority: Authority = Authority.QUANTITY_OR_UNIT
    """What established or refuted it."""

    refuted_by: str = ""
    """The role or contract that refuted the premise, when one did."""

    canonical_declaration: str = ""
    """`Class.member` for the declaration the premise belongs to --- the
    *scalar* one where a wrapper delegates, so a polyphase resistor does not
    forget that it is an array of signed scalar resistors."""

    @property
    def evidence(self) -> dict:
        found = {k: v for k, v in
                 {"quantity": self.quantity, "unit": self.unit,
                  "connector_role": self.connector_role,
                  "semantic_role": self.semantic_role,
                  "binding_source": self.binding_source,
                  "confidence": self.confidence.name}.items() if v is not None}
        found.update(self.binding_evidence or {})
        found["premise_state"] = self.premise.value
        found["authority"] = self.authority.name.lower()
        if self.refuted_by:
            found["refuted_by"] = self.refuted_by
        if self.canonical_declaration:
            found["canonical_declaration"] = self.canonical_declaration
        return found


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
