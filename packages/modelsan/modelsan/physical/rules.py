"""The interface a domain rule pack implements.

Everything domain-specific lives behind this. The engine imports no domain
module and contains no `if electrical:` — it iterates whatever packs are
registered and asks each the same three questions: which variables do you match,
what predicate do you assert, and where did that claim come from.
"""

from __future__ import annotations

from dataclasses import dataclass, field, replace
from typing import Protocol, runtime_checkable

from .invariant import (
    Comparison,
    Domain,
    Enforcement,
    Predicate,
    RuleProvenance,
    Term,
)
from .matching import Authority, Confidence, Match, Premise, match_variable


@dataclass(frozen=True)
class QuantityRule:
    """A bound on any variable measuring a given physical quantity.

    Covers the common case — `mass > 0`, `0 <= SOC <= 1` — without the pack
    author writing matching logic. A pack needing something structural (a
    relation between several variables, a conservation law) implements
    `Rule` directly instead.
    """

    rule_id: str
    domain: Domain
    quantities: frozenset[str]
    op: Comparison
    bound: float
    origin: str
    units: frozenset[str] = frozenset()
    reference: str = ""
    severity: str = "medium"
    enforcement: Enforcement = Enforcement.EITHER
    minimum_confidence: Confidence = Confidence.QUANTITY
    """Default rejects a unit-only match, which is the brief's requirement that
    `Ohm` alone must not imply positivity."""

    parameters_only: bool = False
    """Some bounds constrain a design choice, not a trajectory: a resistance is
    a parameter, whereas a temperature is state that must hold at all times."""

    requires_declared_bound: bool = False
    """Fire only where the declaration already carries a bound.

    For a rule whose quantity is shared between an absolute value and a
    difference — MSL gives both `quantity="ThermodynamicTemperature"` — the
    presence of the type's own `min` is the only discriminator available, and
    asserting the domain without it reports every difference in the library."""

    def applies(self, variable, semantics=None) -> Match | None:
        if self.parameters_only and not getattr(variable, "is_parameter", False):
            return None
        if self.requires_declared_bound and getattr(variable, "minimum", None) is None:
            return None
        found = match_variable(variable, self.quantities, self.units)
        if found.confidence < self.minimum_confidence:
            return None
        # A quantity rule has no notion of a component, so its premise is
        # always unknown --- but it can still say which declaration it is
        # asking about, and a report whose `declaration` reads "—" is one the
        # reader cannot act on.
        return replace(found, premise=Premise.UNKNOWN,
                       authority=Authority.QUANTITY_OR_UNIT,
                       canonical_declaration=_declaration_of(None, variable))

    def predicate(self, variable) -> Predicate:
        return Predicate(
            left=Term.variable(variable.id, variable.name),
            op=self.op,
            right=Term.constant(self.bound),
        )

    def provenance(self) -> RuleProvenance:
        return RuleProvenance(rule_id=self.rule_id, domain=self.domain,
                              origin=self.origin, reference=self.reference)


@dataclass(frozen=True)
class SemanticRule:
    """A bound that applies to whatever *means* a given thing.

    The difference from [`QuantityRule`] is what the rule is keyed on. A
    quantity rule says "anything measuring conductance is positive", which is
    false of Chua's diode. This says "anything that is a *passive* conductance
    is positive", and leaves the binder to decide which objects those are.

    `excluded_roles` is what keeps coverage from collapsing to the catalogued
    classes. The rule still fires on the declared quantity where nothing is
    known about the component — a negative resistance is anomalous by default —
    but stands down where something is known to the contrary. Making the
    *suppressing* claim the one that must be explicit is the conservative
    direction: the alternative silently stops checking every class nobody has
    got round to cataloguing.

    Severity follows the evidence rather than being fixed, so a reader can tell
    "this is a passive resistor and its resistance is negative" from "this is
    resistance-valued and negative, and I do not know what declared it".
    """

    rule_id: str
    domain: Domain
    quantities: frozenset[str]
    op: Comparison
    bound: float
    origin: str
    confirming_roles: frozenset[str] = frozenset()
    """Roles that make the rule's premise *established* rather than assumed."""

    excluded_roles: frozenset[str] = frozenset()
    """Roles under which the rule must not fire at all."""

    units: frozenset[str] = frozenset()
    reference: str = ""
    severity: str = "medium"
    confirmed_severity: str = "high"
    enforcement: Enforcement = Enforcement.EITHER
    minimum_confidence: Confidence = Confidence.QUANTITY
    parameters_only: bool = False

    def applies(self, variable, semantics=None) -> Match | None:
        if self.parameters_only and not getattr(variable, "is_parameter", False):
            return None

        bound_roles = (semantics.role_names(variable.id)
                       if semantics is not None else set())

        # A refuted premise is a *result*, not an absence. Returning `None` here
        # discarded the fact that a rule was considered and correctly declined,
        # which is exactly the record a reader needs to see that the analyzer
        # knew about the signed resistor rather than never having looked.
        refuting = bound_roles & self.excluded_roles
        if refuting:
            binding = next(
                (semantics.binding_for(variable.id, role)
                 for role in sorted(refuting)), None)
            return Match(
                confidence=Confidence.QUANTITY_AND_UNIT,
                quantity=getattr(variable, "physical_quantity", None),
                unit=getattr(variable, "unit", None),
                semantic_role=sorted(refuting)[0],
                binding_source=binding.source.name.lower() if binding else None,
                binding_evidence=dict(binding.evidence) if binding else {},
                premise=Premise.REFUTED,
                authority=_authority_of(binding),
                refuted_by=sorted(refuting)[0],
                canonical_declaration=_declaration_of(binding, variable),
            )

        confirming = bound_roles & self.confirming_roles
        if confirming:
            binding = next(
                (semantics.binding_for(variable.id, role) for role in sorted(confirming)),
                None)
            evidence = dict(binding.evidence) if binding else {}
            return Match(
                confidence=Confidence.QUANTITY_AND_UNIT,
                quantity=getattr(variable, "physical_quantity", None),
                unit=getattr(variable, "unit", None),
                semantic_role=sorted(confirming)[0],
                binding_source=binding.source.name.lower() if binding else None,
                binding_evidence=evidence,
                premise=Premise.ESTABLISHED,
                authority=_authority_of(binding),
                canonical_declaration=_declaration_of(binding, variable),
            )

        # No component evidence either way. The rule still matches --- dropping
        # it here would trade a false positive for a missed one --- but its
        # premise is unsettled, and the policy that reads `premise` turns it
        # into a question to the author rather than a claim about the model.
        found = match_variable(variable, self.quantities, self.units)
        if found.confidence < self.minimum_confidence:
            return None
        return replace(found, premise=Premise.UNKNOWN,
                       authority=Authority.QUANTITY_OR_UNIT,
                       canonical_declaration=_declaration_of(None, variable))

    def severity_for(self, match: Match) -> str:
        return self.confirmed_severity if match.semantic_role else self.severity

    def predicate(self, variable) -> Predicate:
        return Predicate(
            left=Term.variable(variable.id, variable.name),
            op=self.op,
            right=Term.constant(self.bound),
        )

    def provenance(self) -> RuleProvenance:
        return RuleProvenance(rule_id=self.rule_id, domain=self.domain,
                              origin=self.origin, reference=self.reference)


