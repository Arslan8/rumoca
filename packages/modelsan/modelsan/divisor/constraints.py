"""What a parameter is actually allowed to be.

A zero witness is only evidence if the value it proposes is a value the model
permits. This module collects, per variable, every constraint the artifact
carries: the declared bounds, the bounds inherited from the type, whether the
value is fixed at all, and any assertion the model makes about it.

Getting this wrong has a direction. Reading a constraint as absent when it is
present invents a defect; reading one as present when it is absent hides one.
The first is what this project actually did — `min=Modelica.Constants.eps` was
read as no bound because the reader tested for a literal — so every accessor
here resolves through constants rather than pattern-matching on syntax.
"""

from __future__ import annotations

import math
from dataclasses import dataclass, field

from ..dae import BinaryOp, ops
from ..physical.engine import constant_value


#: Floating-point comparisons against a declared bound are relative, never
#: absolute: the bounds in question span 2.2e-308 to 1e6.
def _slack(bound: float, value: float) -> float:
    return 1e-9 * max(abs(bound), abs(value), 1e-300)


def _relaxed(floor: float, value: float) -> float:
    return floor * (1 - 1e-9)


@dataclass(frozen=True)
class Domain:
    """The closed interval a variable may take, and whether it may move."""

    low: float = -math.inf
    high: float = math.inf
    settable: bool = True
    """False for a constant, or for a value the model fixes outright."""

    reason: str = ""
    """Why it is not settable, or which bound came from where."""

    min_magnitude: float = 0.0
    """`assert(abs(v) >= c)` forbids an interval around zero rather than
    moving an endpoint, which a single interval cannot express. MSL writes
    exactly this to mean "non-zero", and reading it as no constraint is how
    `1/(k*Ni)` came to be reported."""

    def admits(self, value: float) -> bool:
        # Every comparison here is relative. MSL bounds a quantity away from
        # zero with values like `Modelica.Constants.eps` (2.2e-16) and
        # `small` (2.2e-308); an absolute slack of 1e-12 swamps both, and a
        # bound of `min=2.2e-14` then "admits" zero. It did, and `Ni = 0` was
        # proposed against a declaration that forbids it.
        if self.min_magnitude > 0.0 and abs(value) < _relaxed(self.min_magnitude, value):
            return False
        if self.low != -math.inf and value < self.low - _slack(self.low, value):
            return False
        if self.high != math.inf and value > self.high + _slack(self.high, value):
            return False
        return True

    def clamp(self, value: float) -> float:
        return min(max(value, self.low), self.high)

    @property
    def admits_zero(self) -> bool:
        return self.admits(0.0)


@dataclass
class Environment:
    """Every variable's domain and its value at the declared configuration."""

    domains: dict[int, Domain] = field(default_factory=dict)
    values: dict[int, float] = field(default_factory=dict)
    names: dict[int, str] = field(default_factory=dict)
    #: Expressions an assertion requires to stay away from zero, by a
    #: structural key. Matched against a denominator to decide "guarded".
    guarded_shapes: set[str] = field(default_factory=set)
    #: Human-readable assertions, for the report.
    assertions: list[str] = field(default_factory=list)
    #: Decides whether a symbol's value can be changed at all, and explains
    #: why not when it cannot. See `_Immutability`.
    immutability: object = None
    #: Binding expressions, so a witness propagates into derived parameters.
    #: `T_rising = rising` must become zero when `rising` does, or the branch
    #: that divides by it cannot be shown unreachable.
    bindings: dict[int, object] = field(default_factory=dict)
    #: A non-parameter variable that one equation defines in terms of others.
    #: `i_s = p_s/(vps - vns)` divides by two *variables*, and they are
    #: determined by `vps = Vps` and `vns = Vns`; without this the witness
    #: search sees two quantities it may not touch and reports nothing.
    definitions: dict[int, object] = field(default_factory=dict)

    def domain(self, variable_id: int) -> Domain:
        return self.domains.get(variable_id, Domain())


def shape_key(expression) -> str:
    """A structural key for an expression, ignoring identity.

    Two expression nodes that compute the same thing over the same variables
    must produce the same key, because an assertion is written once and the
    denominator it protects is a different node with the same shape.
    """
    return repr(expression)


def _bound(expression) -> float | None:
    """A declared bound as a number, resolving constant references."""
    if expression is None:
        return None
    value = constant_value(expression)
    if value is None or isinstance(value, bool):
        return None
    try:
        value = float(value)
    except (TypeError, ValueError):
        return None
    return None if math.isnan(value) else value


def _declared_value(variable) -> float | None:
    """The value this variable actually has at the declared configuration.

    A parameter's binding is its value. A *variable's* `start` is an initial
    guess for the solver, not a value the model asserts — reading it as one
    gave `opAmp.vps` the value 0, which made `vps - vns` look like it was
    already zero before anything was changed and suppressed a real finding.
    `start` counts only where `fixed = true` makes it a constraint.
    """
    value = _bound(variable.binding)
    if value is not None:
        return value
    if variable.is_parameter or variable.fixed:
        return _bound(variable.start)
    return None


