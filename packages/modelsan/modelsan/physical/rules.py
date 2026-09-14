"""The interface a domain rule pack implements.

Everything domain-specific lives behind this. The engine imports no domain
module and contains no `if electrical:` — it iterates whatever packs are
registered and asks each the same three questions: which variables do you match,
what predicate do you assert, and where did that claim come from.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Protocol, runtime_checkable

from .invariant import (
    Comparison,
    Domain,
    Enforcement,
    Predicate,
    RuleProvenance,
    Term,
)
from .matching import Confidence, Match, match_variable


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

    def applies(self, variable) -> Match | None:
        if self.parameters_only and not getattr(variable, "is_parameter", False):
            return None
        found = match_variable(variable, self.quantities, self.units)
        return found if found.confidence >= self.minimum_confidence else None

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

    def applies(self, variable) -> Match | None: ...
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