@runtime_checkable
class Rule(Protocol):
    """The general form, for rules that are not a simple bound."""

    rule_id: str
    domain: Domain

    def applies(self, variable, semantics=None) -> Match | None: ...
    def predicate(self, variable) -> Predicate: ...
    def provenance(self) -> RuleProvenance: ...


@dataclass
class RulePack:
    """One physical domain's rules, registered as a unit."""

    domain: Domain
    rules: list = field(default_factory=list)
    description: str = ""

    def __len__(self) -> int:
        return len(self.rules)


class RuleRegistry:
    """Registered packs. Adding a domain means registering one more."""

    def __init__(self) -> None:
        self._packs: dict[Domain, RulePack] = {}

    def register(self, pack: RulePack) -> None:
        existing = self._packs.get(pack.domain)
        if existing is None:
            self._packs[pack.domain] = pack
        else:
            existing.rules.extend(pack.rules)

    def packs(self, domains: set[Domain] | None = None) -> list[RulePack]:
        return [p for d, p in self._packs.items() if domains is None or d in domains]

    def rules(self, domains: set[Domain] | None = None) -> list:
        return [r for p in self.packs(domains) for r in p.rules]

    @property
    def domains(self) -> list[Domain]:
        return sorted(self._packs, key=lambda d: d.value)

    def __len__(self) -> int:
        return sum(len(p) for p in self._packs.values())


#: Which binder source corresponds to which authority. A user mapping outranks
#: a component catalogue because the user knows the application; the component
#: outranks the quantity because the quantity does not name a purpose.
_AUTHORITY_OF_SOURCE = {
    "user": Authority.USER_ASSUMPTION,
    "component_type": Authority.COMPONENT_CONTRACT,
    "connector": Authority.COMPONENT_CONTRACT,
    "quantity": Authority.QUANTITY_OR_UNIT,
    "unit": Authority.QUANTITY_OR_UNIT,
    "heuristic": Authority.NAME_HEURISTIC,
}


def _authority_of(binding) -> Authority:
    if binding is None:
        return Authority.QUANTITY_OR_UNIT
    name = getattr(getattr(binding, "source", None), "name", "") or ""
    return _AUTHORITY_OF_SOURCE.get(name.lower(), Authority.QUANTITY_OR_UNIT)


def _declaration_of(binding, variable) -> str:
    """`Class.member` for the declaration the premise belongs to.

    Taken from the binding's own evidence when it has one, because that is the
    *delegated* class where a wrapper delegates: a polyphase resistor's premise
    belongs to `Analog.Basic.Resistor.R`, and losing that is how the wrapper
    forgets it is an array of signed scalar resistors.
    """
    evidence = dict(getattr(binding, "evidence", None) or {})
    declared = evidence.get("declaration") or evidence.get("canonical_declaration")
    if declared:
        return str(declared)
    owner = evidence.get("declaring_class") or getattr(
        variable, "declaring_class", None)
    member = str(getattr(variable, "name", "")).rsplit(".", 1)[-1]
    return f"{owner}.{member}" if owner else member
