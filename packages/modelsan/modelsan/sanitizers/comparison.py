"""Comparing execution results, shared by DeterminismSan and DifferentialSan.

Both sanitizers ask the same question — did these two runs agree? — of
different pairs. Doing the numerics once keeps their thresholds consistent and
keeps the calibration in one place.

The calibration is the hard part and was arrived at empirically. Judging a
trajectory by *pointwise* relative error reports a finding every time a
quantity decays through zero: `damper1.f` at 8.3e-4 against 9.4e-4 is a 12%
relative difference and a 1.1e-4 absolute one, on a force whose range over the
run is order 1. Scaling the tolerance by each signal's own range over the whole
run is what makes one threshold mean the same thing for every variable.
"""

from __future__ import annotations

import math
from dataclasses import dataclass

from ..backends.base import ExecutionResult


@dataclass(frozen=True)
class Divergence:
    kind: str
    variable: str
    time: float
    left: float
    right: float
    detail: str


def compare_traces(left: ExecutionResult, right: ExecutionResult, *,
                   rtol: float = 0.05, atol: float = 1e-9,
                   max_reports: int = 3) -> list[Divergence]:
    """Variables both runs reported, compared on each signal's own scale."""
    if not (left.trace and right.trace):
        return []
    common = [n for n in left.trace.columns if n in right.trace.columns]
    found: list[Divergence] = []

    for name in common:
        if len(found) >= max_reports:
            break
        a_values, b_values = left.trace.columns[name], right.trace.columns[name]
        scale = max(
            max((abs(v) for v in a_values if not math.isnan(v)), default=0.0),
            max((abs(v) for v in b_values if not math.isnan(v)), default=0.0),
        )
        limit = atol + rtol * scale
        for index, time in enumerate(left.trace.times):
            if index >= len(a_values) or index >= len(b_values):
                break
            a, b = a_values[index], b_values[index]
            if math.isnan(a) and math.isnan(b):
                continue
            if math.isnan(a) != math.isnan(b):
                found.append(Divergence(
                    "nan-disagreement", name, time, a, b,
                    "one run produced NaN and the other did not"))
                break
            if abs(a - b) > limit:
                found.append(Divergence(
                    "trajectory-divergence", name, time, a, b,
                    f"|difference| {abs(a - b):.3g} exceeds {limit:.3g} "
                    f"(rtol={rtol:g} of signal scale {scale:.3g})"))
                break
    return found


def compare_events(left: ExecutionResult, right: ExecutionResult,
                   tolerance: float = 1e-6) -> str | None:
    """Whether two runs agree on how many events fired and roughly when."""
    a = sorted(e.time for e in left.events if e.time is not None)
    b = sorted(e.time for e in right.events if e.time is not None)
    if len(a) != len(b):
        return f"event count differs: {len(a)} vs {len(b)}"
    for first, second in zip(a, b):
        if abs(first - second) > tolerance:
            return f"event time differs: {first:g} vs {second:g}"
    return None
