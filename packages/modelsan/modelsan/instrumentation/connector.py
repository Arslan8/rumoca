"""Instrumenting the connection graph: what to observe at every port.

The rest of this package asks for one variable at a time and gets back a column
of numbers. That is enough to check a divisor and not enough to check a
network, because the quantity a network conserves is carried jointly by two
members of a connector and means nothing when they are separated.

So a connector observation is a *pair*, tagged with the node it belongs to.
`RbcTracePoint` has carried a `connection` field since the schema was written
— the comment on it says "when it came from connector instrumentation" — and
this is the pass that fills it.

Two things are produced, and they are deliberately separate:

  - `requests(network)` states what a sanitizer needs observed, in the
    vocabulary the planner already resolves. Nothing here knows how a backend
    will satisfy it.
  - `instrument(model, network)` writes the trace points into an artifact, for
    the backend that satisfies them by reading the artifact. That is one
    supplier of the capability, not the definition of it.
"""

from __future__ import annotations

from dataclasses import dataclass

from ..runtime.anchors import CanonicalAnchor, EntityKind
from .capability import Capability
from .request import InstrumentationRequest

#: Who to name as the author of a trace point, so the instrumentation itself
#: has provenance and a later reader can tell a tool's observation from a
#: modeller's.
ADDED_BY = "modelsan.instrumentation.connector"


@dataclass(frozen=True)
class PortObservation:
    """One connector member to observe, and the node it belongs to."""

    node: int
    connector: str
    variable: object
    role: str
    """`potential` or `flow`."""

    sign: int = 1

    @property
    def label(self) -> str:
        return f"{self.connector}:{self.role}:{self.variable.name}"


def observations(network) -> list[PortObservation]:
    """Every connector member worth observing, in node order.

    Both halves of every port, including the potential of a signal node: a
    causal connector conserves nothing, but its value still belongs to the
    node, and leaving it out would make the graph's coverage depend on a
    property of the connector rather than on what was asked for.
    """
    found: list[PortObservation] = []
    for port in network.ports:
        for potential in port.potentials:
            found.append(PortObservation(
                node=port.node, connector=port.connector,
                variable=potential, role="potential"))
        for flow, sign in port.flows:
            found.append(PortObservation(
                node=port.node, connector=port.connector,
                variable=flow, role="flow", sign=sign))
    return found


def requests(network, requested_by: str = "network") -> list[InstrumentationRequest]:
    """What a network analysis needs observed, stated without saying how."""
    found = [
        InstrumentationRequest(
            capability=Capability.OBSERVE_CONNECTOR,
            anchor=CanonicalAnchor(EntityKind.VARIABLE,
                                   observation.variable.id,
                                   observation.variable.name),
            label=observation.label,
            requested_by=requested_by,
        )
        for observation in observations(network)
    ]
    if found:
        # One request for the grouping itself. Observing every member and not
        # knowing which node each belongs to would satisfy every request above
        # and none of the question.
        found.append(InstrumentationRequest(
            capability=Capability.CONNECTION_GRAPH,
            label="connection sets", requested_by=requested_by))
    return found


def instrument(model, network=None) -> int:
    """Write connector trace points into `model`, returning how many.

    Idempotent: a trace point this pass already added is recognised by its
    `added_by` and not duplicated, so instrumenting an instrumented artifact
    is a no-op rather than a doubling.
    """
    from ..network import graph as network_graph

    if network is None:
        network = network_graph.build(model)

    document = model._document["model"]           # noqa: SLF001 — the writer
    points = document.setdefault("trace_points", [])
    existing = {
        (point.get("variable"), point.get("connection_set"), point.get("label"))
        for point in points if point.get("added_by") == ADDED_BY
    }
    next_id = max((point.get("id", -1) for point in points), default=-1) + 1

    added = 0
    for observation in observations(network):
        key = (observation.variable.id, observation.node, observation.label)
        if key in existing:
            continue
        points.append({
            "id": next_id,
            "variable": observation.variable.id,
            "label": observation.label,
            "connection_set": observation.node,
            "quantity": observation.role,
            "unit": getattr(observation.variable, "unit", None),
            "added_by": ADDED_BY,
        })
        existing.add(key)
        next_id += 1
        added += 1
    if added:
        # The typed view is built at load; leaving it stale makes the model
        # summarise itself with the count it had before this pass ran.
        reload = getattr(model, "reload_trace_points", None)
        if callable(reload):
            reload()
    return added
