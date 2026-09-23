"""The Semantic Binder: run every source, resolve to one answer per object.

Resolution is by authority, not by vote. Two bindings for the same object and
the same *concept* are resolved in favour of the higher `BindingSource`; the
loser is recorded as a conflict when the two genuinely disagree, and dropped
silently when one merely refines the other.

Two things this must not do, both of which the brief calls out:

  - Guess when several objects could fill a role. It records an `Ambiguity`
    and binds nothing, because binding the first candidate makes a rule's
    answer depend on declaration order.
  - Silently accept a user mapping that contradicts the model. It applies the
    mapping — the user is the authority — and records a conflict so the
    disagreement stays visible.
"""

from __future__ import annotations

from .binding import (
    Ambiguity,
    BindingConflict,
    BindingSource,
    SemanticBinding,
)
from .catalog import ClassCatalog, builtin_catalog
from .map import SemanticMap
from .providers import (
    ComponentTypeProvider,
    ConnectorProvider,
    NameHeuristicProvider,
    QuantityProvider,
    SemanticProvider,
    UserDeclarationProvider,
    UserProvider,
)
from .role import SemanticRole, compatible

#: A user role in one of these namespaces is checked against what the model's
#: own metadata implies, so a mapping that contradicts the model is reported.
#: Application namespaces are not checked: nothing in the model can confirm or
#: deny that a given angular velocity is a *wheel's*.
_PHYSICAL = "physical"


