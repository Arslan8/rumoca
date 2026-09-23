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
    equation_reads_previous: dict[int, set[int]] = field(
        default_factory=lambda: defaultdict(set))
    """`pre(v)` reads: a dependency, but never a candidate to determine `v`."""
    variable_in: dict[int, set[int]] = field(default_factory=lambda: defaultdict(set))

    def equations(self) -> list[int]:
        return sorted(self.equation_reads)

    def variables(self) -> list[int]:
        return sorted(self.variable_in)

    def reads(self, equation_id: int) -> set[int]:
        return self.equation_reads.get(equation_id, set())

    def reads_previous(self, equation_id: int) -> set[int]:
        return self.equation_reads_previous.get(equation_id, set())

    def written_by(self, variable_id: int) -> set[int]:
        """Equations that mention this variable."""
        return self.variable_in.get(variable_id, set())


#: Keys for the B.1b partition start here. Scalar equations are non-negative
#: and families negative, so a third partition needs its own range rather than
#: a third sign.
_DISCRETE_BASE = 1 << 24


def _owners(model):
    """Every constraint, keyed, with the variables it reads.

    A scalar equation is keyed by its id; an array or `for` equation is a
    *family*, keyed negatively so it cannot collide with one
    (`analysis.structure.family_key`). Families were absent from the artifact
    entirely until TOOLBUG-014, so nothing here saw them.
    """
    for equation in model.equations:
        yield (equation.id, equation.reads, equation.reads_derivative,
               equation.reads_previous)
    for family in getattr(model, "equation_families", ()) or ():
        yield (-(family.id + 1), family.reads, family.reads_derivative,
               family.reads_previous)
    # MLS Appendix B.1b. A separate partition, so its key namespace is separate
    # too (`analysis.structure.discrete_key`).
    for equation in getattr(model, "discrete_real_equations", ()) or ():
        yield (_DISCRETE_BASE + equation.id, equation.reads,
               equation.reads_derivative, equation.reads_previous)


def build(model) -> DependencyGraph:
    """Incidence from the exporter's `reads` sets.

    Deliberately not re-derived by walking expressions: the exporter computed
    these from the compiler's own incidence proof
    (`rumoca_eval_dae::for_each_scalar_coordinate`), which handles array and
    record coordinates that a naive expression walk gets wrong.
    """
    graph = DependencyGraph()
    for eid, reads, derivatives, previous in _owners(model):
        for sink, group in ((graph.equation_reads, reads),
                            (graph.equation_reads_derivative, derivatives),
                            (graph.equation_reads_previous, previous)):
            for variable in group:
                if variable.is_parameter:
                    continue
                sink[eid].add(variable.id)
                graph.variable_in[variable.id].add(eid)
        graph.equation_reads.setdefault(eid, set())
    return graph
