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

import re
from dataclasses import dataclass

from ..analysis.context import AnalysisContext
from ..contracts import ZeroBehavior
from ..physical.aggregate import FIELDS as _TENSOR_FIELDS
from ..findings.location import locate
from ..findings.finding import Finding, Severity, SourceLocation
from ..fuzz.hints import FuzzHint
from ..fuzz.testcase import TestCase
from ..instrumentation.capability import Capability
from ..physical.domains import BUILTIN
from ..physical.engine import PhysicalEngine, constant_value
from ..physical.invariant import Comparison, Enforcement, Predicate, Term
from ..physical.rules import RuleRegistry
from ..runtime.anchors import CanonicalAnchor, EntityKind
from ..runtime.observations import ObservationStream, VariableObservation
from ..semantics import SemanticBinder, SemanticMap
from ..semantics.profiles import profile_packs

FIELD_ORDER = tuple(_TENSOR_FIELDS)

#: Just outside a bound, so a probe lands in the forbidden region rather than
#: on its edge where floating point makes the verdict arbitrary.
MARGIN = 1e-6

#: Rule severity strings as the findings layer spells them.
_SEVERITY = {"high": Severity.HIGH, "medium": Severity.MEDIUM,
             "low": Severity.LOW}


@dataclass(frozen=True)
class _Premise:
    """Whether a rule may be enforced here, and on whose authority.

    The predicate travels with it because a user assumption can *change* it:
    `sign_domain = "nonnegative"` says the right claim is `R >= 0`, not the
    generic `R > 0`, and reporting the generic one would attribute to the user
    a rule they did not state.
    """

    state: str
    authority: str
    predicate: object
    semantic_role: str = ""
    canonical_declaration: str = ""
    source: str = ""
    reason: str = ""

    @property
    def established(self) -> bool:
        return self.state == "established"

    @property
    def refuted(self) -> bool:
        return self.state == "refuted"

    @property
    def evidence(self) -> dict:
        found = {"premise_state": self.state, "authority": self.authority}
        for key, value in (("semantic_role", self.semantic_role),
                           ("canonical_declaration", self.canonical_declaration),
                           ("contract_source", self.source),
                           ("premise_reason", self.reason)):
            if value:
                found[key] = value
        return found


def _readable(quantity) -> str:
    """`TranslationalSpringConstant` -> "a translational spring constant".

    Lower-casing the identifier whole produced "unusual for a
    translationalspringconstant", which reads as a bug in the message rather
    than as a sentence.
    """
    if not quantity:
        return "this quantity"
    words = re.sub(r"(?<!^)(?=[A-Z])", " ", str(quantity)).lower()
    article = "an" if words[:1] in "aeiou" else "a"
    return f"{article} {words}"


#: What each declared sign domain asserts, and how it answers the premise.
_SIGN_DOMAINS = {
    "positive": (Comparison.GT, 0.0, "established"),
    "nonnegative": (Comparison.GE, 0.0, "established"),
    "negative": (Comparison.LT, 0.0, "established"),
    "nonpositive": (Comparison.LE, 0.0, "established"),
    "signed": (None, None, "refuted"),
}


