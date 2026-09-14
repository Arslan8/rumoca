"""Machine-readable output, so evaluation never parses terminal text.

Everything a campaign needs to compute — unique bugs, bugs per sanitizer, bugs
per model, sanitizer overlap, time-to-bug — comes from this.
"""

from __future__ import annotations

import json
from dataclasses import asdict, is_dataclass
from pathlib import Path

from ..findings.deduplicate import BugDatabase
from ..findings.finding import Finding


def _plain(value):
    if is_dataclass(value) and not isinstance(value, type):
        return {k: _plain(v) for k, v in asdict(value).items()}
    if isinstance(value, dict):
        return {k: _plain(v) for k, v in value.items()}
    if isinstance(value, (list, tuple, set)):
        return [_plain(v) for v in value]
    if hasattr(value, "value") and hasattr(value, "name"):  # Enum
        return value.value
    return value


class JSONReporter:
    name = "json"

    def report(self, findings: list[Finding]) -> str:
        return json.dumps([_plain(f) for f in findings], indent=1, default=str)

    def summarize(self, database: BugDatabase, model: str = "") -> dict:
        return {
            "model": model,
            "unique_bugs": len(database),
            "bugs_per_sanitizer": database.by_sanitizer(),
            "overlap": [
                {"signature": bug.signature,
                 "sanitizers": sorted(bug.sanitizers),
                 "occurrences": bug.occurrences}
                for bug in database.overlap()
            ],
            "bugs": [
                {"signature": bug.signature,
                 "sanitizer": bug.first.sanitizer,
                 "kind": bug.first.kind,
                 "severity": bug.first.severity.value,
                 "occurrences": bug.occurrences,
                 "first_time": bug.first.time,
                 "source": [str(s) for s in bug.first.source_locations],
                 "test_case": bug.first.test_case.describe()
                 if bug.first.test_case else None}
                for bug in database.bugs
            ],
        }

    def write(self, database: BugDatabase, path: str | Path, model: str = "") -> Path:
        destination = Path(path)
        destination.write_text(json.dumps(self.summarize(database, model), indent=1))
        return destination
