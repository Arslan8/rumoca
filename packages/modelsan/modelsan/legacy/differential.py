"""Differential testing: Rumoca against OpenModelica.

Two independent implementations of the same language, given the same model,
should produce the same trajectory. When they do not, at least one is wrong —
and that is a bug signal needing no oracle, no reference answer, and no
annotation on the model.

This is the only detector here that can find a bug in a *mature* tool. The
others test whether a model breaks; this tests whether two compilers agree
about what the model means.

What is compared, in order of how damning a difference is:

1. **Acceptance.** One tool compiles a model the other rejects. When Rumoca
   accepts something OMC rejects, that is a candidate soundness bug.
2. **Structure.** Equation and variable counts after flattening.
3. **Trajectory.** Common variables sampled at common times, within tolerance.

Numeric comparison uses a relative tolerance with an absolute floor: two
solvers with different step control never agree bit-for-bit, and demanding
that would report every model.
"""

from __future__ import annotations

import csv
import math
import re
import shutil
import subprocess
import tempfile
from dataclasses import dataclass, field
from pathlib import Path


@dataclass
class OmcResult:
    accepted: bool
    equations: int | None = None
    variables: int | None = None
    trajectory: dict[str, list[float]] = field(default_factory=dict)
    times: list[float] = field(default_factory=list)
    message: str = ""


def omc_available() -> bool:
    return shutil.which("omc") is not None


def _script(body: str) -> str:
    return f'loadModel(Modelica); getErrorString();\n{body}\ngetErrorString();\n'


def _run_omc(script: str, cwd: Path, timeout: float) -> str:
    path = cwd / "run.mos"
    path.write_text(script)
    try:
        # OMC's bundled clang cannot find the system headers in every
        # environment; forcing gcc is what makes simulation work here.
        done = subprocess.run(
            ["omc", str(path)],
            cwd=cwd,
            capture_output=True,
            text=True,
            timeout=timeout,
            env={**__import__("os").environ, "CC": "gcc"},
        )
        return done.stdout + done.stderr
    except subprocess.TimeoutExpired:
        return "TIMEOUT"


def omc_check(model: str, timeout: float = 180.0) -> OmcResult:
    """Flatten and check a model, without simulating."""
    with tempfile.TemporaryDirectory() as work:
        out = _run_omc(_script(f"checkModel({model});"), Path(work), timeout)
    if "TIMEOUT" in out:
        return OmcResult(accepted=False, message="omc timeout")
    ok = "completed successfully" in out
    counts = re.search(r"has (\d+) equation\(s\) and (\d+) variable\(s\)", out)
    return OmcResult(
        accepted=ok,
        equations=int(counts.group(1)) if counts else None,
        variables=int(counts.group(2)) if counts else None,
        message="" if ok else out.strip()[-400:],
    )


def omc_simulate(
    model: str, *, t_end: float = 1.0, intervals: int = 50, timeout: float = 300.0
) -> OmcResult:
    """Simulate and return the trajectory as columns."""
    with tempfile.TemporaryDirectory() as work:
        work_path = Path(work)
        body = (
            f'simulate({model}, stopTime={t_end}, numberOfIntervals={intervals},'
            f' outputFormat="csv");'
        )
        out = _run_omc(_script(body), work_path, timeout)
        if "TIMEOUT" in out:
            return OmcResult(accepted=False, message="omc timeout")
        found = re.search(r'resultFile = "([^"]*)"', out)
        if not found or not found.group(1):
            return OmcResult(accepted=False, message=out.strip()[-400:])
        result = Path(found.group(1))
        if not result.exists():
            result = work_path / result.name
        if not result.exists():
            return OmcResult(accepted=False, message="omc produced no result file")

        columns: dict[str, list[float]] = {}
        with result.open() as handle:
            reader = csv.reader(handle)
            header = next(reader)
            for name in header:
                columns[name] = []
            for row in reader:
                for name, cell in zip(header, row):
                    try:
                        columns[name].append(float(cell))
                    except ValueError:
                        columns[name].append(math.nan)
    times = columns.pop("time", [])
    return OmcResult(accepted=True, trajectory=columns, times=times)


# ── Comparison ───────────────────────────────────────────────────────────────


@dataclass
class Disagreement:
    kind: str
    detail: str
    variable: str = ""
    time: float = 0.0
    rumoca: float = 0.0
    omc: float = 0.0

    def __str__(self) -> str:
        if self.variable:
            return (
                f"  [{self.kind}] {self.variable} at t={self.time:g}: "
                f"rumoca={self.rumoca:.6g} omc={self.omc:.6g}\n      {self.detail}"
            )
        return f"  [{self.kind}] {self.detail}"


def compare_acceptance(model: str, rumoca_ok: bool, omc: OmcResult) -> list[Disagreement]:
    """Acceptance disagreements, the most damning kind."""
    if rumoca_ok and not omc.accepted:
        # The interesting direction: Rumoca accepted something the mature tool
        # rejected. Either OMC is wrong, or Rumoca admitted an invalid model.
        return [
            Disagreement(
                "accepts-what-omc-rejects",
                f"rumoca compiled `{model}`; omc refused: {omc.message[:200]}",
            )
        ]
    if not rumoca_ok and omc.accepted:
        return [
            Disagreement(
                "rejects-what-omc-accepts",
                f"omc checked `{model}` successfully ({omc.equations} eqs,"
                f" {omc.variables} vars); rumoca did not compile it",
            )
        ]
    return []


def compare_trajectories(
    rumoca_names: list[str],
    rumoca_times: list[float],
    rumoca_data: list[list[float]],
    omc: OmcResult,
    *,
    rtol: float = 1e-3,
    atol: float = 1e-6,
    max_reports: int = 3,
) -> list[Disagreement]:
    """Compare common variables at common times.

    Only variables both tools report are compared, and only at times inside
    both horizons. A difference is reported once per variable: a trajectory
    that diverges does so at every later point, and one report is the finding.
    """
    if not omc.trajectory or not rumoca_times or not omc.times:
        return []

    common = [name for name in rumoca_names if name in omc.trajectory]
    if not common:
        return []

    found: list[Disagreement] = []
    for name in common:
        if len(found) >= max_reports:
            break
        left = rumoca_data[rumoca_names.index(name)]
        right = omc.trajectory[name]
        for index, time in enumerate(rumoca_times):
            if index >= len(left):
                break
            # Nearest OMC sample; the two grids rarely coincide exactly.
            nearest = min(range(len(omc.times)), key=lambda k: abs(omc.times[k] - time))
            if abs(omc.times[nearest] - time) > 1e-6 or nearest >= len(right):
                continue
            a, b = left[index], right[nearest]
            if math.isnan(a) and math.isnan(b):
                continue
            if math.isnan(a) != math.isnan(b):
                found.append(
                    Disagreement(
                        "nan-disagreement",
                        "one implementation produced NaN and the other did not",
                        name,
                        time,
                        a,
                        b,
                    )
                )
                break
            if abs(a - b) > atol + rtol * max(abs(a), abs(b)):
                found.append(
                    Disagreement(
                        "trajectory-divergence",
                        f"relative difference {abs(a - b) / max(abs(a), abs(b), 1e-30):.3g}"
                        f" exceeds rtol={rtol:g}",
                        name,
                        time,
                        a,
                        b,
                    )
                )
                break
    return found
