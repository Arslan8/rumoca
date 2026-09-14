"""What a sanitizer needs observed, stated without saying how.

A sanitizer knows it needs the value of a divisor. It must not know how to make
Rumoca report that — whether by a DAE pass inserting a trace point, by a runtime
hook, or by reading a column out of a result file. It states the request; the
planner decides how to satisfy it against the backend in use.

This is what keeps backend-specific instrumentation out of sanitizer code.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class RequestKind(str, Enum):
    OBSERVE_EXPRESSION = "observe_expression"
    """Report the value of one sub-expression as the simulation runs."""

    OBSERVE_VARIABLE = "observe_variable"

    EQUATION_RESIDUAL = "equation_residual"
    """Report `r = F(...)`, which should stay near zero."""

    JACOBIAN = "jacobian"
    """Report conditioning of one algebraic block."""

    SOLVER_STATS = "solver_stats"
    EVENT_LOG = "event_log"


@dataclass(frozen=True)
class InstrumentationRequest:
    """One request, anchored on a canonical DAE id."""

    kind: RequestKind
    expression_id: int | None = None
    variable_id: int | None = None
    equation_id: int | None = None
    block_id: int | None = None
    label: str = ""
    requested_by: str = ""
    """Which sanitizer asked, so an unsatisfiable request can be reported back."""

    def target(self) -> str:
        for name, value in (("expr", self.expression_id), ("var", self.variable_id),
                            ("eq", self.equation_id), ("block", self.block_id)):
            if value is not None:
                return f"{name}:{value}"
        return "global"
