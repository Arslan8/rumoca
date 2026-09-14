#!/usr/bin/env python3
"""Automatic connector logging.

    python connector_logger.py motor.rbc -o motor-traced.rbc

Instruments every quantity that crosses a component boundary, without touching
the Modelica source and without altering a single equation.

Why this is a transformation and not just an analysis: it *writes* trace points
back into the artifact, which Rumoca then lowers into runtime observation. Why
it is safe: a trace point is observation metadata, so the physical model it
describes is bit-for-bit the one that was compiled. Nothing here can change what
the model computes.
"""

from __future__ import annotations

import argparse
import sys

from rumoca_bitcode import Model

TOOL = "connector_logger.py"


def instrument(model: Model, *, cross_component_only: bool = True) -> list:
    """Add one trace point per connector quantity on each connection.

    Both endpoints of a potential connection carry the same value by
    definition, so only one is traced. Flow endpoints are traced separately:
    their values are equal and opposite, and which one you are looking at is
    exactly what a reader wants to know.
    """
    added = []
    seen: set[int] = set()

    for connection in model.connections:
        left_component = _component(connection.left_connector)
        right_component = _component(connection.right_connector)
        if cross_component_only and left_component == right_component:
            continue

        # A connection names one member pair, but the interesting unit of
        # observation is the whole connector: voltage *and* current, angle *and*
        # torque. Walk every member of both connectors.
        for connector in (connection.left_connector, connection.right_connector):
            for variable in model.connector_members(connector):
                if not variable.is_connector_member or variable.id in seen:
                    continue
                if variable.quantity == "potential" and _already_traced(
                    model, connection, variable
                ):
                    continue
                seen.add(variable.id)
                trace = model.add_trace_point(
                    variable,
                    label=variable.name,
                    connection=connection,
                    added_by=TOOL,
                )
                added.append(trace)
    return added


def _component(connector_path: str) -> str:
    return connector_path.split(".", 1)[0] if "." in connector_path else connector_path


def _already_traced(model: Model, connection, variable) -> bool:
    """True when the equal partner of a potential quantity is already traced."""
    member = variable.name.rsplit(".", 1)[1]
    partner_connector = (
        connection.right_connector
        if variable.name.startswith(connection.left_connector + ".")
        else connection.left_connector
    )
    partner = f"{partner_connector}.{member}"
    return any(trace.variable.name == partner for trace in model.trace_points)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", help="a .rbc artifact")
    parser.add_argument("-o", "--output", required=True, help="where to write the instrumented artifact")
    parser.add_argument(
        "--all-connections",
        action="store_true",
        help="instrument internal connections too, not only cross-component ones",
    )
    args = parser.parse_args()

    model = Model.load(args.input)
    if not model.connections:
        print(
            f"{args.input}: no connections found; nothing to instrument.\n"
            "Connector provenance requires a model built from connected components.",
            file=sys.stderr,
        )
        return 1

    added = instrument(model, cross_component_only=not args.all_connections)
    model.save(args.output)

    print(f"{model.name}: added {len(added)} trace point(s)")
    for trace in added:
        unit = f" [{trace.unit}]" if trace.unit else ""
        print(f"  {trace.label:<24} {trace.quantity or '?':<10}{unit}")
    print(f"wrote {args.output}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
