"""Network projection from declared connector identities, including open ports.

This consumes the public contract. It does not certify equation laws; that
remains the native validator's responsibility (docs/connector-validation.md).
"""
from .graph import Balance, Component, Network, Node, Port


def build_declared(model, declarations):
    ports = {p.path: p for p in declarations}
    owners = {c.id: c for c in model.components}
    variables = {v.id: v for v in model.variables}
    if len(ports) != len(declarations):
        raise ValueError("duplicate declared connector path")
    network = Network(absent=False, identity_source="declared-ids")
    membership = {}
    for entry in model.connection_sets:
        bound = []
        for path in entry.connectors:
            if path not in ports or path in membership:
                raise ValueError("missing declared port or overlapping connection sets")
            if ports[path].owner not in owners:
                raise ValueError("missing declared connector owner")
            membership[path] = entry.id
            bound.append(owners[ports[path].owner].path)
        node = Node(id=entry.id, connectors=tuple(entry.connectors), owners=tuple(bound),
                    potentials=tuple(entry.potentials),
                    balances=tuple(Balance(tuple((t.variable, t.sign) for t in balance.terms),
                                           balance.equation) for balance in entry.balances),
                    unconnected=entry.unconnected,
                    potential_equations=tuple(entry.potential_equations))
        network.nodes.append(node)
    claimed = set()
    for declared in declarations:
        if declared.owner not in owners:
            raise ValueError("missing declared connector owner")
        owner = owners[declared.owner]
        potentials, flows = [], []
        node = network.node(membership.get(declared.path))
        signs = {v.id: sign for v, sign in node.flows} if node else {}
        potential_ids = {v.id for v in node.potentials} if node else set()
        for member in declared.members:
            if member.variable_id not in variables or member.variable_id in claimed:
                raise ValueError("missing or multiply owned connector member")
            claimed.add(member.variable_id)
            variable = variables[member.variable_id]
            if member.kind == "potential":
                if node and variable.id not in potential_ids:
                    raise ValueError("declared potential absent from connection set")
                potentials.append(variable)
            elif member.kind == "flow":
                if node and variable.id not in signs:
                    raise ValueError("declared flow absent from connection balance")
                sign = signs[variable.id] if node else (-1 if declared.orientation == "inside" else 1)
                flows.append((variable, sign))
            else:
                raise ValueError("unsupported declared connector member kind")
        port = Port(connector=declared.path, component=owner.path,
                    node=membership.get(declared.path), potentials=tuple(potentials),
                    flows=tuple(flows), connector_id=declared.id, owner_id=declared.owner)
        network.ports.append(port)
        component = network.components.setdefault(owner.path, Component(owner.path, owner.class_name))
        component.ports.append(port)
    return network
