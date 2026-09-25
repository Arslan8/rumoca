"""Writable public Solve programs and ordered lifecycle effects.

No numerical evaluator lives here. The installed compiler owns lowering,
checked reconstruction, operation types, effects, and runtime capabilities.
"""
from __future__ import annotations
from contextlib import contextmanager
from copy import deepcopy
from pathlib import Path
import hashlib
import json
import tempfile
from . import Model
from .compiler import invoke


def lower(model: Model, *, observe=None, executable=None, timeout=None) -> "Program":
    with tempfile.TemporaryDirectory(prefix="rbc-lower-") as tmp:
        source, target = Path(tmp) / "equations.rbc", Path(tmp) / "execution.json"
        document = deepcopy(model._document)
        document.pop("execution", None)
        Model(document).save(source)
        args = ["bitcode", "lower-execution", source, "--output", target]
        if observe is not None:
            for identifier in observe:
                args += ["--observe", str(identifier)]
        invoke(*args, executable=executable, timeout=timeout)
        artifact = Model.load(target)
    return Program(model, artifact._document["execution"])


class Program:
    def __init__(self, model, raw):
        self.model, self.raw = model, raw
        self._saved_signature = self._signature()

    def _signature(self):
        raw = {k: v for k, v in self.raw.items() if k != "revision"}
        return hashlib.sha256(json.dumps(raw, sort_keys=True).encode()).hexdigest()

    @classmethod
    def load(cls, path):
        model = Model.load(path)
        return cls(model, model._document["execution"])

    @property
    def numerical(self):
        """Writable scalar programs/storage/projection and observation mappings."""
        return self.raw["numerical"]

    def function(self, name):
        return self.raw["functions"][name]

    def add_function(self, name):
        if name in self.raw["functions"]:
            raise ValueError(f"duplicate function: {name}")
        self.raw["functions"][name] = []
        return self.function(name)

    def builder(self, pass_name, *, options=None):
        return Builder(self, pass_name, options or {})

    def _document(self):
        # Deliberately reads current equation data, including public raw edits.
        doc = deepcopy(self.model._document)
        doc["execution"] = deepcopy(self.raw)
        return doc

    def validate(self, *, strict=True, executable=None, timeout=None):
        with tempfile.TemporaryDirectory(prefix="rbc-execution-check-") as tmp:
            path = Path(tmp) / "program.rbc"
            Model(self._document()).save(path)
            invoke("bitcode", "check", path, *(["--strict"] if strict else []),
                   executable=executable, timeout=timeout)

    def save(self, path, *, include_equations=True, executable=None, timeout=None):
        if not include_equations:
            raise ValueError("execution v1 requires equations for derivation checking")
        signature = self._signature()
        if signature != self._saved_signature:
            self.raw["revision"] += 1
        self.validate(executable=executable, timeout=timeout)
        Model(self._document()).save(path)
        self._saved_signature = signature

    def relower(self, *, replay=None, observe=None, executable=None, timeout=None):
        """Explicit recipe replay; a caller supplies compatible pass implementations.

        Callbacks run only while authoring, never in the saved runtime process.
        Unknown recipes fail rather than dropping instrumentation.
        """
        recipes = deepcopy(self.raw["passes"])
        replay = replay or {}
        for recipe in recipes:
            if recipe["name"] not in replay:
                raise ValueError(f"no compatible replay implementation: {recipe['name']}")
        observed = [o["variable_id"] for o in self.numerical["observations"]]
        current = {v["id"]: v for v in self.model.raw_model["variables"]}
        for observation in self.numerical["observations"]:
            target = current.get(observation["variable_id"])
            if target is None:
                raise ValueError(f"unknown observation variable {observation['variable_id']}")
            if target["name"] != observation["name"]:
                raise ValueError(f"replay target identity changed: {observation['name']}")
        if observe is not None:
            observed = list(dict.fromkeys([*observed, *observe]))
        fresh = lower(self.model, observe=observed, executable=executable, timeout=timeout)
        for recipe in recipes:
            replay[recipe["name"]](fresh, self.model, **recipe["options"])
        fresh.validate(executable=executable, timeout=timeout)
        return fresh


class Builder:
    def __init__(self, program, pass_name, options):
        if any(p["name"] == pass_name for p in program.raw["passes"]):
            raise ValueError(f"duplicate execution pass: {pass_name}")
        self.program = program
        program.raw["passes"].append({"name": pass_name, "options": deepcopy(options)})
        program.raw["revision"] += 1

    def declare_csv_sink(self, *, key, filename, columns, metadata, column_types=None):
        if any(s["key"] == key or s["filename"] == filename for s in self.program.raw["sinks"]):
            raise ValueError(f"duplicate CSV sink: {key}/{filename}")
        if column_types is None:
            column_types = ["real", "integer", "string"] + ["real"] * (len(columns) - 3)
        self.program.raw["sinks"].append(dict(key=key, filename=filename, columns=columns, column_types=column_types, metadata=metadata))
        return key

    @contextmanager
    def at(self, body, index):
        """Insert at an explicit instruction position in any editable region."""
        yield Emitter(body, index)

    def before_return(self, body):
        return self.at(body, len(body))

    def replace(self, body, index, instruction):
        body[index] = deepcopy(instruction)

    def remove(self, body, index):
        return body.pop(index)


class Emitter:
    def __init__(self, body, index):
        self.body, self.index = body, index

    def argument(self, name):
        if name != "snapshot":
            raise ValueError(f"unknown lifecycle argument: {name}")
        return name

    def emit(self, op, **operands):
        # The implicit read-only snapshot is not a serialized mutable handle.
        operands.pop("snapshot", None)
        result = operands.get("result")
        if op.startswith("snapshot.") or op == "compute":
            if result is None:
                taken = {i.get("result") for i in self.body}
                n = 0
                while f"v{n}" in taken:
                    n += 1
                result = f"v{n}"
                operands["result"] = result
        self.body.insert(self.index, {"op": op, **deepcopy(operands)})
        self.index += 1
        return result
