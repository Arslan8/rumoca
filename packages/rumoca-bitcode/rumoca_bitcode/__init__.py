"""Rumoca Bitcode SDK.

Read, analyse and transform a compiled Modelica model without cloning Rumoca,
without Rust, and without matching any compiler version::

    from rumoca_bitcode import Model

    model = Model.load("motor.rbc")

    for connection in model.connections:
        print(connection)

    model.add_trace_point(some_variable, label="battery.pin.voltage")
    model.save("motor-traced.rbc")

The file format is the interface; this package is one convenient reader of it.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Iterable

from . import _cbor
from .model import (
    MAGIC,
    VERSION,
    BinaryOp,
    BitcodeError,
    Component,
    Conditional,
    Connection,
    Equation,
    Event,
    Expression,
    Literal,
    Provenance,
    Source,
    Span,
    TimeRef,
    TracePoint,
    UnaryOp,
    Unsupported,
    ValueType,
    Variable,
    VariableRef,
)

__all__ = [
    "Model",
    "Variable",
    "Equation",
    "Connection",
    "Event",
    "TracePoint",
    "Component",
    "ValueType",
    "Source",
    "Span",
    "Provenance",
    "Expression",
    "Literal",
    "VariableRef",
    "TimeRef",
    "UnaryOp",
    "BinaryOp",
    "Conditional",
    "Unsupported",
    "BitcodeError",
    "MAGIC",
    "VERSION",
]

_COORDINATE_KINDS = {
    "parameter",
    "input",
    "state",
    "derivative",
    "algebraic",
    "discrete_real",
    "discrete_value",
    "pre_state",
    "pre_algebraic",
    "pre_discrete_real",
    "pre_discrete_value",
}


class Model:
    """A compiled Modelica model loaded from bitcode."""

    def __init__(self, document: dict[str, Any]) -> None:
        magic = document.get("magic")
        if magic != MAGIC:
            raise BitcodeError(f"not a Rumoca Bitcode file: magic is {magic!r}")
        version = document.get("bitcode_version")
        if version != VERSION:
            raise BitcodeError(
                f"unsupported bitcode version {version}: this SDK reads version {VERSION}"
            )
        self._document = document
        self._raw = document["model"]
        self.producer: str = document.get("producer", "")
        self.name: str = self._raw["name"]

        self.sources: list[Source] = [
            Source(id=entry["id"], name=entry["name"], text=entry.get("text"))
            for entry in self._raw.get("sources", [])
        ]
        self.types: list[ValueType] = [
            ValueType(
                id=entry["id"],
                scalar=entry["scalar"],
                dimensions=tuple(entry.get("dimensions", [])),
            )
            for entry in self._raw.get("types", [])
        ]
        self.components: list[Component] = [
            Component(id=entry["id"], path=entry["path"])
            for entry in self._raw.get("components", [])
        ]
        self.variables: list[Variable] = [
            Variable(entry, self) for entry in self._raw.get("variables", [])
        ]
        self.expressions: list[Expression] = self._build_expressions()
        self.equations: list[Equation] = [
            Equation(entry, self) for entry in self._raw.get("equations", [])
        ]
        self.initial_equations: list[Equation] = [
            Equation(entry, self) for entry in self._raw.get("initial_equations", [])
        ]
        self.connections: list[Connection] = [
            Connection(entry, self) for entry in self._raw.get("connections", [])
        ]
        self.events: list[Event] = [Event(entry, self) for entry in self._raw.get("events", [])]
        self.trace_points: list[TracePoint] = [
            TracePoint(entry, self) for entry in self._raw.get("trace_points", [])
        ]

    # ── Loading and saving ───────────────────────────────────────────────────

    @classmethod
    def load(cls, path: str | Path) -> "Model":
        """Load an artifact, detecting CBOR or JSON automatically."""
        data = Path(path).read_bytes()
        return cls(decode(data))

    @classmethod
    def loads(cls, data: bytes) -> "Model":
        return cls(decode(data))

    def save(self, path: str | Path, *, format: str | None = None) -> None:
        """Write the model back out.

        The summary the Rust validator checks is recomputed first, so an
        artifact saved after editing is accepted by ``rumoca compile-bitcode``.
        """
        self.recompute_summary()
        path = Path(path)
        if format is None:
            format = "json" if path.suffix == ".json" else "cbor"
        if format == "json":
            path.write_text(json.dumps(self._document, indent=1) + "\n")
        elif format == "cbor":
            path.write_bytes(_cbor.dumps(self._document))
        else:
            raise ValueError(f"unknown format {format!r}; use 'cbor' or 'json'")

    # ── Convenience views ────────────────────────────────────────────────────

    @property
    def states(self) -> list[Variable]:
        return [variable for variable in self.variables if variable.role == "state"]

    @property
    def parameters(self) -> list[Variable]:
        return [variable for variable in self.variables if variable.role in ("parameter", "constant")]

    @property
    def inputs(self) -> list[Variable]:
        return [variable for variable in self.variables if variable.role == "input"]

    @property
    def outputs(self) -> list[Variable]:
        return [variable for variable in self.variables if variable.role == "output"]

    @property
    def algebraics(self) -> list[Variable]:
        return [variable for variable in self.variables if variable.role == "algebraic"]

    @property
    def summary(self) -> dict[str, int]:
        return dict(self._raw.get("summary", {}))

    def variable(self, name: str) -> Variable:
        """Look a variable up by its flattened name."""
        for variable in self.variables:
            if variable.name == name:
                return variable
        raise KeyError(name)

    def connector_members(self, connector_path: str) -> list[Variable]:
        """Every variable belonging to one connector instance."""
        prefix = connector_path + "."
        return [
            variable
            for variable in self.variables
            if variable.name.startswith(prefix) and "." not in variable.name[len(prefix) :]
        ]

    # ── Transformation ───────────────────────────────────────────────────────

    def add_trace_point(
        self,
        variable: Variable,
        *,
        label: str | None = None,
        connection: Connection | None = None,
        quantity: str | None = None,
        added_by: str | None = None,
    ) -> TracePoint:
        """Request that ``variable`` be observed at runtime.

        Trace points are observation metadata. Adding one does not alter any
        equation, so instrumentation cannot change what the model computes.
        """
        entry: dict[str, Any] = {
            "id": len(self._raw.setdefault("trace_points", [])),
            "variable": variable.id,
            "label": label or variable.name,
        }
        if connection is not None:
            entry["connection"] = connection.id
        resolved_quantity = quantity or variable.quantity
        if resolved_quantity is not None:
            entry["quantity"] = resolved_quantity
        if variable.unit is not None:
            entry["unit"] = variable.unit
        if added_by is not None:
            entry["added_by"] = added_by
        self._raw["trace_points"].append(entry)
        trace = TracePoint(entry, self)
        self.trace_points.append(trace)
        return trace

    def recompute_summary(self) -> None:
        """Recompute the denormalised counts the validator checks."""

        def count(role: str) -> int:
            return sum(1 for variable in self.variables if variable.role == role)

        self._raw["summary"] = {
            "variables": len(self.variables),
            "states": count("state"),
            "parameters": count("parameter"),
            "constants": count("constant"),
            "inputs": count("input"),
            "outputs": count("output"),
            "algebraics": count("algebraic"),
            "discrete_reals": count("discrete_real"),
            "discrete_values": count("discrete_value"),
            "equations": len(self.equations),
            "initial_equations": len(self.initial_equations),
            "expressions": len(self.expressions),
            "relations": len(self._raw.get("relations", [])),
            "conditions": len(self._raw.get("conditions", [])),
            "roots": len(self._raw.get("roots", [])),
            "events": len(self.events),
            "time_events": len(self._raw.get("time_events", [])),
            "connections": len(self.connections),
            "components": len(self.components),
            "trace_points": len(self.trace_points),
        }

    # ── Internals ────────────────────────────────────────────────────────────

    def _provenance(self, raw: dict) -> Provenance:
        origin = raw["origin"]
        kind = origin["kind"] if isinstance(origin, dict) else origin
        generation = origin.get("generation") if isinstance(origin, dict) else None
        span_raw = raw["span"]
        index = span_raw["source"]
        source = self.sources[index] if index < len(self.sources) else None
        span = Span(
            source=source,
            start=span_raw["start"],
            end=span_raw["end"],
            line=span_raw.get("line", 0),
            column=span_raw.get("column", 0),
        )
        return Provenance(origin=kind, generation=generation, span=span)

    def _build_expressions(self) -> list[Expression]:
        """Materialise the expression arena.

        Operands always reference strictly earlier nodes, so one forward pass
        builds the whole tree with no recursion and no cycle risk.
        """
        built: list[Expression] = []
        for entry in self._raw.get("expressions", []):
            node = entry["node"]
            kind = node["kind"]
            provenance = self._provenance(entry["provenance"])
            identifier = entry["id"]

            if kind == "literal":
                value = node["value"]
                built.append(Literal(identifier, provenance, value["kind"], value.get("value")))
            elif kind == "coordinate":
                coordinate = node["coordinate"]
                coordinate_kind = coordinate["kind"]
                if coordinate_kind == "time":
                    built.append(TimeRef(identifier, provenance))
                elif coordinate_kind in _COORDINATE_KINDS:
                    variable = self.variables[coordinate["variable"]]
                    built.append(VariableRef(identifier, provenance, coordinate_kind, variable))
                else:
                    built.append(
                        Unsupported(identifier, provenance, f"coordinate {coordinate_kind}")
                    )
            elif kind == "unary":
                built.append(
                    UnaryOp(identifier, provenance, node["op"], built[node["operand"]])
                )
            elif kind == "binary":
                built.append(
                    BinaryOp(
                        identifier,
                        provenance,
                        node["op"],
                        built[node["lhs"]],
                        built[node["rhs"]],
                    )
                )
            elif kind == "conditional":
                branches = [
                    (built[branch["condition"]], built[branch["value"]])
                    for branch in node["branches"]
                ]
                built.append(
                    Conditional(identifier, provenance, branches, built[node["fallback"]])
                )
            else:
                built.append(Unsupported(identifier, provenance, node.get("detail", kind)))
        return built

    def __repr__(self) -> str:
        return (
            f"<Model {self.name!r}: {len(self.variables)} variables, "
            f"{len(self.equations)} equations, {len(self.connections)} connections>"
        )


def decode(data: bytes) -> dict[str, Any]:
    """Decode an artifact, detecting the encoding from its first byte."""
    for byte in data:
        if byte not in (0x20, 0x09, 0x0A, 0x0D):
            first = byte
            break
    else:
        raise BitcodeError("empty bitcode artifact")
    if first == ord("{"):
        return json.loads(data.decode("utf-8"))
    return _cbor.loads(data)