class _PremisePolicy:
    """Mixed into `PhysicalSan`; kept separate so the policy reads in one place."""

    def _premise_of(self, invariant, variable, context,
                    contracts=None) -> _Premise:
        """Whether this rule may be enforced on this variable.

        Authority order, highest first: intent-independent source arithmetic,
        then a user assumption, then the component contract the binder
        resolved, then the declared quantity. A lower authority never
        contradicts a higher one --- that is the whole content of "component
        semantics override a generic physical heuristic", and the first rung is
        why no amount of declared intent turns a live denominator into a
        question.
        """
        # A source equation that divides by this parameter is a fact about the
        # model, not about anybody's intention. `LCOscillator.C` reaches a
        # denominator and OpenModelica reports the division by zero; asking the
        # author whether they meant it would be hiding an arithmetic failure
        # behind a question about purpose.
        divides = contracts.get(variable.id) if (contracts and variable) else None
        if divides is not None and divides.behavior is ZeroBehavior.DIRECT_DIVISOR:
            return _Premise(
                state="established", authority="source_arithmetic",
                predicate=invariant.predicate,
                canonical_declaration=divides.canonical_declaration or "",
                source=divides.source.value,
                reason="a source equation divides by this parameter, so the "
                       "value is excluded by arithmetic rather than by intent")

        assumed = self._sign_assumption(variable, context)
        if assumed is not None:
            comparison, bound, state = _SIGN_DOMAINS[assumed.sign_domain]
            predicate = invariant.predicate
            if comparison is not None:
                predicate = Predicate(left=invariant.predicate.left,
                                      op=comparison, right=Term.constant(bound))
            return _Premise(
                state=state, authority="user_assumption", predicate=predicate,
                semantic_role=assumed.role,
                canonical_declaration=assumed.target,
                source="user_config",
                reason=(assumed.reason or
                        f"a user assumption declares this "
                        f"{assumed.sign_domain}"))

        evidence = invariant.evidence or {}
        return _Premise(
            state=getattr(invariant, "premise", "unknown"),
            authority=getattr(invariant, "authority", "quantity_or_unit"),
            predicate=invariant.predicate,
            semantic_role=str(evidence.get("semantic_role", "") or ""),
            canonical_declaration=(
                getattr(invariant, "canonical_declaration", "")
                or str(evidence.get("canonical_declaration", "") or "")),
            source=str(evidence.get("binding_source", "") or ""))

    @staticmethod
    def _sign_assumption(variable, context):
        """A user contract naming this declaration's sign domain, if any."""
        assumptions = getattr(context, "assumptions", None)
        if assumptions is None or variable is None:
            return None
        declaring = getattr(variable, "declaring_class", None)
        member = str(getattr(variable, "name", "")).rsplit(".", 1)[-1]
        declaration = f"{declaring}.{member}" if declaring else member
        for assumption in getattr(assumptions, "assumptions", ()):
            if not assumption.sign_domain:
                continue
            if assumption.sign_domain not in _SIGN_DOMAINS:
                continue
            if assumption.matches(declaration, variable.name) is None:
                continue
            assumption.used = True
            return assumption
        return None

    def _refutation(self, invariant, state: _Premise, observed=None,
                    declared_min=None) -> Finding:
        """A rule that was considered and correctly declined.

        Emitted rather than dropped: a rule that silently does not fire is
        indistinguishable from one nobody wrote, and a reader checking whether
        the analyzer knows about the signed resistor needs to see that it does.
        """
        evidence = {"required": str(state.predicate), **state.evidence,
                    "note": "an authoritative contract permits this value, so "
                            "the generic rule does not apply here"}
        if observed is not None:
            evidence["observed"] = observed
        if declared_min is not None:
            evidence["declared_min"] = declared_min
        return self._finding(invariant, kind="physical-rule-does-not-apply",
                             severity=Severity.LOW, evidence=evidence)

    @staticmethod
    def _question(variable, state: _Premise, observation: str) -> str:
        """The advisory, addressed to the author rather than about the model."""
        name = getattr(variable, "name", "this parameter")
        quantity = _readable(getattr(variable, "physical_quantity", None))
        return (f"`{name}` {observation}, which is unusual for "
                f"{quantity} — but nothing declares what this component is, "
                f"so the analyzer cannot tell whether it is intended. Is it? "
                f"If so, declare it: add a component contract, or a "
                f"`[[contracts]]` entry naming the intended `sign_domain`. If "
                f"not, bound the declaration.")


