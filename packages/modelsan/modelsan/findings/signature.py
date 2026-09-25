"""Stable identity for a bug, independent of the execution that found it.

Built only from properties of the *model*, never of the run. Two campaigns that
trigger one defect with different values at different times must agree.

Canonical and backend-anchored signatures are deliberately *not* interchangeable
and are marked as such. A backend-only signature identifies "this variable name,
in this tool"; a canonical one identifies an exact DAE entity. Merging them is a
later cross-backend deduplication step that needs evidence, not an assumption
made here by spelling them the same way.
"""

from __future__ import annotations

import hashlib

from ..runtime.anchors import AnchorQuality
from .finding import Finding

# Excluded from every signature. Listed rather than merely omitted so the intent
# survives future edits.
NEVER_IN_SIGNATURE = frozenset({"time", "test_case", "value", "step_size", "seed"})


def compute(finding: Finding) -> str:
    """A short, stable identifier for what bug this is."""
    parts = [finding.sanitizer, finding.kind]
    # Distinct declared behavioral properties can concern the same signal.
    if finding.evidence.get("contract_id"):
        parts.append(f"contract:{finding.evidence['contract_id']}")
    quality = finding.anchor_quality

    if quality is AnchorQuality.CANONICAL:
        parts += sorted(f"{a.kind.value}:{a.dae_id}" for a in finding.canonical_anchors)
    elif quality is AnchorQuality.BACKEND_ONLY:
        # Namespaced by backend: the same name in two tools is not known to be
        # the same entity, and a signature must not assert that it is.
        parts += sorted(f"{a.backend}/{a.name}" for a in finding.backend_anchors)
    else:
        # No entity anchor at all — a whole-execution failure. The kind plus the
        # failure class is as specific as the evidence supports.
        reason = finding.evidence.get("failure_kind") or finding.evidence.get("reason", "")
        parts.append(f"exec:{str(reason)[:60]}")

    # A source location makes the same component defect one bug across the many
    # models that instantiate it: the DAE ids differ per model, the declaration
    # site does not.
    if finding.source_locations:
        first = finding.source_locations[0]
        parts.append(f"src:{first.file}:{first.line}")

    # The primary anchor is spelled out rather than only folded into the hash.
    # A signature that has to be looked up to mean anything is a worse tool for
    # triage than one that says `range:below-min:var91` on sight; the digest is
    # still there to keep distinct bugs distinct when the anchor is not unique.
    digest = hashlib.sha1("|".join(parts).encode()).hexdigest()[:8]
    return f"{finding.sanitizer}:{finding.kind}:{_anchor_label(finding)}:{digest}"


def _anchor_label(finding: Finding) -> str:
    """A short, readable identifier for what the finding is attached to.

    Backend anchors keep their backend prefix, so a signature never suggests
    that a name observed in one tool is known to be the same entity as the same
    name in another.
    """
    quality = finding.anchor_quality
    if quality is AnchorQuality.CANONICAL:
        first = finding.canonical_anchors[0]
        return f"{first.kind.value[:3]}:{first.dae_id}"
    if quality is AnchorQuality.BACKEND_ONLY:
        first = finding.backend_anchors[0]
        return f"{first.backend}/{first.name}"[:64]
    return "exec"


def attach(findings: list[Finding]) -> list[Finding]:
    for index, finding in enumerate(findings):
        finding.sequence = index
        finding.signature = compute(finding)
    return findings
