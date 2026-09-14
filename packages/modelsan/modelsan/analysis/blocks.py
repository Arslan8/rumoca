"""Algebraic blocks: the sets of equations that must be solved simultaneously.

A block is the unit at which singularity and conditioning are meaningful. A
single equation can be "singular" only in the trivial sense that its coefficient
vanished; a block is singular when its Jacobian loses rank, which is what
actually stops a solver.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from .dependencies import DependencyGraph
from .scc import components


@dataclass
class AlgebraicBlock:
    """One simultaneous system, identified by DAE ids.

    `equation_ids` and `variable_ids` are references into the canonical DAE,
    never copies — a finding anchored on a block resolves straight back to the
    model.
    """

    block_id: int
    equation_ids: list[int] = field(default_factory=list)
    variable_ids: list[int] = field(default_factory=list)

    @property
    def size(self) -> int:
        return len(self.equation_ids)

    @property
    def is_loop(self) -> bool:
        """More than one equation, so it cannot be solved by substitution."""
        return self.size > 1

    @property
    def is_square(self) -> bool:
        return len(self.equation_ids) == len(self.variable_ids)


def build(graph: DependencyGraph) -> list[AlgebraicBlock]:
    """Blocks in dependency order, smallest structural unit first."""
    blocks = []
    for index, component in enumerate(components(graph)):
        variables: set[int] = set()
        for equation in component:
            variables |= graph.reads(equation)
        blocks.append(AlgebraicBlock(
            block_id=index,
            equation_ids=sorted(component),
            variable_ids=sorted(variables),
        ))
    return blocks
