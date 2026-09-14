#!/usr/bin/env python3
"""Dependency graph: which variables and equations depend on which.

    python dependency_graph.py motor.rbc
    python dependency_graph.py motor.rbc --dot | dot -Tsvg -o deps.svg
    python dependency_graph.py motor.rbc --influences throttle

The graph is structured data. Graphviz and the reachability query below are two
renderers of it, not the analysis itself.

Edges come from the ``reads`` list the compiler computed with its own dependency
projection, which resolves function calls and array selection correctly. Walking
the expression tree here would produce a weaker answer.
"""

from __future__ import annotations

import argparse
import json
import sys
from collections import defaultdict

from rumoca_bitcode import Model


class DependencyGraph:
    """A bipartite variable <-> equation graph.

    ``variable -> equation`` means the equation reads the variable.
    ``equation -> variable`` means the equation determines it, which at DAE
    level we approximate by the derivative it writes: a residual does not name
    its unknown, so an acausal equation has no single output.
    """

    def __init__(self, model: Model) -> None:
        self.model = model
        self.reads: dict[int, set[int]] = defaultdict(set)
        self.writes: dict[int, set[int]] = defaultdict(set)
        self.read_by: dict[int, set[int]] = defaultdict(set)

        for equation in model.equations:
            for variable in equation.reads:
                self.reads[equation.id].add(variable.id)
                self.read_by[variable.id].add(equation.id)
            for state in equation.reads_derivative:
                self.writes[equation.id].add(state.id)

    def influences(self, start: str, max_depth: int = 32) -> list[str]:
        """Every variable reachable from ``start`` through equations.

        This is reachability over the bipartite graph: a variable reaches an
        equation that reads it, and that equation reaches every other variable
        it touches.
        """
        origin = self.model.variable(start)
        seen = {origin.id}
        frontier = [origin.id]
        for _ in range(max_depth):
            next_frontier = []
            for variable in frontier:
                for equation in self.read_by.get(variable, ()):
                    touched = self.reads[equation] | self.writes[equation]
                    for other in touched:
                        if other not in seen:
                            seen.add(other)
                            next_frontier.append(other)
            if not next_frontier:
                break
            frontier = next_frontier
        seen.discard(origin.id)
        return sorted(self.model.variables[i].name for i in seen)

    def as_dict(self) -> dict:
        return {
            "model": self.model.name,
            "nodes": {
                "variables": [
                    {"id": v.id, "name": v.name, "role": v.role} for v in self.model.variables
                ],
                "equations": [
                    {"id": e.id, "source": str(e.source.span)} for e in self.model.equations
                ],
            },
            "edges": [
                {"from": {"variable": variable}, "to": {"equation": equation}}
                for equation, variables in sorted(self.reads.items())
                for variable in sorted(variables)
            ]
            + [
                {"from": {"equation": equation}, "to": {"derivative_of": variable}}
                for equation, variables in sorted(self.writes.items())
                for variable in sorted(variables)
            ],
        }

    def to_dot(self) -> str:
        lines = ["digraph dependencies {", "  rankdir=LR;", "  node [fontname=monospace];"]
        for variable in self.model.variables:
            shape = "doubleoctagon" if variable.is_state else "ellipse"
            lines.append(f'  v{variable.id} [label="{variable.name}", shape={shape}];')
        for equation in self.model.equations:
            lines.append(f'  e{equation.id} [label="eq {equation.id}", shape=box];')
        for equation, variables in sorted(self.reads.items()):
            for variable in sorted(variables):
                lines.append(f"  v{variable} -> e{equation};")
        for equation, variables in sorted(self.writes.items()):
            for variable in sorted(variables):
                lines.append(f'  e{equation} -> v{variable} [style=bold, label="der"];')
        lines.append("}")
        return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input")
    parser.add_argument("--dot", action="store_true", help="emit Graphviz")
    parser.add_argument("--json", action="store_true", help="emit the structured graph")
    parser.add_argument("--influences", metavar="VARIABLE", help="what this variable can affect")
    args = parser.parse_args()

    model = Model.load(args.input)
    graph = DependencyGraph(model)

    if args.dot:
        print(graph.to_dot())
        return 0
    if args.json:
        print(json.dumps(graph.as_dict(), indent=2))
        return 0
    if args.influences:
        try:
            reachable = graph.influences(args.influences)
        except KeyError:
            print(f"no variable named {args.influences!r}", file=sys.stderr)
            return 1
        print(f"{args.influences} can influence {len(reachable)} variable(s):")
        for name in reachable:
            print(f"  {name}")
        return 0

    print(f"{model.name}: {len(model.variables)} variables, {len(model.equations)} equations")
    for equation in model.equations:
        reads = ", ".join(v.name for v in equation.reads) or "-"
        writes = ", ".join(f"der({v.name})" for v in equation.reads_derivative)
        arrow = f" -> {writes}" if writes else ""
        print(f"  eq {equation.id:>3} [{equation.source.span}]  reads: {reads}{arrow}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
