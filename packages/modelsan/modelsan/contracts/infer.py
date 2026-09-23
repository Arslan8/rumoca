"""Deriving a zero contract from the model's own source equations.

The distinction that matters is between a parameter that *divides* and one that
*multiplies*. At zero the first is undefined and the second degenerates:

    flow = level/resistance     resistance divides      DIRECT_DIVISOR
    L*der(i) = v                L multiplies a rate     ALGEBRAIC_LIMIT
    Q_flow = G*dT               G multiplies            FEATURE_DISABLED

Four rules make this sound rather than merely plausible:

**Look at every use, not one.** A parameter may multiply in one equation and
divide in another. `p*der(x) = 1` alongside `y = x/p` is a divide-by-zero, and
the multiplicative use does not excuse it.

**A direct reachable denominator wins.** Any source division outranks every
safe multiplicative use, because one of them is undefined at zero and the
others are merely degenerate.

**Source equations only.** `L*der(i) = v` contains no division. The DAE may
hold `der(i) = v/L`, because that is what a solver integrates, and inferring
`DIRECT_DIVISOR` from it blames the modeller for the translation.

**`min=0` proves nothing.** A declaration permitting zero is not a statement
that zero is meaningful. It is the absence of a statement.
"""

from __future__ import annotations

from collections import defaultdict

from ..dae import BinaryOp, Conditional, Literal, VariableRef, ops
from ..dae.traversal import root_expressions
from .behavior import Confidence, Source, ZeroBehavior, ZeroContract


def _rate_variables(model) -> set[int]:
    """Variables that *are* a derivative under another name.

    `Mass` writes `m*a = flange_a.f + flange_b.f` with a separate `der(v) = a`,
    so the coefficient `m` multiplies an algebraic variable rather than a
    `der()` node. Treating that as an ordinary multiplication classifies a
    massless body as `FEATURE_DISABLED` instead of `ALGEBRAIC_LIMIT` — close
    enough that both suppress, but the wrong reason in a report a reader is
    meant to check.
    """
    rates: set[int] = set()
    for equation in model.equations:
        residual = equation.residual
        if not (isinstance(residual, BinaryOp) and residual.op == ops.SUBTRACT):
            continue
        for plain, other in ((residual.lhs, residual.rhs),
                             (residual.rhs, residual.lhs)):
            if (isinstance(plain, VariableRef) and not plain.is_derivative
                    and isinstance(other, VariableRef) and other.is_derivative):
                rates.add(plain.variable.id)
    return rates


def _uses(model, environment=None) -> dict[int, list[tuple[str, object]]]:
    """Every use of every parameter, tagged by how it is used.

    Tags are `divisor` (under a `/`), `guarded-divisor` (under a `/` whose
    denominator provably cannot vanish), `derivative-coefficient` (multiplying
    a `der()`), `coefficient` (multiplying anything else) and `other`.
    """
    found: dict[int, list[tuple[str, object]]] = defaultdict(list)
    rates = _rate_variables(model)

    for owner, root in root_expressions(model):
        generated = getattr(getattr(root, "provenance", None), "is_generated", False)
        _walk(root, found, generated, owner, False, rates, environment)
    return found


def _safe_denominator(expression, environment) -> bool:
    """Whether the denominator provably cannot be zero.

    `SwitchedCapacitor` writes `C = clock/max(eps*oneOhm, abs(R))`. Tagging `R`
    as a divisor because it appears under a `/` is the defect of
    [TOOLBUG-017](../../../../docs/toolbugs/TOOLBUG-017-divisor-reported-parameters-not-denominators.md)
    happening again one layer down: the *denominator* is what has to be able to
    vanish, and `max(eps, |R|)` cannot. The wrong tag then outranked the
    catalogue entry saying this component represents a signed resistance, and
    four findings against a documented idiom survived because of it.
    """
    if environment is None:
        return False
    from ..divisor.reasoning import interval_of

    try:
        span = interval_of(expression, environment)
    except Exception:
        return False
    return span.lo > 0.0 or span.hi < 0.0


