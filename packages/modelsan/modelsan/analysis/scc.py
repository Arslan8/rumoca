"""Strongly connected components of the equation dependency graph.

An SCC of size > 1 is a set of equations that must be solved together — an
algebraic loop. That is the unit SingularitySan and ConditionSan reason about,
so it is computed here once rather than inside either of them.
"""

from __future__ import annotations

from .dependencies import DependencyGraph


def _equation_successors(graph: DependencyGraph) -> dict[int, set[int]]:
    """Equation -> equations it shares a variable with.

    Projecting the bipartite graph onto equations is enough for finding loops,
    and keeps the SCC pass working on one node type.
    """
    successors: dict[int, set[int]] = {e: set() for e in graph.equations()}
    for equation in graph.equations():
        for variable in graph.reads(equation):
            for other in graph.written_by(variable):
                if other != equation:
                    successors[equation].add(other)
    return successors


def components(graph: DependencyGraph) -> list[list[int]]:
    """Tarjan's algorithm, iterative.

    Iterative rather than recursive because MSL models reach thousands of
    equations and CPython's recursion limit is not a property of the model.
    """
    successors = _equation_successors(graph)
    index_of: dict[int, int] = {}
    low: dict[int, int] = {}
    on_stack: set[int] = set()
    stack: list[int] = []
    result: list[list[int]] = []
    counter = 0

    for root in successors:
        if root in index_of:
            continue
        work = [(root, iter(sorted(successors[root])))]
        index_of[root] = low[root] = counter
        counter += 1
        stack.append(root)
        on_stack.add(root)

        while work:
            node, children = work[-1]
            advanced = False
            for child in children:
                if child not in index_of:
                    index_of[child] = low[child] = counter
                    counter += 1
                    stack.append(child)
                    on_stack.add(child)
                    work.append((child, iter(sorted(successors[child]))))
                    advanced = True
                    break
                if child in on_stack:
                    low[node] = min(low[node], index_of[child])
            if advanced:
                continue
            work.pop()
            if work:
                parent = work[-1][0]
                low[parent] = min(low[parent], low[node])
            if low[node] == index_of[node]:
                component = []
                while True:
                    member = stack.pop()
                    on_stack.discard(member)
                    component.append(member)
                    if member == node:
                        break
                result.append(sorted(component))
    return result
