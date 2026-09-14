"""EventSan — pathological event behaviour that a completed run still hides.

1. Bug class    a model whose discrete behaviour is degenerate: the same event
                firing repeatedly at effectively one instant (chattering), or a
                density of events that means the model is spending its time
                switching rather than integrating.
2. Overlap      partial with SolverSan, which sees the *consequence* when
                chattering stalls the integrator. EventSan fires when the run
                completes, which is the case SolverSan cannot see, and names
                the time window rather than the eventual symptom.
3. Signal       runtime: event timestamps. Two events closer together than any
                physical timescale in the model, or a burst in a short window.
4. Needs        OBSERVE_EVENTS. Nothing else — not even variable values.
5. Transform    no.
6. Fuzzing      an oracle over successful runs, which is where its value is:
                it converts "completed" into "completed badly".
7. Signature    the count and the window, not the times. Chattering at t=0.4 in
                one run and t=0.6 in another is the same defect.

**What OMC can and cannot supply.** It reports event times, not which condition
fired. So this reasons about spacing and density only, and its findings carry no
entity anchor. Naming a guilty condition would need `OBSERVE_EVENTS` from a
backend that identifies them, and the sanitizer would then anchor canonically
without changing its logic.
"""

from __future__ import annotations

from ..analysis.context import AnalysisContext
from ..findings.finding import Finding, Severity
from ..fuzz.testcase import TestCase
from ..instrumentation.capability import Capability
from ..runtime.failures import ExecutionPhase
from ..runtime.observations import EventTriggered, ObservationStream


class EventSan:
    name = "event"

    requires = {"runtime": frozenset({Capability.OBSERVE_EVENTS})}

    def __init__(self, chatter_gap: float = 1e-9, chatter_burst: int = 4,
                 storm_count: int = 50, storm_window: float = 1e-3) -> None:
        # Two events closer than this are not two physical events; no MSL model
        # has a timescale where a nanosecond separates distinct behaviour.
        self.chatter_gap = chatter_gap
        # But *two* such events are ordinary event iteration: a clutch engaging
        # in `CoupledClutches` fires a pair 1e-11 apart at every engagement, and
        # calling that chattering would report a stock MSL example as buggy.
        # Chattering is a burst the iteration cannot settle, so require several.
        self.chatter_burst = chatter_burst
        self.storm_count = storm_count
        self.storm_window = storm_window

    def observe(self, stream: ObservationStream, model, context: AnalysisContext,
                testcase: TestCase) -> list[Finding]:
        times = sorted(o.time for o in stream.of(EventTriggered) if o.time is not None)
        if len(times) < 2:
            return []
        return self._chattering(times, testcase) + self._storm(times, testcase)

    def _chattering(self, times: list[float], testcase: TestCase) -> list[Finding]:
        bursts: list[tuple[float, int]] = []
        start, count = times[0], 1
        for previous, current in zip(times, times[1:]):
            if current - previous <= self.chatter_gap:
                count += 1
            else:
                if count >= self.chatter_burst:
                    bursts.append((start, count))
                start, count = current, 1
        if count >= self.chatter_burst:
            bursts.append((start, count))
        if not bursts:
            return []
        worst = max(bursts, key=lambda b: b[1])
        return [Finding(
            sanitizer=self.name,
            kind="chattering",
            severity=Severity.MEDIUM,
            phase=ExecutionPhase.EVENT,
            time=worst[0],
            test_case=testcase,
            evidence={"events_in_burst": worst[1], "bursts": len(bursts),
                      "gap_threshold": self.chatter_gap,
                      "burst_threshold": self.chatter_burst},
        )]

    def _storm(self, times: list[float], testcase: TestCase) -> list[Finding]:
        """Many events in a short window, even when individually separated."""
        worst_count, worst_start = 0, None
        left = 0
        for right, current in enumerate(times):
            while current - times[left] > self.storm_window:
                left += 1
            if right - left + 1 > worst_count:
                worst_count, worst_start = right - left + 1, times[left]
        if worst_count < self.storm_count:
            return []
        return [Finding(
            sanitizer=self.name,
            kind="event-storm",
            severity=Severity.MEDIUM,
            phase=ExecutionPhase.EVENT,
            time=worst_start,
            test_case=testcase,
            evidence={"events": worst_count, "window": self.storm_window,
                      "total_events": len(times)},
        )]
