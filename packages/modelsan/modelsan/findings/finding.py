"""The one shape every sanitizer emits.

Two things this structure is careful about.

**Anchors are typed and optional.** A finding may be anchored to exact DAE
entities, or only to what a backend called something, or to neither — a
whole-execution failure is anchored by its test case alone. All three are
valid. What is not valid is inventing a DAE id to fill the gap.

**Signature and evidence are separate.**

    signature   what bug is this?      properties of the model
    evidence    how was it reached?    time, values, test case

Putting a timestamp in the signature makes every run report new bugs.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any

from ..runtime.anchors import AnchorQuality, BackendAnchor, CanonicalAnchor, quality
from ..runtime.failures import ExecutionPhase


class Severity(str, Enum):
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    INFO = "info"


@dataclass(frozen=True)
class SourceLocation:
    file: str
    line: int
    column: int = 0

    def __str__(self) -> str:
        return f"{self.file}:{self.line}" + (f":{self.column}" if self.column else "")


@dataclass
class Finding:
    """One violation."""

    sanitizer: str
    kind: str
    severity: Severity

    canonical_anchors: list[CanonicalAnchor] = field(default_factory=list)
    backend_anchors: list[BackendAnchor] = field(default_factory=list)
    source_locations: list[SourceLocation] = field(default_factory=list)

    phase: ExecutionPhase | None = None
    time: float | None = None
    test_case: Any = None
    evidence: dict[str, Any] = field(default_factory=dict)

    signature: str = ""
    sequence: int = 0
    """Order within one execution, so a causal chain stays reconstructible."""

    @property
    def anchor_quality(self) -> AnchorQuality:
        """How firmly this attaches to the model.

        Reported alongside every finding so a reader knows whether the
        identity is exact or backend-local, rather than having to infer it.
        """
        return quality(self.canonical_anchors, self.backend_anchors)

    @property
    def anchors(self) -> list[str]:
        return [str(a) for a in self.canonical_anchors] + \
               [str(a) for a in self.backend_anchors]

    def summary(self) -> str:
        where = f" at {self.source_locations[0]}" if self.source_locations else ""
        if not where and self.anchors:
            where = f" on {self.anchors[0]}"
        when = f" (t={self.time:g})" if self.time is not None else ""
        phase = f" [{self.phase.value}]" if self.phase else ""
        return f"[{self.sanitizer}] {self.kind}{phase}{where}{when}"
