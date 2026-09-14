"""Two kinds of identity, kept apart on purpose.

A canonical anchor means one thing precisely:

    this observation or finding is attached to an exact entity in Rumoca's
    canonical DAE bitcode.

A backend anchor means something weaker and still useful:

    this is what the tool that ran the model called it.

They are different types rather than one `variable_id` field because a single
field invites exactly the mistake that destroys the guarantee — hashing a name
into an int, or assigning a sequential id, so that downstream code *looks* like
it can resolve back to the DAE when it cannot.

When the mapping between them is unknown, the correct representation is that
the canonical anchor is absent. Not -1, not a synthesized id.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class AnchorQuality(str, Enum):
    """How firmly a finding is attached to the model."""

    CANONICAL = "canonical"
    """Resolves to an exact DAE entity. Source mapping and cross-run
    comparison are both reliable."""

    BACKEND_ONLY = "backend-only"
    """A real observation from a real tool, but not resolvable to a DAE
    entity. Still a valid finding; weaker identity."""

    NONE = "none"
    """No variable or equation anchor at all — a whole-execution failure, for
    instance. Valid, and anchored only by the test case."""


class EntityKind(str, Enum):
    VARIABLE = "variable"
    EQUATION = "equation"
    EXPRESSION = "expression"
    PARAMETER = "parameter"
    BLOCK = "block"
    EVENT = "event"


@dataclass(frozen=True)
class CanonicalAnchor:
    """An exact entity in the canonical DAE."""

    kind: EntityKind
    dae_id: int
    name: str = ""
    """Convenience for reporting only. The identity is `dae_id`."""

    def __str__(self) -> str:
        label = f"{self.kind.value[:3]}:{self.dae_id}"
        return f"{label}({self.name})" if self.name else label


@dataclass(frozen=True)
class BackendAnchor:
    """What a backend called an entity, when we cannot resolve it further."""

    backend: str
    name: str
    kind: EntityKind = EntityKind.VARIABLE

    def __str__(self) -> str:
        return f"{self.backend}:{self.name}"


def quality(canonical: list[CanonicalAnchor], backend: list[BackendAnchor]) -> AnchorQuality:
    if canonical:
        return AnchorQuality.CANONICAL
    if backend:
        return AnchorQuality.BACKEND_ONLY
    return AnchorQuality.NONE
