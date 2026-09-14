"""The domain-blind sanitizer engine.

It knows how to match rules to variables, build invariants, decide them
statically where the value is known, and say which need runtime observation. It
does not know that electricity or heat exist, and it must not learn: a new
domain is a rule pack, never an edit here.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from .invariant import Domain, Enforcement, PhysicalInvariant
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
    runtime: list[PhysicalInvariant] = field(default_factory=list)
    """Invariants whose truth depends on state and must be observed."""

    undecided: list[PhysicalInvariant] = field(default_factory=list)
    """Statically checkable in principle, but the value is not known here."""

    @property
    def domains(self) -> set[Domain]:
        return {i.domain for i in self.invariants}


def constant_value(expression) -> float | None:
    """Fold a declaration expression to a number, if it is constant.

    Reading only bare literals is not enough, and fails in exactly the place
    this module cares about: `-2.0` reaches the DAE as a unary minus over a
    literal, not as a literal, so a naive reader sees no value for every
    *negative* declaration. `-998` happens to fold and `-2.0` does not, which
    made the omission look like it worked.

    Kept small on purpose — literals, sign, and arithmetic over constants. An
    expression referring to another parameter is not folded here; the engine
    treats it as undecided, which is correct rather than guessed.
    """
    if expression is None:
        return None

    value = getattr(expression, "value", None)
    if isinstance(value, (int, float)) and not isinstance(value, bool):
        return float(value)

    op = getattr(expression, "op", None)
    operand = getattr(expression, "operand", None)
    if op is not None and operand is not None:  # unary
        inner = constant_value(operand)
        if inner is None:
            return None
        if op in ("negate", "minus", "-"):
            return -inner
        if op in ("plus", "+"):
            return inner
        return None

    lhs, rhs = getattr(expression, "lhs", None), getattr(expression, "rhs", None)
    if op is not None and lhs is not None and rhs is not None:
        left, right = constant_value(lhs), constant_value(rhs)
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

    def analyze(self, model, domains: set[Domain] | None = None) -> Analysis:
        analysis = Analysis()
        rules = self.registry.rules(domains)

        for variable in model.variables:
            for rule in rules:
                match = rule.applies(variable)
                if match is None:
                    continue
                predicate = rule.predicate(variable)
                invariant = PhysicalInvariant(
                    id=f"{rule.rule_id}@{variable.id}",
                    predicate=predicate,
                    domain=rule.domain,
                    enforcement=getattr(rule, "enforcement", Enforcement.EITHER),
                    rule=rule.provenance(),
                    severity=getattr(rule, "severity", "medium"),
                    variable_ids=predicate.variables(),
                    component=str(getattr(variable, "component", "") or ""),
                    source=getattr(variable, "source", None),
                    evidence=match.evidence,
                )
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

        holds = invariant.predicate.holds({variable.id: value})
        if holds is False:
            analysis.static_violations.append(Violation(invariant, observed=value))
        elif holds is None:
            analysis.undecided.append(invariant)
        # A statically true invariant needs no runtime check for a parameter,
        # because nothing can change it during the run.

    def unbounded(self, model, domains: set[Domain] | None = None) -> list[PhysicalInvariant]:
        """Invariants the model's own declaration does not already enforce.

        An invariant whose variable declares a `min` at least as strong is
        already guaranteed by the model, and reporting it would be noise. What
        is left is where physics requires something the declaration permits to
        be violated — which is the defect class worth reporting.
        """
        from .invariant import Comparison

        left = []
        for invariant in self.analyze(model, domains).invariants:
            variable = next((v for v in model.variables
                             if v.id in invariant.variable_ids), None)
            if variable is None:
                continue
            declared = _literal(getattr(variable, "minimum", None))
            required = invariant.predicate.right.value
            if invariant.predicate.op in (Comparison.GT, Comparison.GE) and required is not None:
                if declared is not None and declared >= required:
                    continue  # the model already enforces it
            left.append(invariant)
        return left
