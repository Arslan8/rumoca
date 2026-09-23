"""Writing an artifact, not only reading one.

Rumoca Bitcode calls itself "a public, versioned interchange format", and the
spec promises a consumer needs no linkage against Rumoca's crates. Until this
module the only supported way to *modify* an artifact was `add_trace_point`,
and the only way to *produce* one was to be the Rumoca compiler. An interchange
format only one program can write is a export format.

`Builder` closes that. It appends to an existing model or, with
`Model.empty(name)`, starts from nothing, and it holds the three invariants
that are easy to break and expensive to debug:

**The expression arena is topologically ordered.** Every operand id must be
strictly less than its node's id — that is what makes a cycle unrepresentable
and evaluation a single forward pass
(`SPEC_RUMOCA_BITCODE.md` §9a). So the builder appends, and `rewrite_operand`
rebuilds the path from a tree's root rather than splicing in place.

**Ids are positions.** Every table is dense; a gap is a validation error, so
ids are assigned by the builder and never by the caller.

**Provenance is not optional.** Something a tool added must be
distinguishable from something the modeller wrote, so everything here carries
`generated` provenance and the name of the pass that added it.

What it is *not*: a type checker. It will let you multiply a Boolean by a
String, because the validator and the compiler are where that is caught and
duplicating the rule here would mean two places to disagree.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from .connectors import ConnectorBuilder

#: Roles a variable may hold, in the schema's spelling.
ROLES = ("parameter", "constant", "input", "state", "algebraic", "output",
         "discrete_real", "discrete_value")

#: The coordinate kind that names a variable of each role. `derivative` and the
#: `pre_*` kinds are separate constructors: they are a different question about
#: the same variable, not a different variable.
COORDINATE_OF_ROLE = {
    "parameter": "parameter", "constant": "parameter", "input": "input",
    "state": "state", "algebraic": "algebraic", "output": "algebraic",
    "discrete_real": "discrete_real", "discrete_value": "discrete_value",
}

_SCALARS = ("real", "integer", "boolean", "string", "enumeration", "record")


def _span(source: int = 0) -> dict:
    return {"source": source, "start": 0, "end": 0, "line": 0, "column": 0}


def generated(generation: str = "synthetic_residual", source: int = 0) -> dict:
    """Provenance for something a tool produced."""
    return {"origin": {"kind": "generated", "generation": generation},
            "span": _span(source)}


@dataclass
class Builder(ConnectorBuilder):
    """Append-only construction over one artifact.

    Obtain one with `model.builder("my_pass")` rather than constructing it, so
    the model and the document it edits cannot get out of step.
    """

    model: object
    pass_name: str
    generation: str = "synthetic_residual"
    added: dict = field(default_factory=dict)

    def __post_init__(self) -> None:
        self.raw = self.model.raw_model
        for table in ("sources", "types", "variables", "expressions",
                      "equations",
                      "initial_equations", "relations", "conditions", "roots",
                      "events", "time_events", "connections", "components",
                      "trace_points", "discrete_definitions",
                      "discrete_real_equations", "initial_discrete_values",
                      "domains", "functions", "equation_families",
                      "initial_equation_families", "connection_sets"):
            self.raw.setdefault(table, [])

    # ── bookkeeping ──────────────────────────────────────────────────────────

    def _append(self, table: str, entry: dict) -> int:
        index = len(self.raw[table])
        entry["id"] = index
        self.raw[table].append(entry)
        self.added[table] = self.added.get(table, 0) + 1
        return index

    def _provenance(self) -> dict:
        return generated(self.generation)

    # ── sources ──────────────────────────────────────────────────────────────

    def add_source(self, name: str, text: str | None = None) -> int:
        """Register a file a span can point at."""
        entry: dict = {"name": name}
        if text is not None:
            entry["text"] = text
        return self._append("sources", entry)

    def source(self, name: str) -> int:
        for entry in self.raw.get("sources", []):
            if entry["name"] == name:
                return entry["id"]
        return self.add_source(name)

    # ── types ────────────────────────────────────────────────────────────────

    def add_type(self, scalar: str = "real",
                 dimensions: list[int] | None = None) -> int:
        if scalar not in _SCALARS:
            raise ValueError(f"unknown scalar {scalar!r}; expected one of "
                             f"{list(_SCALARS)}")
        entry = {"scalar": scalar}
        if dimensions:
            entry["dimensions"] = list(dimensions)
        return self._append("types", entry)

    def scalar_type(self, scalar: str = "real") -> int:
        """An existing scalar type of this kind, or a new one.

        Reused rather than always appended: a model that ends up with two
        identical Real types has two ids that compare unequal and mean the
        same, which every consumer then has to normalise.
        """
        for entry in self.raw["types"]:
            if entry.get("scalar") == scalar and not entry.get("dimensions"):
                return entry["id"]
        return self.add_type(scalar)

    # ── variables ────────────────────────────────────────────────────────────

    def variable(self, name: str) -> int:
        """The id of an existing variable, by flattened name."""
        for entry in self.raw["variables"]:
            if entry["name"] == name:
                return entry["id"]
        raise KeyError(f"{name!r} is not a variable of {self.raw.get('name')}")

    def add_variable(self, name: str, role: str = "algebraic", *,
                     value_type: int | None = None, causality: str = "local",
                     start: int | None = None, fixed: bool | None = None,
                     binding: int | None = None, unit: str | None = None,
                     quantity: str | None = None, minimum: int | None = None,
                     maximum: int | None = None, scalar_count: int = 1,
                     declaring_class: str | None = None, owner: int | None = None,
                     scalar_type: str | None = None) -> int:
        """Append a variable in any role.

        `start`, `binding`, `minimum` and `maximum` are expression ids, not
        numbers: an attribute in this IR is an expression, and accepting a
        float here would hide that from a caller who then cannot write
        `min = -Modelica.Constants.inf`.
        """
        if owner is not None:
            name = self.raw["components"][owner]["path"] + "." + name
        if scalar_type is not None:
            value_type = self.scalar_type(scalar_type)
        if role == "state" and start is None:
            # A numerical seed, not an initialization constraint. Initial
            # equations own the initial value when fixed is false.
            start = self.real(0.0)
            if fixed is None:
                fixed = False
        if role not in ROLES:
            raise ValueError(f"unknown role {role!r}; expected one of "
                             f"{list(ROLES)}")
        entry: dict = {
            "name": name,
            "role": role,
            "causality": causality,
            "value_type": (self.scalar_type() if value_type is None
                           else value_type),
            "scalar_count": scalar_count,
            "from_source": False,
            "declaration": self._provenance(),
        }
        for key, value in (("start", start), ("binding", binding),
                           ("min", minimum), ("max", maximum),
                           ("unit", unit), ("physical_quantity", quantity),
                           ("declaring_class", declaring_class)):
            if value is not None:
                entry[key] = value
        if fixed is not None:
            entry["fixed"] = fixed
        contract = {"variability": _variability(role)}
        if declaring_class:
            contract["declared_in"] = declaring_class
        entry["contract"] = contract
        if owner is not None:
            entry["component"] = owner
        return self._append("variables", entry)

    def add_state(self, name: str, start: float = 0.0, **kwargs) -> int:
        """A continuous state, fixed at `start` by default.

        Fixed rather than free: a state a pass adds with a free initial value
        is one more unknown for the initialization to solve, which changes the
        system the pass was meant to observe.
        """
        kwargs.setdefault("fixed", True)
        return self.add_variable(name, "state",
                                 start=self.real(start), **kwargs)

    def add_parameter(self, name: str, value: float, **kwargs) -> int:
        return self.add_variable(name, "parameter", causality="parameter",
                                 binding=self.real(value), **kwargs)

    def add_algebraic(self, name: str, **kwargs) -> int:
        return self.add_variable(name, "algebraic", **kwargs)

    def add_discrete(self, name: str, start: float = 0.0,
                     real: bool = True, **kwargs) -> int:
        kwargs.setdefault("fixed", True)
        return self.add_variable(
            name, "discrete_real" if real else "discrete_value",
            value_type=self.scalar_type("real" if real else "integer"),
            start=self.real(start) if real else self.integer(int(start)),
            **kwargs)

    # ── expressions ──────────────────────────────────────────────────────────

    def add_expression(self, node: dict, value_type: int | None = None) -> int:
        """Append one node, checking the topological rule at the mistake.

        A forward operand is a validation error, but the validator runs much
        later and names a node id rather than the line that wrote it.
        """
        index = len(self.raw["expressions"])
        for operand in operands_of(node):
            if operand >= index:
                raise ValueError(
                    f"node {index} would reference operand {operand}, which "
                    f"is not strictly earlier; append its operands first")
        self.raw["expressions"].append({
            "id": index,
            "value_type": (self.scalar_type() if value_type is None
                           else value_type),
            "node": node,
            "provenance": self._provenance(),
        })
        self.added["expressions"] = self.added.get("expressions", 0) + 1
        return index

    # literals
    def real(self, value: float) -> int:
        return self.add_expression(
            {"kind": "literal", "value": {"kind": "real", "value": float(value)}})

    def integer(self, value: int) -> int:
        return self.add_expression(
            {"kind": "literal", "value": {"kind": "integer", "value": int(value)}},
            self.scalar_type("integer"))

    def boolean(self, value: bool) -> int:
        return self.add_expression(
            {"kind": "literal", "value": {"kind": "boolean", "value": bool(value)}},
            self.scalar_type("boolean"))

    def string(self, value: str) -> int:
        return self.add_expression(
            {"kind": "literal", "value": {"kind": "string", "value": str(value)}},
            self.scalar_type("string"))

    # coordinates
    def coordinate(self, variable: int, kind: str | None = None) -> int:
        """Name a variable. `kind` defaults to the one its role implies."""
        if kind is None:
            role = self.raw["variables"][variable].get("role", "algebraic")
            kind = COORDINATE_OF_ROLE.get(role, "algebraic")
        return self.add_expression(
            {"kind": "coordinate",
             "coordinate": {"kind": kind, "variable": variable}},
            self.raw["variables"][variable].get("value_type"))

    def derivative(self, variable: int) -> int:
        return self.add_expression(
            {"kind": "coordinate",
             "coordinate": {"kind": "derivative", "variable": variable}})

    def previous(self, variable: int) -> int:
        """`pre(v)` — the left limit, which is a different quantity from `v`."""
        role = self.raw["variables"][variable].get("role", "algebraic")
        kind = {"state": "pre_state", "algebraic": "pre_algebraic",
                "discrete_real": "pre_discrete_real",
                "discrete_value": "pre_discrete_value"}.get(role)
        if kind is None:
            raise ValueError(f"pre() does not apply to a {role} variable")
        return self.add_expression(
            {"kind": "coordinate",
             "coordinate": {"kind": kind, "variable": variable}},
            self.raw["variables"][variable].get("value_type"))

    def time(self) -> int:
        return self.add_expression({"kind": "coordinate",
                                    "coordinate": {"kind": "time"}})

    # operators
    def unary(self, op: str, operand: int) -> int:
        return self.add_expression({"kind": "unary", "op": op,
                                    "operand": operand})

    def binary(self, op: str, lhs: int, rhs: int,
               value_type: int | None = None) -> int:
        return self.add_expression({"kind": "binary", "op": op,
                                    "lhs": lhs, "rhs": rhs}, value_type)

    def add(self, lhs: int, rhs: int) -> int:
        return self.binary("add", lhs, rhs)

    def subtract(self, lhs: int, rhs: int) -> int:
        return self.binary("subtract", lhs, rhs)

    def multiply(self, lhs: int, rhs: int) -> int:
        return self.binary("multiply", lhs, rhs)

    def divide(self, lhs: int, rhs: int) -> int:
        return self.binary("divide", lhs, rhs)

    def conditional(self, branches: list[tuple[int, int]], fallback: int,
                    value_type: int | None = None) -> int:
        """`if c1 then v1 elseif c2 then v2 else fallback`."""
        return self.add_expression(
            {"kind": "conditional",
             "branches": [{"condition": condition, "value": value}
                          for condition, value in branches],
             "fallback": fallback},
            value_type)

    def builtin(self, name: str, arguments: list[int],
                value_type: int | None = None) -> int:
        return self.add_expression({"kind": "builtin", "name": name,
                                    "arguments": list(arguments)}, value_type)

    def array(self, elements: list[int], value_type: int | None = None) -> int:
        return self.add_expression({"kind": "array",
                                    "elements": list(elements)}, value_type)

    def field_of(self, base: int, field_index: int,
                 value_type: int | None = None) -> int:
        return self.add_expression({"kind": "field", "base": base,
                                    "field": field_index}, value_type)

    def range(self, start: int, stop: int, step: int | None = None) -> int:
        node = {"kind": "range", "start": start, "stop": stop}
        if step is not None:
            node["step"] = step
        return self.add_expression(node)

    def index(self, base: int, subscripts: list[dict],
              value_type: int | None = None) -> int:
        return self.add_expression({"kind": "index", "base": base,
                                    "subscripts": list(subscripts)},
                                   value_type)

    def call(self, function: int, arguments: list[int], output: int = 0,
             owner: int | None = None, value_type: int | None = None) -> int:
        index = len(self.raw["expressions"])
        return self.add_expression(
            {"kind": "call", "function": function, "output": output,
             "owner": index if owner is None else owner,
             "arguments": list(arguments)}, value_type)

    # ── equations ────────────────────────────────────────────────────────────

    def add_equation(self, residual: int, *, initial: bool = False,
                     reads: list[int] | None = None,
                     reads_derivative: list[int] | None = None) -> int:
        """Append `residual = 0`.

        `reads` is precomputed from the expression graph when not supplied.
        The schema carries it so no consumer has to re-derive it, and an
        equation that omits it leaves every dependency analysis with a hole.
        """
        found, derived, previous = self.reads_of(residual)
        entry: dict = {
            "residual": residual,
            "provenance": self._provenance(),
        }
        reads = found if reads is None else reads
        reads_derivative = derived if reads_derivative is None else reads_derivative
        if reads:
            entry["reads"] = sorted(set(reads))
        if reads_derivative:
            entry["reads_derivative"] = sorted(set(reads_derivative))
        if previous:
            entry["reads_previous"] = sorted(set(previous))
        return self._append(
            "initial_equations" if initial else "equations", entry)

    def add_derivative_equation(self, state: int, rhs: int) -> int:
        """`der(state) - rhs = 0`, the form the solver requires.

        Not a convenience. The runtime rejects a state equation that is not a
        *subtractive* derivative residual: writing the algebraically identical
        `der(x) + k*x` fails with "state equation is not a subtractive
        derivative residual", which is a true message about a constraint
        nothing else states. Encoded here so a caller meets it as an API and
        not as a simulation failure.
        """
        return self.add_equation(self.subtract(self.derivative(state), rhs))

    def add_initial_equation(self, residual: int) -> int:
        return self.add_equation(residual, initial=True)

    def ref(self, variable: int) -> int:
        return self.coordinate(variable)

    def sub(self, left: int, right: int) -> int:
        return self.subtract(left, right)

    def mul(self, left: int, right: int) -> int:
        return self.multiply(left, right)

    def div(self, left: int, right: int) -> int:
        return self.divide(left, right)

    def add_discrete_definition(self, targets: list[int],
                                branches: list[dict]) -> int:
        """An MLS Appendix B.1c definition: what a discrete value equals, when.

        Separate from `equations`, which carry continuous residuals only. A
        discrete-valued variable with no definition here is declared and never
        defined, and reconstruction rejects the artifact.
        """
        return self._append("discrete_definitions", {
            "targets": list(targets),
            "branches": list(branches),
            "provenance": self._provenance(),
        })

    # ── events ───────────────────────────────────────────────────────────────

    def add_relation(self, expression: int) -> int:
        return self._append("relations", {"expression": expression,
                                          "provenance": self._provenance()})

    def add_condition(self, node: dict) -> int:
        return self._append("conditions", {"node": node,
                                           "provenance": self._provenance()})

    def always(self) -> int:
        return self.add_condition({"kind": "always"})

    def when_relation(self, relation: int) -> int:
        return self.add_condition({"kind": "relation", "relation": relation})

    def add_root(self, relation: int, activation: int) -> int:
        """A zero crossing the solver must locate."""
        return self._append("roots", {"relation": relation,
                                      "activation": activation,
                                      "provenance": self._provenance()})

    def add_event(self, trigger: int, action: dict,
                  guard: int | None = None) -> int:
        """An action at an event: `assert`, `terminate` or `reinit`."""
        return self._append("events", {
            "trigger": trigger,
            "guard": self.always() if guard is None else guard,
            "action": action,
            "provenance": self._provenance(),
        })

    def assert_action(self, condition: int, message: str) -> dict:
        return {"kind": "assert", "condition": condition, "message": message}

    def terminate_action(self, message: str) -> dict:
        return {"kind": "terminate", "message": message}

    def reinitialize_action(self, variable: int, value: int) -> dict:
        return {"kind": "reinitialize", "variable": variable, "value": value}

    # ── observation ──────────────────────────────────────────────────────────

    def add_trace_point(self, variable: int, label: str, *,
                        connection_set: int | None = None,
                        connection: int | None = None,
                        quantity: str | None = None,
                        unit: str | None = None) -> int:
        entry: dict = {"variable": variable, "label": label,
                       "added_by": self.pass_name}
        for key, value in (("connection_set", connection_set),
                           ("connection", connection),
                           ("quantity", quantity), ("unit", unit)):
            if value is not None:
                entry[key] = value
        return self._append("trace_points", entry)

    # ── rewriting ────────────────────────────────────────────────────────────

    def remove(self, *, variables=(), equations=(), initial_equations=()):
        """Atomically remove scalar declarations/rows; return old-to-new ID maps.

        Remaining uses cause rejection, not cascading deletion. Structured and
        eventful owners need a structured transformation and are rejected here.
        """
        from .removal import remove
        return remove(self, variables=variables, equations=equations,
                      initial_equations=initial_equations)

    def rewrite_equation(self, equation: int, residual: int, *,
                         initial: bool = False) -> None:
        """Point an existing equation at a new residual.

        The one rewrite needing no path rebuild: an equation is not in the
        arena, so it may name a node appended after it. This is how a
        fault-injection pass replaces a term.
        """
        table = "initial_equations" if initial else "equations"
        entry = self.raw[table][equation]
        entry["residual"] = residual
        reads, derived, previous = self.reads_of(residual)
        for key, value in (("reads", reads), ("reads_derivative", derived),
                           ("reads_previous", previous)):
            if value:
                entry[key] = sorted(set(value))
            else:
                entry.pop(key, None)
        entry["provenance"] = self._provenance()

    def rewrite_operand(self, root: int, target: int, replacement: int) -> int:
        """A copy of the tree at `root` with `target` replaced, appended.

        Splicing in place is impossible: an existing node cannot come to
        reference a later one. So every ancestor of `target` is re-appended
        pointing at the new child, and nodes off the path are shared rather
        than copied — the arena is a DAG and there is no reason to grow it
        further than the edit requires.
        """
        memo: dict[int, int] = {target: replacement}

        def rebuild(node_id: int) -> int:
            if node_id in memo:
                return memo[node_id]
            node = self.raw["expressions"][node_id]["node"]
            children = operands_of(node)
            if not any(self._reaches(child, target) for child in children):
                memo[node_id] = node_id
                return node_id
            rebuilt = with_operands(
                node, {child: rebuild(child) for child in children})
            memo[node_id] = self.add_expression(
                rebuilt, self.raw["expressions"][node_id]["value_type"])
            return memo[node_id]

        return rebuild(root)

    def _reaches(self, node_id: int, target: int) -> bool:
        if node_id == target:
            return True
        node = self.raw["expressions"][node_id]["node"]
        return any(self._reaches(child, target) for child in operands_of(node))

    # ── inspection ───────────────────────────────────────────────────────────

    def reads_of(self, root: int) -> tuple[list[int], list[int], list[int]]:
        """`(reads, reads_derivative, reads_previous)` under an expression."""
        reads: list[int] = []
        derivatives: list[int] = []
        previous: list[int] = []
        seen: set[int] = set()

        def walk(node_id: int) -> None:
            if node_id in seen:
                return
            seen.add(node_id)
            node = self.raw["expressions"][node_id]["node"]
            if node.get("kind") == "coordinate":
                coordinate = node.get("coordinate", {})
                variable = coordinate.get("variable")
                kind = coordinate.get("kind", "")
                if variable is not None:
                    if kind == "derivative":
                        derivatives.append(variable)
                    elif kind.startswith("pre_"):
                        previous.append(variable)
                    else:
                        reads.append(variable)
            for child in operands_of(node):
                walk(child)

        walk(root)
        return reads, derivatives, previous

    # ── finishing ────────────────────────────────────────────────────────────

    def finish(self) -> dict:
        """Refresh the typed views and the summary; report what was added.

        Without it the model keeps the views it was built with and summarises
        itself with counts the validator rejects.
        """
        self.model.refresh()
        return dict(self.added)


def _variability(role: str) -> str:
    return {"parameter": "parameter", "constant": "constant",
            "discrete_real": "discrete", "discrete_value": "discrete"
            }.get(role, "continuous")


#: Which fields of each node kind are operands. Kept in one place so a caller
#: never has to know the shape of every node to walk or rewrite one.
_OPERAND_FIELDS = {
    "unary": ("operand",),
    "binary": ("lhs", "rhs"),
    "field": ("base",),
    "range": ("start", "step", "stop"),
    "comprehension": ("body",),
    "index": ("base",),
    "array_update": ("base", "value"),
    "conditional": ("fallback",),
}
_OPERAND_LISTS = {
    "builtin": ("arguments",),
    "array": ("elements",),
    "record": ("fields",),
    "call": ("arguments",),
}


def operands_of(node: dict) -> list[int]:
    """Every expression id this node references."""
    kind = node.get("kind", "")
    found: list[int] = []
    for name in _OPERAND_FIELDS.get(kind, ()):
        value = node.get(name)
        if isinstance(value, int):
            found.append(value)
    for name in _OPERAND_LISTS.get(kind, ()):
        value = node.get(name)
        if isinstance(value, list):
            found.extend(item for item in value if isinstance(item, int))
        elif isinstance(value, int):
            found.append(value)
    for branch in node.get("branches", ()) or ():
        if isinstance(branch, dict):
            found.extend(v for v in branch.values() if isinstance(v, int))
    return found


def with_operands(node: dict, mapping: dict[int, int]) -> dict:
    """A copy of `node` with its operands remapped."""
    out = dict(node)
    kind = node.get("kind", "")
    for name in _OPERAND_FIELDS.get(kind, ()):
        value = out.get(name)
        if isinstance(value, int):
            out[name] = mapping.get(value, value)
    for name in _OPERAND_LISTS.get(kind, ()):
        value = out.get(name)
        if isinstance(value, list):
            out[name] = [mapping.get(item, item) if isinstance(item, int)
                         else item for item in value]
        elif isinstance(value, int):
            out[name] = mapping.get(value, value)
    if node.get("branches"):
        out["branches"] = [
            {k: mapping.get(v, v) if isinstance(v, int) else v
             for k, v in branch.items()}
            for branch in node["branches"]
        ]
    return out
