"""Equation–variable incidence, built once per model.

Several sanitizers need to know which equations touch which variables. Each
building its own graph would be both wasteful and inconsistent, so this is the
one place it happens. Nodes are DAE ids; nothing here copies a DAE object.
"""

from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass, field


@dataclass
class DependencyGraph:
    """Bipartite incidence between equation ids and variable ids.

    Derivatives are tracked separately from values: `der(x)` and `x` are
    different unknowns to a structural analysis, and conflating them makes an
    index-1 system look algebraically singular.
    """

    equation_reads: dict[int, set[int]] = field(default_factory=lambda: defaultdict(set))
    equation_reads_derivative: dict[int, set[int]] = field(
        default_factory=lambda: defaultdict(set))
    variable_in: dict[int, set[int]] = field(default_factory=lambda: defaultdict(set))

    def equations(self) -> list[int]:
        return sorted(self.equation_reads)

    def variables(self) -> list[int]:
        return sorted(self.variable_in)

    def reads(self, equation_id: int) -> set[int]:
        return self.equation_reads.get(equation_id, set())

    def written_by(self, variable_id: int) -> set[int]:
        """Equations that mention this variable."""
        return self.variable_in.get(variable_id, set())


def build(model) -> DependencyGraph:
    """Incidence from the exporter's `reads` sets.

    Deliberately not re-derived by walking expressions: the exporter computed
    these from the compiler's own incidence proof
    (`rumoca_eval_dae::for_each_scalar_coordinate`), which handles array and
    record coordinates that a naive expression walk gets wrong.
    """
    graph = DependencyGraph()
    for equation in model.equations:
        eid = equation.id
        for variable in equation.residual.variables():
            if variable.is_parameter:
                continue
            if getattr(variable, "is_derivative", False):
                graph.equation_reads_derivative[eid].add(variable.id)
            else:
                graph.equation_reads[eid].add(variable.id)
            graph.variable_in[variable.id].add(eid)
        graph.equation_reads.setdefault(eid, set())
    return graph