class SemanticBinder:
    """Builds a [`SemanticMap`] from whatever providers are registered."""

    def __init__(self, providers: list[SemanticProvider] | None = None,
                 catalog: ClassCatalog | None = None,
                 user_mappings: dict[str, str] | None = None,
                 origin: str = "user",
                 heuristics: bool = False,
                 declaration_roles: dict[str, str] | None = None) -> None:
        if providers is not None:
            self.providers = list(providers)
            return
        catalog = catalog or builtin_catalog()
        self.providers = [QuantityProvider(), ConnectorProvider(),
                          ComponentTypeProvider(catalog)]
        if heuristics:
            # Off by default: `R`, `m`, `v` and `T` are exactly the names a
            # physical claim must not rest on.
            self.providers.append(NameHeuristicProvider())
        if user_mappings:
            self.providers.append(UserProvider(user_mappings, origin))
        if declaration_roles:
            self.providers.append(
                UserDeclarationProvider(declaration_roles, origin))

    # ── binding ──────────────────────────────────────────────────────────────

    def bind(self, model) -> SemanticMap:
        produced: list[SemanticBinding] = []
        for provider in self.providers:
            produced.extend(provider.bind(model))

        kept, conflicts = self._resolve(produced)
        ambiguities = self._ambiguities(kept)
        return SemanticMap(bindings=kept, conflicts=conflicts,
                           ambiguities=ambiguities,
                           unmatched_patterns=self._unmatched(produced))

    # ── resolution ───────────────────────────────────────────────────────────

    @staticmethod
    def _concept(role: SemanticRole) -> str:
        """The thing two bindings would have to share to be in competition.

        A namespace: `physical.mass` and `physical.velocity` on one object are
        not a conflict — a variable can be several things at different levels
        of description — whereas two different `physical.*` roles are.
        """
        return role.namespace

    def _resolve(self, produced: list[SemanticBinding]):
        best: dict[tuple[int, str], SemanticBinding] = {}
        extra: list[SemanticBinding] = []
        conflicts: list[BindingConflict] = []

        for binding in produced:
            key = (binding.target_id, self._concept(binding.role))
            standing = best.get(key)
            if standing is None:
                best[key] = binding
                continue
            if standing.role == binding.role:
                # Same claim from two sources: keep the stronger, no conflict.
                if binding.source > standing.source:
                    best[key] = binding
                continue
            winner, loser = ((binding, standing) if binding.source > standing.source
                             else (standing, binding))
            if (winner.role.refines(loser.role) or loser.role.refines(winner.role)
                    or compatible(winner.role, loser.role)):
                # A refinement is not a disagreement; keep both so a rule
                # written against either level still resolves.
                best[key] = winner
                extra.append(loser)
                continue
            best[key] = winner
            conflicts.append(BindingConflict(
                target_name=winner.target_name, accepted=winner, rejected=loser,
                reason=f"{winner.source.name.lower()} says {winner.role}, "
                       f"{loser.source.name.lower()} says {loser.role}; "
                       f"using the {winner.source.name.lower()} binding"))

        kept = list(best.values()) + extra
        conflicts.extend(self._user_contradictions(kept, produced))
        return kept, conflicts

    def _user_contradictions(self, kept, produced) -> list[BindingConflict]:
        """A user role that contradicts what the model's own metadata says.

        Only checked across namespaces, and only against physical evidence: if
        the user calls a Kelvin-valued variable a vehicle speed, the model can
        say so. It cannot say whether an angular velocity belongs to a wheel.
        """
        inferred: dict[int, SemanticBinding] = {}
        for binding in produced:
            if (binding.role.namespace == _PHYSICAL
                    and binding.source in (BindingSource.QUANTITY, BindingSource.UNIT)):
                inferred.setdefault(binding.target_id, binding)

        found = []
        for binding in kept:
            if binding.source is not BindingSource.USER:
                continue
            evidence = inferred.get(binding.target_id)
            if evidence is None or binding.role.namespace == _PHYSICAL:
                continue
            expected = _APPLICATION_PHYSICS.get(binding.role)
            if expected is None or expected == evidence.role:
                continue
            found.append(BindingConflict(
                target_name=binding.target_name, accepted=binding,
                rejected=evidence,
                reason=(f"the model's own metadata makes this {evidence.role} "
                        f"({', '.join(f'{k}={v}' for k, v in evidence.evidence.items())}), "
                        f"but {binding.role} is a {expected}; "
                        f"using the explicit user binding")))
        return found

    def _ambiguities(self, kept) -> list[Ambiguity]:
        """Roles that several objects claim, where a rule needs exactly one.

        Only application roles are reported. A model legitimately has many
        masses; it has one vehicle speed, and a rule asking for it must be told
        rather than handed an arbitrary candidate.
        """
        by_role: dict[SemanticRole, list[SemanticBinding]] = {}
        for binding in kept:
            if binding.role.namespace in (_PHYSICAL, "component"):
                continue
            by_role.setdefault(binding.role, []).append(binding)

        found = []
        for role, bindings in sorted(by_role.items()):
            if len(bindings) < 2:
                continue
            if any(b.source is BindingSource.USER for b in bindings):
                # The user named these deliberately; several wheels is normal.
                continue
            found.append(Ambiguity(
                role=role,
                candidates=tuple(sorted(b.target_name for b in bindings))))
        return found

    def _unmatched(self, produced) -> tuple[str, ...]:
        """User patterns that matched no variable.

        A mistyped path would otherwise fail silently: the mapping simply never
        applies, the rule never fires, and the model reads as clean.
        """
        declared: set[str] = set()
        for provider in self.providers:
            if isinstance(provider, UserProvider):
                declared |= set(provider.mappings)
        if not declared:
            return ()
        matched = {b.evidence.get("pattern") for b in produced
                   if b.source is BindingSource.USER}
        return tuple(sorted(declared - matched))


#: What physics an application role must be, where the model can check it.
#: Absent entries are unverifiable by construction and are not checked.
_APPLICATION_PHYSICS: dict[SemanticRole, SemanticRole] = {
    SemanticRole("automotive.vehicle_speed"): SemanticRole("physical.velocity"),
    SemanticRole("automotive.wheel.angular_velocity"):
        SemanticRole("physical.angular_velocity"),
    SemanticRole("automotive.wheel.radius"): SemanticRole("physical.length"),
    SemanticRole("automotive.motor.torque"): SemanticRole("physical.torque"),
    SemanticRole("hvac.supply_air_temperature"):
        SemanticRole("physical.absolute_temperature"),
    SemanticRole("robotics.joint_velocity"):
        SemanticRole("physical.angular_velocity"),
}
