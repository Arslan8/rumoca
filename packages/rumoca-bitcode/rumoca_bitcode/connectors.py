"""Scalar connector authoring over canonical RBC equations and metadata."""
from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class ConnectorMember:
    name: str
    variable_id: int
    scalar_type: str
    unit: str
    kind: str
    shape: tuple = ()


class Connector:
    def __init__(self, raw, model):
        self.id = raw["id"]
        self.path = raw["path"]
        self.owner = raw["owner"]
        self.orientation = raw["orientation"]
        self.members = tuple(ConnectorMember(
            m["name"], m["variable"],
            model.raw_model["types"][model.raw_model["variables"][m["variable"]]["value_type"]]["scalar"],
            model.raw_model["variables"][m["variable"]].get("unit", ""), m["kind"],
            tuple(model.raw_model["types"][model.raw_model["variables"][m["variable"]]["value_type"]].get("dimensions", [])),
        ) for m in raw["members"])


class ConnectorBuilder:
    """Restricted scalar, non-stream connector construction.

    Sets are finalized atomically: callers must pass the complete set. This
    avoids mistaking edges of a multiway connection for independent flow sums.
    """

    def add_component(self, name, *, type_name=None):
        if any(c["path"] == name for c in self.raw["components"]):
            raise ValueError(f"duplicate component: {name}")
        return self._append("components", {"path": name, "class_name": type_name})

    def add_connector_type(self, name, *, members, flow_convention="positive_into_owner"):
        if flow_convention != "positive_into_owner":
            raise ValueError("unsupported-feature:connector-flow-convention")
        if not members or len({m["name"] for m in members}) != len(members):
            raise ValueError("connector members must be nonempty and unique")
        for m in members:
            if m.get("shape") or m["kind"] not in {"potential", "flow"} or m["scalar_type"] != "real":
                raise ValueError("unsupported-feature:connector-shape-type-or-stream")
        self.raw.setdefault("connector_types", [])
        return self._append("connector_types", {
            "name": name, "members": [dict(m) for m in members],
            "flow_convention": flow_convention})

    def add_connector(self, name, *, owner, type_id, orientation="outside"):
        if orientation not in {"inside", "outside"}:
            raise ValueError("unknown connector orientation")
        component = self.raw["components"][owner]
        path = component["path"] + "." + name
        self.raw.setdefault("connectors", [])
        if any(c["path"] == path for c in self.raw["connectors"]):
            raise ValueError(f"duplicate connector: {path}")
        definition = self.raw["connector_types"][type_id]
        members = []
        for member in definition["members"]:
            variable = self.add_variable(path + "." + member["name"],
                unit=member.get("unit"), quantity=member.get("quantity"),
                start=self.real(0.0), fixed=False)
            self.raw["variables"][variable]["component"] = owner
            self.raw["variables"][variable]["connector"] = {
                "quantity": member["kind"], "connected": False}
            members.append({"name": member["name"], "variable": variable, "kind": member["kind"]})
        return self._append("connectors", {"path": path, "owner": owner,
            "type_id": type_id, "orientation": orientation, "members": members,
            "provenance": self._provenance()})

    def member(self, connector, name):
        for m in self.raw["connectors"][connector]["members"]:
            if m["name"] == name:
                return m["variable"]
        raise KeyError(name)

    def add_connection_set(self, connectors):
        if not connectors or len(set(connectors)) != len(connectors):
            raise ValueError("connection set must contain distinct connectors")
        ports = [self.raw["connectors"][c] for c in connectors]
        if len({p["type_id"] for p in ports}) != 1:
            raise ValueError("connection set types differ")
        paths = [p["path"] for p in ports]
        if any(set(paths) & set(s["connectors"]) for s in self.raw["connection_sets"]):
            raise ValueError("overlapping finalized connection sets; supply the complete set")
        potentials, potential_equations, balances = [], [], []
        for index, prototype in enumerate(ports[0]["members"]):
            variables = [p["members"][index]["variable"] for p in ports]
            for variable in variables:
                self.raw["variables"][variable]["connector"]["connected"] = True
            if prototype["kind"] == "potential":
                potentials.extend(variables)
                for v in variables[1:]:
                    eq = self.add_equation(self.subtract(self.coordinate(variables[0]), self.coordinate(v)))
                    potential_equations.append(eq)
            else:
                terms = [{"variable": v, "negated": p["orientation"] == "inside"}
                         for p, v in zip(ports, variables)]
                exprs = [self.unary("negate", self.coordinate(t["variable"]))
                         if t["negated"] else self.coordinate(t["variable"]) for t in terms]
                expression = exprs[0]
                for expr in exprs[1:]:
                    expression = self.add(expression, expr)
                balances.append({"equation": self.add_equation(expression), "terms": terms})
        return self._append("connection_sets", {"connectors": paths,
            "potentials": potentials, "potential_equations": potential_equations,
            "balances": balances, "unconnected": len(ports) == 1,
            "provenance": self._provenance()})
