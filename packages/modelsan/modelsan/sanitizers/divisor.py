"""DivisorSan — a denominator that a permitted configuration drives to zero.

1. Bug class    a division whose *complete denominator* can be made zero by an
                assignment the model permits. Not "a parameter that can be zero
                appears under a `/`" — that is a different and much weaker
                statement, and reporting it is what this pass used to do.
2. Overlap      DomainSan finds the division site. This decides whether the
                denominator can actually vanish, and exhibits the assignment.
3. Signal       static: a verified witness, plus the path condition under which
                the division executes.
4. Needs        the DAE. Nothing at runtime, so it covers models no backend can
                execute.
5. Transform    no.
6. Fuzzing      the strongest hints available: an exact assignment, already
                checked against the declared bounds.
7. Signature    the denominator's shape plus the witness.

**What changed, and why.** The previous implementation reported every parameter
appearing anywhere in a denominator, on the theory that a parameter that can be
zero can zero the expression containing it. That is false, and it was false
often:

    1 + c_b*B_N + B_N^n     c_b = 0 leaves 1 + B_N^n
    1 + alpha*(T - T_ref)   alpha = 0 leaves 1
    2*pi*fsNominal          pi is a constant and cannot be set at all

Each of those was filed as a finding. The discipline that removes all three is
the same one: **propose a concrete assignment, substitute it, and evaluate the
denominator.** If the result is not zero there is no finding. A parameter's
presence in an expression is not evidence about the expression's value.

Four further conditions must hold before a site is reported as a defect, and
each corresponds to a class of report this pass previously got wrong:

* **The assignment must be permitted.** Bounds, bounds inherited from the type,
  assertions, and whether the value is settable at all. A constant is never a
  witness.
* **The division must be in the source.** `L*der(i) = v` contains no division;
  the DAE contains `der(i) = v/L` because that is what a solver integrates. A
  division the compiler introduced is reported separately and is not evidence
  that the source contract is wrong.
* **The division must still execute under the witness.** `Ramp` divides by
  `duration`, and at `duration = 0` the model takes its step branch, so the
  division is unreachable at exactly the value that would zero it.
* **The denominator must not be asserted away from zero.** MSL writes
  `assert(d >= eps)` immediately above the division it protects; the artifact
  carries that relation, and matching it against the denominator is exact.

Sites that fail one of the last three are reported under their own kinds rather
than discarded, because "this division is guarded" is a useful thing for a
reader to be told, and a guard that is later found insufficient is a finding.
"""

from __future__ import annotations

from ..analysis.context import AnalysisContext
from ..contracts import ContractSet, ZeroBehavior, resolve
from ..divisor import (Environment, Site, Verdict, baseline, build, classify,
                       collect, find, guard_excludes)
from ..findings.finding import Finding, Severity, SourceLocation
from ..findings.location import locate
from ..fuzz.hints import FuzzHint
from ..instrumentation.capability import Capability
from ..runtime.anchors import CanonicalAnchor, EntityKind

class _NoWitness:
    """Stand-in for a site that needs no assignment to fail."""

    assignment: dict = {}


_NO_WITNESS = _NoWitness()


#: Reported, but not as a defect in the model.
#: Reported as unresolved. Not a defect claim, and not a clean bill of health.
UNRESOLVED_KIND = "divisor-zero-unresolved"

GUARDED_KINDS = {
    "asserted": "divisor-guarded-by-assertion",
    "unreachable": "divisor-unreachable-under-witness",
    "generated": "divisor-introduced-by-translation",
}


