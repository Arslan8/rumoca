"""User-supplied zero contracts, read from the existing semantics file.

An extension of `semantics.config`, not a second configuration system: a user
who already has a semantics file should add a table to it, not learn another
format and another search path.

    [[contracts]]
    match = "declaration"
    target = "Modelica.Electrical.Analog.Basic.Inductor.L"
    zero_behavior = "algebraic_limit"
    sign_domain = "nonnegative"
    reason = "Zero produces the ideal-short algebraic constraint v = 0"

    [[contracts]]
    match = "instance"
    target = "plant.optionalLoss.G"
    zero_behavior = "feature_disabled"
    reason = "Zero disables this optional loss model"

An entry may instead name an *aggregate* — a group of declarations whose
constraint is a property of the group — or a *role*, which selects which sign
rule applies to a component rather than stating anything about zero:

    [[contracts]]
    match = "declaration"
    target = "MyLibrary.Body.I"
    aggregate = "symmetric_inertia_tensor"
    domain = "positive_semidefinite"
    reason = "Rigid-body inertia tensor about the center of mass"

    [[contracts]]
    match = "declaration"
    target = "MyLibrary.Motor.Rs"
    role = "machine_winding_resistance"
    sign_domain = "nonnegative"
    reason = "Copper resistance; zero permits an ideal lossless winding"

`zero_behavior` is required only of an entry that makes no other statement: an
entry carrying `aggregate`, `role` or `sign_domain` is about something else,
and demanding a zero behaviour it does not have would force the author to
invent one.

An assumption is an *input* to the analysis and is labelled `ASSUMED`
everywhere it is used. It may override a catalog entry or a heuristic. It may
never override a proven active source division: asserting that a parameter is
safe does not stop the source dividing by it.
"""

from __future__ import annotations

import fnmatch
import tomllib
from dataclasses import dataclass, field
from pathlib import Path

from .behavior import Confidence, Source, ZeroBehavior, ZeroContract

_BEHAVIORS = {b.value: b for b in ZeroBehavior}

#: Aggregates a contract may name, and the domain each accepts. Refused when
#: unknown, for the same reason a misspelt `zero_behavior` is: an entry that
#: silently does nothing is worse than one that fails loudly.
_AGGREGATES = {"symmetric_inertia_tensor": frozenset({"positive_semidefinite"})}

#: Sign domains, and the comparison each implies.
_SIGN_DOMAINS = {"positive": ">", "nonnegative": ">=", "signed": "any",
                 "negative": "<", "nonpositive": "<="}

#: Roles a contract may assign, mapped to the semantic role that carries them.
_ROLES = {
    "passive_resistance": "component.passive.resistance",
    "passive_conductance": "component.passive.conductance",
    "machine_winding_resistance": "component.machine.winding_resistance",
    "machine_winding_conductance": "component.machine.winding_conductance",
    "active_resistance": "component.active.resistance",
    "active_conductance": "component.active.conductance",
    "unrestricted_resistance": "component.unrestricted.resistance",
    "unrestricted_conductance": "component.unrestricted.conductance",
}


@dataclass
class Assumption:
    """One `[[contracts]]` entry."""

    match: str
    """declaration | instance"""
    target: str
    zero_behavior: ZeroBehavior | None
    reason: str
    sign_domain: str = ""
    aggregate: str = ""
    """The group rule this declaration belongs to, if any."""

    domain: str = ""
    """The constraint that group must satisfy."""

    role: str = ""
    """The semantic role this declaration carries, as a role name."""

    origin: str = "<inline>"
    used: bool = field(default=False, compare=False)

    @property
    def confidence(self) -> str:
        return Confidence.ASSUMED.value

    @property
    def source(self) -> str:
        return Source.USER_CONFIG.value

    def explain(self) -> str:
        """One line a suppression or an aggregate finding can quote."""
        what = self.aggregate or self.role or (
            self.zero_behavior.value if self.zero_behavior else "contract")
        return (f"{self.target}: {what} (assumed, from user_config) "
                f"\u2014 {self.reason}")

    @property
    def is_pattern(self) -> bool:
        return any(c in self.target for c in "*?[")

    def matches(self, declaration: str, instance: str) -> str | None:
        """The match kind, or None."""
        candidate = declaration if self.match == "declaration" else instance
        if not candidate:
            return None
        if self.target == candidate:
            return f"exact-{self.match}"
        if self.is_pattern and fnmatch.fnmatch(candidate, self.target):
            return "prefix"
        return None

    def contract(self, declaration: str, instance: str,
                 match_kind: str) -> ZeroContract:
        return ZeroContract(
            behavior=self.zero_behavior, confidence=Confidence.ASSUMED,
            source=Source.USER_CONFIG, reason=self.reason,
            canonical_declaration=declaration, target=instance,
            origin=f"{self.origin}: {self.match} = {self.target!r}",
            match_kind=match_kind)


