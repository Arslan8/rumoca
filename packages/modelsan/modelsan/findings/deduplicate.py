"""Grouping findings into bugs.

Detection and deduplication are separate on purpose: a sanitizer that also
decided what was novel would need to know about every other sanitizer's output,
which is exactly the coupling the architecture forbids.

This starts as signature equality. Source location, dependency structure and
cross-sanitizer evidence can be folded in later without any sanitizer changing.
"""

from __future__ import annotations

from collections import OrderedDict
from dataclasses import dataclass, field

from .finding import Finding


@dataclass
class Bug:
    """One distinct defect, and every finding that witnessed it."""

    signature: str
    findings: list[Finding] = field(default_factory=list)

    @property
    def first(self) -> Finding:
        return self.findings[0]

    @property
    def occurrences(self) -> int:
        return len(self.findings)

    @property
    def sanitizers(self) -> set[str]:
        """Which sanitizers saw it — useful for measuring detector overlap."""
        return {f.sanitizer for f in self.findings}


class BugDatabase:
    """Accumulates findings across executions and groups them by signature."""

    def __init__(self) -> None:
        self._bugs: OrderedDict[str, Bug] = OrderedDict()

    def add(self, finding: Finding) -> Bug:
        bug = self._bugs.get(finding.signature)
        if bug is None:
            bug = Bug(signature=finding.signature)
            self._bugs[finding.signature] = bug
        bug.findings.append(finding)
        return bug

    def extend(self, findings: list[Finding]) -> None:
        for finding in findings:
            self.add(finding)

    @property
    def bugs(self) -> list[Bug]:
        return list(self._bugs.values())

    def __len__(self) -> int:
        return len(self._bugs)

    def by_sanitizer(self) -> dict[str, int]:
        counts: dict[str, int] = {}
        for bug in self._bugs.values():
            counts[bug.first.sanitizer] = counts.get(bug.first.sanitizer, 0) + 1
        return counts

    def overlap(self) -> list[Bug]:
        """Bugs several sanitizers reported *under the same signature*.

        This is structurally almost always empty, and that is correct rather
        than a defect: a signature begins with the sanitizer's name, because
        DomainSan's view of a division by zero and SolverSan's view of the
        resulting failure are different statements about the model and should
        not collapse into one.

        For "did several sanitizers see one event", use
        `findings.correlate.summarize`, which groups across sanitizers by
        shared anchors and execution order instead.
        """
        return [bug for bug in self._bugs.values() if len(bug.sanitizers) > 1]
