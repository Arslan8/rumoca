"""The equation-variable bipartite graph, and a matching over it.

Modelica equations are acausal: `x = y` constrains both, and which one is
"solved for" is the compiler's choice, not the model's. So the question
"is this variable determined?" is a *matching* question over a bipartite
graph, not something readable from the syntax of an assignment.

A maximum matching answers it. Every unknown matched to a distinct equation
means the system is structurally solvable; an unmatched unknown means no
equation is left to determine it, and an unmatched equation means a constraint
with nothing to constrain.

**Arrays are counted, not skipped.** `Real x[3]` is *three* unknowns and a
`for i in 1:3` equation is *three* rows, but the canonical model carries each
as a single object with a count. So the graph is weighted: every node has a
capacity (a variable's `scalar_count`, a family's `scalar_rows`, 1 for a
scalar), and the matching is a maximum flow rather than a one-to-one pairing.
On an all-scalar model every capacity is 1 and this reduces exactly to the
ordinary bipartite matching.

The weighting is an over-approximation in the safe direction: it assumes any
row of a family can determine any scalar the family touches, which is true of
the common `x[i] = f(i)` shape and too generous for a family whose rows touch
disjoint slices. Being too generous means a *missed* defect, never an invented
one, which is the right way for a bug finder to be wrong.

**Structural, not algebraic.** `x + y = 0` and `2x + 2y = 0` match perfectly
and are singular. The matching proves nothing about rank, and §15 of the brief
is explicit that the two must not be conflated: a matching failure is a
`STRUCTURAL_MATCH_FAILURE`, never an `ALGEBRAIC_SINGULARITY`.
"""

from __future__ import annotations

from collections import deque
from dataclasses import dataclass, field

from .dependencies import DependencyGraph


#: Keys for MLS Appendix B.1b equations. Kept identical to
#: `dependencies._DISCRETE_BASE`, which is the other half of the same scheme.
DISCRETE_BASE = 1 << 24


def discrete_key(equation_id: int) -> int:
    return DISCRETE_BASE + equation_id


def is_discrete(key: int) -> bool:
    return key >= DISCRETE_BASE


def family_key(family_id: int) -> int:
    """A graph key for an equation family.

    Families and scalar equations are numbered independently, so family 0 and
    equation 0 would collide. Families take the negatives; `is_family` and
    `family_id_of` read them back.
    """
    return -(family_id + 1)


def is_family(key: int) -> bool:
    return key < 0


def family_id_of(key: int) -> int:
    return -key - 1


@dataclass
class StructuralGraph:
    """Which equations touch which unknowns, and how many of each there are.

    Only *unknowns* participate. A parameter is data, not something an equation
    has to determine, and including them would make every system look
    hopelessly under-constrained.
    """

    incident: dict[int, set[int]] = field(default_factory=dict)
    """equation key -> unknown ids it reads"""

    touching: dict[int, set[int]] = field(default_factory=dict)
    """unknown id -> equation keys that read it"""

    unknowns: set[int] = field(default_factory=set)
    equations: set[int] = field(default_factory=set)

    unknown_capacity: dict[int, int] = field(default_factory=dict)
    """unknown id -> how many scalars it stands for"""

    equation_capacity: dict[int, int] = field(default_factory=dict)
    """equation key -> how many scalar rows it stands for"""

    def region_of(self, seeds: set[int], equations: set[int]) -> tuple[set[int], set[int]]:
        """The connected component reachable from `seeds`.

        Reporting "the model is structurally singular" is useless; reporting
        the handful of equations and unknowns that actually fail to match is
        what a maintainer can act on (§14).
        """
        seen_variables: set[int] = set()
        seen_equations: set[int] = set()
        frontier = list(seeds)
        while frontier:
            variable = frontier.pop()
            if variable in seen_variables:
                continue
            seen_variables.add(variable)
            for equation in self.touching.get(variable, ()):
                if equation in seen_equations or equation not in equations:
                    continue
                seen_equations.add(equation)
                frontier.extend(self.incident.get(equation, ()))
        return seen_variables, seen_equations