class DivisorSan:
    name = "divisor"

    requires = {
        "static": frozenset({Capability.CANONICAL_MODEL}),
        "hints": frozenset({Capability.CANONICAL_MODEL}),
    }

    def analyze(self, model, context: AnalysisContext) -> list[Finding]:
        environment = build(model)
        contracts = resolve(model, environment,
                            assumptions=getattr(context, "assumptions", None))
        findings: list[Finding] = []
        for site in collect(model, environment):
            finding = self._judge(site, environment, contracts)
            if finding is not None:
                findings.append(finding)
        return findings

    # ── one site ─────────────────────────────────────────────────────────────

    def _judge(self, site: Site, environment: Environment,
               contracts: ContractSet) -> Finding | None:
        """Decide one division, three ways.

        The question is `constraints AND path AND denominator == 0`. `SAT`
        reports with the assignment, `UNSAT` records the proof, and `UNKNOWN`
        reports as unresolved --- never as confirmed. Collapsing the third into
        either of the others is what this pass used to do, in both directions.
        """
        at_declared = baseline(site.denominator, environment)
        names = environment.names

        # A denominator already zero needs no assignment, and asking for one
        # first is how `constant Real c = 0; y = 1/c` came to be reported as
        # nothing at all: there is no knob to turn.
        if at_declared is not None and at_declared == 0.0:
            closed = guard_excludes(site, {}, environment)
            shared = self._evidence(site, environment, None, at_declared)
            if closed is not None:
                return self._finding(
                    site, GUARDED_KINDS["unreachable"], Severity.LOW, _NO_WITNESS,
                    {**shared, "verdict": "UNSAT",
                     "guard_that_excludes_it": closed,
                     "proof": f"the denominator is zero as declared, and {closed}",
                     "note": "the branch containing the division is not taken "
                             "where the denominator vanishes, so it is never "
                             "evaluated there"})
            return self._finding(
                site, "divisor-zero-at-declared-values", Severity.HIGH,
                _NO_WITNESS,
                {**shared, "verdict": "SAT",
                 "proof": "no assignment is needed: the denominator is zero at "
                          "the model's own declared values",
                 "note": "the division fails without anything being changed, so "
                         "no parameter can be blamed and none needs to be"})

        verdict = classify(site, environment)
        shared = self._evidence(site, environment, verdict, at_declared)

        if verdict.status == "UNSAT":
            # Suppressed, per the acceptance criterion --- but not all silently.
            # A denominator that simply cannot be zero (a constant, a sum of
            # positives) is not worth a line: 2660 of them in this corpus, one
            # per division in every model, which is noise rather than evidence.
            # A denominator the model *actively guards* is worth a line, because
            # the guard is a design decision a reader may want to challenge.
            if "excludes zero" in verdict.proof:
                return None
            kind = (GUARDED_KINDS["asserted"] if "asserts" in verdict.proof
                    else GUARDED_KINDS["unreachable"])
            return self._finding(
                site, kind, Severity.LOW, verdict.witness or _NO_WITNESS,
                {**shared,
                 "note": "reported so the guard can be seen and challenged, "
                         "not as a defect; zero is outside the domain this "
                         "division is evaluated in"})

        if verdict.status == "UNKNOWN":
            if verdict.witness is None:
                # Nothing to show: no assignment, no proof. Silence is right.
                return None
            return self._finding(
                site, "divisor-zero-unresolved", Severity.MEDIUM,
                verdict.witness,
                {**shared,
                 "note": "an assignment drives the denominator to zero, but "
                         "whether the division is evaluated there could not be "
                         "decided from the artifact; this is unresolved, not "
                         "confirmed"})

        if site.generated:
            return self._finding(
                site, GUARDED_KINDS["generated"], Severity.LOW, verdict.witness,
                {**shared, "generation": site.generation or "unknown",
                 "note": "this division was introduced by the compiler, not "
                         "written in the source; it is evidence about the "
                         "translation, not about the model's contract"})

        # The shared contract has the last word on what zero *means* for the
        # symbols this witness moves. A parameter that multiplies a derivative
        # gives an algebraic limit at zero, not an undefined quotient, and the
        # division the DAE shows is the compiler's own solved form.
        limited = self._supported_limit(verdict.witness, contracts)
        if limited is not None:
            return self._finding(
                site, GUARDED_KINDS["generated"], Severity.LOW, verdict.witness,
                {**shared, "contract": limited.explain(),
                 "contract_confidence": limited.confidence.value,
                 "note": "zero is a supported limit of this component rather "
                         "than a division by zero; the quotient the DAE shows "
                         "is the compiler's solved form, not the source"})

        relational = "equal to" in (verdict.witness.rationale or "")
        return self._finding(
            site,
            "divisor-zero-when-parameters-equal" if relational
            else "divisor-reachable-zero",
            Severity.HIGH, verdict.witness,
            {**shared,
             "note": ("the denominator is a difference, so it vanishes when the "
                      "two sides are equal; no `min` on either can express a "
                      "constraint between two parameters and an assertion is "
                      "the only mechanism") if relational else
                     ("a permitted assignment drives the complete denominator "
                      "to zero and the division is still evaluated there")})

    @staticmethod
    def _supported_limit(witness, contracts: ContractSet):
        """A contract saying zero is meaningful for every symbol moved.

        Every symbol, not any: a witness that zeroes one parameter whose zero
        is an ideal limit *and* another that genuinely divides is still a
        divide-by-zero.
        """
        if witness is None or not getattr(witness, "assignment", None):
            return None
        chosen = None
        for variable_id, value in witness.assignment.items():
            if value != 0.0:
                return None        # not a zero witness; the contract is silent
            contract = contracts.zero_is_safe(variable_id)
            if contract is None or contract.behavior in (
                    ZeroBehavior.FORBIDDEN,):
                return None
            chosen = chosen or contract
        return chosen

    def _evidence(self, site: Site, environment: Environment,
                  verdict: Verdict | None, at_declared: float | None) -> dict:
        """Everything a reader needs to check the claim without rerunning it."""
        witness = verdict.witness if verdict else None
        return {
            "denominator": repr(site.denominator)[:300],
            "witness": (witness.rendered(environment.names) if witness
                        else "none needed"),
            "witness_rationale": (witness.rationale if witness
                                  else "the denominator is zero as declared"),
            "denominator_at_witness": witness.residual if witness else 0.0,
            "denominator_at_declared_values": at_declared,
            "denominator_range": verdict.denominator_range if verdict else "",
            "path_condition": " and ".join(site.guards) or "always evaluated",
            "verdict": verdict.status if verdict else "SAT",
            "proof": verdict.proof if verdict else "",
            "constraints": self._constraints(site, environment, witness),
        }

    # ── reporting helpers ────────────────────────────────────────────────────

    @staticmethod
    def _constraints(site: Site, environment: Environment, witness) -> str:
        """What was consulted about each variable the witness moves."""
        if witness is None:
            return ""
        parts = []
        for variable_id in sorted(witness.assignment):
            domain = environment.domain(variable_id)
            name = environment.names.get(variable_id, str(variable_id))
            bound = []
            if domain.low != float("-inf"):
                bound.append(f"min={domain.low:g}")
            if domain.high != float("inf"):
                bound.append(f"max={domain.high:g}")
            if domain.reason:
                bound.append(domain.reason)
            parts.append(f"{name}: {', '.join(bound) or 'unbounded'}")
        return "; ".join(parts)

    def _finding(self, site: Site, kind: str, severity: Severity,
                 witness, evidence: dict) -> Finding:
        return Finding(
            sanitizer=self.name, kind=kind, severity=severity,
            canonical_anchors=[
                CanonicalAnchor(EntityKind.EXPRESSION, site.division.id),
                *[CanonicalAnchor(EntityKind.PARAMETER, i)
                  for i in sorted(witness.assignment)],
            ],
            source_locations=_location(site),
            evidence=evidence,
        )

    # ── fuzzing ──────────────────────────────────────────────────────────────

    def hints(self, model, context: AnalysisContext) -> list[FuzzHint]:
        environment = build(model)
        found, emitted = [], set()
        for site in collect(model, environment):
            if site.asserted or site.generated:
                continue
            witness = find(site.denominator, environment)
            if witness is None:
                continue
            if guard_excludes(site, witness.assignment, environment):
                continue
            for variable_id, value in witness.assignment.items():
                if variable_id in emitted:
                    continue
                if not environment.domain(variable_id).settable:
                    continue
                emitted.add(variable_id)
                found.append(FuzzHint(
                    target=environment.names.get(variable_id, ""),
                    values=(value,),
                    reason=f"zeroes {repr(site.denominator)[:80]} "
                           f"({witness.rationale})",
                    source=self.name, variable_ids=(variable_id,)))
        return found


def _location(site: Site) -> list[SourceLocation]:
    return locate(site.division.provenance)
