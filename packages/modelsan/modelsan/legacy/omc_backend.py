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
    nonfinite: str = ""
    """A variable that went inf or NaN while the run still reported success."""


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
    # Output density is capped at build time. The default 500 intervals writes
    # a ~1.2 MB CSV *per trial*, and with one CSV per probe that I/O dominated
    # the run: a sweep that searched 739 models before the silent-failure oracle
    # was added searched 202 after it, with 594 harness timeouts. Fifty points
    # detect a non-finite value or a bound violation just as well.
    lines.append(f'buildModel({model}, stopTime={t_end}, numberOfIntervals=50);'
                 ' getErrorString();')
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
    command = [str(built.executable), "-outputFormat=csv"]
    if overrides:
        command += ["-override", ",".join(f"{k}={v:g}" for k, v in overrides.items())]
    try:
        done = subprocess.run(command, cwd=work, capture_output=True, text=True,
                              timeout=timeout, env=ENV)
    except subprocess.TimeoutExpired:
        return Run(ok=False, detail="simulation timeout")
    if done.returncode == 0:
        # A zero exit is not success. An integrator can carry inf or NaN to the
        # end of the run and report completion, which is worse than a crash:
        # the user gets a trajectory rather than an error. Negative resistance
        # is the case that exposed this — it does not fail, it produces a
        # physically impossible answer cleanly.
        bad = nonfinite_variable(built.executable.parent /
                                 f"{built.executable.name}_res.csv")
        if bad:
            return Run(ok=False, detail=f"run completed with non-finite `{bad}`",
                       nonfinite=bad)
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


def nonfinite_variable(result: Path) -> str:
    """The first variable holding inf or NaN, if any.

    Scanned as text rather than parsed: the files run to megabytes and the
    question is only whether a non-finite token appears anywhere.
    """
    try:
        with result.open(errors="replace") as handle:
            header = handle.readline()
            names = [n.strip().strip('"') for n in header.split(",")]
            for line in handle:
                low = line.lower()
                if "nan" not in low and "inf" not in low:
                    continue
                for index, cell in enumerate(line.split(",")):
                    token = cell.strip().strip('"').lower()
                    if "nan" in token or "inf" in token:
                        return names[index] if index < len(names) else "?"
    except OSError:
        return ""
    return ""


def probes(parameter: Parameter) -> list[tuple[float, str]]:
    """Values the parameter's own declaration permits, with what each proves.

    Declaration shapes and what is worth trying:

    * `min=0` — zero is explicitly permitted. The BUG-002 shape.
    * no lower bound — zero *and every negative value* are permitted by
      omission. Negative resistance, negative inertia and negative capacitance
      are not physical components; nothing but the declaration can reject them,
      and there is no declaration.
    * `min=DBL_MIN` — OMC's spelling of "positive". Zero is excluded and
      DBL_MIN is a denormal no author chose, so probe nothing.
    * a real positive bound — probe the bound, the value the component claims
      to support.
    * an upper bound — probe it for the same reason.
    """
    if is_data_element(parameter):
        return []

    low, high, start = parameter.min, parameter.max, parameter.start
    out: list[tuple[float, str]] = []

    if low is None:
        out.append((0.0, "zero-permitted-by-omission"))
        # Magnitude matched to the declared value, so the probe stays in the
        # range the model was designed for and only the sign changes.
        scale = abs(start) if start not in (None, 0.0) else 1.0
        out.append((-scale, "negative-permitted-by-omission"))
    elif low == 0.0:
        out.append((0.0, "zero-permitted-by-bound"))
    elif low > DBL_MIN:
        out.append((low, "fails-at-its-own-positive-bound"))
    elif low < 0.0:
        out.append((low, "fails-at-its-own-negative-bound"))

    if high is not None and high != start:
        out.append((high, "fails-at-its-own-upper-bound"))

    return [
        (value, why)
        for value, why in out
        if (low is None or low <= DBL_MIN or value >= low)
        and (high is None or value <= high)
        and value != start
    ]


def tier(parameter: Parameter) -> str:
    """Kept for the older sweep format; `probes` now returns the claim itself."""
    return "unbounded" if parameter.min is None else "declared-permits"
