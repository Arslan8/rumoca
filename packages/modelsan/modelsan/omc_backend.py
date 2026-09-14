#!/usr/bin/env python3
"""Run ModelSan's parameter search through OpenModelica.

ModelSan's detectors read Rumoca's DAE, so they only ever see models Rumoca can
compile — 332 of 847 on the current corpus. The remaining 515 are unreachable
for reasons that have nothing to do with the models: external objects, Fluid
media, record-array vectorisation. Those are compiler gaps, and waiting on them
caps what the sanitizer can find.

The dynamic half of the search does not need Rumoca. It needs a simulator, a
list of parameters, and their declared bounds. OpenModelica supplies all three:
`buildModel` emits an executable and an `_init.xml` naming every parameter with
its `start`, `min` and `max`. Building once and re-running the executable with
`-override` is also far cheaper than recompiling per trial.

This backend is therefore not a fallback — it is what makes coverage a property
of the corpus rather than of one front end.
"""

from __future__ import annotations

import os
import re
import subprocess
import xml.etree.ElementTree as ET
from dataclasses import dataclass
from pathlib import Path

# OMC ships its own clang, which cannot find stddef.h in this environment.
ENV = {**os.environ, "CC": "gcc"}

# The assertion OMC prints when a divisor vanishes names the expression, which
# is more than the numerical residual a solver failure usually gives.
DIVISION = re.compile(r"division by zero.*divisor b expression is: (\S+)")


# OMC writes DBL_MIN as the lower bound of a quantity declared merely positive.
# It is a representation artifact, not a bound anyone wrote, so probing there
# asks whether the model survives a denormal — a question about floating point,
# not about the domain the model declared.
DBL_MIN = 2.2250738585072014e-308


@dataclass
class Parameter:
    name: str
    start: float | None
    min: float | None
    max: float | None


@dataclass
class Built:
    executable: Path
    parameters: list[Parameter]
    message: str = ""

    @property
    def ok(self) -> bool:
        return self.executable is not None and self.executable.exists()


@dataclass
class Run:
    ok: bool
    detail: str = ""
    blamed: str = ""
    """The parameter OMC's own assertion names, when it names one."""


def _number(text: str | None) -> float | None:
    if text is None:
        return None
    try:
        value = float(text)
    except ValueError:
        return None
    # OMC writes unset bounds as ±1e60 rather than omitting them.
    return None if abs(value) >= 1e59 else value


def read_parameters(init_xml: Path) -> list[Parameter]:
    """Every scalar parameter, with the bounds the model declared."""
    try:
        root = ET.parse(init_xml).getroot()
    except (OSError, ET.ParseError):
        return []
    found = []
    for variable in root.iter("ScalarVariable"):
        if variable.get("variability") != "parameter":
            continue
        value = variable.find("Real")
        if value is None:  # Integer, Boolean and String parameters are skipped
            continue
        found.append(Parameter(
            name=variable.get("name", ""),
            start=_number(value.get("start")),
            min=_number(value.get("min")),
            max=_number(value.get("max")),
        ))
    return [p for p in found if p.name]


def build(model: str, libraries: list[str], work: Path, t_end: float,
          timeout: float = 600) -> Built:
    """Compile `model` to a standalone executable once."""
    lines = [f'loadFile("{library}"); getErrorString();' for library in libraries]
    lines.append(f'buildModel({model}, stopTime={t_end}); getErrorString();')
    script = work / "build.mos"
    script.write_text("\n".join(lines) + "\n")
    try:
        done = subprocess.run(["omc", str(script)], cwd=work, capture_output=True,
                              text=True, timeout=timeout, env=ENV)
    except subprocess.TimeoutExpired:
        return Built(executable=None, parameters=[], message="build timeout")

    executable = work / model
    if not executable.exists():
        return Built(executable=None, parameters=[],
                     message=(done.stdout + done.stderr).strip()[-300:])
    return Built(executable=executable,
                 parameters=read_parameters(work / f"{model}_init.xml"))


def run(built: Built, overrides: dict[str, float], work: Path,
        timeout: float = 120) -> Run:
    """Run the built executable with parameter overrides.

    An override naming a parameter the model does not have is only a warning to
    OMC and the run still succeeds, so callers must take names from
    `built.parameters` rather than guessing them.
    """
    command = [str(built.executable)]
    if overrides:
        command += ["-override", ",".join(f"{k}={v:g}" for k, v in overrides.items())]
    try:
        done = subprocess.run(command, cwd=work, capture_output=True, text=True,
                              timeout=timeout, env=ENV)
    except subprocess.TimeoutExpired:
        return Run(ok=False, detail="simulation timeout")
    if done.returncode == 0:
        return Run(ok=True)
    text = (done.stdout + done.stderr).strip()
    blamed = DIVISION.search(text)
    return Run(ok=False, detail=" ".join(text.split())[-220:],
               blamed=blamed.group(1) if blamed else "")


ARRAY_ELEMENT = re.compile(r"\[\d+(,\d+)*\]$")


def is_data_element(parameter: Parameter) -> bool:
    """A single element of a parameter array, e.g. `table.table[2]`.

    Zeroing one entry of a lookup table is data corruption, not a choice of
    operating point, and the failure it causes says nothing about a declared
    domain. ModelSan's claim is about bounds a component wrote and cannot
    honour, so these are out of scope rather than merely noisy.
    """
    return bool(ARRAY_ELEMENT.search(parameter.name))


def probes(parameter: Parameter) -> list[float]:
    """Values the parameter's own declaration permits, worth trying.

    Four declaration shapes, three behaviours:

    * `min=0` — zero is explicitly permitted. Probe it. This is the BUG-002
      shape and the strongest claim available.
    * no bound — zero is permitted by omission. Probe it. Weaker, because
      nothing was written down to contradict.
    * `min=DBL_MIN` — OMC's spelling of "positive". Zero is excluded, and
      DBL_MIN itself is a denormal no author chose, so probe nothing.
    * a real positive bound — probe the bound itself, which is the value the
      component claims to support and may not.
    """
    if is_data_element(parameter):
        return []

    declared = parameter.min

    if declared is None:
        candidates = [0.0]
    elif declared == 0.0:
        candidates = [0.0]
    elif declared <= DBL_MIN:
        candidates = []
    else:
        candidates = [declared]

    return [
        value
        for value in candidates
        if (parameter.max is None or value <= parameter.max)
        and value != parameter.start
    ]


def tier(parameter: Parameter) -> str:
    """How strong a claim a finding on this parameter supports.

    `declared-permits` is airtight: the component wrote a bound that *includes*
    the value that breaks it, so the declaration is provably a promise it
    cannot keep — the BUG-002 shape.

    `unbounded` is weaker: nothing was declared, so arguing the value is
    reachable is a judgement about what the quantity means rather than a
    contradiction of anything written down — the BUG-010 shape. Real, but the
    argument has to be made rather than read off the source.
    """
    return "unbounded" if parameter.min is None else "declared-permits"
