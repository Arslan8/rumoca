"""Wiring the layers together. The only component that knows all of them exist.

Each layer below is independently testable and independently replaceable; this
is where the flow in the architecture diagram is actually expressed:

    DAE -> analysis -> instrumentation -> execution -> observations
                                                          |
                                            sanitizers <--+
                                                |
                                          findings -> dedup -> reporting
"""

from __future__ import annotations

from dataclasses import dataclass, field

from .analysis.context import AnalysisContext
from .backends.base import ExecutionResult, Status
from .findings.deduplicate import BugDatabase
from .findings.finding import Finding
from .findings.signature import attach
from .fuzz.hints import FuzzHint, merge
from .fuzz.testcase import NOMINAL, TestCase
from .instrumentation.planner import InstrumentationPlanner, Plan
from .sanitizers.registry import SanitizerRegistry


@dataclass
class RunOutcome:
    """Everything one campaign over one model produced."""

    model_name: str
    baseline: ExecutionResult | None = None
    database: BugDatabase = field(default_factory=BugDatabase)
    hints: list[FuzzHint] = field(default_factory=list)
    plan: Plan | None = None
    executed: int = 0
    skipped_sanitizers: set[str] = field(default_factory=set)
    note: str = ""


class Pipeline:
    def __init__(self, registry: SanitizerRegistry, backend) -> None:
        self.registry = registry
        self.backend = backend

    def collect_hints(self, model, context: AnalysisContext) -> list[FuzzHint]:
        hints: list[FuzzHint] = []
        for sanitizer in self.registry.hint_providers():
            hints.extend(sanitizer.hints(model, context))
        return merge(hints)

    def plan_instrumentation(self, model, context: AnalysisContext) -> Plan:
        requests = []
        for sanitizer in self.registry.instrumentation_requesters():
            requests.extend(sanitizer.requests(model, context))
        capabilities = getattr(self.backend, "capabilities", frozenset())
        return InstrumentationPlanner(capabilities).plan(requests)

    def judge(self, result: ExecutionResult, model, context: AnalysisContext,
              testcase: TestCase) -> list[Finding]:
        """Run every runtime observer over one execution.

        Ordering is preserved across sanitizers so a causal chain — conditioning,
        then step rejection, then a NaN — stays reconstructible.
        """
        findings: list[Finding] = []
        for sanitizer in self.registry.runtime_observers():
            findings.extend(
                sanitizer.observe(result.observations, model, context, testcase))
        findings.sort(key=lambda f: (f.time if f.time is not None else 0.0))
        return attach(findings)

    def run(self, model, model_path: str, model_name: str,
            testcases: list[TestCase] | None = None) -> RunOutcome:
        outcome = RunOutcome(model_name=model_name)
        context = AnalysisContext(model)

        outcome.hints = self.collect_hints(model, context)
        outcome.plan = self.plan_instrumentation(model, context)
        outcome.skipped_sanitizers = outcome.plan.skipped_sanitizers()

        if not self.backend.prepare(model_path, model_name):
            outcome.note = "backend could not build the model"
            return outcome

        # Static analyzers do not need an execution, but they run after the
        # build so that a model the backend cannot handle is reported as such
        # rather than as a clean static result.
        for sanitizer in self.registry.static_analyzers():
            outcome.database.extend(attach(sanitizer.analyze(model, context)))

        baseline = self.backend.run(NOMINAL, outcome.plan.satisfied)
        outcome.baseline = baseline
        outcome.executed += 1
        if not baseline.ok:
            # Without a clean baseline nothing can be attributed to a test case;
            # the first candidate tried would be blamed for a pre-existing
            # failure. Report the baseline itself and stop.
            outcome.note = ("model does not run at its declared values: "
                            f"{baseline.message[:120]}")
            return outcome

        for testcase in (testcases or []):
            result = self.backend.run(testcase, outcome.plan.satisfied)
            outcome.executed += 1
            if not result.ran:
                continue
            outcome.database.extend(self.judge(result, model, context, testcase))

        # The baseline is judged too: a violation present at declared values is
        # a finding about the model that needs no perturbation at all.
        outcome.database.extend(self.judge(baseline, model, context, NOMINAL))
        return outcome
