#!/usr/bin/env python3
"""Connector graph: components, their connectors, and what is connected.

    python connector_graph.py circuit.rbc
    python connector_graph.py circuit.rbc --dot | dot -Tsvg -o topology.svg

Modelica connections are not directional messages. A connector carries
*potential* quantities, which are equated across a connection, and *flow*
quantities, which obey a signed conservation law. This pass keeps that
distinction rather than flattening every connection into "a sends to b".
"""

from __future__ import annotations

import argparse
import json
import sys
from collections import defaultdict

from rumoca_bitcode import Model


def connector_of(variable) -> str:
    """The connector instance a member belongs to: ``src.p.v`` -> ``src.p``."""
    return variable.name.rsplit(".", 1)[0]


def build(model: Model) -> dict:
    members: dict[str, list] = defaultdict(list)
    for variable in model.variables:
        if variable.is_connector_member:
            members[connector_of(variable)].append(variable)

    connectors = {}
    for path, variable_list in sorted(members.items()):
        component = path.split(".", 1)[0] if "." in path else ""
        connectors[path] = {
            "connector": path,
            "component": component,
            "members": [
                {
                    "name": variable.name.rsplit(".", 1)[1],
                    "variable": variable.name,
                    "quantity": variable.quantity,
                    "unit": variable.unit,
                    "connected": variable.connected,
                }
                for variable in sorted(variable_list, key=lambda v: v.name)
            ],
        }

    connections = [
        {
            "id": connection.id,
            "left": connection.left_connector,
            "right": connection.right_connector,
            "quantity": connection.quantity,
            "left_variable": connection.left.name,
            "right_variable": connection.right.name,
            "source": str(connection.source.span),
        }
        for connection in model.connections
    ]

    return {
        "model": model.name,
        "components": [component.path for component in model.components],
        "connectors": list(connectors.values()),
        "connections": connections,
    }


def to_dot(graph: dict) -> str:
    lines = ["graph topology {", "  rankdir=LR;", "  node [fontname=monospace];"]
    by_component: dict[str, list] = defaultdict(list)
    for connector in graph["connectors"]:
        by_component[connector["component"]].append(connector)
    for index, (component, connectors) in enumerate(sorted(by_component.items())):
        lines.append(f"  subgraph cluster_{index} {{")
        lines.append(f'    label="{component or graph["model"]}"; style=rounded;')
        for connector in connectors:
            quantities = ",".join(
                sorted({member["quantity"] or "?" for member in connector["members"]})
            )
            node = connector["connector"].replace(".", "_")
            lines.append(f'    {node} [label="{connector["connector"]}\\n({quantities})", shape=box];')
        lines.append("  }")
    for connection in graph["connections"]:
        left = connection["left"].replace(".", "_")
        right = connection["right"].replace(".", "_")
        style = "bold" if connection["quantity"] == "flow" else "solid"
        lines.append(f'  {left} -- {right} [style={style}, label="{connection["quantity"]}"];')
    lines.append("}")
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input")
    parser.add_argument("--dot", action="store_true")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    model = Model.load(args.input)
    graph = build(model)

    if args.dot:
        print(to_dot(graph))
        return 0
    if args.json:
        print(json.dumps(graph, indent=2))
        return 0

    print(f"model {graph['model']}")
    print(f"  components: {', '.join(graph['components']) or '-'}")
    print()
    print("  connectors:")
    for connector in graph["connectors"]:
        print(f"    {connector['connector']}")
        for member in connector["members"]:
            mark = "*" if member["connected"] else " "
            unit = f" [{member['unit']}]" if member["unit"] else ""
            print(f"      {mark} {member['name']:<16} {member['quantity']}{unit}")
    print()
    print("  connections:")
    if not graph["connections"]:
        print("    (none)")
    for connection in graph["connections"]:
        print(
            f"    [{connection['id']}] {connection['left']} <-> {connection['right']}"
            f"  ({connection['quantity']})  {connection['source']}"
        )
    return 0


if __name__ == "__main__":
    sys.exit(main())