@dataclass
class AssumptionSet:
    """Every user contract, and which of them were used."""

    assumptions: list[Assumption] = field(default_factory=list)
    origin: str = "<none>"

    @classmethod
    def load(cls, path: str | Path) -> "AssumptionSet":
        location = Path(path)
        return cls.from_dict(tomllib.loads(location.read_text()),
                             origin=str(location))

    @classmethod
    def from_dict(cls, data: dict, origin: str = "<inline>") -> "AssumptionSet":
        found = []
        for entry in data.get("contracts") or []:
            aggregate = str(entry.get("aggregate", "")).lower()
            domain = str(entry.get("domain", "")).lower()
            role = str(entry.get("role", "")).lower()
            sign_domain = str(entry.get("sign_domain", "")).lower()

            if aggregate and aggregate not in _AGGREGATES:
                raise ValueError(
                    f"{origin}: unknown aggregate {entry.get('aggregate')!r}; "
                    f"expected one of {sorted(_AGGREGATES)}")
            if aggregate and domain and domain not in _AGGREGATES[aggregate]:
                raise ValueError(
                    f"{origin}: aggregate {aggregate!r} does not take domain "
                    f"{entry.get('domain')!r}; expected one of "
                    f"{sorted(_AGGREGATES[aggregate])}")
            if role and role not in _ROLES:
                raise ValueError(
                    f"{origin}: unknown role {entry.get('role')!r}; expected "
                    f"one of {sorted(_ROLES)}")
            if sign_domain and sign_domain not in _SIGN_DOMAINS:
                raise ValueError(
                    f"{origin}: unknown sign_domain "
                    f"{entry.get('sign_domain')!r}; expected one of "
                    f"{sorted(_SIGN_DOMAINS)}")

            stated = "zero_behavior" in entry
            behavior = _BEHAVIORS.get(str(entry.get("zero_behavior", "")).lower())
            if behavior is None and (stated
                                     or not (aggregate or role or sign_domain)):
                # A typo here silently disables the rule, so it is refused. An
                # entry that states an aggregate, a role or a sign domain
                # instead is making a different claim and needs no zero
                # behaviour: `sign_domain = "signed"` is about every value, not
                # about zero, and forcing an author to name one would make them
                # invent a statement they did not want to make.
                raise ValueError(
                    f"{origin}: unknown zero_behavior "
                    f"{entry.get('zero_behavior')!r}; expected one of "
                    f"{sorted(_BEHAVIORS)}")
            match = str(entry.get("match", "declaration")).lower()
            if match not in ("declaration", "instance"):
                raise ValueError(
                    f"{origin}: match must be 'declaration' or 'instance', "
                    f"got {match!r}")
            found.append(Assumption(
                match=match, target=str(entry.get("target", "")),
                zero_behavior=behavior,
                reason=str(entry.get("reason", "")) or "no reason given",
                sign_domain=sign_domain, aggregate=aggregate, domain=domain,
                role=_ROLES.get(role, ""), origin=origin))
        return cls(assumptions=found, origin=origin)

    def lookup(self, declaration: str, instance: str) -> ZeroContract | None:
        """The most specific assumption matching, or None.

        Exact beats pattern, and a later entry beats an earlier one at the same
        specificity, so a file can narrow a broad rule by adding a narrow one.
        """
        best: tuple[int, Assumption, str] | None = None
        for assumption in self.assumptions:
            if assumption.zero_behavior is None:
                continue        # an aggregate or role entry says nothing here
            kind = assumption.matches(declaration, instance)
            if kind is None:
                continue
            rank = 1 if kind == "prefix" else 2
            if best is None or rank >= best[0]:
                best = (rank, assumption, kind)
        if best is None:
            return None
        _, assumption, kind = best
        assumption.used = True
        return assumption.contract(declaration, instance, kind)

    @property
    def aggregates(self) -> list[Assumption]:
        """Entries that name a group rule rather than a zero behaviour."""
        return [a for a in self.assumptions if a.aggregate]

    @property
    def roles(self) -> dict[str, Assumption]:
        """Declaration -> the role the user assigned it."""
        return {a.target: a for a in self.assumptions if a.role}

    @property
    def unused(self) -> list[Assumption]:
        """Assumptions that matched nothing. A typo is silent otherwise."""
        return [a for a in self.assumptions if not a.used]

    def __bool__(self) -> bool:
        return bool(self.assumptions)
