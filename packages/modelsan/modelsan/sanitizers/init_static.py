"""InitSan (static) — invariants evaluated in the initialization context.

The design rule from the brief, and the reason this is small: **InitSan is a
new evaluation context for existing invariants, not a new family of rules.**
`0 <= SOC <= 1` is one predicate; asking it of the running model is DomainSan
and asking it of `t = 0` is this. The physics, the semantic bindings and the
applicability model are all reused untouched.

What it adds is the environment: an [`InitialState`] built from declared
bounds, parameter values, `fixed` starts and initial equations, propagated to a
fixed point. That environment is what makes this more than `start`-checking —
`xFromInitEq` has `start = 0.0` by default and is initialized to `-1` by an
equation, and only the environment knows that.

Five checks, all static:

    domain        an existing physical invariant, evaluated at t = 0
    relation      a declared relation between two initial values
    bounds        a fixed initial value outside the variable's own min/max
    precondition  1/x, sqrt(x), log(x), asin(x) where the initial range
                  refutes the operation's domain
    contradiction constraints that cannot all hold, i.e. an empty interval

Reporting policy is the brief's §20: PROVEN_FALSE is reported, PROVEN_TRUE is
silent, and UNKNOWN is silent except for one deliberately separate class — a
divisor whose initial range *contains* zero without being pinned to it. That is
a risk, not a violation, and it is kinded differently so a count of violations
never absorbs it.
"""

from __future__ import annotations

from ..analysis.context import AnalysisContext
from ..dae import BinaryOp, ops
from ..dae.traversal import walk_expressions
from ..findings.finding import Finding, Severity
from ..findings.location import locate
from ..instrumentation.capability import Capability
from ..intervals.initial_state import InitialState
from ..intervals.interval import Interval
from ..intervals.propagate import evaluate, propagate
from ..physical.domains import BUILTIN
from ..physical.engine import PhysicalEngine
from ..physical.invariant import Comparison
from ..physical.rules import RuleRegistry
from ..runtime.anchors import CanonicalAnchor, EntityKind
from ..semantics import SemanticBinder

#: Builtins whose argument domain is narrower than the reals.
PRECONDITIONS: dict[str, tuple[Comparison, float, str]] = {
    "sqrt": (Comparison.GE, 0.0, "sqrt requires a non-negative argument"),
    "log": (Comparison.GT, 0.0, "log requires a strictly positive argument"),
    "log10": (Comparison.GT, 0.0, "log10 requires a strictly positive argument"),
}

#: Builtins whose argument must lie in a closed interval.
BOUNDED_DOMAIN: dict[str, tuple[float, float]] = {
    "asin": (-1.0, 1.0),
    "acos": (-1.0, 1.0),
}


