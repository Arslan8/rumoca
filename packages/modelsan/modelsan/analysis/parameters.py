"""How parameters reach the equations that consume them.

BUG-006 and BUG-014 were both defects where the parameter carrying the unsound
bound and the expression that failed were in different components, connected
through a derived parameter. A per-component check cannot see those, so the
chain is computed here.
"""

from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass, field


@dataclass
class ParameterGraph:
    """Which parameters each parameter's binding depends on."""

    depends_on: dict[int, set[int]] = field(default_factory=lambda: defaultdict(set))
    dependents: dict[int, set[int]] = field(default_factory=lambda: defaultdict(set))

    def reachable_from(self, parameter_id: int) -> set[int]:
        """Every parameter whose value changes when this one does.

        Transitive, because a chain can be longer than one step:
        `k -> C -> C*der(v)` in BUG-006 goes through one derived parameter, and
        nothing says the next one will not go through two.
        """
        seen: set[int] = set()
        queue = [parameter_id]
        while queue:
            current = queue.pop()
            for child in self.dependents.get(current, set()):
                if child not in seen:
                    seen.add(child)
                    queue.append(child)
        return seen


def build(model) -> ParameterGraph:
    graph = ParameterGraph()
    for variable in model.variables:
        if not variable.is_parameter or variable.binding is None:
            continue
        for read in variable.binding.variables():
            if read.is_parameter and read.id != variable.id:
                graph.depends_on[variable.id].add(read.id)
                graph.dependents[read.id].add(variable.id)
    return graph
