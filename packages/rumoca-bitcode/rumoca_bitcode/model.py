"""Object model for Rumoca Bitcode.

A pass author works with these classes, never with raw dictionaries::

    from rumoca_bitcode import Model

    model = Model.load("motor.rbc")
    for variable in model.variables:
        print(variable.name, variable.role, variable.unit)

Objects are thin views over the decoded document, so an edit through a helper
method is reflected when the model is saved. Editing the underlying ``raw``
dictionaries directly is allowed but unsupported: use the helpers, then call
:meth:`Model.save`, which recomputes the summary the validator checks.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterator

from . import _cbor

MAGIC = "RUMOCA-RBC"
VERSION = 1


class BitcodeError(Exception):
    """The artifact is not bitcode this SDK can read."""


# ── Provenance ───────────────────────────────────────────────────────────────


@dataclass(frozen=True)
class Source:
    """One source file referenced by the model."""

    id: int
    name: str
    text: str | None = None

    @property
    def short_name(self) -> str:
        return Path(self.name).name


@dataclass(frozen=True)
class Span:
    """A resolved source location.

    ``line`` and ``column`` are 1-based and precomputed by the exporter, so
    reporting ``Motor.mo:52`` never requires the source text.
    """

    source: Source | None
    start: int
    end: int
    line: int
    column: int

    def __str__(self) -> str:
        name = self.source.short_name if self.source else "<unknown>"
        if self.line:
            return f"{name}:{self.line}:{self.column}"
        return f"{name}@{self.start}"

    def text(self) -> str | None:
        """The exact source text this span covers, if the artifact embeds it."""
        if self.source is None or self.source.text is None:
            return None
        return self.source.text[self.start : self.end]


@dataclass(frozen=True)
class Provenance:
    """Why an object exists and where it came from."""

    origin: str
    """``"source"`` or ``"generated"``."""
    generation: str | None
    """For generated objects, the lowering kind, e.g. ``"connection_equation"``."""
    span: Span

    @property
    def is_generated(self) -> bool:
        return self.origin == "generated"

    def __str__(self) -> str:
        if self.generation:
            return f"{self.span} ({self.generation})"
        return str(self.span)


# ── Expressions ──────────────────────────────────────────────────────────────


class Expression:
    """Base class for the expression tree."""

    __slots__ = ("id", "provenance")

    def __init__(self, id: int, provenance: Provenance) -> None:
        self.id = id
        self.provenance = provenance

    def children(self) -> list["Expression"]:
        return []

    def walk(self) -> Iterator["Expression"]:
        """Yield this node and every descendant, parents first."""
        yield self
        for child in self.children():
            yield from child.walk()

    def variables(self) -> list["Variable"]:
        """Every variable this expression reads, in first-appearance order."""
        seen: dict[int, Variable] = {}
        for node in self.walk():
            if isinstance(node, VariableRef):
                seen.setdefault(node.variable.id, node.variable)
        return list(seen.values())


class Literal(Expression):
    __slots__ = ("kind", "value")

    def __init__(self, id, provenance, kind: str, value: Any) -> None:
        super().__init__(id, provenance)
        self.kind = kind
        self.value = value

    def __repr__(self) -> str:
        return repr(self.value) if self.kind == "string" else f"{self.value}"


class VariableRef(Expression):
    """A leaf naming a model quantity.

    ``kind`` distinguishes ``x`` from ``der(x)`` from ``pre(x)``; they are
    different coordinates of the same variable.
    """

    __slots__ = ("kind", "variable")

    def __init__(self, id, provenance, kind: str, variable: "Variable") -> None:
        super().__init__(id, provenance)
        self.kind = kind
        self.variable = variable

    @property
    def is_derivative(self) -> bool:
        return self.kind == "derivative"

    @property
    def is_previous(self) -> bool:
        return self.kind.startswith("pre_")

    def __repr__(self) -> str:
        if self.is_derivative:
            return f"der({self.variable.name})"
        if self.is_previous:
            return f"pre({self.variable.name})"
        return self.variable.name


class TimeRef(Expression):
    __slots__ = ()

    def __repr__(self) -> str:
        return "time"


class UnaryOp(Expression):
    __slots__ = ("op", "operand")

    def __init__(self, id, provenance, op: str, operand: Expression) -> None:
        super().__init__(id, provenance)
        self.op = op
        self.operand = operand

    def children(self) -> list[Expression]:
        return [self.operand]

    _SYMBOLS = {"negate": "-", "not": "not "}

    def __repr__(self) -> str:
        return f"{self._SYMBOLS.get(self.op, self.op + ' ')}{self.operand!r}"


class BinaryOp(Expression):
    __slots__ = ("op", "lhs", "rhs")

    def __init__(self, id, provenance, op: str, lhs: Expression, rhs: Expression) -> None:
        super().__init__(id, provenance)
        self.op = op
        self.lhs = lhs
        self.rhs = rhs

    def children(self) -> list[Expression]:
        return [self.lhs, self.rhs]

    _SYMBOLS = {
        "add": "+", "subtract": "-", "multiply": "*", "divide": "/", "power": "^",
        "equal": "==", "not_equal": "<>", "less": "<", "less_equal": "<=",
        "greater": ">", "greater_equal": ">=", "and": "and", "or": "or",
    }

    def __repr__(self) -> str:
        # Infix, fully parenthesised: a report a human reads should look like
        # the model they wrote, and explicit parentheses beat guessing at
        # precedence.
        return f"({self.lhs!r} {self._SYMBOLS.get(self.op, self.op)} {self.rhs!r})"


class Conditional(Expression):
    """``if c1 then v1 elseif c2 then v2 else fallback``."""

    __slots__ = ("branches", "fallback")

    def __init__(self, id, provenance, branches, fallback: Expression) -> None:
        super().__init__(id, provenance)
        self.branches = branches
        self.fallback = fallback

    def children(self) -> list[Expression]:
        out: list[Expression] = []
        for condition, value in self.branches:
            out.extend((condition, value))
        out.append(self.fallback)
        return out

    def __repr__(self) -> str:
        arms = " ".join(
            f"if {condition!r} then {value!r}" for condition, value in self.branches
        )
        return f"({arms} else {self.fallback!r})"


class BuiltinCall(Expression):
    """A pure built-in: `sqrt(x)`, `log(x)`, `min(a, b)`, ...

    `name` is the Modelica spelling, so a consumer matches on `"sqrt"` rather
    than on an ordinal that could shift between compiler versions.
    """

    __slots__ = ("name", "arguments")

    def __init__(self, id, provenance, name: str, arguments) -> None:
        super().__init__(id, provenance)
        self.name = name
        self.arguments = arguments

    def children(self) -> list[Expression]:
        return list(self.arguments)

    def __repr__(self) -> str:
        return f"{self.name}({', '.join(repr(a) for a in self.arguments)})"


class Unsupported(Expression):
    """A node bitcode v1 could not represent.

    Its presence means the artifact does not fully describe the model. A pass
    that cares about completeness should refuse rather than assume a value.
    """

    __slots__ = ("detail",)

    def __init__(self, id, provenance, detail: str) -> None:
        super().__init__(id, provenance)
        self.detail = detail

    def __repr__(self) -> str:
        return f"Unsupported({self.detail!r})"


# ── Model objects ────────────────────────────────────────────────────────────


@dataclass(frozen=True)
class ValueType:
    id: int
    scalar: str
    dimensions: tuple[int, ...]

    @property
    def is_scalar(self) -> bool:
        return not self.dimensions

    def __str__(self) -> str:
        if self.is_scalar:
            return self.scalar
        return f"{self.scalar}[{','.join(str(d) for d in self.dimensions)}]"


@dataclass(frozen=True)
class Component:
    """A component instance, identified by its flattened path."""

    id: int
    path: str

    def __str__(self) -> str:
        return self.path


class Variable:
    """One model variable in any role."""

    __slots__ = ("_raw", "_model")

    def __init__(self, raw: dict, model: "Model") -> None:
        self._raw = raw
        self._model = model

    id = property(lambda self: self._raw["id"])
    name = property(lambda self: self._raw["name"])
    role = property(lambda self: self._raw["role"])
    causality = property(lambda self: self._raw["causality"])
    scalar_count = property(lambda self: self._raw["scalar_count"])
    unit = property(lambda self: self._raw.get("unit"))
    description = property(lambda self: self._raw.get("description"))
    fixed = property(lambda self: self._raw.get("fixed"))
    tunable = property(lambda self: self._raw.get("tunable", False))
    from_source = property(lambda self: self._raw.get("from_source", False))

    @property
    def type(self) -> ValueType:
        return self._model.types[self._raw["value_type"]]

    @property
    def source(self) -> Provenance:
        return self._model._provenance(self._raw["declaration"])

    @property
    def component(self) -> Component | None:
        index = self._raw.get("component")
        return None if index is None else self._model.components[index]

    @property
    def is_state(self) -> bool:
        return self.role == "state"

    @property
    def is_parameter(self) -> bool:
        return self.role in ("parameter", "constant")

    @property
    def is_connector_member(self) -> bool:
        return self._raw.get("connector") is not None

    @property
    def quantity(self) -> str | None:
        """``"potential"``, ``"flow"`` or ``"stream"`` for a connector member."""
        connector = self._raw.get("connector")
        return None if connector is None else connector["quantity"]

    @property
    def connected(self) -> bool:
        connector = self._raw.get("connector")
        return bool(connector and connector.get("connected"))

    def _expression(self, key: str) -> Expression | None:
        index = self._raw.get(key)
        return None if index is None else self._model.expressions[index]

    start = property(lambda self: self._expression("start"))
    binding = property(lambda self: self._expression("binding"))
    minimum = property(lambda self: self._expression("min"))
    maximum = property(lambda self: self._expression("max"))

    def __repr__(self) -> str:
        unit = f" [{self.unit}]" if self.unit else ""
        return f"<Variable {self.id} {self.name} {self.role}{unit}>"


class Equation:
    """A residual equation: the model asserts ``residual == 0``."""

    __slots__ = ("_raw", "_model")

    def __init__(self, raw: dict, model: "Model") -> None:
        self._raw = raw
        self._model = model

    id = property(lambda self: self._raw["id"])

    @property
    def residual(self) -> Expression:
        return self._model.expressions[self._raw["residual"]]

    @property
    def source(self) -> Provenance:
        return self._model._provenance(self._raw["provenance"])

    @property
    def reads(self) -> list[Variable]:
        """Variables this equation reads.

        Precomputed by the compiler's own dependency projection, which resolves
        function calls and array selection correctly. Prefer this over walking
        the expression tree yourself.
        """
        return [self._model.variables[i] for i in self._raw.get("reads", [])]

    @property
    def reads_derivative(self) -> list[Variable]:
        """States whose derivative this equation reads."""
        return [self._model.variables[i] for i in self._raw.get("reads_derivative", [])]

    def __repr__(self) -> str:
        return f"<Equation {self.id} at {self.source.span}>"


class Connection:
    """One ``connect(...)`` relationship.

    A connection is symmetric: ``left`` and ``right`` are endpoints of an
    equality (for a potential quantity) or of a conservation law (for a flow
    quantity). It is not a directional message.
    """

    __slots__ = ("_raw", "_model")

    def __init__(self, raw: dict, model: "Model") -> None:
        self._raw = raw
        self._model = model

    id = property(lambda self: self._raw["id"])
    quantity = property(lambda self: self._raw["quantity"])
    left_connector = property(lambda self: self._raw["left_connector"])
    right_connector = property(lambda self: self._raw["right_connector"])

    @property
    def left(self) -> Variable:
        return self._model.variables[self._raw["left"]]

    @property
    def right(self) -> Variable:
        return self._model.variables[self._raw["right"]]

    @property
    def members(self) -> list[Variable]:
        return [self.left, self.right]

    @property
    def source(self) -> Provenance:
        return self._model._provenance(self._raw["provenance"])

    @property
    def is_flow(self) -> bool:
        return self.quantity == "flow"

    def __repr__(self) -> str:
        return f"<Connection {self.id} {self.left_connector} <-> {self.right_connector} ({self.quantity})>"


class Event:
    """An action performed when an event fires."""

    __slots__ = ("_raw", "_model")

    def __init__(self, raw: dict, model: "Model") -> None:
        self._raw = raw
        self._model = model

    id = property(lambda self: self._raw["id"])
    kind = property(lambda self: self._raw["action"]["kind"])

    @property
    def source(self) -> Provenance:
        return self._model._provenance(self._raw["provenance"])

    @property
    def state(self) -> Variable | None:
        """For a ``reinitialize`` action, the state it resets."""
        action = self._raw["action"]
        if action["kind"] != "reinitialize":
            return None
        return self._model.variables[action["state"]]

    @property
    def value(self) -> Expression | None:
        action = self._raw["action"]
        index = action.get("value") if action["kind"] == "reinitialize" else None
        return None if index is None else self._model.expressions[index]

    def __repr__(self) -> str:
        return f"<Event {self.id} {self.kind} at {self.source.span}>"


class TracePoint:
    """A request to observe a value at runtime."""

    __slots__ = ("_raw", "_model")

    def __init__(self, raw: dict, model: "Model") -> None:
        self._raw = raw
        self._model = model

    id = property(lambda self: self._raw["id"])
    label = property(lambda self: self._raw["label"])
    unit = property(lambda self: self._raw.get("unit"))
    quantity = property(lambda self: self._raw.get("quantity"))
    added_by = property(lambda self: self._raw.get("added_by"))

    @property
    def variable(self) -> Variable:
        return self._model.variables[self._raw["variable"]]

    @property
    def connection(self) -> Connection | None:
        index = self._raw.get("connection")
        return None if index is None else self._model.connections[index]

    def __repr__(self) -> str:
        return f"<TracePoint {self.id} {self.label!r}>"