def build(model, graph: DependencyGraph) -> StructuralGraph:
    """Bipartite incidence over the continuous system.

    Only the unknowns the *continuous* equations are responsible for. A
    variable determined elsewhere is not under-constrained just because no
    residual row mentions it:

      - a discrete-time variable is defined by an MLS Appendix B.1c definition
        (`when` activation), which lives in `discrete_definitions`;
      - a clocked variable belongs to a clock partition;
      - an input is supplied from outside the model by definition.

    Counting those as unmatched produced 1505 findings across 194 models, every
    one of them a clocked or discrete variable in a model that is perfectly
    well posed. ChuaCircuit, which has neither, matched 44 of 44.
    """
    determined_elsewhere: set[int] = set()
    for definition in getattr(model, "discrete_definitions", ()) or ():
        for target in getattr(definition, "targets", ()) or ():
            determined_elsewhere.add(getattr(target, "id", target))

    unknowns = {
        v.id for v in model.variables
        if not v.is_parameter
        and v.id not in determined_elsewhere
        and v.role not in ("discrete_real", "discrete_value", "input")
    }
    # A discrete-Real unknown is determined by a B.1b equation, so the two
    # enter the graph together or not at all. Including only the equations —
    # which is what happened while the B.1b partition went unexported and then
    # briefly after it was added — leaves the system looking over-constrained
    # by exactly the number of discrete-Real variables.
    discrete_real = {v.id for v in model.variables if v.role == "discrete_real"}
    if getattr(model, "discrete_real_equations", None):
        unknowns |= discrete_real
    capacity = {
        v.id: max(1, getattr(v, "scalar_count", 1) or 1)
        for v in model.variables if v.id in unknowns
    }

    def incident(key: int) -> set[int]:
        """What one constraint can determine.

        Value reads *and* derivative reads: the DAE counts a continuous state
        as one unknown, and the equation that contains `der(x)` is the one that
        determines it. Excluding derivative reads drops any state that appears
        only as `der(x)` out of the graph entirely — three of them in
        `Polyphase.Examples.Utilities.AnalysatorDC`.

        `pre(v)` reads are excluded, and that is the other half of the same
        point: `pre(v)` is the value `v` held at event entry, a known, so an
        equation reading it is not a candidate to determine `v`.
        """
        return {v for v in graph.reads(key) | graph.equation_reads_derivative.get(key, set())
                if v in unknowns}

    structural = StructuralGraph(unknowns=set(), equations=set())
    for equation in model.equations:
        reads = incident(equation.id)
        # An equation touching no unknown constrains nothing and is kept out of
        # the matching; it is reported separately rather than skewing the count.
        _add(structural, equation.id, reads, 1, capacity)

    # An array or `for` equation. Its rows were invisible to this graph until
    # the compiler started exporting families (TOOLBUG-014); before that, a
    # model with one looked short by exactly its extent, and the only honest
    # response was to skip the model entirely.
    for family in getattr(model, "equation_families", ()) or ():
        key = family_key(family.id)
        _add(structural, key, incident(key), max(1, family.scalar_rows), capacity)

    for equation in getattr(model, "discrete_real_equations", ()) or ():
        key = discrete_key(equation.id)
        _add(structural, key, incident(key), 1, capacity)
    return structural


def _add(structural: StructuralGraph, key: int, reads: set[int],
         rows: int, capacity: dict[int, int]) -> None:
    structural.incident[key] = reads
    structural.equations.add(key)
    structural.equation_capacity[key] = rows
    for variable in reads:
        structural.touching.setdefault(variable, set()).add(key)
        structural.unknowns.add(variable)
        structural.unknown_capacity[variable] = capacity.get(variable, 1)


@dataclass
class Matching:
    """A maximum matching, plus what it could not cover.

    With array unknowns and equation families a node is matched *partially*:
    `x[3]` can have two of its three scalars determined. `covered` records how
    much of each node the matching used.
    """

    witness_equations: set = field(default_factory=set)
    """Equations on the source side of the min cut: the over-constrained part."""
    witness_variables: set = field(default_factory=set)
    """Unknowns on the source side: the ones the shortfall is about."""

    covered_variables: dict[int, int] = field(default_factory=dict)
    covered_equations: dict[int, int] = field(default_factory=dict)
    variable_to_equation: dict[int, int] = field(default_factory=dict)
    """One representative equation per matched unknown, for reporting."""
    equation_to_variable: dict[int, int] = field(default_factory=dict)

    @property
    def size(self) -> int:
        return sum(self.covered_variables.values())

    def unmatched_variables(self, graph: StructuralGraph) -> set[int]:
        """Unknowns with at least one scalar no equation row determines."""
        return {
            v for v in graph.unknowns
            if self.covered_variables.get(v, 0) < graph.unknown_capacity.get(v, 1)
        }

    def unmatched_equations(self, graph: StructuralGraph) -> set[int]:
        """Equations with at least one row that determines nothing."""
        return {
            e for e in graph.equations
            if graph.incident.get(e)
            and self.covered_equations.get(e, 0) < graph.equation_capacity.get(e, 1)
        }