def _walk(node, found, generated: bool, owner, in_divisor: bool = False,
          rates: set[int] | None = None, environment=None) -> None:
    rates = rates or set()
    if isinstance(node, BinaryOp) and node.op == ops.DIVIDE:
        _walk(node.lhs, found, generated, owner, in_divisor, rates, environment)
        _walk(node.rhs, found, generated, owner,
              "guarded" if _safe_denominator(node.rhs, environment) else True,
              rates, environment)
        return

    if isinstance(node, BinaryOp) and node.op == ops.MULTIPLY and not in_divisor:
        for side, other in ((node.lhs, node.rhs), (node.rhs, node.lhs)):
            if isinstance(side, VariableRef) and not side.is_derivative:
                tag = ("derivative-coefficient"
                       if _reads_derivative(other, rates) else "coefficient")
                found[side.variable.id].append(
                    (tag if not generated else "generated-" + tag, owner))
        _walk(node.lhs, found, generated, owner, in_divisor, rates, environment)
        _walk(node.rhs, found, generated, owner, in_divisor, rates, environment)
        return

    if isinstance(node, VariableRef) and not node.is_derivative:
        if in_divisor == "guarded":
            found[node.variable.id].append(("guarded-divisor", owner))
        elif in_divisor:
            tag = "generated-divisor" if generated else "divisor"
            found[node.variable.id].append((tag, owner))
        return

    for child in node.children():
        _walk(child, found, generated, owner, in_divisor, rates, environment)


def _reads_derivative(expression, rates: set[int]) -> bool:
    """A `der()`, or a variable one equation defines as a `der()`."""
    for node in expression.walk():
        if not isinstance(node, VariableRef):
            continue
        if node.is_derivative or node.variable.id in rates:
            return True
    return False


def infer(model, environment=None) -> dict[int, ZeroContract]:
    """A zero contract for every parameter the source equations mention."""
    contracts: dict[int, ZeroContract] = {}
    uses = _uses(model, environment)
    by_id = {v.id: v for v in model.variables}

    for variable_id, occurrences in uses.items():
        variable = by_id.get(variable_id)
        if variable is None or not variable.is_parameter:
            continue
        tags = {tag for tag, _ in occurrences}
        declaration = _declaration(variable)

        # A source division outranks everything. One undefined use is enough.
        if "divisor" in tags:
            contracts[variable_id] = ZeroContract(
                behavior=ZeroBehavior.DIRECT_DIVISOR,
                confidence=Confidence.PROVEN, source=Source.EQUATION,
                reason="a source equation divides by this parameter",
                canonical_declaration=declaration, target=variable.name)
            continue

        if "derivative-coefficient" in tags:
            contracts[variable_id] = ZeroContract(
                behavior=ZeroBehavior.ALGEBRAIC_LIMIT,
                confidence=Confidence.PROVEN, source=Source.EQUATION,
                reason="the parameter multiplies a derivative, so at zero the "
                       "differential relation becomes an algebraic constraint "
                       "rather than an undefined quotient",
                canonical_declaration=declaration, target=variable.name)
            continue

        if "coefficient" in tags:
            contracts[variable_id] = ZeroContract(
                behavior=ZeroBehavior.FEATURE_DISABLED,
                confidence=Confidence.PROVEN, source=Source.EQUATION,
                reason="the parameter appears only as a multiplier, so at zero "
                       "the term it scales drops out and the rest of the model "
                       "is unaffected",
                canonical_declaration=declaration, target=variable.name)
            continue

        if tags & {"generated-divisor"}:
            contracts[variable_id] = ZeroContract(
                behavior=ZeroBehavior.UNKNOWN,
                confidence=Confidence.PROVEN, source=Source.EQUATION,
                reason="the only division by this parameter was introduced by "
                       "the compiler when it solved for a derivative; the "
                       "source contains none, so this says nothing about the "
                       "component's contract",
                canonical_declaration=declaration, target=variable.name)
    return contracts


def _declaration(variable) -> str:
    """`Class.member`, the identity a catalog or a user contract matches on."""
    contract = getattr(variable, "contract", None)
    declared_in = getattr(contract, "declared_in", None) if contract else None
    member = variable.name.rsplit(".", 1)[-1]
    return f"{declared_in}.{member}" if declared_in else member


