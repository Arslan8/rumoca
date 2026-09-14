"""The one description of "run the model like this".

Sanitizers are oracles; they judge executions. They do not construct them. A
fuzzer builds a TestCase, a backend runs it, sanitizers judge the observations.
Keeping the structure common is what lets a finding record exactly what
triggered it, and lets a minimizer shrink it without knowing which fuzzer or
sanitizer was involved.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(frozen=True)
class TestCase:
    """One executable configuration of a model."""

    parameters: dict[str, float] = field(default_factory=dict)
    initial_values: dict[str, float] = field(default_factory=dict)
    input_trajectory: Any = None
    solver_options: dict[str, Any] = field(default_factory=dict)

    # Why this case was generated. Carried for reporting, never for identity —
    # two fuzzers arriving at the same configuration produce the same run.
    origin: str = ""

    @property
    def is_nominal(self) -> bool:
        """The model's own declared configuration, which is the baseline.

        Every finding has to be judged against this: without it the first
        candidate tried gets blamed for a pre-existing failure.
        """
        return not self.parameters and not self.initial_values

    def with_parameter(self, name: str, value: float) -> "TestCase":
        return TestCase(
            parameters={**self.parameters, name: value},
            initial_values=dict(self.initial_values),
            input_trajectory=self.input_trajectory,
            solver_options=dict(self.solver_options),
            origin=self.origin,
        )

    def describe(self) -> str:
        if self.is_nominal:
            return "declared configuration"
        bits = [f"{k}={v:g}" for k, v in sorted(self.parameters.items())]
        bits += [f"{k}(0)={v:g}" for k, v in sorted(self.initial_values.items())]
        return ", ".join(bits)


NOMINAL = TestCase(origin="declared")
