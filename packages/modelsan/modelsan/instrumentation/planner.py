"""Deciding, before anything runs, what coverage is actually available.

The problem this solves: without it, "no finding" is ambiguous. It can mean the
model was clean, or that the sanitizer could not observe the execution at all.
Those must never look the same in an evaluation.

So every sanitizer declares the capabilities it requires — per component, since
a sanitizer's static half often works when its runtime half cannot — and the
planner resolves those against what the environment provides, recording
SUPPORTED, PARTIAL or UNSUPPORTED with a reason.

Nothing here knows which backend is in use.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum

from .capability import Capability
from .request import InstrumentationRequest


class Support(str, Enum):
    SUPPORTED = "supported"
    PARTIAL = "partial"
    """Some components can run, others cannot. The usual case for a sanitizer
    with a static half and a runtime half."""
    UNSUPPORTED = "unsupported"


@dataclass
class ComponentSupport:
    """Whether one component of one sanitizer can run."""

    component: str
    support: Support
    required: frozenset[Capability] = frozenset()
    missing: frozenset[Capability] = frozenset()

    @property
    def reason(self) -> str:
        if self.support is Support.SUPPORTED:
            return ""
        names = ", ".join(sorted(c.value for c in self.missing))
        return f"{names} unavailable"


@dataclass
class SanitizerSupport:
    name: str
    components: list[ComponentSupport] = field(default_factory=list)

    @property
    def support(self) -> Support:
        states = {c.support for c in self.components}
        if not states or states == {Support.UNSUPPORTED}:
            return Support.UNSUPPORTED
        if Support.UNSUPPORTED in states:
            return Support.PARTIAL
        return Support.SUPPORTED

    @property
    def skipped(self) -> list[ComponentSupport]:
        return [c for c in self.components if c.support is Support.UNSUPPORTED]


@dataclass
class Plan:
    """The resolved coverage for one execution environment."""

    available: frozenset[Capability] = frozenset()
    sanitizers: dict[str, SanitizerSupport] = field(default_factory=dict)
    satisfied: list[InstrumentationRequest] = field(default_factory=list)
    unsupported: list[tuple[InstrumentationRequest, str]] = field(default_factory=list)

    def skipped_sanitizers(self) -> dict[str, str]:
        """Sanitizer components that will not run, and why.

        Returned rather than merely logged, because an evaluation needs to know
        what coverage was active for each backend before it can interpret a
        finding count.
        """
        skipped = {}
        for support in self.sanitizers.values():
            for component in support.skipped:
                skipped[f"{support.name}.{component.component}"] = component.reason
        return skipped

    def can_run(self, sanitizer: str, component: str = "runtime") -> bool:
        support = self.sanitizers.get(sanitizer)
        if support is None:
            return False
        for entry in support.components:
            if entry.component == component:
                return entry.support is Support.SUPPORTED
        return False

    def describe(self) -> str:
        lines = ["Capabilities available:"]
        lines += [f"    {c.value}" for c in sorted(self.available, key=lambda c: c.value)]
        missing = sorted({c for s in self.sanitizers.values()
                          for comp in s.components for c in comp.missing},
                         key=lambda c: c.value)
        if missing:
            lines.append("Unavailable:")
            lines += [f"    {c.value}" for c in missing]
        lines.append("Result:")
        for support in sorted(self.sanitizers.values(), key=lambda s: s.name):
            for component in support.components:
                state = ("enabled" if component.support is Support.SUPPORTED
                         else f"skipped ({component.reason})")
                lines.append(f"    {support.name}.{component.component}: {state}")
        return "\n".join(lines)


class CapabilityPlanner:
    """Resolves declared requirements against what the environment provides."""

    def __init__(self, available: frozenset[Capability]) -> None:
        self.available = available

    def plan(self, sanitizers: list, requests: list[InstrumentationRequest]) -> Plan:
        plan = Plan(available=self.available)

        for sanitizer in sanitizers:
            name = getattr(sanitizer, "name", repr(sanitizer))
            # `requires` maps component name -> required capabilities. A
            # sanitizer that declares nothing is assumed to need nothing, which
            # is true of pure static analysis.
            requirements: dict[str, frozenset[Capability]] = getattr(
                sanitizer, "requires", {}) or {}
            support = SanitizerSupport(name=name)
            for component, needed in requirements.items():
                needed = frozenset(needed)
                missing = needed - self.available
                support.components.append(ComponentSupport(
                    component=component,
                    support=Support.SUPPORTED if not missing else Support.UNSUPPORTED,
                    required=needed,
                    missing=missing,
                ))
            if not support.components:
                support.components.append(
                    ComponentSupport(component="static", support=Support.SUPPORTED))
            plan.sanitizers[name] = support

        for request in requests:
            if request.capability in self.available:
                plan.satisfied.append(request)
            else:
                plan.unsupported.append(
                    (request, f"{request.capability.value} unavailable"))
        return plan
