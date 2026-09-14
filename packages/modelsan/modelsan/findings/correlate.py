"""Grouping findings from *different* sanitizers that describe one event.

`BugDatabase` groups by signature, which answers "have we seen this bug before?".
It cannot answer "are these four findings one bug?", because a signature
deliberately begins with the sanitizer's name — DomainSan's view of a division
by zero and SolverSan's view of the resulting failure *should* be distinct
signatures, since they are distinct statements about the model.

That left `BugDatabase.overlap()` structurally always empty, which is
misleading: it reads as "no sanitizer overlap" when it means "overlap cannot be
expressed this way".

Correlation is the missing step. Within one execution, a single defect usually
surfaces as a sequence:

    parameter configuration
        -> algebraic block becomes singular   (SingularitySan)
        -> conditioning degrades              (ConditionSan)
        -> timestep collapses                 (SolverSan)
        -> a NaN appears                      (NumericSan)

Those are four findings and one bug. This groups them into an *episode* without
deciding which is the root cause — that judgement needs more than co-occurrence,
and asserting it here would be the same overreach as treating a single-tool
failure as a model defect.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from .finding import Finding


@dataclass
class Episode:
    """Findings from one execution that plausibly describe one event.

    `findings` keeps execution order, so the sequence above stays readable and
    a later root-cause analysis has the evidence it needs.
    """

    test_case_description: str
    findings: list[Finding] = field(default_factory=list)

    @property
    def sanitizers(self) -> list[str]:
        """In the order they fired, deduplicated — this is the causal chain."""
        seen, ordered = set(), []
        for finding in self.findings:
            if finding.sanitizer not in seen:
                seen.add(finding.sanitizer)
                ordered.append(finding.sanitizer)
        return ordered

    @property
    def is_multi_sanitizer(self) -> bool:
        return len(set(f.sanitizer for f in self.findings)) > 1

    @property
    def signatures(self) -> list[str]:
        return sorted({f.signature for f in self.findings if f.signature})

    @property
    def anchors(self) -> set[str]:
        return {a for f in self.findings for a in f.anchors}

    def timeline(self) -> list[str]:
        """The sequence, formatted the way a reader reconstructs causality."""
        lines = []
        for finding in sorted(self.findings,
                              key=lambda f: (f.time if f.time is not None else -1.0,
                                             f.sequence)):
            when = f"{finding.time:.3f}" if finding.time is not None else "  init"
            lines.append(f"{when}  {finding.sanitizer:14} {finding.kind}")
        return lines


def _shares_anchor(left: Finding, right: Finding) -> bool:
    """Whether two findings name any entity in common.

    Compared as rendered anchors so a canonical and a backend anchor never
    match by accident: `var:91` and `openmodelica/tank.level` are different
    strings even when they happen to be the same variable, which is correct —
    we do not know that they are.
    """
    return bool(set(left.anchors) & set(right.anchors))


def correlate(findings: list[Finding], *, window: float = 0.05) -> list[Episode]:
    """Group one execution's findings into episodes.

    Two findings join the same episode when they come from the same test case
    and either name a common entity or occur close together in simulation time.
    Time proximity is the weaker criterion and is why `window` is small: a
    cascade unfolds over a few solver steps, not over a whole run.

    Findings with no time at all — static analysis, initialization failures —
    are grouped by anchor only. A static finding and a runtime failure on the
    same variable is exactly the pairing worth seeing.
    """
    def related(finding: Finding, member: Finding) -> bool:
        if _shares_anchor(finding, member):
            return True
        return (finding.time is not None and member.time is not None
                and abs(finding.time - member.time) <= window)

    episodes: list[Episode] = []
    for finding in sorted(findings, key=lambda f: f.sequence):
        description = (finding.test_case.describe()
                       if finding.test_case is not None else "")
        # Every episode this finding relates to, not just the first. Taking the
        # first makes grouping depend on arrival order: a step collapse
        # compared against an untimed static finding before the NaN existed
        # would start its own episode and never merge, splitting one cascade in
        # two.
        matches = [e for e in episodes
                   if e.test_case_description == description
                   and any(related(finding, m) for m in e.findings)]
        if not matches:
            episode = Episode(test_case_description=description)
            episodes.append(episode)
        else:
            episode = matches[0]
            # This finding is the evidence that the matched episodes are one
            # event, so fold them together.
            for other in matches[1:]:
                episode.findings.extend(other.findings)
                episodes.remove(other)
        episode.findings.append(finding)

    for episode in episodes:
        episode.findings.sort(key=lambda f: f.sequence)
    return episodes


def summarize(findings: list[Finding]) -> dict:
    """Counts an evaluation needs, with the distinction made explicit.

    `findings` overstates how much is wrong; `episodes` is the number of
    distinct events; `multi_sanitizer_episodes` is how often several detectors
    saw one thing — which is the number that says whether the suite is
    diverse or merely redundant.
    """
    episodes = correlate(findings)
    multi = [e for e in episodes if e.is_multi_sanitizer]
    pairs: dict[tuple[str, ...], int] = {}
    for episode in multi:
        key = tuple(sorted(set(episode.sanitizers)))
        pairs[key] = pairs.get(key, 0) + 1
    return {
        "findings": len(findings),
        "episodes": len(episodes),
        "multi_sanitizer_episodes": len(multi),
        "co_occurrence": {"+".join(k): v for k, v in
                          sorted(pairs.items(), key=lambda kv: -kv[1])},
    }
