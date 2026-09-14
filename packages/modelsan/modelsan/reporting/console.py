"""Human-readable output. The only place findings become text."""

from __future__ import annotations

from ..findings.deduplicate import BugDatabase
from ..findings.finding import Finding


class ConsoleReporter:
    name = "console"

    def __init__(self, show_evidence: bool = False) -> None:
        self.show_evidence = show_evidence

    def report(self, findings: list[Finding]) -> str:
        if not findings:
            return "no findings"
        lines = []
        for finding in sorted(findings, key=lambda f: (f.time or 0, f.sequence)):
            lines.append(f"  {finding.summary()}")
            if self.show_evidence and finding.evidence:
                for key, value in sorted(finding.evidence.items()):
                    lines.append(f"        {key}: {value}")
        return "\n".join(lines)

    def summarize(self, database: BugDatabase) -> str:
        """The evaluation numbers, computed rather than parsed out of a log."""
        lines = [f"{len(database)} distinct bug(s)"]
        for sanitizer, count in sorted(database.by_sanitizer().items()):
            lines.append(f"  {count:4}  {sanitizer}")
        overlap = database.overlap()
        if overlap:
            lines.append(f"\n{len(overlap)} bug(s) seen by more than one sanitizer:")
            for bug in overlap:
                lines.append(f"  {bug.signature}  <- {', '.join(sorted(bug.sanitizers))}")
        return "\n".join(lines)
