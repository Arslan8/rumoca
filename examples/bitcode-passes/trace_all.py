#!/usr/bin/env python3
"""Trace every observable variable, so a run can be compared against another tool.

    python trace_all.py model.rbc -o model-traced.rbc

`--simulate --trace-out` only reports variables the artifact declares as trace
points, and a freshly compiled artifact declares none. Differential testing
needs the whole state vector, not a chosen subset, so this pass instruments
everything and lets the comparison decide what is common to both tools.

Like connector_logger.py this only *adds observation metadata*: no equation,
variable or parameter is touched, so the model that runs is the model that was
compiled.
"""

from __future__ import annotations

import argparse
import sys

from rumoca_bitcode import Model

TOOL = "trace_all.py"


def instrument(model: Model, *, include_parameters: bool = False) -> list:
    """Add one trace point per variable that varies over the run.

    Parameters are constant for the whole trajectory, so tracing them costs a
    column per sample and tells the reader nothing a single line could not.
    They are available behind a flag for the case where a differential run
    disagrees and the parameter values themselves are in question.
    """
    added = []
    for variable in model.variables:
        if variable.is_parameter and not include_parameters:
            continue
        added.append(
            model.add_trace_point(variable, label=variable.name, added_by=TOOL)
        )
    return added


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", help="a .rbc artifact")
    parser.add_argument("-o", "--output", required=True)
    parser.add_argument(
        "--include-parameters",
        action="store_true",
        help="also trace parameters, which are constant over the run",
    )
    parser.add_argument("--quiet", action="store_true")
    args = parser.parse_args()

    model = Model.load(args.input)
    added = instrument(model, include_parameters=args.include_parameters)
    if not added:
        print(f"{args.input}: no traceable variables", file=sys.stderr)
        return 1
    model.save(args.output)
    if not args.quiet:
        print(f"{model.name}: added {len(added)} trace point(s)")
        print(f"wrote {args.output}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
