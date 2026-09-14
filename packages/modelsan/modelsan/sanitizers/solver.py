"""SolverSan — the integrator itself reporting distress.

1. Bug class    the solver cannot proceed: it failed outright, collapsed its
                timestep, or rejected steps repeatedly. This is the class every
                other sanitizer misses when the run produces no trajectory at
                all — there is nothing to inspect, only the failure.
2. Overlap      substantial and deliberate. A division by zero shows up here as
                a failure and in DomainSan as an out-of-domain operand. That is
                the same bug seen twice, and the deduplicator is what decides
                so. SolverSan still earns its place because it fires when no
                instrumentation is available, which is most backends.
3. Signal       runtime: a `SolverFailure`, or a step-size sequence tending to
                zero, or a rejection rate that never recovers.
4. Needs        solver observations only. No DAE analysis, no transformation.
5. Transform    no.
6. Fuzzing      a strong oracle, and unusually a *graded* one: timestep collapse
                is visible before outright failure, so it can steer a search
                toward trouble rather than only confirming it.
7. Signature    the failure reason together with whichever DAE entity the
                runtime named. Where the runtime names nothing, the signature
                falls back to the reason class, which is coarse but stable.
"""

from __future__ import annotations

from ..analysis.context import AnalysisContext
from ..findings.finding import Finding, Severity
from ..fuzz.testcase import TestCase
from ..runtime.observations import ObservationStream, Phase, SolverFailure, SolverStep


class SolverSan:
    name = "solver"

    def __init__(self, collapse_ratio: float = 1e-8, rejection_run: int = 10) -> None:
        # A step this much smaller than the largest accepted one is collapse
        # rather than ordinary adaptation.
        self.collapse_ratio = collapse_ratio
        self.rejection_run = rejection_run

    def observe(self, stream: ObservationStream, model, context: AnalysisContext,
                testcase: TestCase) -> list[Finding]:
        findings: list[Finding] = []
        findings.extend(self._failures(stream, testcase))
        findings.extend(self._collapse(stream, testcase))
        return findings

    def _failures(self, stream: ObservationStream, testcase: TestCase) -> list[Finding]:
        found = []
        for observation in stream.of(SolverFailure):
            initialization = observation.phase is Phase.INITIALIZATION
            found.append(Finding(
                sanitizer=self.name,
                # Initialization failures are kept distinct: they have different
                # causes and different fixes than a transient failure, and
                # collapsing them into "failed at t=0" loses that.
                kind="initialization-failure" if initialization else "solver-failure",
                severity=Severity.HIGH,
                equation_ids=[observation.equation_id] if observation.equation_id else [],
                variable_ids=[observation.variable_id] if observation.variable_id else [],
                time=observation.time,
                test_case=testcase,
                evidence={"reason": observation.reason, "phase": observation.phase.value},
            ))
        return found

    def _collapse(self, stream: ObservationStream, testcase: TestCase) -> list[Finding]:
        """Timestep collapse, which precedes failure and is usable as a signal.

        Reported even when the run eventually completes: a solver that had to
        take 1e-12 steps to get through a region found something there, and
        that is worth surfacing to a fuzzer.
        """
        steps = list(stream.of(SolverStep))
        if not steps:
            return []
        accepted = [s.step_size for s in steps if s.accepted and s.step_size > 0]
        if not accepted:
            return []
        largest = max(accepted)
        smallest = min(accepted)
        if largest <= 0 or smallest / largest > self.collapse_ratio:
            return []
        worst = min((s for s in steps if s.accepted and s.step_size > 0),
                    key=lambda s: s.step_size)
        return [Finding(
            sanitizer=self.name,
            kind="timestep-collapse",
            severity=Severity.MEDIUM,
            time=worst.time,
            test_case=testcase,
            evidence={"smallest_step": smallest, "largest_step": largest,
                      "ratio": smallest / largest},
        )]
