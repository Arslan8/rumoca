"""The connection graph: components, ports, and the nodes that join them.

Every other analysis in this package reasons about one declaration or one
equation. That is why the physical rules needed component contracts bolted on:
a declaration in isolation does not say what the thing *is*, and an equation in
isolation does not say what it belongs to.

A connector view changes the subject. An acausal model is a network — a
component is a box with ports, a port carries a potential and a flow, and a
node is where several ports meet and agree. Questions that have no form at
declaration level have an obvious one here: what meets at this node, what does
this component do to the power crossing its ports, which ports are wired to
nothing.

    Node   (MLS §9.2 connection set) --- one potential, one conservation law
    Port   one connector instance of one component, at one node
    Network  the whole graph, indexed both ways

Nothing here is causal. `left` and `right` never appear: a node is a set, and a
port is not an input or an output.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum


@dataclass(frozen=True)
class Balance:
    """One conservation law at a node: signed members summing to zero."""

    terms: tuple
    """`(variable, sign)` pairs."""

    equation: int | None = None

    @property
    def quantities(self) -> set:
        return {str(getattr(v, "physical_quantity", "") or "")
                for v, _ in self.terms} - {""}

    def render(self) -> str:
        return " + ".join(
            f"{'-' if sign < 0 else '+'}{v.name}" for v, sign in self.terms
        ) + " = 0"


class NodeKind(str, Enum):
    ACAUSAL = "acausal"
    """Carries a conservation law: several ports, flows summing to zero."""

    SIGNAL = "signal"
    """Potential only. A causal connector — `RealInput`, or an orientation
    object nested inside a frame — has no flow member and conserves nothing."""

    UNCONNECTED = "unconnected"
    """One port, wired to nothing, its flow forced to zero by MLS §9.2.

    Not a defect. A component compiled standalone has unconnected ports by
    construction, and that is the single commonest reason a model looks
    structurally singular in this corpus."""


@dataclass(frozen=True)
class Port:
    """One connector instance of one component, seen from its node."""

    connector: str
    """Instance path of the connector itself, e.g. `L.n`."""

    component: str
    """The instance that owns it, e.g. `L`. Empty at the top level."""

    node: int
    potentials: tuple = ()
    flows: tuple = ()
    """`(variable, sign)` pairs, the sign as the conservation law gives it."""

    @property
    def name(self) -> str:
        return self.connector

    def __str__(self) -> str:
        return self.connector


@dataclass
class Node:
    """One connection set: what is equated here and what is conserved here."""

    id: int
    connectors: tuple[str, ...]
    potentials: tuple = ()
    balances: tuple = ()
    """One `Balance` per conservation law. A MultiBody frame has two."""

    unconnected: bool = False
    potential_equations: tuple[int, ...] = ()
    source: object = None

    @property
    def flows(self) -> tuple:
        """`(variable, sign)` over every balance, for callers that only need
        the members. Anything checking a *law* must use `balances`."""
        return tuple(term for balance in self.balances for term in balance.terms)

    @property
    def kind(self) -> NodeKind:
        if self.unconnected:
            return NodeKind.UNCONNECTED
        return NodeKind.ACAUSAL if self.balances else NodeKind.SIGNAL

    @property
    def degree(self) -> int:
        return len(self.connectors)

    @property
    def components(self) -> tuple[str, ...]:
        seen: list[str] = []
        for connector in self.connectors:
            owner = _owner(connector)
            if owner and owner not in seen:
                seen.append(owner)
        return tuple(seen)

    @property
    def boundary(self) -> tuple[str, ...]:
        """Connectors belonging to the top-level model rather than to an
        instance inside it.

        A sub-circuit compiled on its own keeps its interface pins, and they
        are wired to its internals and to nothing else. The node then has one
        side and behaves as if it were short of an equation --- which is what
        a structural matching reports, without being able to say why.
        """
        return tuple(connector for connector in self.connectors
                     if not _owner(connector))

    def __str__(self) -> str:
        return " -- ".join(self.connectors) or f"node {self.id}"


@dataclass
class Component:
    """One instance, and the ports through which it meets the rest."""

    path: str
    class_name: str | None = None
    ports: list[Port] = field(default_factory=list)

    @property
    def leaf_class(self) -> str:
        return (self.class_name or "").rsplit(".", 1)[-1]

    @property
    def label(self) -> str:
        """A name for a reader. The top-level model owns its own connectors
        and has no instance path, which renders as nothing at all."""
        return self.path or "<top level>"

    def __str__(self) -> str:
        return f"{self.label}: {self.class_name or 'unknown class'}"


@dataclass
class Network:
    """The connection graph of one model."""

    nodes: list[Node] = field(default_factory=list)
    components: dict[str, Component] = field(default_factory=dict)
    ports: list[Port] = field(default_factory=list)

    #: Set when the artifact carries no connection sets at all, so that "no
    #: findings" from a network pass is distinguishable from "nothing to look
    #: at". An artifact produced before the exporter emitted sets, or a model
    #: with no `connect` in it, both land here.
    absent: bool = True

    def node(self, id: int) -> Node | None:
        return self.nodes[id] if 0 <= id < len(self.nodes) else None

    def ports_of(self, component: str) -> list[Port]:
        found = self.components.get(component)
        return list(found.ports) if found else []

    def neighbours(self, component: str) -> list[str]:
        """Components reachable from this one through one node."""
        seen: list[str] = []
        for port in self.ports_of(component):
            node = self.node(port.node)
            if node is None:
                continue
            for other in node.components:
                if other != component and other not in seen:
                    seen.append(other)
        return seen

    def summary(self) -> dict:
        kinds: dict[str, int] = {}
        for node in self.nodes:
            kinds[node.kind.value] = kinds.get(node.kind.value, 0) + 1
        return {"nodes": len(self.nodes), "components": len(self.components),
                "ports": len(self.ports), "by_kind": kinds}


def _owner(connector: str) -> str:
    return connector.rpartition(".")[0]


def build(model) -> Network:
    """Read the connection graph out of a canonical model.

    Reads `connection_sets`, which the exporter builds from Flat's connect
    equalities and flow sums. An artifact without them yields an empty network
    marked `absent`, never a network that merely looks unconnected.
    """
    sets = list(getattr(model, "connection_sets", ()) or ())
    network = Network(absent=not sets)

    classes = {component.path: getattr(component, "class_name", None)
               for component in getattr(model, "components", ()) or ()}

    for entry in sets:
        node = Node(
            id=int(entry.id),
            connectors=tuple(entry.connectors),
            potentials=tuple(entry.potentials),
            balances=tuple(
                Balance(terms=tuple((term.variable, term.sign)
                                    for term in balance.terms),
                        equation=balance.equation)
                for balance in entry.balances),
            unconnected=bool(entry.unconnected),
            potential_equations=tuple(
                getattr(entry, "potential_equations", ()) or ()),
        )
        network.nodes.append(node)

        for connector in node.connectors:
            owner = _owner(connector)
            prefix = f"{connector}."
            port = Port(
                connector=connector,
                component=owner,
                node=node.id,
                potentials=tuple(v for v in node.potentials
                                 if v.name.startswith(prefix)),
                flows=tuple((v, sign) for v, sign in node.flows
                            if v.name.startswith(prefix)),
            )
            network.ports.append(port)
            component = network.components.get(owner)
            if component is None:
                # A class is looked up for the owner and, failing that, for the
                # connector itself: a top-level `connect(a.p, b.p)` has owners
                # in the component table, while a bare connector at the top
                # level is its own instance.
                component = Component(path=owner,
                                      class_name=classes.get(owner))
                network.components[owner] = component
            component.ports.append(port)
    return network
