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
    OBSERVE_DOMAIN_FAILURE = "observe_domain_failure"
    """Reached native scalar domain violation; may have execution-only identity."""
    OBSERVE_EQUATION_RESIDUAL = "observe_equation_residual"
    OBSERVE_JACOBIAN = "observe_jacobian"
    OBSERVE_EVENTS = "observe_events"
    OBSERVE_SOLVER_STEPS = "observe_solver_steps"

    OBSERVE_FAILURE = "observe_failure"
    """That a run failed, with a classified reason. Every backend can do this,
    which is why SolverSan works everywhere."""

    OBSERVE_CONNECTOR = "observe_connector"
    """A connector member observed *with the node it belongs to*.

    Distinct from `OBSERVE_VARIABLE`, which is satisfied by a column of
    numbers. A conservation law is carried jointly by the members of a node,
    and observing each of them without knowing which node they share answers
    every part of the request except the question."""

    CONNECTION_GRAPH = "connection_graph"
    """The artifact carries connection sets: what each `connect` set equates
    and conserves. Static, like `CANONICAL_MODEL`, and separate from it —
    artifacts produced before the exporter emitted sets have one and not the
    other, and a network pass must report itself skipped rather than clean."""

    CANONICAL_MODEL = "canonical_model"
    """A canonical DAE is available for this model at all.

    Rumoca compiles a minority of any real corpus, so for many models the only
    thing present is an execution. Sanitizers that read model structure declare
    this, and the planner then reports them as skipped rather than letting a
    model nothing could analyse look clean.
    """

    CANONICAL_IDENTITY = "canonical_identity"
    """Observations carry Rumoca DAE ids rather than only backend names. A
    sanitizer that must anchor canonically requires this; one that can work
    from backend anchors does not."""
