"""What a sanitizer needs observed, stated without saying how.

A sanitizer knows it needs the value of a divisor. It must not know how to make
that happen — whether by a DAE pass inserting a trace point, a runtime hook, or
a column in a result file. It states the request against a canonical DAE id;
the planner decides whether anything can satisfy it.
"""

from __future__ import annotations

from dataclasses import dataclass

from ..runtime.anchors import CanonicalAnchor
from .capability import Capability


@dataclass(frozen=True)
class InstrumentationRequest:
    """One request, anchored on a canonical DAE entity.

    Requests are always canonical: we are asking for something *in the model*
    to be observed, and if we could not name it in the DAE we would not know
    what we were asking for.
    """

    capability: Capability
    anchor: CanonicalAnchor | None = None
    label: str = ""
    requested_by: str = ""
    """Which sanitizer asked, so an unsatisfiable request names what is lost."""

    def target(self) -> str:
        return str(self.anchor) if self.anchor else "global"
