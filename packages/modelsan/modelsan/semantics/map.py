"""The resolved semantic map: what every object in one model means.

Deliberately a first-class artifact rather than a private detail of
PhysicalSan. Connector logging, differential analysis, fault injection and
model slicing all need the same question answered, and none of them should have
to re-derive it.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from .binding import Ambiguity, BindingConflict, SemanticBinding
from .role import SemanticRole


@dataclass
class SemanticMap:
    """Bindings for one model, indexed both ways."""

    bindings: list[SemanticBinding] = field(default_factory=list)
    conflicts: list[BindingConflict] = field(default_factory=list)
    ambiguities: list[Ambiguity] = field(default_factory=list)
    unmatched_patterns: tuple[str, ...] = ()
    """User mappings that matched nothing. A typo is silent otherwise."""

    def __post_init__(self) -> None:
        self._by_role: dict[SemanticRole, list[SemanticBinding]] = {}
        self._by_target: dict[int, list[SemanticBinding]] = {}
        for binding in self.bindings:
            self._by_role.setdefault(binding.role, []).append(binding)
            self._by_target.setdefault(binding.target_id, []).append(binding)

    # ── lookup by role: what a sanitizer rule asks ───────────────────────────

    def get(self, role: str) -> SemanticBinding | None:
        """The single object filling `role`, or None.

        None when nothing fills it *and* when several do — an ambiguous role
        has no answer, and returning an arbitrary one of the candidates would
        make a rule's verdict depend on declaration order. Check `ambiguities`
        to tell the two cases apart.
        """
        found = self._by_role.get(SemanticRole(role), [])
        return found[0] if len(found) == 1 else None

    def all(self, role: str) -> list[SemanticBinding]:
        """Every object filling `role`. For rules that are happy with many."""
        return list(self._by_role.get(SemanticRole(role), []))

    def has(self, role: str) -> bool:
        return bool(self._by_role.get(SemanticRole(role)))

    # ── lookup by object: what a finding asks ────────────────────────────────

    def roles_of(self, target_id: int) -> list[SemanticBinding]:
        return list(self._by_target.get(target_id, []))

    def role_names(self, target_id: int) -> set[SemanticRole]:
        return {b.role for b in self._by_target.get(target_id, [])}

    def binding_for(self, target_id: int, role: str) -> SemanticBinding | None:
        wanted = SemanticRole(role)
        for binding in self._by_target.get(target_id, []):
            if binding.role == wanted:
                return binding
        return None

    # ── reporting ────────────────────────────────────────────────────────────

    @property
    def roles(self) -> list[SemanticRole]:
        return sorted(self._by_role)

    def summary(self) -> dict:
        by_source: dict[str, int] = {}
        for binding in self.bindings:
            key = binding.source.name.lower()
            by_source[key] = by_source.get(key, 0) + 1
        return {
            "bindings": len(self.bindings),
            "roles": len(self._by_role),
            "objects": len(self._by_target),
            "by_source": by_source,
            "conflicts": len(self.conflicts),
            "ambiguities": len(self.ambiguities),
            "unmatched_user_patterns": list(self.unmatched_patterns),
        }

    def report(self) -> str:
        lines = [f"semantic map: {len(self.bindings)} bindings over "
                 f"{len(self._by_target)} objects, {len(self._by_role)} roles"]
        for conflict in self.conflicts:
            lines.append(conflict.describe())
        for ambiguity in self.ambiguities:
            lines.append(ambiguity.describe())
        for pattern in self.unmatched_patterns:
            lines.append(f"user mapping matched nothing: {pattern}")
        return "\n".join(lines)