def build(model) -> Environment:
    """Collect domains, declared values and assertions for one model."""
    environment = Environment()
    immutability = _Immutability(model)
    for variable in model.variables:
        low = _bound(variable.minimum)
        high = _bound(variable.maximum)

        settable, reason = immutability.settable(variable)
        value = _declared_value(variable)
        if not settable and value is not None:
            low = high = value

        environment.domains[variable.id] = Domain(
            low=low if low is not None else -math.inf,
            high=high if high is not None else math.inf,
            settable=settable, reason=reason)
        if value is not None:
            environment.values[variable.id] = value
        if variable.binding is not None:
            environment.bindings[variable.id] = variable.binding
        environment.names[variable.id] = variable.name

    environment.immutability = immutability
    _collect_assertions(model, environment)
    _collect_definitions(model, environment)
    return environment


class _Immutability:
    """Whether a symbol's value can be changed by any admissible configuration.

    The rule the review settled on, and the one this implements:

        Suppress only when the **complete effective binding and dependency
        chain** proves the denominator cannot be zero --- not merely because a
        symbol is constant, final, or protected.

    So each prefix is read for exactly what it says:

    * ``constant`` fixes the value, *provided everything its binding reads is
      also fixed*.
    * ``final`` closes the declaration to modifiers. It does not close the
      binding: ``final parameter d = p`` is reachable by setting ``p``, and
      reporting it is correct.
    * ``protected`` is visibility. A ``protected parameter`` is settable before
      translation and must still be reported.
    * ``Evaluate=true`` is a translation hint. A structural parameter may still
      be given a different value and the model retranslated.
    """

    def __init__(self, model) -> None:
        self._by_id = {v.id: v for v in model.variables}
        self._cache: dict[int, tuple[bool, str]] = {}

    def settable(self, variable) -> tuple[bool, str]:
        """(settable, why not) for one symbol."""
        immutable, why = self._immutable(variable.id, set())
        if immutable:
            return False, why
        if not variable.is_parameter:
            # A state or algebraic is determined by the equations rather than
            # set by the user. It can still *be* zero, so it keeps its domain,
            # but a witness may not simply assign it.
            return False, f"{variable.role}, determined by the model"
        return True, ""

    def _immutable(self, variable_id: int, seen: set[int]) -> tuple[bool, str]:
        if variable_id in self._cache:
            return self._cache[variable_id]
        if variable_id in seen:
            # A binding cycle cannot be proved immutable; treat it as settable,
            # which is the direction that reports rather than hides.
            return False, ""
        variable = self._by_id.get(variable_id)
        if variable is None:
            return False, ""
        contract = getattr(variable, "contract", None)
        if contract is None:
            # An artifact without contracts: fall back to the DAE role, which
            # is all that used to be available.
            fixed = variable.role == "constant"
            answer = (fixed, "declared constant" if fixed else "")
            self._cache[variable_id] = answer
            return answer

        if contract.is_constant:
            basis = "declared constant"
        elif contract.is_final:
            basis = "declared final, so no modifier can override it"
        else:
            answer = (False, "")
            self._cache[variable_id] = answer
            return answer

        # The prefix is necessary and not sufficient. Everything the binding
        # reads must be immutable too, or the value is reachable through it.
        chain = list(contract.binding_depends_on)
        if not chain and variable.binding is None:
            # `final parameter p;` with no binding is configured elsewhere.
            answer = (False, "")
            self._cache[variable_id] = answer
            return answer

        for dependency in chain:
            immutable, _ = self._immutable(dependency, seen | {variable_id})
            if not immutable:
                name = self._by_id[dependency].name if dependency in self._by_id \
                    else str(dependency)
                answer = (False, f"{basis}, but its binding reads {name}, "
                                 f"which is adjustable")
                self._cache[variable_id] = answer
                return answer

        detail = basis
        if chain:
            detail += " and every symbol its binding reads is immutable too"
        answer = (True, detail)
        self._cache[variable_id] = answer
        return answer


def _collect_definitions(model, environment: Environment) -> None:
    """Record `v = <expr>` for variables one equation defines outright.

    Only the unambiguous shape is taken: a residual `a - b` in which exactly
    one side is a bare reference to a variable that has no value of its own.
    Anything requiring algebra is left alone, because a wrong definition here
    produces a wrong witness, which is the failure being fixed.
    """
    from ..dae import BinaryOp, VariableRef, ops

    equations = list(model.equations) + list(model.initial_equations)
    for equation in equations:
        residual = equation.residual
        if not (isinstance(residual, BinaryOp) and residual.op == ops.SUBTRACT):
            continue
        for defined, expression in ((residual.lhs, residual.rhs),
                                    (residual.rhs, residual.lhs)):
            if not isinstance(defined, VariableRef):
                continue
            if defined.is_derivative or defined.is_previous:
                continue
            variable = defined.variable
            if variable.id in environment.values:
                continue          # already has a declared value
            if variable.id in environment.definitions:
                continue          # first definition wins; a second is ambiguity
            if any(v.id == variable.id for v in expression.variables()):
                continue          # implicit, not a definition
            environment.definitions[variable.id] = expression


