"""Stable identity for a bug, independent of the execution that found it.

Two runs that trigger the same defect with different parameter values, at
different times, on different models must produce the same signature. Otherwise
every fuzzing campaign reports thousands of "unique" bugs and the count means
nothing.

The rule is: a signature is built only from things that are properties of the
*model*, never of the *run*.
"""

from __future__ import annotations

import hashlib

from .finding import Finding

# Deliberately excluded from every signature. Listed rather than merely omitted
# so the intent survives future edits.
NEVER_IN_SIGNATURE = frozenset({"time", "test_case", "value", "step_size", "seed"})


def compute(finding: Finding) -> str:
    """A short, stable identifier for what bug this is.

    Built from the sanitizer, the violation kind, and whichever DAE entities the
    sanitizer chose to anchor on. Anchoring is the sanitizer's decision because
    it is the sanitizer that knows what makes two occurrences the same:
    DomainSan anchors on the expression performing the unsafe operation,
    RangeSan on the variable and the bound it broke, SingularSan on the block.
    """
    parts = [finding.sanitizer, finding.kind]
    for label, ids in (
        ("eq", finding.equation_ids),
        ("var", finding.variable_ids),
        ("par", finding.parameter_ids),
        ("expr", finding.expression_ids),
    ):
        if ids:
            parts.append(f"{label}:{','.join(str(i) for i in sorted(set(ids)))}")

    # Source location is included when present, because the same defect reached
    # through two different instantiations of one component is one bug — the
    # DAE ids differ per model, the declaration site does not.
    if finding.source_locations:
        first = finding.source_locations[0]
        parts.append(f"src:{first.file}:{first.line}")

    digest = hashlib.sha1("|".join(parts).encode()).hexdigest()[:12]
    return f"{finding.sanitizer}:{finding.kind}:{digest}"


def attach(findings: list[Finding]) -> list[Finding]:
    """Fill in signatures and execution ordering for a run's findings."""
    for index, finding in enumerate(findings):
        finding.sequence = index
        finding.signature = compute(finding)
    return findings
