"""One place that owns the shared analyses, so they are computed once.

A sanitizer asks the context for what it needs. It never rebuilds the
dependency graph, and two sanitizers asking for blocks get the same objects, so
their findings anchor on the same block ids.
"""

from __future__ import annotations

from functools import cached_property

from . import blocks as _blocks
from . import dependencies as _dependencies
from . import parameters as _parameters


class AnalysisContext:
    """Lazily-computed, cached analyses over one canonical DAE."""

    def __init__(self, model) -> None:
        self.model = model

    @cached_property
    def dependencies(self) -> _dependencies.DependencyGraph:
        return _dependencies.build(self.model)

    @cached_property
    def blocks(self) -> list[_blocks.AlgebraicBlock]:
        return _blocks.build(self.dependencies)

    @cached_property
    def parameters(self) -> _parameters.ParameterGraph:
        return _parameters.build(self.model)

    @cached_property
    def algebraic_loops(self) -> list[_blocks.AlgebraicBlock]:
        return [b for b in self.blocks if b.is_loop]

    def variable(self, variable_id: int):
        for variable in self.model.variables:
            if variable.id == variable_id:
                return variable
        return None

    def equation(self, equation_id: int):
        for equation in self.model.equations:
            if equation.id == equation_id:
                return equation
        return None
