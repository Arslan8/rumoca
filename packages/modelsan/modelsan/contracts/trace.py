"""Explicit behavioral contracts over observations, never a Modelica evaluator.

These contracts state expectations supplied by a user or a documented component
API. They do not infer intent from a variable's name, unit, or current values.
"""
from __future__ import annotations

from bisect import bisect_left, bisect_right
from dataclasses import dataclass
import math

from ..runtime.observations import (
    ExecutionFailureObservation, SimulationEnd, SimulationStart,
    UnorderedVariableObservation, VariableObservation,
)


class Unavailable(ValueError):
    """The evidence cannot establish this contract, rather than a passing test."""


@dataclass(frozen=True)
class Verdict:
    checked: int
    witness: dict | None = None


class Signals:
    def __init__(self, stream):
        self.rows = {}
        self.complete = False
        starts, ends, invalid = 0, 0, False
        for observation in stream:
            invalid |= isinstance(observation, ExecutionFailureObservation)
            if isinstance(observation, SimulationStart):
                starts += 1
                invalid |= bool(self.rows) or starts > 1 or ends > 0
            if isinstance(observation, SimulationEnd):
                ends += 1
                self.complete = observation.completed
            if isinstance(observation, (VariableObservation, UnorderedVariableObservation)):
                invalid |= ends > 0
                self.rows.setdefault(observation.label, []).append(observation)
        self.complete &= not invalid and ends == 1

    def get(self, name, *, temporal=True):
        if not self.complete:
            raise Unavailable('execution did not complete; behavioral coverage unavailable')
        rows = self.rows.get(name, [])
        if not rows:
            raise Unavailable(f'missing observations for {name}')
        identities = {(r.canonical, r.backend) for r in rows}
        if len(identities) != 1:
            raise Unavailable(f'ambiguous observation identity for {name}')
        if len({type(row) for row in rows}) != 1:
            raise Unavailable(f'mixed ordered and unordered observations for {name}')
        previous = -math.inf
        previous_index = -1
        for row in rows:
            if isinstance(row, UnorderedVariableObservation):
                if temporal:
                    raise Unavailable(f'{name} has value samples but no validated temporal order')
                if (row.time is not None or row.reported_time is None
                        or not math.isfinite(row.reported_time)
                        or not isinstance(row.row_index, int) or row.row_index <= previous_index):
                    raise Unavailable(f'invalid unordered sample provenance for {name}')
                previous_index = row.row_index
            else:
                if row.time is None or not math.isfinite(row.time) or row.time < previous:
                    raise Unavailable(f'invalid or unordered timestamps for {name}')
                previous = row.time
            if not math.isfinite(row.value):
                raise Unavailable(f'nonfinite {name}; numerical failure requires separate triage')
        return rows


@dataclass(frozen=True, kw_only=True)
class TraceContract:
    contract_id: str
    origin: str
    atol: float = 1e-8
    rtol: float = 1e-7

    def __post_init__(self):
        if not self.contract_id.strip() or not self.origin.strip():
            raise ValueError('a contract requires an id and the source of its expectation')
        if any(not math.isfinite(v) or v < 0 for v in (self.atol, self.rtol)):
            raise ValueError('contract tolerances must be finite and nonnegative')

    def agrees(self, actual, expected):
        return abs(actual-expected) <= self.atol + self.rtol*max(abs(actual), abs(expected))


@dataclass(frozen=True, kw_only=True)
class Equality(TraceContract):
    actual: str
    expected: str

    def evaluate(self, signals):
        left, right = signals.get(self.actual), signals.get(self.expected)
        if len(left) != len(right) or any(a.time != b.time for a, b in zip(left, right)):
            raise Unavailable('equality requires synchronized rows, including both sides of events')
        for index, (a, b) in enumerate(zip(left, right)):
            if not self.agrees(a.value, b.value):
                return Verdict(index+1, dict(time=a.time, actual=a.value, expected=b.value,
                                            signal=self.actual, reference=self.expected))
        return Verdict(len(left))


def edge_tolerance(time, period):
    return max(math.ulp(time)*8, period*1e-9)


