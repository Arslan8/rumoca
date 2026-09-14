"""The one shape every sanitizer emits.

A sanitizer decides *what constitutes a violation*. It does not decide how the
violation is printed, whether it duplicates an earlier one, or how it is
counted. Those are separate concerns downstream, and they only work if every
sanitizer hands them the same structure.

The split that matters most here is signature vs evidence:

    signature  what bug is this?
    evidence   how did this execution reach it?

Simulation time, floating-point values and test-case ids belong in evidence.
Putting them in the signature makes every run report a "new" bug.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any


class Severity(str, Enum):
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    INFO = "info"


@dataclass(frozen=True)
class SourceLocation:
    """Where in the Modelica source a DAE entity came from."""

    file: str
    line: int
    column: int = 0

    def __str__(self) -> str:
        return f"{self.file}:{self.line}" + (f":{self.column}" if self.column else "")


@dataclass
class Finding:
    """One violation, attributed to canonical DAE entities.

    Ids are DAE ids. They are carried rather than resolved objects so a finding
    survives serialization, can be compared across executions and backends, and
    can be deduplicated without the model being loaded.
    """

    sanitizer: str
    kind: str
    severity: Severity

    # Where in the model. All DAE ids.
    equation_ids: list[int] = field(default_factory=list)
    variable_ids: list[int] = field(default_factory=list)
    parameter_ids: list[int] = field(default_factory=list)
    expression_ids: list[int] = field(default_factory=list)

    source_locations: list[SourceLocation] = field(default_factory=list)

    # How this execution reached it. Never part of the signature.
    time: float | None = None
    test_case: Any = None
    evidence: dict[str, Any] = field(default_factory=dict)

    # Set by the signature module rather than by the sanitizer, so the rule for
    # "same bug" stays in one place.
    signature: str = ""

    # Ordering within one execution, so a causal chain can be reconstructed
    # later — an ill-conditioned block, then step rejection, then a NaN are
    # very often one bug seen four times.
    sequence: int = 0

    def summary(self) -> str:
        where = ""
        if self.source_locations:
            where = f" at {self.source_locations[0]}"
        when = f" (t={self.time:g})" if self.time is not None else ""
        return f"[{self.sanitizer}] {self.kind}{where}{when}"
