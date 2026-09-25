"""The execution boundary.

Everything tool-specific — how a tool is launched, where it writes files, what
its result format is — stops here.

The invariant this module exists to enforce:

    **A failed execution is still an execution result.**

No backend returns None, and none returns a result with nothing in it. A run
that died during initialization still reports which phase it reached, what kind
of failure it was, and what the tool actually said. That is what lets a
sanitizer reason about failures for which no trajectory exists — which is most
of the interesting ones.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Protocol

from ..fuzz.testcase import TestCase
from ..runtime.failures import ExecutionFailure, ExecutionPhase, FailureKind
from ..runtime.observations import ObservationStream


class ExecutionStatus(str, Enum):
    SUCCESS = "success"
    """Ran to completion. Says nothing about whether the answer is correct."""

    FAILED = "failed"
    """The model, as configured, did not run. Evidence about the model."""

    TIMEOUT = "timeout"

    ABORTED = "aborted"
    """Stopped for a reason outside the model — killed, resource limit."""

    BACKEND_ERROR = "backend-error"
    """The tool could not attempt it: build failure, unsupported construct.
    Evidence about the *backend*, and never about the model. Counting these as
    model failures is how a coverage gap becomes a false bug report."""


@dataclass
class SolverStats:
    steps: int = 0
    accepted: int = 0
    rejected: int = 0
    smallest_step: float | None = None
    largest_step: float | None = None
    nonlinear_iterations: int = 0


@dataclass
class Trace:
    """A recorded trajectory. Absent when the run produced none."""

    times: list[float] = field(default_factory=list)
    columns: dict[str, list[float]] = field(default_factory=dict)

    def __len__(self) -> int:
        return len(self.times)

    @property
    def final_state(self) -> dict[str, float]:
        return {name: values[-1] for name, values in self.columns.items() if values}


@dataclass
class ExecutionResult:
    """What one backend produced for one test case. Always returned."""

    backend: str
    status: ExecutionStatus
    phase: ExecutionPhase = ExecutionPhase.SIMULATION
    """The furthest phase reached, successfully or not."""

    observations: ObservationStream = field(default_factory=ObservationStream)
    trace: Trace | None = None
    """None means no trajectory was produced — an explicit fact, not a gap."""

    events: list = field(default_factory=list)
    solver_stats: SolverStats | None = None
    failure: ExecutionFailure | None = None
    backend_metadata: dict = field(default_factory=dict)

    @property
    def ok(self) -> bool:
        return self.status is ExecutionStatus.SUCCESS

    @property
    def informative(self) -> bool:
        """Whether this result says anything about the *model*.

        A backend error does not. Distinguishing it from a model failure is the
        difference between "this model is broken" and "we could not look at it".
        """
        return self.status in (ExecutionStatus.SUCCESS, ExecutionStatus.FAILED,
                               ExecutionStatus.TIMEOUT)

    @property
    def has_trace(self) -> bool:
        return self.trace is not None and len(self.trace) > 0

    @classmethod
    def backend_error(cls, backend: str, message: str,
                      phase: ExecutionPhase = ExecutionPhase.COMPILATION) -> "ExecutionResult":
        """The constructor for "the tool could not attempt this"."""
        return cls(
            backend=backend,
            status=ExecutionStatus.BACKEND_ERROR,
            phase=phase,
            failure=ExecutionFailure(kind=FailureKind.BUILD_ERROR, phase=phase,
                                     message=message[:200], raw=message),
        )


class Backend(Protocol):
    """Runs a test case and always returns a normalized result."""

    name: str
    capabilities: frozenset
    """Which observation capabilities this execution environment can provide."""

    def prepare(self, model_path: str, model_name: str) -> ExecutionResult | None:
        """One-time work, or a result when preparation prevents execution.

        Unsupported compilation is BACKEND_ERROR. A typed, source-backed proof
        of a model defect can instead be FAILED in the COMPILATION phase.
        """

    def run(self, testcase: TestCase, instrumentation: list | None = None) -> ExecutionResult:
        ...
