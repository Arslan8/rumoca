"""The domain-blind sanitizer engine.

It knows how to match rules to variables, build invariants, decide them
statically where the value is known, and say which need runtime observation. It
does not know that electricity or heat exist, and it must not learn: a new
domain is a rule pack, never an edit here.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from .invariant import Domain, Enforcement, PhysicalInvariant
from .matching import Premise
from .rules import RuleRegistry


@dataclass
class Violation:
    """An invariant decided false from the declaration alone."""

    invariant: PhysicalInvariant
    observed: float
    where: str = "declaration"


@dataclass
class Analysis:
    """What the engine produced for one model."""

    invariants: list[PhysicalInvariant] = field(default_factory=list)
    static_violations: list[Violation] = field(default_factory=list)
    refuted: list[PhysicalInvariant] = field(default_factory=list)
    """Rules an authoritative component contract declined. Not violations, and
    kept because a rule silently not firing is indistinguishable from one that
    was never written."""

    runtime: list[PhysicalInvariant] = field(default_factory=list)
    """Invariants whose truth depends on state and must be observed."""

    undecided: list[PhysicalInvariant] = field(default_factory=list)
    """Statically checkable in principle, but the value is not known here."""

    semantics: object = None
    """The [`SemanticMap`] the rules were matched against, when one was given.
    Carried so a finding can report the binding that justified it."""

    @property
    def domains(self) -> set[Domain]:
        return {i.domain for i in self.invariants}


def constant_value(expression, _seen: frozenset[int] = frozenset()) -> float | None:
    """Fold a declaration expression to a number, if the declaration fixes one.

    Reading only bare literals is not enough, and fails in exactly the place
    this module cares about: `-2.0` reaches the DAE as a unary minus over a
    literal, not as a literal, so a naive reader sees no value for every
    *negative* declaration. `-998` happens to fold and `-2.0` does not, which
    made the omission look like it worked.

    A reference to another parameter is followed, because a declaration is no
    less fixed for being written in two steps:

        parameter Real scale = 2.5;
        parameter SI.Resistance R = -scale * 5;

    `R` is definitively -12.5 and definitively impossible, but neither half
    says so alone. Rumoca folds this chain away only when the result is an
    exact integer, so before this the sanitizer reported `-scale * 5` as merely
    *unbounded* while reporting the identical `-2 * 5` as *violated* — the
    weaker claim, decided by whether the arithmetic happened to land on a whole
    number. Following the chain here makes the verdict depend on the model
    rather than on the compiler, and is what lets the same answer come back
    with or without `--no-fold-parameter-bindings`.

    Only a parameter's *binding* is followed. A `start` is a solver's initial
    guess, and treating one as a fixed value partway down a chain would report
    a violation the declaration does not actually commit to.
    """
    if expression is None:
        return None

    value = getattr(expression, "value", None)
    if isinstance(value, (int, float)) and not isinstance(value, bool):
        return float(value)

    variable = getattr(expression, "variable", None)
    if variable is not None:
        # `der(x)` and `pre(x)` name a trajectory, not the declaration. The
        # plain kind is spelled after the variable's variability ("parameter",
        # "constant", ...), so these are excluded by name rather than by
        # allow-listing a spelling that would silently stop matching.
        if getattr(expression, "is_derivative", False):
            return None
        if getattr(expression, "is_previous", False):
            return None
        if not getattr(variable, "is_parameter", False):
            return None
        if variable.id in _seen:  # a cyclic binding is not a value
            return None
        return constant_value(getattr(variable, "binding", None),
                              _seen | {variable.id})

    # `if PRef <= 0 then 0 else <expr>` is a value when the condition decides.
    # MSL writes derived parameters this way often enough that skipping it left
    # the folder mode-dependent: Rumoca resolves the branch itself when the
    # result is an exact integer, so the same declaration read as a value or as
    # an absence depending on which arm it landed on.
    branches = getattr(expression, "branches", None)
    if branches is not None:
        for condition, value in branches:
            decided = _constant_condition(condition, _seen)
            if decided is None:
                return None  # an undecided arm makes the whole thing undecided
            if decided:
                return constant_value(value, _seen)
        return constant_value(getattr(expression, "fallback", None), _seen)

    op = getattr(expression, "op", None)
    operand = getattr(expression, "operand", None)
    if op is not None and operand is not None:  # unary
        inner = constant_value(operand, _seen)
        if inner is None:
            return None
        if op in ("negate", "minus", "-"):
            return -inner
        if op in ("plus", "+"):
            return inner
        return None

    lhs, rhs = getattr(expression, "lhs", None), getattr(expression, "rhs", None)
    if op is not None and lhs is not None and rhs is not None:
        left, right = constant_value(lhs, _seen), constant_value(rhs, _seen)
        if left is None or right is None:
            return None
        if op == "add":
            return left + right
        if op == "subtract":
            return left - right
        if op == "multiply":
            return left * right
        if op == "divide":
            return left / right if right != 0 else None
        if op == "power":
            try:
                result = left ** right
            except (OverflowError, ZeroDivisionError, ValueError):
                return None
            return float(result) if isinstance(result, (int, float)) else None
    return None


#: Comparisons over two constants, as the DAE spells the operators.
_RELATIONS = {
    "less": lambda a, b: a < b,
    "less_equal": lambda a, b: a <= b,
    "greater": lambda a, b: a > b,
    "greater_equal": lambda a, b: a >= b,
    "equal": lambda a, b: a == b,
    "not_equal": lambda a, b: a != b,
}


def _constant_condition(expression, _seen: frozenset[int]) -> bool | None:
    """Decide a condition, or `None` when the declaration does not fix it.

    Kept separate from [`constant_value`] rather than folded into it: a
    comparison is not a number, and letting `a < b` come back as `0.0` would
    have every caller read a false condition as the value zero.
    """
    if expression is None:
        return None

    value = getattr(expression, "value", None)
    if isinstance(value, bool):
        return value

    op = getattr(expression, "op", None)
    operand = getattr(expression, "operand", None)
    if op == "not" and operand is not None:
        inner = _constant_condition(operand, _seen)
        return None if inner is None else not inner

    lhs, rhs = getattr(expression, "lhs", None), getattr(expression, "rhs", None)
    if op in ("and", "or") and lhs is not None and rhs is not None:
        left, right = _constant_condition(lhs, _seen), _constant_condition(rhs, _seen)
        if left is None or right is None:
            return None
        return (left and right) if op == "and" else (left or right)

    relation = _RELATIONS.get(op)
    if relation is not None and lhs is not None and rhs is not None:
        left, right = constant_value(lhs, _seen), constant_value(rhs, _seen)
        if left is None or right is None:
            return None
        return relation(left, right)

    # A Boolean parameter reference is as fixed as a numeric one.
    variable = getattr(expression, "variable", None)
    if variable is not None:
        if getattr(expression, "is_derivative", False):
            return None
        if getattr(expression, "is_previous", False):
            return None
        if not getattr(variable, "is_parameter", False) or variable.id in _seen:
            return None
        return _constant_condition(getattr(variable, "binding", None),
                                   _seen | {variable.id})
    return None


def _literal(expression) -> float | None:
    return constant_value(expression)


def known_value(variable) -> float | None:
    """The variable's value, if the declaration fixes it.

    A parameter's binding is its value; a `start` is only an initial guess for
    a state, so it is used only where the variable cannot vary.
    """
    binding = _literal(getattr(variable, "binding", None))
    if binding is not None:
        return binding
    if getattr(variable, "is_parameter", False):
        return _literal(getattr(variable, "start", None))
    return None


class PhysicalEngine:
    """Matches rules to a model and decides what it can."""

    def __init__(self, registry: RuleRegistry) -> None:
        self.registry = registry

    def analyze(self, model, domains: set[Domain] | None = None,
                semantics=None) -> Analysis:
        """Decide every rule that applies to every variable.

        `semantics` is a [`SemanticMap`]. Rules that key on roles consult it;
        rules that key on the declared quantity ignore it, so a caller with no
        binder still gets the behaviour it had before there was one.
        """
        analysis = Analysis()
        rules = self.registry.rules(domains)
        analysis.semantics = semantics

        for variable in model.variables:
            for rule in rules:
                match = rule.applies(variable, semantics)
                if match is None:
                    continue
                predicate = rule.predicate(variable)
                invariant = PhysicalInvariant(
                    id=f"{rule.rule_id}@{variable.id}",
                    predicate=predicate,
                    domain=rule.domain,
                    enforcement=getattr(rule, "enforcement", Enforcement.EITHER),
                    rule=rule.provenance(),
                    severity=(rule.severity_for(match)
                              if hasattr(rule, "severity_for")
                              else getattr(rule, "severity", "medium")),
                    variable_ids=predicate.variables(),
                    component=str(getattr(variable, "component", "") or ""),
                    source=getattr(variable, "source", None),
                    evidence=match.evidence,
                    premise=match.premise.value,
                    authority=match.authority.name.lower(),
                    canonical_declaration=match.canonical_declaration,
                )
                # A refuted premise means an authoritative contract permits the
                # value. It is recorded so a reader can see the rule was
                # considered and declined, and it is never enforced.
                if match.premise is Premise.REFUTED:
                    analysis.refuted.append(invariant)
                    continue
                analysis.invariants.append(invariant)
                self._decide(invariant, variable, analysis)
        return analysis

    def _decide(self, invariant: PhysicalInvariant, variable, analysis: Analysis) -> None:
        """Static where the declaration settles it, runtime where it cannot."""
        if invariant.enforcement is Enforcement.RUNTIME:
            analysis.runtime.append(invariant)
            return

        value = known_value(variable)
        if value is None:
            # Not decidable here. A parameter with no fixed value can still be
            # set at runtime, and a state always varies, so both are deferred
            # rather than silently passed.
            (analysis.runtime if not getattr(variable, "is_parameter", False)
             else analysis.undecided).append(invariant)
            return

        # A value the declaration explicitly permits is not a violation, even
        # where physics would forbid it in general. `Body.I_31(min=-C.inf) = 0`
        # is an off-diagonal inertia-tensor element: MSL states that any sign is
        # allowed, and a point mass really does have a zero tensor. Reporting
        # `I_31 > 0` there argues with the declaration rather than with the
        # model, which is the same error as asserting `R > 0` on a resistor MSL
        # documents as permitting either sign.
        #
        # If the permitted domain is itself wrong, that is what the
        # `physical-domain-*` kinds are for; it is not a violation of it.
        declared = _literal(getattr(variable, "minimum", None))
        permitted = declared is not None and value >= declared

        holds = invariant.predicate.holds({variable.id: value})
        if holds is False and not permitted:
            analysis.static_violations.append(Violation(invariant, observed=value))
        elif holds is False:
            analysis.undecided.append(invariant)
        elif holds is None:
            analysis.undecided.append(invariant)
        # A statically true invariant needs no runtime check for a parameter,
        # because nothing can change it during the run.

    def unbounded(self, model, domains: set[Domain] | None = None,
                  semantics=None) -> list[PhysicalInvariant]:
        """Invariants the model's own declaration does not already enforce.

        An invariant whose variable declares a `min` at least as strong is
        already guaranteed by the model, and reporting it would be noise. What
        is left is where physics requires something the declaration permits to
        be violated — which is the defect class worth reporting.
        """
        from .invariant import Comparison

        left = []
        for invariant in self.analyze(model, domains, semantics).invariants:
            variable = next((v for v in model.variables
                             if v.id in invariant.variable_ids), None)
            if variable is None:
                continue
            declared = _literal(getattr(variable, "minimum", None))
            required = invariant.predicate.right.value
            if declared is not None and required is not None:
                # Strictness matters, and getting it wrong hides the single most
                # common defect in MSL. `SI.Mass` declares `min=0`, which does
                # *not* enforce `m > 0` — it permits exactly the value the rule
                # forbids. Treating `declared >= required` as sufficient made
                # PhysicalSan silent on BUG-002.
                if invariant.predicate.op is Comparison.GT and declared > required:
                    continue
                if invariant.predicate.op is Comparison.GE and declared >= required:
                    continue
            left.append(invariant)
        return left