class InitStaticSan:
    name = "init-static"

    requires = {"static": frozenset({Capability.CANONICAL_MODEL})}

    def __init__(self, packs=None, binder=None) -> None:
        registry = RuleRegistry()
        for pack in (packs if packs is not None else BUILTIN):
            registry.register(pack)
        self.engine = PhysicalEngine(registry)
        self.binder = binder or SemanticBinder()

    # ── the context ──────────────────────────────────────────────────────────

    def initial_state(self, model) -> InitialState:
        state = InitialState(model)
        propagate(model, state)
        return state

    def analyze(self, model, context: AnalysisContext) -> list[Finding]:
        state = self.initial_state(model)
        semantics = self.binder.bind(model)
        findings: list[Finding] = []
        bounds = self._declared_bounds(model, state)
        # A variable already explained by the precise diagnostic is not also
        # reported as an unexplained contradiction.
        explained = {a.dae_id for f in bounds for a in f.canonical_anchors}
        findings += bounds
        findings += [f for f in self._contradictions(state)
                     if not any(a.dae_id in explained for a in f.canonical_anchors)]
        findings += self._invariants(model, state, semantics)
        findings += self._preconditions(model, state)
        return findings

    # ── contradictions (Milestone 7) ─────────────────────────────────────────

    def _contradictions(self, state: InitialState) -> list[Finding]:
        found = []
        for variable_id in state.contradictions:
            found.append(Finding(
                sanitizer=self.name, kind="init-contradiction",
                severity=Severity.HIGH,
                canonical_anchors=[CanonicalAnchor(
                    EntityKind.VARIABLE, variable_id, state.name(variable_id))],
                evidence={
                    "variable": state.name(variable_id),
                    "result": "PROVEN_FALSE",
                    "derived_from": " | ".join(str(w) for w in state.why(variable_id)),
                    "note": "the initialization constraints on this variable "
                            "cannot all hold; no initial value satisfies them",
                }))
        return found

    # ── a fixed initial value outside the declared bounds (§15) ──────────────

    def _declared_bounds(self, model, state: InitialState) -> list[Finding]:
        found = []
        for variable in model.variables:
            # Only a *constraint* can violate a bound. A `start` with
            # `fixed = false` is a guess, and §15 is explicit that it must not
            # be reported merely for lying outside the range.
            if getattr(variable, "fixed", None) is not True:
                continue
            # The *asserted* initial value, before it is met with the bound.
            # Reading the environment here would find an empty interval — the
            # seeding already intersected the two — and the generic
            # contradiction would swallow a case §15 wants named precisely:
            # "initial value 15, allowed range [0, 10]".
            from ..physical.engine import constant_value
            value = constant_value(getattr(variable, "start", None))
            if value is None:
                continue
            interval = Interval.point(value)
            declared = self._declared_interval(variable)
            if declared.is_unknown:
                continue
            if declared.meet(interval).is_empty:
                found.append(Finding(
                    sanitizer=self.name, kind="init-outside-declared-bounds",
                    severity=Severity.HIGH,
                    canonical_anchors=[CanonicalAnchor(
                        EntityKind.VARIABLE, variable.id, variable.name)],
                    source_locations=locate(variable),
                    evidence={
                        "variable": variable.name,
                        "initial_value": str(interval),
                        "allowed_range": str(declared),
                        "result": "PROVEN_FALSE",
                        "derived_from": " | ".join(
                            str(w) for w in state.why(variable.id)),
                        "note": "a fixed initial value outside the range the "
                                "variable's own declaration permits",
                    }))
        return found

    @staticmethod
    def _declared_interval(variable) -> Interval:
        from ..physical.engine import constant_value
        lo = constant_value(getattr(variable, "minimum", None))
        hi = constant_value(getattr(variable, "maximum", None))
        if lo is None and hi is None:
            return Interval.unknown()
        return Interval(lo if lo is not None else -Interval.unknown().hi,
                        hi if hi is not None else Interval.unknown().hi)

    # ── existing invariants, in this context (Milestones 4 and 5) ────────────

    def _invariants(self, model, state, semantics) -> list[Finding]:
        found = []
        analysis = self.engine.analyze(model, None, semantics)
        for invariant in analysis.invariants:
            values = {}
            intervals = {}
            for variable_id in invariant.variable_ids:
                interval = state.interval(variable_id)
                if interval.is_unknown or interval.is_empty:
                    break
                intervals[variable_id] = interval
            else:
                verdict = self._decide(invariant, intervals)
                if verdict is not False:
                    continue        # PROVEN_TRUE and UNKNOWN are silent (§20)
                names = ", ".join(
                    f"{state.name(i)} in {intervals[i]}" for i in intervals)
                derived = " | ".join(
                    str(w) for i in intervals for w in state.why(i))
                found.append(Finding(
                    sanitizer=self.name, kind="init-invariant-violated",
                    severity=Severity.HIGH,
                    canonical_anchors=[CanonicalAnchor(EntityKind.VARIABLE, i,
                                                       state.name(i))
                                       for i in intervals],
                    source_locations=locate(invariant.source),
                    evidence={
                        "invariant": str(invariant.predicate),
                        "initial_range": names,
                        "result": "PROVEN_FALSE",
                        "domain": invariant.domain.value,
                        "rule": invariant.rule.rule_id,
                        "rule_origin": invariant.rule.origin,
                        "matched_by": invariant.evidence,
                        "derived_from": derived,
                        "note": "the initialization establishes a value the "
                                "invariant forbids",
                    }))
        return found

    @staticmethod
    def _decide(invariant, intervals: dict[int, Interval]) -> bool | None:
        """Three-valued, over intervals rather than points."""
        predicate = invariant.predicate
        left = predicate.left
        right = predicate.right
        left_interval = intervals.get(getattr(left, "variable_id", None))
        if left_interval is None:
            return None
        bound = getattr(right, "value", None)
        if bound is None:
            return None
        other = Interval.point(bound)
        return {
            Comparison.GT: left_interval.gt,
            Comparison.GE: left_interval.ge,
            Comparison.LT: left_interval.lt,
            Comparison.LE: left_interval.le,
        }[predicate.op](other)

    # ── operation preconditions (Milestone 6) ────────────────────────────────

    @staticmethod
    def _guarded(model) -> set[int]:
        """Expression ids sitting inside a conditional branch.

        MSL protects nearly every risky division with a guard:

            L_stat = noEvent(if abs(i) > eps then abs(Psi/i) else abs(Psi/eps))
            TDi    = if F > 0 then NL/F else TD

        Walking every expression and reading the divisor's range ignores the
        condition that makes the branch safe. At t = 0 both `i` and `F` are
        zero, so the naive reading calls these proven divisions by zero — and
        all 23 "violations" in the first corpus run were exactly this.
        Establishing that a guard is *insufficient* needs the branch condition
        reasoned about; until then the honest answer is to say nothing.
        """
        guarded: set[int] = set()
        for _owner, node in walk_expressions(model):
            branches = getattr(node, "branches", None)
            if branches is None:
                continue
            for condition, value in branches:
                for inner in value.walk():
                    guarded.add(inner.id)
                for inner in condition.walk():
                    guarded.add(inner.id)
            fallback = getattr(node, "fallback", None)
            if fallback is not None:
                for inner in fallback.walk():
                    guarded.add(inner.id)
        return guarded

    def _preconditions(self, model, state: InitialState) -> list[Finding]:
        found, seen = [], set()
        guarded = self._guarded(model)
        for _owner, node in walk_expressions(model):
            if node.id in guarded:
                continue
            checks = []
            if isinstance(node, BinaryOp) and node.op == ops.DIVIDE:
                checks.append((node.rhs, "divisor must not be zero", None))
            name = getattr(node, "name", None)
            arguments = getattr(node, "arguments", None)
            if name and arguments:
                if name in PRECONDITIONS:
                    checks.append((arguments[0], PRECONDITIONS[name][2], name))
                elif name in BOUNDED_DOMAIN:
                    checks.append((arguments[0],
                                   f"{name} requires an argument in "
                                   f"[{BOUNDED_DOMAIN[name][0]:g}, "
                                   f"{BOUNDED_DOMAIN[name][1]:g}]", name))
            for operand, requirement, builtin in checks:
                verdict, interval = self._precondition_verdict(operand, state, builtin)
                if verdict is None:
                    continue
                key = (node.id, requirement)
                if key in seen:
                    continue
                seen.add(key)
                proven = verdict is False
                found.append(Finding(
                    sanitizer=self.name,
                    kind=("init-precondition-violated" if proven
                          else "init-precondition-at-risk"),
                    severity=Severity.HIGH if proven else Severity.LOW,
                    canonical_anchors=[CanonicalAnchor(EntityKind.EXPRESSION, node.id)],
                    source_locations=locate(node),
                    evidence={
                        "expression": repr(node)[:140],
                        "requirement": requirement,
                        "initial_range": str(interval),
                        "result": "PROVEN_FALSE" if proven else "UNKNOWN",
                        "note": ("the initialization establishes a value the "
                                 "operation does not accept" if proven else
                                 "the initial range of this operand contains a "
                                 "value the operation does not accept; whether "
                                 "it takes one is not decidable statically"),
                    }))
        return found

    @staticmethod
    def _precondition_verdict(operand, state, builtin) -> tuple[bool | None, Interval]:
        interval = evaluate(operand, state)
        if interval.is_unknown or interval.is_empty:
            return None, interval
        if builtin is None:                        # a divisor
            if interval.is_point and interval.lo == 0.0:
                return False, interval             # provably zero
            if interval.spans_zero:
                return True, interval              # at risk, not proven
            return None, interval
        if builtin in PRECONDITIONS:
            op, bound, _ = PRECONDITIONS[builtin]
            required = Interval.point(bound)
            holds = interval.ge(required) if op is Comparison.GE else interval.gt(required)
            if holds is False:
                return False, interval
            if holds is None:
                return True, interval
            return None, interval
        lo, hi = BOUNDED_DOMAIN[builtin]
        allowed = Interval(lo, hi)
        if allowed.meet(interval).is_empty:
            return False, interval
        if interval.lo < lo or interval.hi > hi:
            return True, interval
        return None, interval
