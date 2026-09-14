"""Static analysis over a compiled model: find operations that can go invalid.

This is Detector #1. It does not try to prove anything safe — proving
`resistance != 0` for all reachable states is a much harder problem than
finding the operations where it *might* not hold, and the second is what
directs a parameter search.

Every site is reported with the variables and parameters its constrained
argument depends on, because those are exactly the knobs a search should turn.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from rumoca_bitcode import BinaryOp, BuiltinCall, Model, Unsupported, VariableRef

from .domains import Domain, domain_for_binary, domain_for_builtin


@dataclass
class Site:
    """One operation that can leave its mathematical domain."""

    domain: Domain
    equation_id: int
    source: str
    expression: str
    argument: str
    """Rendering of the constrained argument."""
    parameters: list = field(default_factory=list)
    """Parameters the constrained argument depends on — the search knobs."""
    variables: list = field(default_factory=list)
    """Runtime variables it depends on."""

    @property
    def condition(self) -> str:
        return self.domain.describe(self.argument)

    def __str__(self) -> str:
        knobs = ", ".join(p.name for p in self.parameters) or "(none)"
        return (
            f"  {self.domain.operation}: requires {self.condition}\n"
            f"      equation E{self.equation_id} at {self.source}\n"
            f"      expression   {self.expression}\n"
            f"      constrained  {self.argument}\n"
            f"      parameters   {knobs}\n"
            f"      why          {self.domain.why}"
        )


def _constrained_argument(node, domain: Domain):
    if isinstance(node, BinaryOp):
        return node.lhs if domain.argument == 0 else node.rhs
    if isinstance(node, BuiltinCall):
        if domain.argument < len(node.arguments):
            return node.arguments[domain.argument]
    return None


def find_domain_sites(model: Model) -> list[Site]:
    """Every operation in the model whose domain can be left."""
    sites: list[Site] = []
    for equation in model.equations + model.initial_equations:
        for node in equation.residual.walk():
            domain = None
            if isinstance(node, BinaryOp):
                domain = domain_for_binary(node.op)
            elif isinstance(node, BuiltinCall):
                domain = domain_for_builtin(node.name)
            if domain is None:
                continue

            argument = _constrained_argument(node, domain)
            if argument is None:
                continue

            # A literal argument is decided at compile time; if it is safe there
            # is nothing for a search to vary, and if it is unsafe the compiler
            # would have folded it.
            reads = argument.variables()
            if not reads and not _has_time(argument):
                continue

            sites.append(
                Site(
                    domain=domain,
                    equation_id=equation.id,
                    source=str(equation.source.span),
                    expression=repr(node),
                    argument=repr(argument),
                    parameters=[v for v in reads if v.is_parameter],
                    variables=[v for v in reads if not v.is_parameter],
                )
            )
    return sites


def _has_time(expression) -> bool:
    return any(type(node).__name__ == "TimeRef" for node in expression.walk())


def incomplete(model: Model) -> int:
    """How many expressions the artifact could not represent.

    Reported before any result that depends on a complete picture.
    """
    return sum(
        1
        for equation in model.equations
        for node in equation.residual.walk()
        if isinstance(node, Unsupported)
    )


def declared_ranges(model: Model) -> list:
    """Variables carrying a literal `min` or `max`.

    These are properties the author wrote down, so a value outside them is a
    contradiction of the model's own claim — no physics inference required.
    """
    out = []
    for variable in model.variables:
        for bound in (variable.minimum, variable.maximum):
            if bound is not None and hasattr(bound, "value"):
                out.append(variable)
                break
    return out


def risk_knobs(model: Model, risks: list["SingularRisk"]) -> list:
    """Parameters a structural risk implicates, most constrained first.

    `find_singular_risks` over-approximates: `m * a = f` and `f = d * v` are
    structurally identical residuals, and only the first is fatal at zero. Which
    one it is depends on the variable the equation is *matched to*, which needs
    BLT information bitcode does not carry.

    So the static pass is a candidate generator and simulation is the oracle.
    Ordering the search by these candidates is what makes that cheap: the
    parameter most likely to break the model is tried first, rather than
    somewhere in an exhaustive sweep.
    """
    return [risk.parameter for risk in risks]


def search_knobs(model: Model, sites: list[Site]) -> list:
    """Parameters worth varying, most promising first.

    Parameters gating a domain site come first and in order of how many sites
    they gate — those have a specific predicate to violate. When the model also
    declares ranges, every remaining parameter follows, because any of them can
    push a variable out of a declared bound without a domain site involved.
    """
    counts: dict[int, tuple] = {}
    for site in sites:
        for parameter in site.parameters:
            entry, hits = counts.get(parameter.id, (parameter, 0))
            counts[parameter.id] = (entry, hits + 1)
    ordered = [p for p, _ in sorted(counts.values(), key=lambda pair: -pair[1])]

    if declared_ranges(model):
        seen = {p.id for p in ordered}
        ordered += [p for p in model.parameters if p.id not in seen]

    # Structural risks go to the front: they name a parameter with a specific
    # predicate to violate, so they are the cheapest place for a search to
    # start.
    risks = [r.parameter for r in find_singular_risks(model)]
    front = [p for p in risks if p.type.scalar in ("real", "integer")]
    seen = {p.id for p in front}
    rest = [p for p in ordered if p.id not in seen and p.type.scalar in ("real", "integer")]
    return front + rest


# ── Detector: a declared bound that admits a structurally fatal value ─────────


@dataclass
class SingularRisk:
    """A parameter whose declared bound admits a value that breaks the model.

    Two shapes, both fatal and both invisible to the compiler:

    * **divisor** — the parameter appears as a denominator, so zero yields
      inf or nan.
    * **derivative coefficient** — the parameter multiplies a `der(x)` term.
      At zero, `J * der(w) = tau` degenerates to `0 = tau`: the equation stops
      determining its unknown and the system loses rank.

    The risk is that the *declaration* permits it. `m(min=0)` states that zero
    is legal; the component cannot survive it. MSL writes
    `min=Modelica.Constants.eps` elsewhere for exactly this reason, so the
    idiom exists and is simply not applied consistently.
    """

    parameter: object
    shape: str
    """``"divisor"`` or ``"derivative-coefficient"``."""
    equation_id: int
    source: str
    expression: str
    declared_min: float | None
    """``None`` when no `min` is declared at all — also permissive."""

    @property
    def admits_zero(self) -> bool:
        return self.declared_min is None or self.declared_min <= 0.0

    def __str__(self) -> str:
        bound = "no min declared" if self.declared_min is None else f"min = {self.declared_min:g}"
        return (
            f"  {self.shape}: `{self.parameter.name}` ({bound}) may be zero\n"
            f"      equation E{self.equation_id} at {self.source}\n"
            f"      {self.expression}"
        )


def _literal_value(expression):
    return getattr(expression, "value", None) if expression is not None else None


def _is_derivative(node) -> bool:
    return isinstance(node, VariableRef) and node.is_derivative


def _sole_parameter(expression):
    """The one parameter an expression reads, if it reads exactly one and nothing else."""
    reads = expression.variables()
    if len(reads) != 1 or not reads[0].is_parameter:
        return None
    return reads[0]


def _appears_only_within(residual, product, variable_ids: set[int]) -> bool:
    """True when those variables occur nowhere in `residual` outside `product`.

    Walks the whole residual once and counts occurrences inside and outside the
    candidate product. Equality of the two counts means the product is the
    variables' only appearance, so zeroing its coefficient removes them from
    the equation.
    """
    inside = {node.variable.id for node in product.walk() if isinstance(node, VariableRef)}
    inside &= variable_ids
    if inside != variable_ids:
        return False
    within = set(id(node) for node in product.walk())
    for node in residual.walk():
        if id(node) in within:
            continue
        if isinstance(node, VariableRef) and node.variable.id in variable_ids:
            return False
    return True


def find_singular_risks(model: Model) -> list[SingularRisk]:
    """Parameters whose declared bound admits a structurally fatal value."""
    risks: list[SingularRisk] = []

    for equation in model.equations:
        for node in equation.residual.walk():
            if not isinstance(node, BinaryOp):
                continue

            if node.op == "divide":
                parameter = _sole_parameter(node.rhs)
                shape = "divisor"
            elif node.op == "multiply":
                # A parameter that is the *sole coefficient* of a term: zeroing
                # it deletes that term's variables from the equation entirely.
                #
                # `J * der(w) = tau` is the obvious case, but MSL usually writes
                # `a = der(v); m * a = f`, so matching `der(...)` syntactically
                # misses it. What actually matters is whether the multiplied
                # variable survives elsewhere in the same equation: if it does
                # not, the equation stops determining it at zero.
                parameter, other = None, None
                for side, opposite in ((node.lhs, node.rhs), (node.rhs, node.lhs)):
                    candidate = _sole_parameter(side)
                    if candidate is not None:
                        parameter, other = candidate, opposite
                        break
                if parameter is None:
                    continue
                coefficients = {v.id for v in other.variables() if not v.is_parameter}
                if not coefficients:
                    continue
                if not _appears_only_within(equation.residual, node, coefficients):
                    continue
                shape = (
                    "derivative-coefficient"
                    if any(_is_derivative(n) for n in other.walk())
                    else "sole-coefficient"
                )
            else:
                continue

            if parameter is None:
                continue

            minimum = _literal_value(parameter.minimum)
            risk = SingularRisk(
                parameter=parameter,
                shape=shape,
                equation_id=equation.id,
                source=str(equation.source.span),
                expression=repr(node),
                declared_min=None if minimum is None else float(minimum),
            )
            if risk.admits_zero:
                risks.append(risk)

    # One report per parameter: a parameter used as a divisor in six equations
    # is one declaration to fix, not six findings.
    seen: set[int] = set()
    unique = []
    for risk in risks:
        if risk.parameter.id in seen:
            continue
        seen.add(risk.parameter.id)
        unique.append(risk)
    return unique
