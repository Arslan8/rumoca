#!/usr/bin/env python3
"""Resolve which component class actually declares a parameter.

A finding names an instance path — `L.L`, `genericFluxTube.material.B_myMax`.
Reporting it against a file found by grepping the leaf name is unsafe: 14
components declare `k`, 26 declare `Goff`. The declaring class has to come from
the model's own structure.

`getComponents(Class)` returns each component's class, so the path is walked one
segment at a time. Everything for one round is issued in a single OMC session,
because loading MSL dominates the cost.
"""
import os, re, subprocess, tempfile
from pathlib import Path

MSL = ("/data/mrumoca/rumoca/target/msl/ModelicaStandardLibrary-4.1.0/"
       "Modelica 4.1.0/package.mo")
CORPUS = "/data/mrumoca/rumoca/target/corpus/ModelicaStandardLibrary-4.1.0"
ENV = {**os.environ, "CC": "gcc"}

# {Class.Path, componentName, "comment", "public", ...}
ENTRY = re.compile(r"\{([\w.]+)\s*,\s*(\w+)\s*,")


def components(classes: list[str], timeout: float = 900) -> dict[str, dict[str, str]]:
    """{class: {component name: component class}} for each class asked about."""
    if not classes:
        return {}
    needs_test = any(c.startswith("ModelicaTest.") for c in classes)
    lines = [f'loadFile("{CORPUS}/Modelica/package.mo"); getErrorString();',
             f'loadFile("{CORPUS}/ModelicaTest/package.mo"); getErrorString();'] \
        if needs_test else [f'loadFile("{MSL}"); getErrorString();']
    for i, name in enumerate(classes):
        lines.append(f'print("@@C {i}\\n");')
        lines.append(f"getComponents({name});")

    with tempfile.TemporaryDirectory() as work:
        script = Path(work) / "c.mos"
        script.write_text("\n".join(lines) + "\n")
        try:
            done = subprocess.run(["omc", str(script)], cwd=work, capture_output=True,
                                  text=True, timeout=timeout, env=ENV)
            text = done.stdout + done.stderr
        except subprocess.TimeoutExpired:
            return {}

    out = {}
    for chunk in text.split("@@C ")[1:]:
        head, _, body = chunk.partition("\n")
        try:
            index = int(head.strip())
        except ValueError:
            continue
        out[classes[index]] = {name: cls for cls, name in ENTRY.findall(body)}
    return out


def declaring_classes(pairs: list[tuple[str, str]]) -> dict[tuple[str, str], str]:
    """For each (model, parameter path), the class that declares the leaf.

    Walked breadth-first so every path advances one segment per OMC session.
    """
    # state: key -> (current class, remaining segments)
    state = {}
    for model, path in pairs:
        segments = path.split(".")
        state[(model, path)] = (model, segments[:-1])

    for _ in range(6):  # deepest MSL instance paths seen are ~4 segments
        pending = sorted({cls for cls, rest in state.values() if rest})
        if not pending:
            break
        table = components(pending)
        for key, (cls, rest) in list(state.items()):
            if not rest:
                continue
            child = table.get(cls, {}).get(rest[0])
            if child is None:
                state[key] = (cls, [])  # cannot resolve further; keep what we have
            else:
                state[key] = (child, rest[1:])
    return {key: cls for key, (cls, _) in state.items()}


if __name__ == "__main__":
    import json, sys
    pairs = [tuple(line.split("\t")) for line in sys.stdin.read().splitlines() if "\t" in line]
    resolved = declaring_classes(pairs)
    print(json.dumps({f"{m}\t{p}": c for (m, p), c in resolved.items()}, indent=1))
