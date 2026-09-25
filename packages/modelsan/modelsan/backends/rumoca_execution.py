"""Saved-program observation transport; never re-lowers numerical edits.

SPEC_0007 stage 4 / writable-execution-ir: effects are execution-owned and
equation edits invalidate their derivation. Native validation is authoritative.
"""
from __future__ import annotations

import csv
import math
import json
import re
from pathlib import Path

from rumoca_bitcode.execution import Program

PASS_NAME = "modelsan.observe-variables"
FILENAME = "modelsan-observations.csv"


def instrument(program, model, *, variable_ids):
    """Replayable execution pass: append observations without changing equations."""
    if len(variable_ids) != len(set(variable_ids)):
        raise ValueError("duplicate observation variable ID")
    variables = {v.id: v for v in model.variables}
    observed = {o["variable_id"]: o for o in program.numerical["observations"]}
    for identifier in variable_ids:
        target, observation = variables.get(identifier), observed.get(identifier)
        if target is None or observation is None or observation["name"] != target.name:
            raise ValueError(f"missing/stale observation {identifier}; explicitly lower with "
                             "complete observations and replay compatible passes")
    b = program.builder(PASS_NAME, options={"variable_ids": list(variable_ids)})
    sink = b.declare_csv_sink(
        key=PASS_NAME, filename=FILENAME,
        columns=["time_s", "publish_id", "phase", *[f"v{i}" for i in variable_ids]],
        metadata={"variables": [{"id": i, "name": variables[i].name} for i in variable_ids]},
    )
    with b.before_return(program.function("run_start")) as ir:
        ir.emit("csv.open", sink=sink)
    with b.before_return(program.function("publish")) as ir:
        values = [ir.emit("snapshot.time"), ir.emit("snapshot.sequence"), ir.emit("snapshot.phase")]
        values += [ir.emit("snapshot.value", variable_id=i) for i in variable_ids]
        ir.emit("csv.write_row", sink=sink, values=values)
    with b.before_return(program.function("run_finish")) as ir:
        ir.emit("csv.close", sink=sink)


def prepare(source: Path, destination: Path, *, executable: str, timeout: float,
            replay=None):
    program = Program.load(source)
    program.validate(executable=executable, timeout=timeout)
    if any(sink["filename"] == "domain-diagnostics.json" for sink in program.raw["sinks"]):
        raise ValueError("domain-diagnostics.json is reserved by ModelSan")
    targets = [v for v in program.model.variables if not v.is_parameter]
    if not targets:
        raise ValueError("no traceable variables")
    observed = {o["variable_id"] for o in program.numerical["observations"]}
    if replay is not None and not {v.id for v in targets} <= observed:
        program = program.relower(replay=replay, observe=[v.id for v in targets],
                                  executable=executable, timeout=timeout)
    instrument(program, program.model, variable_ids=[v.id for v in targets])
    program.save(destination, executable=executable, timeout=timeout)
    return targets


def read_trace(path: Path, targets):
    """Reject malformed evidence; preserve NaN/Inf values for NumericSan."""
    if not path.exists():
        return [], {}
    expected = ["time_s", "publish_id", "phase", *[f"v{v.id}" for v in targets]]
    times, columns = [], {v.name: [] for v in targets}
    with path.open(newline="", encoding="utf-8") as stream:
        rows = csv.DictReader(stream)
        if rows.fieldnames != expected:
            raise ValueError("malformed executable observation header")
        for row in rows:
            if None in row or any(value is None for value in row.values()):
                raise ValueError("malformed executable observation row")
            t = float(row["time_s"])
            if (not math.isfinite(t) or (times and t <= times[-1])
                    or int(row["publish_id"]) != len(times)
                    or row["phase"] not in {"initial", "sample", "settled"}):
                raise ValueError("invalid executable publication coordinates")
            times.append(t)
            for v in targets:
                columns[v.name].append(float(row[f"v{v.id}"]))
    return times, columns


def read_domain_diagnostics(path, stream):
    """Execution identities are deliberately not presented as DAE expression IDs."""
    from ..runtime.anchors import BackendAnchor, EntityKind
    from ..runtime.observations import ExpressionObservation
    if not path.exists():
        return {"available": False}
    evidence = json.loads(path.read_text())
    if (not isinstance(evidence, dict) or evidence.get("schema_version") != 1 or evidence.get("kind") != "solve-domain-diagnostics"
            or evidence.get("coordinates") != "internal-evaluation"
            or evidence.get("execution_policy") != "interpreter"
            or evidence.get("coverage") != "scalar-output-rows"
            or type(evidence.get("unobserved_evaluations")) is not int
            or evidence["unobserved_evaluations"] < 0
            or type(evidence.get("truncated")) is not bool
            or not isinstance(evidence.get("faults"), list)):
        raise ValueError("unknown domain diagnostic schema")
    requirements = {"division": "nonzero", "sqrt": "non-negative", "log": "positive",
                    "inverse-trig": "unit-interval"}
    for fault in evidence["faults"]:
        operation, requirement = fault["operation"], fault["requirement"]
        if requirements.get(operation) != requirement:
            raise ValueError("unknown domain operation/requirement")
        value, time = float(fault["operand_value"]), float(fault["time"])
        fingerprint, index = fault["program_sha1"], fault["instruction_index"]
        if (not math.isfinite(time) or not math.isfinite(value)
                or not re.fullmatch(r"[0-9a-f]{40}", fingerprint)
                or type(index) is not int or index < 0):
            raise ValueError("invalid domain diagnostic coordinate")
        stream.add(ExpressionObservation(time=time, value=value,
            backend=BackendAnchor("rumoca", f"solve:{fingerprint}/op:{index}", EntityKind.EXPRESSION),
            role=f"executed:{operation}:{requirement}"))
    from .rumoca_diagnostics import read_solver
    read_solver(evidence["solver"], stream)
    return evidence
