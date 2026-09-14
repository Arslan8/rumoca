"""What an execution environment can observe.

A capability is a question about the *environment*, never about which tool is
in use. `DomainSan` asks "does anything here provide OBSERVE_EXPRESSION?" — not
"am I running on Rumoca?". That capability may eventually be supplied by a DAE
instrumentation pass, by a runtime hook, by an FMU wrapper, or by a backend not
yet written, and the sanitizer should not change when the supplier does.
"""

from __future__ import annotations

from enum import Enum


class Capability(str, Enum):
    OBSERVE_VARIABLE = "observe_variable"
    OBSERVE_EXPRESSION = "observe_expression"
    OBSERVE_EQUATION_RESIDUAL = "observe_equation_residual"
    OBSERVE_JACOBIAN = "observe_jacobian"
    OBSERVE_EVENTS = "observe_events"
    OBSERVE_SOLVER_STEPS = "observe_solver_steps"

    OBSERVE_FAILURE = "observe_failure"
    """That a run failed, with a classified reason. Every backend can do this,
    which is why SolverSan works everywhere."""

    CANONICAL_IDENTITY = "canonical_identity"
    """Observations carry Rumoca DAE ids rather than only backend names. A
    sanitizer that must anchor canonically requires this; one that can work
    from backend anchors does not."""
