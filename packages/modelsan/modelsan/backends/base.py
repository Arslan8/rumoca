"""The execution boundary.

Everything a backend knows — how a tool is launched, where it writes temporary
files, what its result format is, which flags it needs — stops here. Above this
line there is one `ExecutionResult` and one observation vocabulary.

DifferentialSan is the reason this matters most: comparing two tools is only
tractable if neither tool's launch details reach the comparison.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Protocol

from ..fuzz.testcase import TestCase
from ..runtime.observations import ObservationStream


class Status(str, Enum):
    OK = "ok"
    """Ran to completion. Says nothing about whether the answer is right."""

    FAILED = "failed"
    """The tool reported failure."""

    BUILD_FAILED = "build-failed"
    """Never ran. Not evidence about the model."""

    TIMEOUT = "timeout"

    UNSUPPORTED = "unsupported"
    """The backend cannot handle this model. Also not evidence about the model."""


@dataclass
class ExecutionResult:
    """What one backend produced for one test case, normalized."""

    status: Status
    backend: str = ""
    observations: ObservationStream = field(default_factory=ObservationStream)
    trace: dict[str, list[float]] = field(default_factory=dict)
    times: list[float] = field(default_factory=list)
    final_state: dict[str, float] = field(default_factory=dict)
    solver_stats: dict[str, float] = field(default_factory=dict)
    message: str = ""

    @property
    def ran(self) -> bool:
        """Whether this result says anything about the model at all.

        A build failure or an unsupported construct is a fact about the tool.
        Treating it as a model failure is how a coverage gap turns into a false
        bug report.
        """
        return self.status in (Status.OK, Status.FAILED)

    @property
    def ok(self) -> bool:
        return self.status is Status.OK


class Backend(Protocol):
    """Runs a test case and returns a normalized result."""

    name: str

    def prepare(self, model_path: str, model_name: str) -> bool:
        """Do any one-time work (compile, build) for this model."""

    def run(self, testcase: TestCase, instrumentation: list | None = None) -> ExecutionResult:
        """Execute one configuration of the prepared model."""
