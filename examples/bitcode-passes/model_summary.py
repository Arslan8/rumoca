#!/usr/bin/env python3
"""Model summary: counts every kind of object in a compiled model.

    python model_summary.py motor.rbc

Deliberately the simplest possible pass. Its job is to prove the artifact
carries enough to describe a model at a glance, and to be the thing you copy
when writing your own.
"""

from __future__ import annotations

import argparse
import json
import sys

from rumoca_bitcode import Model


def summarize(model: Model) -> dict:
    connectors = {
        variable.name.rsplit(".", 1)[0]
        for variable in model.variables
        if variable.is_connector_member
    }
    return {
        "model": model.name,
        "producer": model.producer,
        "variables": len(model.variables),
        "states": len(model.states),
        "parameters": len(model.parameters),
        "inputs": len(model.inputs),
        "outputs": len(model.outputs),
        "algebraics": len(model.algebraics),
        "equations": len(model.equations),
        "initial_equations": len(model.initial_equations),
        "events": len(model.events),
        "components": len(model.components),
        "connections": len(model.connections),
        "connectors": len(connectors),
        "trace_points": len(model.trace_points),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", help="a .rbc artifact")
    parser.add_argument("--json", action="store_true", help="machine-readable output")
    args = parser.parse_args()

    model = Model.load(args.input)
    result = summarize(model)

    if args.json:
        print(json.dumps(result, indent=2))
        return 0

    print(f"model {result['model']}  (compiled by {result['producer']})")
    width = max(len(key) for key in result)
    for key, value in result.items():
        if key in ("model", "producer"):
            continue
        print(f"  {key:<{width}} {value}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
