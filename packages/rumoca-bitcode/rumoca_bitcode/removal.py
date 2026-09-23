"""Atomic scalar equation/state removal, including dense-ID remapping.

Structured/event tables fail explicitly; no guessed reference traversal.
"""
from copy import deepcopy


def remove(builder, *, variables=(), equations=(), initial_equations=()):
    from .builder import operands_of, with_operands
    from . import Model
    raw = deepcopy(builder.raw)
    for table in ("domains", "functions", "equation_families", "initial_equation_families",
                  "discrete_definitions", "discrete_real_equations", "initial_discrete_values",
                  "relations", "conditions", "roots", "events", "time_events", "connections"):
        if raw.get(table):
            raise ValueError(f"scalar removal does not support {table}; use a structured transformation")
    maps = {}
    for table, removed in (("variables", variables), ("equations", equations),
                           ("initial_equations", initial_equations)):
        removed = set(removed)
        if not removed <= {r["id"] for r in raw[table]}:
            raise ValueError(f"unknown removal target in {table}")
        kept = [r for r in raw[table] if r["id"] not in removed]
        maps[table] = {r["id"]: i for i, r in enumerate(kept)}
        for i, r in enumerate(kept):
            r["id"] = i
        raw[table] = kept

    def variable(old):
        if old not in maps["variables"]:
            raise ValueError(f"removed variable {old} is still referenced")
        return maps["variables"][old]

    def equation(old):
        if old not in maps["equations"]:
            raise ValueError(f"removed equation {old} is owned by a connection set")
        return maps["equations"][old]

    roots = []
    attributes = ("start", "binding", "min", "max", "nominal")
    for v in raw["variables"]:
        roots += [v[k] for k in attributes if v.get(k) is not None]
        contract = v.get("contract") or {}
        if "binding_depends_on" in contract:
            contract["binding_depends_on"] = [variable(i) for i in contract["binding_depends_on"]]
    for table in ("equations", "initial_equations"):
        for row in raw[table]:
            roots.append(row["residual"])
            for key in ("reads", "reads_derivative", "reads_previous"):
                if key in row:
                    row[key] = [variable(i) for i in row[key]]
    for c in raw.get("connectors", []):
        for m in c["members"]:
            m["variable"] = variable(m["variable"])
    for c in raw.get("connection_sets", []):
        c["potentials"] = [variable(i) for i in c["potentials"]]
        c["potential_equations"] = [equation(i) for i in c.get("potential_equations", [])]
        for balance in c.get("balances", []):
            if balance.get("equation") is not None:
                balance["equation"] = equation(balance["equation"])
            for term in balance["terms"]:
                term["variable"] = variable(term["variable"])
    for trace in raw.get("trace_points", []):
        trace["variable"] = variable(trace["variable"])

    live = set()
    pending = roots[:]
    while pending:
        identifier = pending.pop()
        if identifier in live:
            continue
        live.add(identifier)
        node = raw["expressions"][identifier]["node"]
        if node["kind"] not in {"literal", "coordinate", "unary", "binary", "builtin", "conditional"}:
            raise ValueError(f"scalar removal does not support {node['kind']} expressions")
        pending.extend(operands_of(node))
    expressions = [e for e in raw["expressions"] if e["id"] in live]
    expression_map = {e["id"]: i for i, e in enumerate(expressions)}
    for i, entry in enumerate(expressions):
        entry["id"] = i
        entry["node"] = with_operands(entry["node"], expression_map)
        coordinate = entry["node"].get("coordinate", {})
        if "variable" in coordinate:
            coordinate["variable"] = variable(coordinate["variable"])
    raw["expressions"] = expressions
    for v in raw["variables"]:
        for key in attributes:
            if v.get(key) is not None:
                v[key] = expression_map[v[key]]
    for table in ("equations", "initial_equations"):
        for row in raw[table]:
            row["residual"] = expression_map[row["residual"]]
    document = deepcopy(builder.model._document)
    document.pop("execution", None)
    document["model"] = raw
    candidate = Model(document)
    candidate.validate()
    # Commit only after authoritative checked import; old Programs retain their
    # model object and consequently see the changed digest at validation/run.
    builder.raw.clear()
    builder.raw.update(raw)
    builder.model.refresh()
    return {**maps, "expressions": expression_map}
