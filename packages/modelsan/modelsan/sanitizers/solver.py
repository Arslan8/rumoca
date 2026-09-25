"""SolverSan — a broad failure oracle over executions that produced no result.

1. Bug class    the execution did not deliver a usable answer: it failed during
                initialization or integration, or its timestep collapsed. This
                is the class every trajectory-based sanitizer misses, because
                there is no trajectory to inspect.
2. Overlap      large, and intended. A division by zero is a SolverSan finding
                and a DomainSan finding; a singular block will be a SolverSan
                finding and a SingularitySan finding. Deduplication decides they
                are one bug.
3. Signal       an explicit failure observation, or a step-size sequence
                collapsing toward zero.
4. Needs        OBSERVE_FAILURE, which every backend can provide. Step collapse
                additionally wants OBSERVE_SOLVER_STEPS and degrades cleanly
                without it.
5. Transform    no.
6. Fuzzing      a strong oracle, and unusually a graded one: collapse is visible
                before outright failure, so it can steer a search rather than
                only confirm.
7. Signature    the normalized failure kind and phase, plus whatever entity the
                runtime named. Where nothing is named the signature is coarse
                but stable.

**This is a failure oracle, not a root-cause sanitizer.** A solver failure is
often the last symptom of a chain:

    parameter configuration -> algebraic block becomes singular -> solver fails
    bad event behaviour     -> timestep collapses               -> solver fails

SolverSan reports that the execution failed and how the runtime described it. It
does not attempt to identify the underlying cause, and it is not reduced or
suppressed when a more specific sanitizer also fires — that correlation is the
deduplicator\'s job, and the sequence is preserved so it remains possible.
"""

from __future__ import annotations

from ..analysis.context import AnalysisContext
from ..findings.finding import Finding, Severity, SourceLocation
from ..backends.compile_diagnostics import source_labels
from ..fuzz.testcase import TestCase
from ..instrumentation.capability import Capability
from ..runtime.failures import ExecutionPhase, FailureKind
from ..runtime.observations import (
    BackendFailure,
    CompilationFailure,
    ExecutionFailureObservation,
    ObservationStream,
    SolverStep,
)

#: Failure kinds that describe the *tool*, not the model. Reported so coverage
#: stays visible, but at INFO: counting these as model bugs is how a build
#: failure becomes a false finding.
TOOL_FAILURES = (BackendFailure,)


class SolverSan:
    name = "solver"

    requires = {
        "failure": frozenset({Capability.OBSERVE_FAILURE}),
        "collapse": frozenset({Capability.OBSERVE_SOLVER_STEPS}),
    }

    def __init__(self, collapse_ratio: float = 1e-8) -> None:
        self.collapse_ratio = collapse_ratio

    def observe(self, stream: ObservationStream, model, context: AnalysisContext,
                testcase: TestCase) -> list[Finding]:
        return self._failures(stream, testcase) + self._collapse(stream, testcase)

    def _failures(self, stream: ObservationStream, testcase: TestCase) -> list[Finding]:
        found = []
        for observation in stream.of(ExecutionFailureObservation):
            interrupted = observation.kind is FailureKind.ABORTED
            tool_side = isinstance(observation, TOOL_FAILURES) or interrupted
            compiler_proof = (observation.diagnostic
                              if isinstance(observation, CompilationFailure) else {})
            found.append(Finding(
                sanitizer=self.name,
                # Phase is part of the kind: an initialization failure is a
                # different defect from a transient one and must not collapse
                # into "failed at t=0".
                kind=("compile-time-array-bounds" if compiler_proof and observation.kind is FailureKind.ARRAY_BOUNDS
                      else "execution-aborted" if interrupted else "backend-failure" if tool_side
                      else f"{observation.phase.value}-failure"),
                severity=Severity.INFO if tool_side else Severity.HIGH,
                canonical_anchors=([observation.canonical]
                                   if observation.canonical else []),
                backend_anchors=([observation.backend]
                                 if observation.backend else []),
                source_locations=[SourceLocation(label['file'], label['line'], label['column'])
                                  for label in source_labels(compiler_proof)],
                phase=observation.phase,
                time=observation.time,
                test_case=testcase,
                evidence={
                    "failure_kind": observation.kind.value,
                    "reason": observation.reason,
                    # Kept verbatim so the classifier can be improved later
                    # without re-running a corpus.
                    "raw": observation.raw[:400],
                    "tool_side": tool_side,
                    **({'compiler_diagnostic': compiler_proof,
                        'proof_stage': 'constant-evaluation'} if compiler_proof else {}),
                },
            ))
        return found

    def _collapse(self, stream: ObservationStream, testcase: TestCase) -> list[Finding]:
        """Timestep collapse, which precedes failure and is usable as a signal.

        Reported even when the run completes: a solver forced down to 1e-12
        found something there, and that is worth handing to a fuzzer.
        """
        steps = [s for s in stream.of(SolverStep) if s.accepted and s.step_size > 0]
        if not steps:
            return []
        largest = max(s.step_size for s in steps)
        worst = min(steps, key=lambda s: s.step_size)
        if largest <= 0 or worst.step_size / largest > self.collapse_ratio:
            return []
        return [Finding(
            sanitizer=self.name,
            kind="timestep-collapse",
            severity=Severity.MEDIUM,
            phase=ExecutionPhase.SIMULATION,
            time=worst.time,
            test_case=testcase,
            evidence={"smallest_step": worst.step_size, "largest_step": largest,
                      "ratio": worst.step_size / largest},
        )]