class PhysicalSan(_PremisePolicy):
    name = "physical"

    requires = {
        "static": frozenset({Capability.CANONICAL_MODEL}),
        "hints": frozenset({Capability.CANONICAL_MODEL}),
        "runtime": frozenset({Capability.OBSERVE_VARIABLE,
                              Capability.CANONICAL_MODEL}),
    }

    def __init__(self, packs=None, domains: set | None = None,
                 binder=None, semantics: dict | None = None,
                 config=None) -> None:
        """`semantics` is a mapping of flat path -> role, as a user supplies it.

        `config` is a parsed [`SemanticConfig`], which is the same thing read
        from a file the user keeps outside the Modelica source, so a mapping
        can be written against a library they do not own.
        """
        registry = RuleRegistry()
        for pack in (packs if packs is not None else BUILTIN):
            registry.register(pack)
        # Profiles are opt-in: selecting one says its rules are relevant, and
        # nothing more. Which variable is the vehicle speed still needs a
        # binding, which is why a profile alone changes no verdict.
        for pack in profile_packs(config.profiles if config is not None else ()):
            registry.register(pack)
        self.engine = PhysicalEngine(registry)
        self.domains = domains
        self.registry = registry

        mappings = dict(semantics or {})
        origin = "inline"
        if config is not None:
            mappings.update(config.mappings)
            origin = config.origin
        self.binder = binder or SemanticBinder(user_mappings=mappings, origin=origin)
        self._semantics: SemanticMap | None = None

    def semantics_for(self, model) -> SemanticMap:
        """The semantic map for `model`, built once and reused.

        Exposed rather than kept private: the binding is useful to connector
        logging, differential analysis and fault injection, none of which
        should have to re-derive it.
        """
        if self._semantics is None:
            self._semantics = self.binder.bind(model)
        return self._semantics

    # ── static ───────────────────────────────────────────────────────────────

    def analyze(self, model, context: AnalysisContext) -> list[Finding]:
        self._adopt_declaration_roles(context)
        semantics = self.semantics_for(model)
        analysis = self.engine.analyze(model, self.domains, semantics)
        contracts = self._contracts(model, context)
        findings = []

        # Groups whose constraint is a property of the group. An inertia
        # tensor is symmetric positive semidefinite; its off-diagonal entries
        # are signed products of inertia and mean nothing on their own. Six
        # scalar findings per tensor is both noise and a miss, because a
        # tensor with three positive diagonal entries can still have a
        # negative eigenvalue.
        aggregates, claimed = self._aggregates(model, context)
        findings += aggregates

        for violation in analysis.static_violations:
            if set(violation.invariant.variable_ids) & claimed:
                continue
            # A contract speaks about zero, and only about zero. A parameter
            # that *is* zero where its component documents zero as a supported
            # limit is not a violated invariant, it is the rule being wrong
            # about that component --- `CoreParameters.GcRef` ships at zero and
            # its consumer branches on exactly that. A negative value is a
            # different claim, and no zero contract excuses it.
            variable = self._variable_for(model, violation.invariant)
            contract = (contracts.zero_is_safe(variable.id)
                        if variable is not None else None)
            supported = None
            if contract is not None:
                # `ALLOWED` says the quantity rule does not bind this component
                # at all --- `SwitchedCapacitor` is documented as representing
                # "a positive or negative resistance" and is instantiated at
                # `R = -1`. Every other zero-safe behaviour is a statement
                # about *zero*, and excuses only zero.
                if contract.behavior is ZeroBehavior.ALLOWED:
                    supported = contract
                elif violation.observed == 0.0:
                    supported = contract
            if supported is not None:
                findings.append(self._finding(
                    violation.invariant,
                    kind=("physical-rule-does-not-apply"
                          if supported.behavior is ZeroBehavior.ALLOWED
                          else "physical-zero-is-a-supported-limit"),
                    severity=Severity.LOW,
                    evidence={
                        "observed": violation.observed,
                        "required": str(violation.invariant.predicate),
                        "where": violation.where,
                        "contract": supported.explain(),
                        "contract_behavior": supported.behavior.value,
                        "contract_confidence": supported.confidence.value,
                        "contract_source": supported.source.value,
                        "note": (
                            "the component documents this quantity as taking "
                            "the value it holds, so the rule derived from the "
                            "quantity alone does not bind it"
                            if supported.behavior is ZeroBehavior.ALLOWED else
                            "the declared value is zero and this component "
                            "documents zero as a meaningful limit, so the "
                            "positivity rule does not apply here")}))
                continue
            # A quantity match is not a component. `SI.Resistance` is declared
            # by passive resistors, by negative-impedance converters and by
            # anything else measuring ohms, and a rule that fired on the
            # quantity alone reported `Nr.Ga = -0.76` in `ChuaCircuit` at the
            # highest confidence. Without a declaring class to establish the
            # premise this is a *question*: the same evidence, still visible,
            # and not counted as a confirmed violation.
            state = self._premise_of(violation.invariant, variable,
                                     context, contracts)
            if state.refuted:
                findings.append(self._refutation(violation.invariant, state,
                                                 observed=violation.observed))
                continue
            findings.append(self._finding(
                violation.invariant,
                kind=("physical-invariant-violated" if state.established
                      else "physical-intent-question"),
                # Graded by what established the rule's premise, not fixed. A
                # negative value on a variable *known* to be a passive
                # resistance is a different claim from a negative value on one
                # that is merely resistance-valued, and a reader triaging a
                # thousand findings needs to see which they are looking at.
                severity=(_SEVERITY.get(violation.invariant.severity,
                                        Severity.HIGH)
                          if state.established else Severity.LOW),
                evidence={"observed": violation.observed,
                          "required": str(state.predicate),
                          "where": violation.where,
                          **state.evidence,
                          **({} if state.established else {
                              "observation": "observed-value",
                              "question": self._question(
                                  variable, state,
                                  f"holds {violation.observed:g}")})}))

        # A declaration that *permits* a forbidden value is a weaker but real
        # defect: it has not happened yet, and nothing in the model stops it.
        for invariant in self.engine.unbounded(model, self.domains, semantics):
            if invariant in (v.invariant for v in analysis.static_violations):
                continue
            if set(invariant.variable_ids) & claimed:
                continue
            if invariant.predicate.op not in (Comparison.GT, Comparison.GE):
                continue
            # An explicit `min=0` is the author stating that zero is allowed.
            # That is a much stronger signal than silence, and overriding it
            # with a strict `> 0` on no evidence is second-guessing the
            # library: `IdealCommutingSwitch.Goff(final min=0) = 1e-5` is an
            # off-state conductance whose ideal value *is* zero.
            #
            # It is still reported, because `Mass.m(min=0)` is exactly this
            # shape and zero provably breaks it in two tools (BUG-002). But it
            # is a different claim from "nothing bounds this at all", so it
            # gets its own kind rather than being counted with it.
            # A declaration defect is a claim about something a user can set.
            # `HeatPort.T` is a connector variable: the invariant "a temperature
            # stays above absolute zero" is true and is a *runtime* property, so
            # reporting it as an unbounded declaration says nothing anyone can
            # act on — and four such declarations produced 38% of the findings
            # in the full-corpus run.
            #
            # It is still emitted, under its own kind, because the invariant is
            # real and an observation could violate it. Suppressing it would
            # also remove it from the false-positive accounting a precision
            # figure depends on.
            variable = self._variable_for(model, invariant)
            settable = bool(getattr(variable, "is_parameter", False))
            declared = self._declared_minimum(model, invariant)
            explicit = declared is not None and declared == 0.0
            role = getattr(variable, "role", "unknown")

            if not settable:
                findings.append(self._finding(
                    invariant,
                    kind="physical-runtime-invariant-unobserved",
                    severity=Severity.LOW,
                    evidence={
                        "required": str(invariant.predicate),
                        "variable_role": role,
                        "note": "this is a runtime property of a "
                                f"{role} variable, not a declaration a user "
                                "can bound; deciding it needs an observation"}))
                continue

            # A blanket `> 0` rule is the wrong rule where the component
            # documents zero as a supported limit. `Inductor.L` at zero is an
            # ideal short, not a missing bound, and the SI quantity cannot say
            # so: the component-specific contract can.
            supported = contracts.zero_is_safe(variable.id) if variable else None
            if supported is not None:
                findings.append(self._finding(
                    invariant,
                    kind=("physical-rule-does-not-apply"
                          if supported.behavior is ZeroBehavior.ALLOWED
                          else "physical-zero-is-a-supported-limit"),
                    severity=Severity.LOW,
                    evidence={
                        "required": str(invariant.predicate),
                        "declared_min": declared,
                        "variable_role": role,
                        "premise_state": "refuted",
                        "authority": "component_contract",
                        "contract": supported.explain(),
                        "contract_behavior": supported.behavior.value,
                        "contract_confidence": supported.confidence.value,
                        "contract_source": supported.source.value,
                        "note": (
                            "the component documents this quantity as taking "
                            "the value the rule forbids, so the rule derived "
                            "from the quantity alone does not bind it"
                            if supported.behavior is ZeroBehavior.ALLOWED else
                            "the positivity rule does not apply: this "
                            "component documents zero as a meaningful limit, "
                            "so reporting a missing bound would contradict "
                            "its contract")}))
                continue

            # The trap this policy exists to close. A declaration whose premise
            # nobody established is not a domain defect: it is a question about
            # what the author meant. Reporting it as a medium-severity defect
            # asserted an intent the analyzer does not know, and suppressing it
            # would trade that false positive for a missed one, so it stays
            # visible at advisory strength with the missing premise named.
            state = self._premise_of(invariant, variable, context,
                                     contracts)
            if state.refuted:
                findings.append(self._refutation(invariant, state,
                                                 declared_min=declared))
                continue
            if not state.established:
                findings.append(self._finding(
                    invariant,
                    kind="physical-intent-question",
                    severity=Severity.LOW,
                    evidence={
                        "required": str(state.predicate),
                        "declared_min": declared,
                        "variable_role": role,
                        "observation": "permissive-declaration",
                        **state.evidence,
                        "question": self._question(
                            variable, state,
                            "carries no bound that would exclude it"
                            if declared is None else
                            f"is bounded only by min={declared:g}")}))
                continue

            findings.append(self._finding(
                invariant,
                kind=("physical-bound-permits-zero" if explicit
                      else "physical-domain-unenforced"),
                severity=Severity.LOW if explicit else Severity.MEDIUM,
                evidence={
                    "required": str(state.predicate),
                    "declared_min": declared,
                    "variable_role": role,
                    **state.evidence,
                    "note": (
                        "the declaration explicitly permits zero (`min=0`); "
                        "whether zero is actually admissible needs execution, "
                        "and for Mass/Inertia it is not"
                        if explicit else
                        "nothing bounds this declaration, so it permits values "
                        "the component's own contract forbids")}))

        findings.extend(self._binding_diagnostics(semantics))
        return findings

    def _adopt_declaration_roles(self, context) -> None:
        """Let a `[[contracts]]` entry that names a role reach the binder.

        A role is not a zero behaviour: `role = "machine_winding_resistance"`
        selects *which* sign rule applies to a component, so it belongs to the
        semantic binding rather than to the contract set. It arrives in the
        same file because a user should not need two.
        """
        assumptions = getattr(context, "assumptions", None)
        roles = getattr(assumptions, "roles", None) if assumptions else None
        if not roles or getattr(self, "_roles_adopted", False):
            return
        from ..semantics.providers import UserDeclarationProvider

        self.binder.providers.append(UserDeclarationProvider(
            {target: a.role for target, a in roles.items()},
            origin=getattr(assumptions, "origin", "user")))
        for assumption in roles.values():
            assumption.used = True
        self._semantics = None
        self._roles_adopted = True

    def _aggregates(self, model, context) -> tuple[list[Finding], set[int]]:
        """Findings whose subject is a group, and the variables they claim.

        A variable a group rule has taken responsibility for is removed from
        every scalar rule: that is what stops one inertia tensor producing six
        positivity findings, and it has to be an exclusion rather than a
        suppression so the aggregate verdict is the only thing said about it.
        """
        from ..physical.aggregate import Verdict, tensors

        try:
            from ..divisor import build
            environment = build(model)
        except Exception:
            environment = None

        try:
            found = tensors(model, environment)
        except Exception:
            return [], set()

        assumed = self._aggregate_assumptions(context)
        findings: list[Finding] = []
        claimed: set[int] = set()
        for tensor in found:
            claimed |= tensor.variable_ids
            note = assumed.get(tensor.declaring_class)
            evidence = {
                "aggregate": "symmetric_inertia_tensor",
                "component": tensor.owner or model.name,
                "declaring_class": tensor.declaring_class,
                "fields": ", ".join(tensor.field_names),
                "matrix": tensor.render(),
                "required": (f"{tensor.owner + '.' if tensor.owner else ''}"
                             f"I is positive semidefinite"),
                "verdict": tensor.verdict.value,
                "reason": tensor.reason,
            }
            if tensor.eigenvalues is not None:
                evidence["eigenvalues"] = ", ".join(
                    f"{x:g}" for x in tensor.eigenvalues)
            if tensor.failed_minor:
                evidence["violated_minor"] = tensor.failed_minor
            if tensor.realizable is False:
                # Not a defect on its own, and deliberately not reported as
                # one: [[2,-1,0],[-1,2,0],[0,0,1]] is a valid tensor whose
                # principal moments are 1, 1, 3, and 3 > 1 + 1.
                evidence["rigid_body_realizable"] = "no"
            if note is not None:
                evidence["contract"] = note.explain()
                evidence["contract_confidence"] = note.confidence
                evidence["contract_source"] = note.source
                evidence["contract_origin"] = note.origin

            if tensor.verdict is Verdict.INVALID:
                findings.append(self._aggregate_finding(
                    tensor, "physical-inertia-tensor-not-semidefinite",
                    Severity.HIGH, evidence))
            elif tensor.verdict is Verdict.UNKNOWN:
                evidence["note"] = (
                    "the tensor could not be assembled from values this "
                    "analysis can resolve, so neither its validity nor its "
                    "invalidity is claimed; the scalar fields are excluded "
                    "from the positivity rule either way, because that rule "
                    "is wrong about products of inertia")
                findings.append(self._aggregate_finding(
                    tensor, "physical-inertia-tensor-undecided",
                    Severity.LOW, evidence))
        return findings, claimed

    def _aggregate_finding(self, tensor, kind, severity, evidence) -> Finding:
        anchor = tensor.matrix or next(iter(tensor.fields.values()))
        return Finding(
            sanitizer=self.name, kind=kind, severity=severity,
            canonical_anchors=[CanonicalAnchor(EntityKind.PARAMETER, anchor.id,
                                               anchor.name)],
            source_locations=locate(anchor),
            evidence=evidence)

    @staticmethod
    def _aggregate_assumptions(context):
        """User contracts that name an aggregate, keyed by declaring class."""
        assumptions = getattr(context, "assumptions", None)
        if assumptions is None:
            return {}
        return {a.target: a for a in getattr(assumptions, "aggregates", ())}

    @staticmethod
    def _contracts(model, context):
        """The shared zero-behaviour contracts for this model.

        Built here rather than passed in so that a caller holding only a model
        still gets the suppression; the cost is one pass over the equations.
        """
        from ..contracts import ZeroBehavior, resolve
        from ..divisor import build

        try:
            return resolve(model, build(model),
                           assumptions=getattr(context, "assumptions", None))
        except Exception:
            # A contract failure must not take the whole pass down; without
            # one every rule simply applies as before.
            from ..contracts import ContractSet
            return ContractSet()

    @staticmethod
    def _variable_for(model, invariant):
        """The variable an invariant constrains, if it constrains one."""
        for variable in model.variables:
            if variable.id in invariant.variable_ids:
                return variable
        return None

    @staticmethod
    def _declared_minimum(model, invariant) -> float | None:
        """The `min` the declaration carries, if it carries one."""
        for variable in model.variables:
            if variable.id in invariant.variable_ids:
                return constant_value(getattr(variable, "minimum", None))
        return None

    @staticmethod
    def _binding_diagnostics(semantics: SemanticMap) -> list[Finding]:
        """Report what the binder could not settle, rather than hiding it.

        These are statements about the *analysis*, not about the model's
        physics, and they carry their own kinds so a count of physical defects
        never absorbs them. Staying silent here is what makes an unbound role
        indistinguishable from a satisfied one.
        """
        found = []
        for conflict in semantics.conflicts:
            found.append(Finding(
                sanitizer="physical", kind="semantic-binding-conflict",
                severity=Severity.LOW,
                canonical_anchors=[CanonicalAnchor(
                    EntityKind.VARIABLE, conflict.accepted.target_id,
                    conflict.accepted.target_name)],
                evidence={"target": conflict.target_name,
                          "using": str(conflict.accepted.role),
                          "using_source": conflict.accepted.source.name.lower(),
                          "ignored": str(conflict.rejected.role),
                          "ignored_source": conflict.rejected.source.name.lower(),
                          "note": conflict.reason}))
        for ambiguity in semantics.ambiguities:
            found.append(Finding(
                sanitizer="physical", kind="semantic-binding-ambiguous",
                severity=Severity.LOW, canonical_anchors=[],
                evidence={"role": str(ambiguity.role),
                          "candidates": ", ".join(ambiguity.candidates),
                          "note": "several objects could fill this role; rules "
                                  "requiring it were not applied. Provide an "
                                  "explicit semantic mapping."}))
        for pattern in semantics.unmatched_patterns:
            found.append(Finding(
                sanitizer="physical", kind="semantic-mapping-unmatched",
                severity=Severity.LOW, canonical_anchors=[],
                evidence={"pattern": pattern,
                          "note": "this user mapping matched no variable; a "
                                  "mistyped path would otherwise fail silently"}))
        return found

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
    return locate(source)