def bounds_contract(variable, environment) -> ZeroContract | None:
    """What the declaration's own bounds say about zero."""
    domain = environment.domain(variable.id)

    # `min = -Modelica.Constants.inf` is not the absence of a bound. It is the
    # author writing down that the full signed range is intended --- the
    # off-diagonal elements of an inertia tensor are legitimately negative, and
    # `Body.mo` says so explicitly. Reading it as "nothing bounds this
    # declaration" contradicts the declaration it is quoting.
    if _is_explicit_infinite_min(variable):
        return ZeroContract(
            behavior=ZeroBehavior.ALLOWED, confidence=Confidence.PROVEN,
            source=Source.BOUND,
            reason="the declaration carries `min = -inf`, which states that the "
                   "full signed range is intended rather than leaving the "
                   "quantity unbounded by omission",
            canonical_declaration=_declaration(variable), target=variable.name)

    if domain.admits(0.0):
        return None
    return ZeroContract(
        behavior=ZeroBehavior.FORBIDDEN, confidence=Confidence.PROVEN,
        source=Source.BOUND,
        reason=f"the declaration excludes zero ({domain.reason or 'by its bounds'})",
        canonical_declaration=_declaration(variable), target=variable.name)


def declared_value_contract(variable, environment) -> ZeroContract | None:
    """Zero as the declaration's *own* value, rather than as a bound it forgot.

    `CoreParameters.GcRef` is

        final parameter SI.Conductance GcRef = if PRef <= 0 then 0 else ...

    with `PRef = 0` by default, so the record ships with `GcRef = 0` and the
    model that uses it writes `if PRef <= 0 then Gc = 0` beside it. A rule that
    demands `GcRef > 0` contradicts the value the library chose. A declaration
    is not silent about a value it evaluates to.

    This is declaration-level evidence, so it carries `BOUND` authority: a
    source division still outranks it, and a parameter defaulted to zero that
    something divides by stays a divide-by-zero.
    """
    binding = getattr(variable, "binding", None)
    if binding is None:
        return None

    from ..divisor.witness import Unevaluable, evaluate

    if _has_zero_branch(binding):
        return ZeroContract(
            behavior=ZeroBehavior.FEATURE_DISABLED,
            confidence=Confidence.DECLARED, source=Source.BOUND,
            reason="the binding is a conditional with a literal zero branch, "
                   "so the declaration itself names zero as one of the two "
                   "values it intends",
            canonical_declaration=_declaration(variable), target=variable.name)

    try:
        value = evaluate(binding, environment, {})
    except (Unevaluable, ZeroDivisionError, OverflowError, ValueError):
        return None
    if value != 0.0:
        return None

    return ZeroContract(
        behavior=ZeroBehavior.FEATURE_DISABLED, confidence=Confidence.DECLARED,
        source=Source.BOUND,
        reason="the declaration's own binding evaluates to zero at the "
               "declared configuration, so zero is the value the library "
               "chose rather than one it failed to exclude",
        canonical_declaration=_declaration(variable), target=variable.name)


def _has_zero_branch(expression, depth: int = 0) -> bool:
    """A binding that writes zero as one of its own alternatives.

    `GcRef = if PRef <= 0 then 0 else PRef/VRef^2/m` is the library saying that
    zero conductance is the *no core losses* configuration, and the model that
    consumes it writes `if PRef <= 0 then Gc = 0` beside it. Whether the
    current defaults select that branch is beside the point: the declaration
    has named zero either way.
    """
    if depth > 6 or not isinstance(expression, Conditional):
        return False
    alternatives = [value for _, value in expression.branches]
    alternatives.append(expression.fallback)
    for branch in alternatives:
        if (isinstance(branch, Literal) and branch.kind in ("real", "integer")
                and float(branch.value) == 0.0):
            return True
        if _has_zero_branch(branch, depth + 1):
            return True
    return False


def _is_explicit_infinite_min(variable) -> bool:
    """Whether the declaration writes `min = -inf` rather than omitting `min`.

    `Modelica.Constants.inf` is the largest representable number, not IEEE
    infinity, so `math.isinf` is the wrong test and reports nothing.
    """
    import math
    import sys

    from ..physical.engine import constant_value

    if variable.minimum is None:
        return False
    value = constant_value(variable.minimum)
    try:
        value = float(value)
    except (TypeError, ValueError):
        return False
    if math.isnan(value):
        return False
    return value <= -sys.float_info.max * 0.999
