"""What a running simulation reports back.

These are runtime *metadata*, not a model representation. Nothing here describes
the model; everything here describes one execution of it. A sanitizer consumes
observations and DAE ids together — the observation says what happened, the id
says where in the model it happened.

Defining these once is what stops every sanitizer reaching into backend
internals. A backend adapter produces observations; sanitizers never see a
solver log, a CSV column, or a process exit code.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Iterator


class Phase(str, Enum):
    """Initialization is not just "the run at t=0".

    An initialization failure has different causes and different fixes than a
    transient failure, so observations carry the phase and InitSan can filter on
    it rather than guessing from a timestamp.
    """

    INITIALIZATION = "initialization"
    TRANSIENT = "transient"
    EVENT = "event"


@dataclass
class Observation:
    """Base for everything the runtime reports. `time` may be None pre-init."""

    time: float | None = None
    phase: Phase = Phase.TRANSIENT


@dataclass
class SimulationStart(Observation):
    pass


@dataclass
class SimulationEnd(Observation):
    completed: bool = False
    message: str = ""


@dataclass
class InitializationStart(Observation):
    phase: Phase = Phase.INITIALIZATION


@dataclass
class InitializationEnd(Observation):
    phase: Phase = Phase.INITIALIZATION
    converged: bool = True
    iterations: int = 0


@dataclass
class VariableObservation(Observation):
    """One variable's value at one instant. `variable_id` is the DAE id."""

    variable_id: int = -1
    name: str = ""
    value: float = 0.0


@dataclass
class ExpressionObservation(Observation):
    """The value of an instrumented sub-expression.

    This is what makes DomainSan able to say "the divisor was zero" rather than
    "something downstream became inf".
    """

    expression_id: int = -1
    value: float = 0.0
    label: str = ""


@dataclass
class EquationResidual(Observation):
    """`r = F(x, x', z, p, t)` for one equation, which should be ~0."""

    equation_id: int = -1
    residual: float = 0.0
    scale: float | None = None


@dataclass
class EventTriggered(Observation):
    phase: Phase = Phase.EVENT
    event_id: int = -1
    condition_id: int = -1
    old_value: Any = None
    new_value: Any = None


@dataclass
class EventIteration(Observation):
    phase: Phase = Phase.EVENT
    event_id: int = -1
    iterations: int = 0
    converged: bool = True


@dataclass
class SolverStep(Observation):
    step_size: float = 0.0
    accepted: bool = True
    nonlinear_iterations: int = 0


@dataclass
class SolverFailure(Observation):
    reason: str = ""
    equation_id: int | None = None
    variable_id: int | None = None


@dataclass
class JacobianObservation(Observation):
    """Conditioning of one algebraic block, for detecting trouble early."""

    block_id: int = -1
    condition_estimate: float | None = None
    rank: int | None = None
    dimension: int = 0


@dataclass
class ObservationStream:
    """Everything one execution reported, in the order it happened.

    Order is preserved because a single defect commonly surfaces as several
    observations in sequence — conditioning degrades, then steps are rejected,
    then a residual blows up, then a NaN appears. Discarding the order discards
    the evidence that those were one event.
    """

    observations: list[Observation] = field(default_factory=list)

    def add(self, observation: Observation) -> None:
        self.observations.append(observation)

    def of(self, *kinds: type) -> Iterator[Observation]:
        for observation in self.observations:
            if isinstance(observation, kinds):
                yield observation

    def __iter__(self) -> Iterator[Observation]:
        return iter(self.observations)

    def __len__(self) -> int:
        return len(self.observations)
