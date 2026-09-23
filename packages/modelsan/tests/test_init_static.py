"""InitSan: invariants evaluated in the initialization context.

The cases that must stay *silent* matter as much as the ones that must fire.
A start value is only a constraint when `fixed = true`, and an analysis that
forgets that reports every suggested guess in the library.
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path[:0] = [str(Path(__file__).resolve().parents[2] / "rumoca-bitcode"),
                str(Path(__file__).resolve().parents[1])]

from modelsan.intervals.initial_state import InitialState          # noqa: E402
from modelsan.intervals.interval import INF, Interval              # noqa: E402
from modelsan.intervals.propagate import evaluate, propagate       # noqa: E402


def check(condition: bool, label: str) -> None:
    print(f"  {'ok  ' if condition else 'FAIL'} {label}")
    assert condition, label


# ── interval arithmetic ──────────────────────────────────────────────────────


def test_multiplication_takes_all_four_corners():
    print("\n== a product is not lo*lo to hi*hi ==")
    # [-2,1] * [-3,4] contains 6, which neither corner *pair* reaches. Taking
    # only lo*lo and hi*hi is the classic interval bug.
    product = Interval(-2, 1) * Interval(-3, 4)
    check(product.contains(6.0), f"6 is reachable and must be in {product}")
    check(product.contains(-8.0), f"-8 likewise, got {product}")


def test_division_by_a_zero_spanning_interval_widens():
    print("\n== a divisor spanning zero gives up, it does not guess ==")
    # [1,2] / [-1,1] is (-inf,-1] u [1,inf), which an interval cannot hold.
    # The enclosing unknown is honest; anything tighter is wrong.
    check((Interval(1, 2) / Interval(-1, 1)).is_unknown,
          "the result must widen to unknown")
    check((Interval(1, 2) / Interval(2, 4)) == Interval(0.25, 1.0),
          "a divisor away from zero divides exactly")


def test_squaring_is_not_monotone_through_zero():
    print("\n== [-3,1]^2 is [0,9], not [9,1] ==")
    check(Interval(-3, 1).power(2) == Interval(0, 9), "squaring folds at zero")


def test_comparison_is_three_valued():
    print("\n== overlap is UNKNOWN, never False ==")
    check(Interval(5, 9).gt(Interval(1, 4)) is True, "disjoint and above")
    check(Interval(1, 2).gt(Interval(5, 9)) is False, "disjoint and below")
    check(Interval(1, 9).gt(Interval(1, 4)) is None,
          "overlapping is undecidable, and must not read as False")


def test_contradictory_constraints_give_an_empty_interval():
    print("\n== x >= 5 and x <= 3 is empty ==")
    check(Interval(5, INF).meet(Interval(-INF, 3)).is_empty,
          "the meet of disjoint constraints is empty")


def test_zero_times_unbounded_is_zero():
    print("\n== 0 * [-inf, inf] is 0, not nan ==")
    # IEEE says 0*inf is nan; propagating that would poison the interval.
    check((Interval.point(0) * Interval.unknown()) == Interval.point(0),
          "an exact zero annihilates an unbounded factor")


# ── the environment ──────────────────────────────────────────────────────────


class FakeVar:
    def __init__(self, id, name, *, fixed=None, start=None, minimum=None,
                 maximum=None, binding=None, parameter=False):
        self.id, self.name = id, name
        self.fixed, self.start = fixed, start
        self.minimum, self.maximum, self.binding = minimum, maximum, binding
        self.is_parameter = parameter
        self.source = None


class Lit:
    def __init__(self, value): self.value = value


class FakeModel:
    def __init__(self, variables, initial_equations=()):
        self.variables = variables
        self.initial_equations = list(initial_equations)
        self.equations = self.expressions = self.events = []


def test_fixed_start_constrains_and_a_guess_does_not():
    print("\n== `fixed` is the whole design ==")
    # Identical declarations but for `fixed`. Conflating them is the fastest
    # route to reporting every suggested start value in the library.
    pinned = FakeVar(1, "xFixed", fixed=True, start=Lit(5))
    guess = FakeVar(2, "xGuess", fixed=False, start=Lit(7))
    absent = FakeVar(3, "xNone", fixed=None, start=Lit(9))
    state = InitialState(FakeModel([pinned, guess, absent]))

    check(state.interval(1) == Interval.point(5), "fixed = true pins the value")
    check(state.interval(2).is_unknown, "fixed = false constrains nothing")
    check(state.interval(3).is_unknown,
          "unspecified `fixed` is not a constraint either")


def test_a_parameter_binding_is_a_value():
    print("\n== a parameter's binding pins it ==")
    state = InitialState(FakeModel([
        FakeVar(1, "p", parameter=True, binding=Lit(10))]))
    check(state.interval(1) == Interval.point(10), "p = 10")


def test_declared_bounds_seed_a_box():
    print("\n== min/max give a range even with no start ==")
    state = InitialState(FakeModel([
        FakeVar(1, "x", minimum=Lit(0), maximum=Lit(10))]))
    check(state.interval(1) == Interval(0, 10), "the declaration is the range")


def main() -> int:
    failures = 0
    for name, function in sorted(globals().items()):
        if name.startswith("test_") and callable(function):
            try:
                function()
            except AssertionError as error:
                failures += 1
                print(f"  FAILED: {error}")
    print(f"\n{'all InitSan tests passed' if not failures else f'{failures} failed'}")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
