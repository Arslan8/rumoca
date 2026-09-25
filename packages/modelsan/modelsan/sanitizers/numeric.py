"""NumericSan — non-finite and extreme values in a run that did not report failure.

1. Bug class    a simulation that completes and hands back inf or NaN. This is
                the class that looks like success: the user gets a trajectory,
                not an error. Negative resistance is the case that exposed it —
                it does not crash, it produces a physically impossible answer
                cleanly.
2. Overlap      DomainSan names the operation, this names the contaminated
                value. On a division by zero both fire and the deduplicator
                should collapse them; NumericSan still earns its place because
                a NaN can arrive from overflow or cancellation with no
                restricted operation involved.
3. Signal       runtime: a variable's value is not finite, or its magnitude is
                far outside what the model's own nominal scale suggests.
4. Needs        variable observations; DAE ids to attribute them.
5. Transform    no. Ordinary variable output is enough.
6. Fuzzing      as an oracle, yes — it turns "ran to completion" into a
                verdict. It provides no hints, because it does not know which
                input caused the contamination.
7. Signature    the DAE variable id that first went non-finite, plus the kind.

Reporting only the *first* contaminated variable is deliberate: once one value
is NaN, everything downstream of it is too, and listing all of them describes
the propagation rather than the defect.
"""

from __future__ import annotations

import math

from ..analysis.context import AnalysisContext
from ..findings.location import locate
from ..findings.finding import Finding, Severity, SourceLocation
from ..fuzz.testcase import TestCase
from ..instrumentation.capability import Capability
from ..runtime.observations import (
    ObservationStream, UnorderedVariableObservation, VariableObservation,
)

# A magnitude no physical MSL quantity reaches, chosen well above any plausible
# unit-scale so that a merely large value is not mistaken for a broken one.
EXTREME = 1e30


class NumericSan:
    name = "numeric"

    #: Needs variable values. Declared, so the planner can report that this
    #: sanitizer was inactive rather than letting silence read as "clean".
    requires = {"runtime": frozenset({Capability.OBSERVE_VARIABLE})}

    def __init__(self, extreme_magnitude: float = EXTREME) -> None:
        self.extreme_magnitude = extreme_magnitude

    def observe(self, stream: ObservationStream, model, context: AnalysisContext,
                testcase: TestCase) -> list[Finding]:
        findings: list[Finding] = []
        seen: set[tuple[str, int | str]] = set()

        for observation in stream.of(VariableObservation, UnorderedVariableObservation):
            kind = self._classify(observation.value)
            if kind is None:
                continue
            key = (kind, observation.label)
            if key in seen:
                continue
            seen.add(key)
            provenance = (dict(sample_order="unordered", reported_time=observation.reported_time,
                               row_index=observation.row_index)
                          if isinstance(observation, UnorderedVariableObservation) else {})
            findings.append(Finding(
                sanitizer=self.name,
                kind=kind,
                severity=Severity.HIGH if kind != "extreme-magnitude" else Severity.MEDIUM,
                canonical_anchors=([observation.canonical]
                                   if observation.canonical else []),
                backend_anchors=([observation.backend]
                                 if observation.backend else []),
                source_locations=self._location(context, observation.canonical),
                phase=observation.phase,
                time=observation.time,
                test_case=testcase,
                evidence={
                    "variable": observation.label,
                    "value": observation.value,
                    "anchor_quality": observation.anchor_quality.value,
                    **provenance,
                },
            ))
        return self._first_only(findings)

    def _classify(self, value: float) -> str | None:
        if isinstance(value, float) and math.isnan(value):
            return "nan"
        if isinstance(value, float) and math.isinf(value):
            return "inf"
        if abs(value) > self.extreme_magnitude:
            return "extreme-magnitude"
        return None

    @staticmethod
    def _first_only(findings: list[Finding]) -> list[Finding]:
        """Keep the earliest timed or first received untimed occurrence per kind.

        A NaN contaminates every variable that reads it within one step, so the
        set of affected variables measures fan-out, not severity. The earliest
        one is the closest thing available to the source. Untimed samples only
        establish the value's presence, never which event came first.
        """
        earliest: dict[str, Finding] = {}
        for finding in findings:
            current = earliest.get(finding.kind)
            if current is None or (finding.time or 0) < (current.time or 0):
                earliest[finding.kind] = finding
        return list(earliest.values())

    @staticmethod
    def _location(context: AnalysisContext, anchor) -> list[SourceLocation]:
        if anchor is None or context is None or context.model is None:
            return []
        return locate(context.variable(anchor.dae_id))
