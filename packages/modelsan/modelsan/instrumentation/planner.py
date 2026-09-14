"""Turning requests into something a backend can actually do.

Not every backend can satisfy every request. OpenModelica reports variables and
solver statistics but will not expose an arbitrary sub-expression; Rumoca can be
instrumented at the DAE level but has no Jacobian conditioning hook yet.

The planner's job is to say honestly which requests were satisfied, so a
sanitizer that depends on an unavailable observation is *skipped* rather than
silently reporting nothing and looking like a clean result.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from .request import InstrumentationRequest, RequestKind


@dataclass
class Plan:
    """What will be instrumented, and what could not be."""

    satisfied: list[InstrumentationRequest] = field(default_factory=list)
    unsupported: list[tuple[InstrumentationRequest, str]] = field(default_factory=list)

    def skipped_sanitizers(self) -> set[str]:
        """Sanitizers whose requests went unmet, and which must not be trusted."""
        return {request.requested_by for request, _ in self.unsupported
                if request.requested_by}


class InstrumentationPlanner:
    """Matches requests against what a backend advertises it can observe."""

    def __init__(self, capabilities: set[RequestKind]) -> None:
        self.capabilities = capabilities

    def plan(self, requests: list[InstrumentationRequest]) -> Plan:
        plan = Plan()
        for request in requests:
            if request.kind in self.capabilities:
                plan.satisfied.append(request)
            else:
                plan.unsupported.append(
                    (request, f"backend cannot provide {request.kind.value}"))
        return plan