#: Relations that put a floor under the left-hand side.
_LOWER = {ops.RELATIONS and "greater", "greater_equal"}
_UPPER = {"less", "less_equal"}


def _collect_assertions(model, environment: Environment) -> None:
    """Record what the model's `assert` statements forbid.

    An assertion in MSL is overwhelmingly of the form
    `assert(<denominator> >= eps, "...")`, written immediately above the
    division it protects. Matching the asserted expression against the
    denominator structurally is therefore both simple and exactly right: the
    model has already said that this quantity does not reach zero.
    """
    relations = model._raw.get("relations", [])
    asserted = set()
    for event in getattr(model, "events", ()) or ():
        if event.kind != "assert":
            continue
        # The guard of an assert event is the *negation* of the condition, so
        # the relation the modeller wrote is reached through it. Rather than
        # replay the condition algebra, take every relation declared at the
        # same source span: an assert contributes exactly its own relations.
        span = event.source.span
        for relation in relations:
            provenance = relation.get("provenance", {}).get("span", {})
            if (provenance.get("source") == span.source.id
                    and provenance.get("line") == span.line):
                asserted.add(relation["expression"])

    for index in sorted(asserted):
        try:
            expression = model.expressions[index]
        except (IndexError, KeyError):
            continue
        if not (isinstance(expression, BinaryOp)
                and expression.op in ops.RELATIONS):
            continue
        environment.assertions.append(repr(expression))
        _apply_relation(expression, environment)


def _flip(op: str) -> str:
    return {"greater": "less", "greater_equal": "less_equal",
            "less": "greater", "less_equal": "greater_equal"}.get(op, op)


def _abs_argument(expression):
    """The argument of `abs(...)`, or None if this is not an abs call."""
    if type(expression).__name__ == "BuiltinCall" and expression.name == "abs":
        if len(expression.arguments) == 1:
            return expression.arguments[0]
    return None


def _apply_relation(relation, environment: Environment) -> None:
    """Narrow a domain, or mark a whole expression as guarded away from zero."""
    left, right, op = relation.lhs, relation.rhs, relation.op
    left_value, right_value = _bound(left), _bound(right)

    # `<expr> >= eps` or `<expr> > 0`: the expression itself is guarded.
    if right_value is not None and op in ("greater", "greater_equal"):
        if right_value >= 0.0:
            environment.guarded_shapes.add(shape_key(left))
    if left_value is not None and op in ("less", "less_equal"):
        if left_value <= 0.0:
            environment.guarded_shapes.add(shape_key(right))

    # `abs(v) >= c`: the model's idiom for "non-zero". It is not a bound on
    # either end, so it cannot narrow the interval; it punches a hole at zero.
    for side, other, comparison in ((left, right, op),
                                    (right, left, _flip(op))):
        magnitude = _abs_argument(side)
        limit = _bound(other)
        if magnitude is None or limit is None or limit <= 0.0:
            continue
        if comparison not in ("greater", "greater_equal"):
            continue
        variables = magnitude.variables()
        if len(variables) != 1 or repr(magnitude) != variables[0].name:
            continue
        variable = variables[0]
        current = environment.domain(variable.id)
        environment.domains[variable.id] = Domain(
            low=current.low, high=current.high, settable=current.settable,
            min_magnitude=max(current.min_magnitude, limit),
            reason=(current.reason + "; " if current.reason else "")
                   + f"assert abs({variable.name}) >= {limit:g}")

    # `p >= c` where the left side is one variable: narrow its domain.
    for side, other, flip in ((left, right, False), (right, left, True)):
        variables = side.variables()
        if len(variables) != 1 or repr(side) != variables[0].name:
            continue
        limit = _bound(other)
        if limit is None:
            continue
        comparison = op
        if flip:
            comparison = {"greater": "less", "greater_equal": "less_equal",
                          "less": "greater", "less_equal": "greater_equal"}.get(op, op)
        variable = variables[0]
        current = environment.domain(variable.id)
        low, high = current.low, current.high
        if comparison in ("greater", "greater_equal"):
            low = max(low, limit)
        elif comparison in ("less", "less_equal"):
            high = min(high, limit)
        else:
            continue
        environment.domains[variable.id] = Domain(
            low=low, high=high, settable=current.settable,
            min_magnitude=current.min_magnitude,
            reason=(current.reason + "; " if current.reason else "")
                   + f"assert {variable.name} {comparison} {limit:g}")
