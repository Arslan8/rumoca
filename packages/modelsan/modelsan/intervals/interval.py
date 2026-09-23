"""Interval arithmetic, three-valued comparison, and the domains of operations.

Built rather than reused: `range.py` is a *runtime* bound checker and there was
no interval type in this project at all.

Two rules make this usable for a sanitizer rather than merely correct:

**Widen, never narrow.** Every operation returns a superset of the true result
set. A bound that is too wide produces `UNKNOWN` and silence; a bound that is
too narrow produces a confident wrong answer. Given this project measured its
consequence-claims at 0-7% precision, silence is the better failure.

**`UNKNOWN` is not a value.** A comparison that cannot be settled returns
`None`, which propagates. It never becomes `False`, and a caller that treats
"could not tell" as "does not hold" would report a violation nobody can act on.
"""

from __future__ import annotations

import math
from dataclasses import dataclass

INF = math.inf


@dataclass(frozen=True)
class Interval:
    """A closed range. `lo > hi` is the empty interval — a contradiction."""

    lo: float = -INF
    hi: float = INF

    # ── construction ─────────────────────────────────────────────────────────

    @staticmethod
    def point(value: float) -> "Interval":
        return Interval(value, value)

    @staticmethod
    def unknown() -> "Interval":
        return Interval(-INF, INF)

    @staticmethod
    def empty() -> "Interval":
        """No value satisfies this. Produced by contradictory constraints."""
        return Interval(1.0, -1.0)

    # ── predicates ───────────────────────────────────────────────────────────

    @property
    def is_empty(self) -> bool:
        return self.lo > self.hi

    @property
    def is_point(self) -> bool:
        return self.lo == self.hi and math.isfinite(self.lo)

    @property
    def is_unknown(self) -> bool:
        return self.lo == -INF and self.hi == INF

    def contains(self, value: float) -> bool:
        return self.lo <= value <= self.hi

    @property
    def spans_zero(self) -> bool:
        return not self.is_empty and self.lo <= 0.0 <= self.hi

    # ── lattice ──────────────────────────────────────────────────────────────

    def meet(self, other: "Interval") -> "Interval":
        """Both constraints hold. Empty when they contradict each other."""
        return Interval(max(self.lo, other.lo), min(self.hi, other.hi))

    def join(self, other: "Interval") -> "Interval":
        """Either may hold — the enclosing range."""
        if self.is_empty:
            return other
        if other.is_empty:
            return self
        return Interval(min(self.lo, other.lo), max(self.hi, other.hi))

    # ── arithmetic ───────────────────────────────────────────────────────────

    def __add__(self, other: "Interval") -> "Interval":
        if self.is_empty or other.is_empty:
            return Interval.empty()
        return Interval(self.lo + other.lo, self.hi + other.hi)

    def __sub__(self, other: "Interval") -> "Interval":
        if self.is_empty or other.is_empty:
            return Interval.empty()
        return Interval(self.lo - other.hi, self.hi - other.lo)

    def __neg__(self) -> "Interval":
        return Interval.empty() if self.is_empty else Interval(-self.hi, -self.lo)

    def __mul__(self, other: "Interval") -> "Interval":
        """All four corner products.

        Taking `lo*lo` and `hi*hi` is the classic mistake: `[-2,1] * [-3,4]`
        contains 6, which neither corner pair reaches.
        """
        if self.is_empty or other.is_empty:
            return Interval.empty()
        corners = [_mul(a, b) for a in (self.lo, self.hi) for b in (other.lo, other.hi)]
        return Interval(min(corners), max(corners))

    def __truediv__(self, other: "Interval") -> "Interval":
        """Division, widening to unknown when the divisor can be zero.

        `[1,2] / [-1,1]` is not an interval — the true result set is
        `(-inf,-1] u [1,inf)`, which this representation cannot hold. Returning
        the enclosing `(-inf,inf)` is the honest answer; returning something
        tighter would be wrong.
        """
        if self.is_empty or other.is_empty:
            return Interval.empty()
        if other.spans_zero:
            return Interval.unknown()
        corners = [_div(a, b) for a in (self.lo, self.hi) for b in (other.lo, other.hi)]
        return Interval(min(corners), max(corners))

    def power(self, exponent: float) -> "Interval":
        """Only the cases that are sound without case analysis."""
        if self.is_empty:
            return Interval.empty()
        if exponent == 2:
            # Squaring is not monotone through zero: [-3,1]^2 is [0,9].
            if self.spans_zero:
                return Interval(0.0, max(self.lo * self.lo, self.hi * self.hi))
            corners = [self.lo * self.lo, self.hi * self.hi]
            return Interval(min(corners), max(corners))
        if self.lo >= 0 and exponent > 0 and math.isfinite(exponent):
            try:
                return Interval(self.lo ** exponent, self.hi ** exponent)
            except (OverflowError, ValueError):
                return Interval.unknown()
        return Interval.unknown()

    # ── three-valued comparison ──────────────────────────────────────────────

    def gt(self, other: "Interval") -> bool | None:
        if self.is_empty or other.is_empty:
            return None
        if self.lo > other.hi:
            return True
        if self.hi <= other.lo:
            return False
        return None

    def ge(self, other: "Interval") -> bool | None:
        if self.is_empty or other.is_empty:
            return None
        if self.lo >= other.hi:
            return True
        if self.hi < other.lo:
            return False
        return None

    def lt(self, other: "Interval") -> bool | None:
        return other.gt(self)

    def le(self, other: "Interval") -> bool | None:
        return other.ge(self)

    def __str__(self) -> str:
        if self.is_empty:
            return "(empty)"
        if self.is_point:
            return f"{self.lo:g}"
        low = "-inf" if self.lo == -INF else f"{self.lo:g}"
        high = "+inf" if self.hi == INF else f"{self.hi:g}"
        return f"[{low}, {high}]"


def _mul(a: float, b: float) -> float:
    # 0 * inf is nan in IEEE and 0 here: an unbounded quantity scaled by an
    # exact zero is zero, and propagating nan would poison the whole interval.
    if (a == 0.0 and math.isinf(b)) or (b == 0.0 and math.isinf(a)):
        return 0.0
    return a * b


def _div(a: float, b: float) -> float:
    if b == 0.0:
        return INF if a > 0 else -INF if a < 0 else 0.0
    if math.isinf(a) and math.isinf(b):
        return INF if (a > 0) == (b > 0) else -INF
    return a / b
