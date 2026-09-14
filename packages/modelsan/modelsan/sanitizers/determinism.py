"""DeterminismSan — the same configuration producing different answers.

1. Bug class    hidden state. A model that gives two answers to one question
                has something the DAE does not describe: an external function
                with side effects, an uninitialized value, a solver reading
                something it should not, iteration order leaking into results.
2. Overlap      none. Every other sanitizer judges a single run against a
                property; this one judges two runs against each other, so it
                can fire where every individual run looks perfect.
3. Signal       two executions of one `TestCase` disagreeing on the trajectory,
                the event sequence, or the final state.
4. Needs        the ability to run the same case twice. No instrumentation, no
                DAE analysis.
5. Transform    no.
6. Fuzzing      an oracle, and a cheap one — it needs no expected value, only a
                second run.
7. Signature    the sanitizer plus what disagreed. Deliberately coarse: a model
                is either reproducible or it is not, and which variable exposed
                it is evidence.

A caveat worth stating: a genuinely nondeterministic *solver* would also trip
this. Anything it reports needs that ruled out before it is called a model bug —
the same discipline that removed two Rumoca-only findings from the MSL set.
"""

from __future__ import annotations

from ..backends.base import ExecutionResult
from ..findings.finding import Finding, Severity
from ..fuzz.testcase import TestCase
from .comparison import compare_events, compare_traces


class DeterminismSan:
    name = "determinism"

    #: Needs no capability; it needs the *pipeline* to run a case more than
    #: once, which is a scheduling property rather than an observation one.
    requires = {"differential": frozenset()}
    repeats = 2

    def compare(self, results: dict[str, ExecutionResult], model,
                testcase: TestCase) -> list[Finding]:
        runs = [r for r in results.values() if r.informative]
        if len(runs) < 2:
            return []
        first, second = runs[0], runs[1]

        if first.status is not second.status:
            return [Finding(
                sanitizer=self.name, kind="status-nondeterminism",
                severity=Severity.HIGH, test_case=testcase,
                evidence={"first": first.status.value, "second": second.status.value},
            )]

        event_mismatch = compare_events(first, second)
        if event_mismatch:
            return [Finding(
                sanitizer=self.name, kind="event-nondeterminism",
                severity=Severity.HIGH, test_case=testcase,
                evidence={"detail": event_mismatch},
            )]

        # Two runs of one build should agree bit for bit, so the tolerance here
        # is far tighter than the cross-tool one: any visible difference is the
        # finding.
        divergences = compare_traces(first, second, rtol=0.0, atol=1e-12)
        return [Finding(
            sanitizer=self.name, kind="trajectory-nondeterminism",
            severity=Severity.HIGH,
            time=divergences[0].time, test_case=testcase,
            evidence={"variable": divergences[0].variable,
                      "first": divergences[0].left,
                      "second": divergences[0].right},
        )] if divergences else []