@dataclass(frozen=True, kw_only=True)
class PeriodicPulse(TraceContract):
    actual: str
    period: float
    start: float
    duty: float = 0.5

    def __post_init__(self):
        super().__post_init__()
        if not math.isfinite(self.period) or self.period <= 0:
            raise ValueError('pulse period must be positive and finite')
        if not math.isfinite(self.start) or not 0 <= self.duty <= 1:
            raise ValueError('pulse needs finite start and duty in [0,1]')

    def evaluate(self, signals):
        checked = 0
        for row in signals.get(self.actual):
            delta = row.time-self.start
            if not math.isfinite(delta):
                raise Unavailable('pulse phase arithmetic exceeds finite representation')
            phase = delta % self.period
            tolerance = edge_tolerance(row.time, self.period)
            edges = (abs(delta), phase, self.period-phase,
                     abs(phase-self.duty*self.period))
            if min(edges) <= tolerance:
                continue  # No claim about pre/post-event ordering from a scalar time.
            expected = float(delta >= 0 and phase < self.duty*self.period)
            checked += 1
            if not self.agrees(row.value, expected):
                return Verdict(checked, dict(time=row.time, actual=row.value, expected=expected,
                                             signal=self.actual, phase=phase))
        if not checked:
            raise Unavailable('no pulse observations away from switching boundaries')
        return Verdict(checked)


@dataclass(frozen=True, kw_only=True)
class SampleDelay(TraceContract):
    """One sample delay of a continuous input; output is held between ticks."""
    actual: str
    input: str
    period: float
    start: float = 0.0
    initial: float = 0.0

    def __post_init__(self):
        super().__post_init__()
        if not math.isfinite(self.period) or self.period <= 0:
            raise ValueError('sample period must be positive and finite')
        if not all(math.isfinite(v) for v in (self.start, self.initial)):
            raise ValueError('sample start and initial output must be finite')

    def _input_at(self, rows, times, when):
        tolerance = edge_tolerance(when, self.period)
        lo, hi = bisect_left(times, when-tolerance), bisect_right(times, when+tolerance)
        if lo == hi:
            raise Unavailable(f'input was not observed at required sample time {when:g}')
        values = [row.value for row in rows[lo:hi]]
        if not all(self.agrees(value, values[-1]) for value in values):
            raise Unavailable('input is discontinuous at a tick; continuous-input contract inapplicable')
        return values[-1]

    def evaluate(self, signals):
        source = signals.get(self.input)
        times = [row.time for row in source]
        checked = 0
        for row in signals.get(self.actual):
            delta = row.time-self.start
            if not math.isfinite(delta) or not math.isfinite(delta/self.period):
                raise Unavailable('sample schedule arithmetic exceeds finite representation')
            phase = delta % self.period
            if min(phase, self.period-phase) <= edge_tolerance(row.time, self.period):
                continue
            tick = math.floor(delta/self.period)
            expected = (self.initial if tick < 1 else
                        self._input_at(source, times, self.start+(tick-1)*self.period))
            checked += 1
            if not self.agrees(row.value, expected):
                return Verdict(checked, dict(time=row.time, actual=row.value, expected=expected,
                                             signal=self.actual, input=self.input, sample_index=tick-1))
        if not checked:
            raise Unavailable('no delay observations inside sample intervals')
        return Verdict(checked)


@dataclass(frozen=True, kw_only=True)
class Cardinality(TraceContract):
    """Minimum levels consistent with each observation's +/- tolerance interval."""
    actual: str
    maximum: int

    def __post_init__(self):
        super().__post_init__()
        if isinstance(self.maximum, bool) or not isinstance(self.maximum, int) or self.maximum < 1:
            raise ValueError('maximum distinct levels must be a positive integer')

    def evaluate(self, signals):
        rows = signals.get(self.actual, temporal=False)
        intervals = []
        for row in rows:
            error = self.atol + self.rtol*abs(row.value)
            low, high = row.value-error, row.value+error
            if not math.isfinite(low) or not math.isfinite(high):
                raise Unavailable('level uncertainty interval exceeds finite representation')
            intervals.append((high, low, row))
        representatives, point = [], None
        # Greedy interval stabbing gives the minimum number of possible levels.
        # Two jittered readings of one level must not count as two levels.
        for high, low, row in sorted(intervals, key=lambda item: item[0]):
            if point is not None and low <= point <= high:
                continue
            point = high
            representatives.append(row.value)
            if len(representatives) > self.maximum:
                provenance = (dict(sample_order='unordered', reported_time=row.reported_time,
                                   row_index=row.row_index)
                              if isinstance(row, UnorderedVariableObservation) else {})
                return Verdict(len(rows), dict(time=row.time, signal=self.actual,
                    observed_levels=representatives, maximum=self.maximum,
                    observed_count_lower_bound=len(representatives), **provenance))
        return Verdict(len(rows))


KINDS = {'equality': Equality, 'periodic_pulse': PeriodicPulse,
         'sample_delay': SampleDelay, 'cardinality': Cardinality}


def from_dict(data):
    options = dict(data)
    kind = options.pop('kind')
    if kind not in KINDS:
        raise ValueError(f'unknown behavioral contract: {kind}')
    return KINDS[kind](**options)