def maximum_matching(graph: StructuralGraph) -> Matching:
    """Maximum flow from equation rows to unknown scalars (Dinic's algorithm).

    Flow rather than Kuhn's augmenting-path matching because the nodes carry
    capacities: an array unknown absorbs `scalar_count` rows and a family
    supplies `scalar_rows`. Dinic rather than repeated BFS augmentation because
    a single MSL array can have a four-figure extent, and unit-augmenting that
    many times is the difference between a second and an hour.

    Iterative throughout. An earlier recursive augmentation overflowed the
    stack on deep DAEs despite a comment claiming otherwise.
    """
    flow = _Flow()
    source, sink = flow.node(), flow.node()
    equation_node = {e: flow.node() for e in sorted(graph.equations)}
    variable_node = {v: flow.node() for v in sorted(graph.unknowns)}

    for equation, node in equation_node.items():
        rows = graph.equation_capacity.get(equation, 1)
        if rows > 0 and graph.incident.get(equation):
            flow.edge(source, node, rows)
    for variable, node in variable_node.items():
        flow.edge(node, sink, graph.unknown_capacity.get(variable, 1))
    for equation, reads in graph.incident.items():
        for variable in sorted(reads):
            # An equation row can determine any one scalar it touches, so the
            # middle edges carry the whole node capacity, not one unit.
            flow.edge(equation_node[equation], variable_node[variable],
                      graph.equation_capacity.get(equation, 1))

    flow.run(source, sink)

    # The source side of the final min cut: the equations and unknowns that
    # actually witness the shortfall. Reporting the whole model as singular is
    # useless (§14), and the connected component is usually most of the model.
    cut = flow.source_side(source)
    matching = Matching()
    matching.witness_equations = {e for e, node in equation_node.items()
                                  if node in cut}
    matching.witness_variables = {v for v, node in variable_node.items()
                                  if node in cut}
    for equation, reads in sorted(graph.incident.items()):
        for variable in sorted(reads):
            used = flow.used(equation_node[equation], variable_node[variable])
            if used <= 0:
                continue
            matching.covered_equations[equation] = (
                matching.covered_equations.get(equation, 0) + used)
            matching.covered_variables[variable] = (
                matching.covered_variables.get(variable, 0) + used)
            matching.variable_to_equation.setdefault(variable, equation)
            matching.equation_to_variable.setdefault(equation, variable)
    return matching


class _Flow:
    """Dinic's algorithm on an adjacency list of paired forward/back edges.

    Kept private and minimal: the only client is `maximum_matching`, and a
    general-purpose flow library would be more code to audit than the twenty
    lines the matching actually needs.
    """

    def __init__(self) -> None:
        self.to: list[int] = []
        self.capacity: list[int] = []
        self.original: list[int] = []
        self.adjacency: list[list[int]] = []
        self.index: dict[tuple[int, int], int] = {}

    def node(self) -> int:
        self.adjacency.append([])
        return len(self.adjacency) - 1

    def edge(self, source: int, target: int, capacity: int) -> None:
        # Forward and back edge are added as a consecutive pair, so `edge ^ 1`
        # is the partner and `to[edge ^ 1]` is where the edge came from.
        self.index[(source, target)] = len(self.to)
        self.adjacency[source].append(len(self.to))
        self.to.append(target)
        self.capacity.append(capacity)
        self.original.append(capacity)
        self.adjacency[target].append(len(self.to))
        self.to.append(source)
        self.capacity.append(0)
        self.original.append(0)

    def used(self, source: int, target: int) -> int:
        edge = self.index.get((source, target))
        if edge is None:
            return 0
        return self.original[edge] - self.capacity[edge]

    def run(self, source: int, sink: int) -> int:
        total = 0
        while True:
            level = self._levels(source, sink)
            if level is None:
                return total
            progress = [0] * len(self.adjacency)
            while True:
                pushed = self._push(source, sink, level, progress)
                if not pushed:
                    break
                total += pushed

    def source_side(self, source: int) -> set[int]:
        """Nodes still reachable from the source in the residual graph.

        With the flow maximal this is one side of a minimum cut, which is the
        smallest honest explanation of why the matching fell short.
        """
        seen = {source}
        queue = deque([source])
        while queue:
            node = queue.popleft()
            for edge in self.adjacency[node]:
                if self.capacity[edge] > 0 and self.to[edge] not in seen:
                    seen.add(self.to[edge])
                    queue.append(self.to[edge])
        return seen

    def _levels(self, source: int, sink: int) -> list[int] | None:
        level = [-1] * len(self.adjacency)
        level[source] = 0
        queue = deque([source])
        while queue:
            node = queue.popleft()
            for edge in self.adjacency[node]:
                if self.capacity[edge] > 0 and level[self.to[edge]] < 0:
                    level[self.to[edge]] = level[node] + 1
                    queue.append(self.to[edge])
        return None if level[sink] < 0 else level

    def _push(self, source: int, sink: int, level: list[int],
              progress: list[int]) -> int:
        """One blocking-flow path, found iteratively.

        A recursive DFS here is the textbook spelling and is exactly what
        overflows on a wide model, so the path is carried on an explicit stack.
        """
        path: list[int] = []
        node = source
        while True:
            if node == sink:
                bottleneck = min(self.capacity[edge] for edge in path)
                for edge in path:
                    self.capacity[edge] -= bottleneck
                    self.capacity[edge ^ 1] += bottleneck
                return bottleneck
            advanced = False
            while progress[node] < len(self.adjacency[node]):
                edge = self.adjacency[node][progress[node]]
                target = self.to[edge]
                if self.capacity[edge] > 0 and level[target] == level[node] + 1:
                    path.append(edge)
                    node = target
                    advanced = True
                    break
                progress[node] += 1
            if advanced:
                continue
            if not path:
                return 0
            # Dead end: retreat, and never try this edge again on this phase.
            edge = path.pop()
            node = self.to[edge ^ 1]
            progress[node] += 1
