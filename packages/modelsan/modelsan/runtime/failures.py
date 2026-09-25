"""Failure classification shared by observations and execution results.

Normalized kinds exist so a sanitizer can reason about *what sort* of failure
happened without parsing a tool's prose. The prose is kept alongside, never
instead: the classifier will improve, and re-deriving a better classification
from stored raw messages is much cheaper than re-running a corpus.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class ExecutionPhase(str, Enum):
    """Where in the lifecycle something happened.

    Initialization is separated from simulation throughout, because an
    initialization failure has different causes and different fixes, and
    collapsing it into "failed at t=0" throws that away.
    """

    COMPILATION = "compilation"
    INITIALIZATION = "initialization"
    SIMULATION = "simulation"
    EVENT = "event"
    FINALIZATION = "finalization"


class FailureKind(str, Enum):
    """Normalized failure classes. Extend rather than overload."""

    COMPILATION_ERROR = "compilation-error"
    BUILD_ERROR = "build-error"

    SINGULAR_SYSTEM = "singular-system"
    NONLINEAR_SOLVER_FAILURE = "nonlinear-solver-failure"
    DIVISION_BY_ZERO = "division-by-zero"
    NON_FINITE_VALUE = "non-finite-value"
    ARRAY_BOUNDS = "array-index-out-of-bounds"
    STEP_SIZE_TOO_SMALL = "step-size-too-small"
    EVENT_ITERATION_FAILURE = "event-iteration-failure"
    ASSERTION_VIOLATED = "assertion-violated"

    TIMEOUT = "timeout"
    ABORTED = "aborted"

    UNKNOWN = "unknown"
    """The run failed and the classifier did not recognise the message. The raw
    text is retained so this can be reclassified later without re-running."""


@dataclass(frozen=True)
class ExecutionFailure:
    """Why an execution did not produce a usable result."""

    kind: FailureKind
    phase: ExecutionPhase
    message: str = ""
    """Normalized, human-readable summary."""

    raw: str = ""
    """The backend's own words, kept verbatim for later reclassification."""

    time: float | None = None

    def __str__(self) -> str:
        when = f" at t={self.time:g}" if self.time is not None else ""
        return f"{self.kind.value} during {self.phase.value}{when}: {self.message}"
