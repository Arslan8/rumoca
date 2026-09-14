"""DifferentialSan — two independent implementations disagreeing.

1. Bug class    a model, or a tool, that two mature implementations do not
                agree about. Without a reference answer this is the only
                available oracle for *correctness* as opposed to survival.
2. Overlap      none at the oracle level, and it is the one sanitizer that can
                adjudicate the others: a failure only one backend produces is
                that backend's gap, not the model's defect.
3. Signal       one `TestCase`, several backends, differing acceptance or
                differing trajectories.
4. Needs        two backends. No instrumentation.
5. Transform    no.
6. Fuzzing      a strong oracle over runs that all succeed.
7. Signature    the disagreement kind plus the variable, namespaced by the
                backend pair — a disagreement between A and B is not the same
                finding as one between A and C.

**It does not know how any tool is launched.** It receives `ExecutionResult`s
and compares them; where the results came from is the backend adapters' problem,
which is the whole reason that boundary exists.

**Interpretation is deliberately conservative.** Disagreement locates a problem
without saying whose it is. Rumoca failing where OpenModelica succeeds is far
more likely to be a Rumoca gap than an MSL bug, and treating it otherwise
already produced two false findings in this project.
"""

from __future__ import annotations

from ..backends.base import ExecutionResult, ExecutionStatus
from ..findings.finding import Finding, Severity
from ..fuzz.testcase import TestCase
from ..runtime.anchors import BackendAnchor, EntityKind
from .comparison import compare_traces


class DifferentialSan:
    name = "differential"

    requires = {"differential": frozenset()}

    def __init__(self, rtol: float = 0.05) -> None:
        self.rtol = rtol

    def compare(self, results: dict[str, ExecutionResult], model,
                testcase: TestCase) -> list[Finding]:
        # A backend that could not attempt the model says nothing about it.
        usable = {name: r for name, r in results.items() if r.informative}
        if len(usable) < 2:
            return []

        findings = self._acceptance(usable, testcase)
        findings += self._trajectories(usable, testcase)
        return findings

    def _acceptance(self, results: dict[str, ExecutionResult],
                    testcase: TestCase) -> list[Finding]:
        succeeded = sorted(n for n, r in results.items() if r.ok)
        failed = sorted(n for n, r in results.items() if not r.ok)
        if not succeeded or not failed:
            return []
        return [Finding(
            sanitizer=self.name,
            kind="acceptance-disagreement",
            # Medium, not high: this locates a disagreement, and the most
            # common cause is a coverage gap in the failing tool rather than a
            # defect in the model.
            severity=Severity.MEDIUM,
            test_case=testcase,
            evidence={
                "succeeded": succeeded,
                "failed": failed,
                "failure": next((results[n].failure.message for n in failed
                                 if results[n].failure), ""),
                "note": "a failure in only one tool is more often that tool's "
                        "gap than the model's defect; confirm before reporting",
            },
        )]

    def _trajectories(self, results: dict[str, ExecutionResult],
                      testcase: TestCase) -> list[Finding]:
        running = sorted(n for n, r in results.items() if r.ok and r.has_trace)
        findings = []
        for index, left_name in enumerate(running):
            for right_name in running[index + 1:]:
                left, right = results[left_name], results[right_name]
                for divergence in compare_traces(left, right, rtol=self.rtol):
                    findings.append(Finding(
                        sanitizer=self.name,
                        kind=divergence.kind,
                        severity=Severity.MEDIUM,
                        backend_anchors=[
                            BackendAnchor(left_name, divergence.variable,
                                          EntityKind.VARIABLE),
                            BackendAnchor(right_name, divergence.variable,
                                          EntityKind.VARIABLE),
                        ],
                        time=divergence.time,
                        test_case=testcase,
                        evidence={
                            "variable": divergence.variable,
                            left_name: divergence.left,
                            right_name: divergence.right,
                            "detail": divergence.detail,
                        },
                    ))
        return findings
