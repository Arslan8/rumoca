"""One statement that a model object means something, and why.

Provenance is not decoration. PhysicalSan reports invariant violations, and a
violation is only actionable if the reader can see *why* the checker thought
the rule applied. "R must be positive" is a different claim depending on
whether `R` was identified as a resistance from its unit, from the class that
declared it, or because the user said so — and the first of those is the one
that is sometimes wrong.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import IntEnum

from .role import SemanticRole


class BindingSource(IntEnum):
    """Where a binding came from. Higher wins; see `binder.resolve`.

    The order is the brief's priority list, and it is an ordering of
    *authority*, not of quality: a user binding wins over a unit inference
    because the user knows the application, not because the unit was
    unreliable.
    """

    HEURISTIC = 1
    """A name or structural pattern. Weak hint only."""
    UNIT = 2
    """The declared `unit` alone."""
    QUANTITY = 3
    """The declared MLS §4.8 `quantity` attribute."""
    CONNECTOR = 4
    """Connector role and what the variable is connected to."""
    COMPONENT_TYPE = 5
    """The fully qualified class that declared the variable."""
    USER = 6
    """An explicit mapping the user supplied."""


#: Sources weak enough that a rule should not fire on them unaccompanied.
WEAK_SOURCES = frozenset({BindingSource.HEURISTIC, BindingSource.UNIT})


@dataclass(frozen=True)
class SemanticBinding:
    """`target` means `role`, on the authority of `source`."""

    role: SemanticRole
    target_id: int
    target_name: str
    source: BindingSource
    evidence: dict = field(default_factory=dict)
    """What supported it: the unit read, the class matched, the file a user
    mapping came from. Rendered into every finding this binding contributes
    to."""

    target_kind: str = "variable"
    """variable | parameter | component | connector"""

    @property
    def is_weak(self) -> bool:
        return self.source in WEAK_SOURCES

    def describe(self) -> str:
        detail = ", ".join(f"{k}={v}" for k, v in self.evidence.items())
        return (f"{self.target_name} -> {self.role} "
                f"[{self.source.name.lower()}{': ' + detail if detail else ''}]")


@dataclass(frozen=True)
class BindingConflict:
    """Two sources disagree about what one object means.

    Not an error. The brief is explicit that the user stays in control, so the
    binder applies the higher-authority binding and records this so the
    disagreement stays visible rather than being silently resolved.
    """

    target_name: str
    accepted: SemanticBinding
    rejected: SemanticBinding
    reason: str

    def describe(self) -> str:
        return (f"semantic binding conflict on {self.target_name}\n"
                f"  using   {self.accepted.describe()}\n"
                f"  ignored {self.rejected.describe()}\n"
                f"  {self.reason}")


@dataclass(frozen=True)
class Ambiguity:
    """A role several objects could fill, and none uniquely.

    Reported instead of binding, because binding the first candidate would make
    a rule's verdict depend on declaration order.
    """

    role: SemanticRole
    candidates: tuple[str, ...]

    def describe(self) -> str:
        return (f"unable to uniquely bind {self.role}\n"
                + "".join(f"  candidate: {c}\n" for c in self.candidates)
                + "  provide an explicit semantic mapping")
