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

    # Only real-valued parameters have a numeric boundary to sit on. A Boolean
    # switch or a String tag is a structural choice, not a value to perturb.
    return [p for p in ordered if p.type.scalar in ("real", "integer")]
