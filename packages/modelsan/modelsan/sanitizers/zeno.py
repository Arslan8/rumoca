"""ZenoSan — event intervals collapsing toward zero.

1. Bug class    Zeno behaviour: infinitely many events in finite time. The
                model is not merely switching often, it is switching *ever
                faster*, and no integrator can pass the accumulation point.
2. Overlap      deliberately narrower than EventSan. Chattering is many events
                close together; Zeno is a monotone shrinking of the gaps, which
                is a different defect with a different fix (a hysteresis band
                rather than a guard). Keeping them apart is the point.
3. Signal       runtime: a run of consecutive intervals each a constant factor
                smaller than the last.
4. Needs        OBSERVE_EVENTS.
5. Transform    no.
6. Fuzzing      a strong oracle, and an early one — the ratio is detectable
                well before the accumulation point is reached, so it fires on
                runs that still complete.
7. Signature    the sanitizer and the decay shape, not the times.
"""

from __future__ import annotations

from ..analysis.context import AnalysisContext
from ..findings.finding import Finding, Severity
from ..fuzz.testcase import TestCase
from ..instrumentation.capability import Capability
from ..runtime.failures import ExecutionPhase
from ..runtime.observations import EventTriggered, ObservationStream


class ZenoSan:
    name = "zeno"

    requires = {"runtime": frozenset({Capability.OBSERVE_EVENTS})}

    def __init__(self, decay: float = 0.7, run_length: int = 5) -> None:
        # Each interval at most this fraction of the previous one. 0.7 is loose
        # enough to catch a slow accumulation and tight enough that ordinary
        # irregular switching does not qualify.
        self.decay = decay
        self.run_length = run_length

    def observe(self, stream: ObservationStream, model, context: AnalysisContext,
                testcase: TestCase) -> list[Finding]:
        times = sorted(o.time for o in stream.of(EventTriggered) if o.time is not None)
        gaps = [b - a for a, b in zip(times, times[1:]) if b > a]
        if len(gaps) < self.run_length:
            return []

        best_start, best_length = None, 0
        length, start = 1, 0
        for index in range(1, len(gaps)):
            if gaps[index] <= gaps[index - 1] * self.decay:
                length += 1
            else:
                if length > best_length:
                    best_length, best_start = length, start
                length, start = 1, index
        if length > best_length:
            best_length, best_start = length, start

        if best_length < self.run_length:
            return []

        window = gaps[best_start:best_start + best_length]
        return [Finding(
            sanitizer=self.name,
            kind="zeno-accumulation",
            severity=Severity.HIGH,
            phase=ExecutionPhase.EVENT,
            time=times[best_start],
            test_case=testcase,
            evidence={
                "consecutive_shrinking_intervals": best_length,
                "first_interval": window[0],
                "last_interval": window[-1],
                "decay_threshold": self.decay,
            },
        )]
