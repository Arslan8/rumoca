"""PhysicalSan — physical invariants, across arbitrary domains.

1. Bug class    a model that permits, or reaches, a state physics forbids:
                negative resistance, negative absolute temperature, a state of
                charge above one. Distinct from every other sanitizer because
                it needs no failure at all — a run that completes with a
                negative mass is wrong, and nothing else here notices.
2. Overlap      it subsumes part of SingularitySan's motivation (`m > 0`) but
                arrives from the opposite direction: SingularitySan asks what
                breaks the solver, this asks what physics forbids. They agree
                on mass and disagree on damping, where `d = 0` is structurally
                harmless and physically fine but `d < 0` is neither.
3. Signal       static: a declared value violates the invariant, or a
                declaration permits values that would. runtime: an observed
                value violates it.
4. Needs        the DAE's declared `quantity` metadata. Runtime rules
                additionally need OBSERVE_VARIABLE.
5. Transform    not yet. Runtime rules are checked against observations; a DAE
                pass inserting in-model assertions is the natural next step and
                the invariant representation already supports it.
6. Fuzzing      strong and principled: an invariant states exactly which values
                are forbidden, so hints aim just outside the physical domain
                rather than guessing.
7. Signature    the rule id plus the DAE variable — stable across models and
                across runs.

This is infrastructure, not a circuit checker. It contains no domain knowledge;
all of it lives in `physical/domains/`.
"""

from __future__ import annotations

from ..analysis.context import AnalysisContext
from ..findings.finding import Finding, Severity, SourceLocation
from ..fuzz.hints import FuzzHint
from ..fuzz.testcase import TestCase
from ..instrumentation.capability import Capability
from ..physical.domains import BUILTIN
from ..physical.engine import PhysicalEngine
from ..physical.invariant import Comparison, Enforcement
from ..physical.rules import RuleRegistry
from ..runtime.anchors import CanonicalAnchor, EntityKind
from ..runtime.observations import ObservationStream, VariableObservation

#: Just outside a bound, so a probe lands in the forbidden region rather than
#: on its edge where floating point makes the verdict arbitrary.
MARGIN = 1e-6


class PhysicalSan:
    name = "physical"

    requires = {
        "static": frozenset({Capability.CANONICAL_MODEL}),
        "hints": frozenset({Capability.CANONICAL_MODEL}),
        "runtime": frozenset({Capability.OBSERVE_VARIABLE,
                              Capability.CANONICAL_MODEL}),
    }

    def __init__(self, packs=None, domains: set | None = None) -> None:
        registry = RuleRegistry()
        for pack in (packs if packs is not None else BUILTIN):
            registry.register(pack)
        self.engine = PhysicalEngine(registry)
        self.domains = domains
        self.registry = registry

    # ── static ───────────────────────────────────────────────────────────────

    def analyze(self, model, context: AnalysisContext) -> list[Finding]:
        analysis = self.engine.analyze(model, self.domains)
        findings = []

        for violation in analysis.static_violations:
            findings.append(self._finding(
                violation.invariant,
                kind="physical-invariant-violated",
                severity=Severity.HIGH,
                evidence={"observed": violation.observed,
                          "required": str(violation.invariant.predicate),
                          "where": violation.where}))

        # A declaration that *permits* a forbidden value is a weaker but real
        # defect: it has not happened yet, and nothing in the model stops it.
        for invariant in self.engine.unbounded(model, self.domains):
            if invariant in (v.invariant for v in analysis.static_violations):
                continue
            if invariant.predicate.op not in (Comparison.GT, Comparison.GE):
                continue
            findings.append(self._finding(
                invariant,
                kind="physical-domain-unenforced",
                severity=Severity.MEDIUM,
                evidence={"required": str(invariant.predicate),
                          "note": "the declaration permits values physics forbids"}))
        return findings

    # ── hints ────────────────────────────────────────────────────────────────

    def hints(self, model, context: AnalysisContext) -> list[FuzzHint]:
        """Probe just outside each physical domain.

        Unlike a generic boundary probe this knows *why* the value is
        interesting, so the reason travels with the hint into any finding.
        """
        by_id = {v.id: v for v in model.variables}
        found = []
        for invariant in self.engine.unbounded(model, self.domains):
            for variable_id in invariant.variable_ids:
                variable = by_id.get(variable_id)
                if variable is None or not variable.is_parameter:
                    continue
                bound = invariant.predicate.right.value
                if bound is None:
                    continue
                op = invariant.predicate.op
                if op is Comparison.GT:
                    values = (bound, bound - MARGIN)
                elif op is Comparison.GE:
                    values = (bound - MARGIN,)
                elif op is Comparison.LE:
                    values = (bound + MARGIN,)
                else:
                    values = (bound + MARGIN,)
                found.append(FuzzHint(
                    target=variable.name, values=values,
                    reason=f"{invariant.domain.value}: {invariant.rule.origin[:70]}",
                    source=self.name, variable_ids=(variable.id,)))
        return found

    # ── runtime ──────────────────────────────────────────────────────────────

    def observe(self, stream: ObservationStream, model, context: AnalysisContext,
                testcase: TestCase) -> list[Finding]:
        """Check invariants that must hold throughout the run."""
        analysis = self.engine.analyze(model, self.domains)
        watched = {}
        for invariant in analysis.runtime:
            for variable_id in invariant.variable_ids:
                watched.setdefault(variable_id, []).append(invariant)
        if not watched:
            return []

        worst: dict[str, Finding] = {}
        for observation in stream.of(VariableObservation):
            anchor = observation.canonical
            if anchor is None:
                continue  # a runtime rule must anchor to the DAE variable it constrains
            for invariant in watched.get(anchor.dae_id, ()):
                if invariant.predicate.holds({anchor.dae_id: observation.value}) is not False:
                    continue
                bound = invariant.predicate.right.value or 0.0
                excess = abs(observation.value - bound)
                previous = worst.get(invariant.id)
                if previous and previous.evidence["excess"] >= excess:
                    continue
                worst[invariant.id] = self._finding(
                    invariant,
                    kind="physical-invariant-violated",
                    severity=Severity.HIGH,
                    time=observation.time, testcase=testcase,
                    evidence={"observed": observation.value,
                              "required": str(invariant.predicate),
                              "excess": excess, "where": "runtime"})
        return list(worst.values())

    # ── shared ───────────────────────────────────────────────────────────────

    def _finding(self, invariant, kind, severity, time=None, testcase=None,
                 evidence=None) -> Finding:
        return Finding(
            sanitizer=self.name,
            kind=kind,
            severity=severity,
            canonical_anchors=[CanonicalAnchor(EntityKind.VARIABLE, v)
                               for v in invariant.variable_ids],
            source_locations=_location(invariant.source),
            time=time,
            test_case=testcase,
            evidence={
                # Both provenances travel with the finding: where the model said
                # it, and where the claim that it is wrong came from.
                "domain": invariant.domain.value,
                "rule": invariant.rule.rule_id,
                "rule_origin": invariant.rule.origin,
                "rule_reference": invariant.rule.reference,
                "matched_by": invariant.evidence,
                **(evidence or {}),
            },
        )


def _location(source) -> list[SourceLocation]:
    span = getattr(source, "span", None) if source else None
    if span is None:
        return []
    return [SourceLocation(file=getattr(span, "source_name", "") or "?",
                           line=getattr(span, "line", 0) or 0)]
