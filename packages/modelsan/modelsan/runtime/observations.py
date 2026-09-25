"""What a running simulation reports back — including that it stopped running.

Runtime *metadata*, never a model representation. Nothing here describes the
model; everything describes one execution of it.

Two rules this module enforces:

**A failure is an observation.** A sanitizer must never have to infer that a
run failed from the absence of data. `trace is None` is not a signal, it is a
missing signal, and the two mean different things — "the model was clean" and
"we could not see" must stay distinguishable.

**Identity is explicit.** An observation carries a `CanonicalAnchor` when the
producer genuinely knows the DAE entity, a `BackendAnchor` when it only knows
what the tool called it, and neither when it is about the whole execution. No
sentinel ids.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Iterator

from .anchors import AnchorQuality, BackendAnchor, CanonicalAnchor, quality
from .failures import ExecutionPhase, FailureKind

# Re-exported so callers have one import for "the phase of a run".
Phase = ExecutionPhase


@dataclass
class Observation:
    """Base for everything the runtime reports."""

    time: float | None = None
    phase: ExecutionPhase = ExecutionPhase.SIMULATION


@dataclass
class Anchored(Observation):
    """An observation about a specific entity, however well we can identify it."""

    canonical: CanonicalAnchor | None = None
    backend: BackendAnchor | None = None

    @property
    def anchor_quality(self) -> AnchorQuality:
        return quality([self.canonical] if self.canonical else [],
                       [self.backend] if self.backend else [])

    @property
    def label(self) -> str:
        """Best available human name, for reporting only."""
        if self.canonical and self.canonical.name:
            return self.canonical.name
        if self.backend:
            return self.backend.name
        return str(self.canonical) if self.canonical else "?"


# ── Lifecycle ────────────────────────────────────────────────────────────────


@dataclass
class SimulationStart(Observation):
    pass


@dataclass
class SimulationEnd(Observation):
    completed: bool = False
    message: str = ""


@dataclass
class InitializationStart(Observation):
    phase: ExecutionPhase = ExecutionPhase.INITIALIZATION


@dataclass
class InitializationEnd(Observation):
    phase: ExecutionPhase = ExecutionPhase.INITIALIZATION
    converged: bool = True
    iterations: int = 0


# ── Values ───────────────────────────────────────────────────────────────────


@dataclass
class VariableObservation(Anchored):
    value: float = 0.0


@dataclass
class UnorderedVariableObservation(Anchored):
    """A measured value whose reported time cannot establish a trajectory.

    Row order and the unmodified reported coordinate remain evidence. They do
    not become a validated observation time or imply either side of an event.
    Only properties that are independent of temporal order may use these values.
    """

    value: float = 0.0
    reported_time: float | None = None
    row_index: int = 0


@dataclass
class ExpressionObservation(Anchored):
    """The value of an instrumented sub-expression.

    This is what lets DomainSan say "the divisor was zero" rather than
    "something downstream became inf".
    """

    value: float = 0.0
    role: str = ""


@dataclass
class EquationResidual(Anchored):
    """`r = F(x, x', z, p, t)` for one equation, which should stay near zero."""

    residual: float = 0.0
    scale: float | None = None
    coordinates: str = "published"


# ── Events ───────────────────────────────────────────────────────────────────


@dataclass
class EventTriggered(Anchored):
    phase: ExecutionPhase = ExecutionPhase.EVENT
    old_value: Any = None
    new_value: Any = None


@dataclass
class EventIteration(Anchored):
    phase: ExecutionPhase = ExecutionPhase.EVENT
    iterations: int = 0
    converged: bool = True


# ── Solver ───────────────────────────────────────────────────────────────────


@dataclass
class SolverStep(Observation):
    step_size: float = 0.0
    accepted: bool = True
    nonlinear_iterations: int = 0
    coordinates: str = "integrator"


@dataclass
class JacobianObservation(Observation):
    block_id: int | None = None
    condition_estimate: float | None = None
    rank: int | None = None
    dimension: int = 0
    rows: list[int] = field(default_factory=list)
    columns: list[int] = field(default_factory=list)
    values_column_major: list[float | None] = field(default_factory=list)
    coordinates: str = "internal-evaluation"


# ── Failures. First-class observations, not absences. ────────────────────────


@dataclass
class ExecutionFailureObservation(Anchored):
    """Base for every way an execution can stop producing useful output."""

    kind: FailureKind = FailureKind.UNKNOWN
    reason: str = ""
    raw: str = ""


@dataclass
class CompilationFailure(ExecutionFailureObservation):
    phase: ExecutionPhase = ExecutionPhase.COMPILATION
    kind: FailureKind = FailureKind.COMPILATION_ERROR
    diagnostic: dict[str, Any] = field(default_factory=dict)


@dataclass
class BackendFailure(ExecutionFailureObservation):
    """The tool itself could not run — a build error, a missing dependency.

    Distinct from a model failure on purpose: this is evidence about the
    backend, and treating it as evidence about the model is how a coverage gap
    becomes a false bug report.
    """

    phase: ExecutionPhase = ExecutionPhase.COMPILATION
    kind: FailureKind = FailureKind.BUILD_ERROR


@dataclass
class InitializationFailure(ExecutionFailureObservation):
    phase: ExecutionPhase = ExecutionPhase.INITIALIZATION


@dataclass
class SolverFailure(ExecutionFailureObservation):
    phase: ExecutionPhase = ExecutionPhase.SIMULATION


@dataclass
class EventIterationFailure(ExecutionFailureObservation):
    phase: ExecutionPhase = ExecutionPhase.EVENT
    kind: FailureKind = FailureKind.EVENT_ITERATION_FAILURE


@dataclass
class SimulationAbort(ExecutionFailureObservation):
    """Stopped for a reason that is not a numerical failure — timeout, kill."""

    kind: FailureKind = FailureKind.ABORTED


@dataclass
class ObservationStream:
    """Everything one execution reported, in order.

    Order is preserved because a single defect commonly surfaces as several
    observations in sequence — conditioning degrades, steps are rejected, a
    residual grows, a NaN appears. Discarding the order discards the evidence
    that those were one event.
    """

    observations: list[Observation] = field(default_factory=list)

    def add(self, observation: Observation) -> None:
        self.observations.append(observation)

    def of(self, *kinds: type) -> Iterator[Observation]:
        for observation in self.observations:
            if isinstance(observation, kinds):
                yield observation

    @property
    def failures(self) -> list[ExecutionFailureObservation]:
        return list(self.of(ExecutionFailureObservation))

    @property
    def has_trace(self) -> bool:
        """Whether any variable has validated temporal observations.

        Unordered value samples deliberately do not constitute a trajectory;
        only explicitly order-independent analyses may consume them.
        """
        return any(isinstance(o, VariableObservation) for o in self.observations)

    def __iter__(self) -> Iterator[Observation]:
        return iter(self.observations)

    def __len__(self) -> int:
        return len(self.observations)
