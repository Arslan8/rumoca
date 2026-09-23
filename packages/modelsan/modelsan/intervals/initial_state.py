"""The initialization environment: what each variable can be at t = 0.

Populated from the four things the artifact actually carries, in increasing
order of authority:

    declared min/max        a box the value must lie in
    start, fixed = false    a *guess*. Contributes nothing.
    start, fixed = true     an initial constraint. A point.
    parameter binding       a value. A point.
    initial equation        a constraint, propagated separately

The `fixed` three-state is the whole design. `Option<bool>` arrives as
True / False / None and they mean different things:

    fixed = true    x(start=5) constrains x to 5
    fixed = false   x(start=5) suggests 5 and constrains nothing
    fixed = None    unspecified; the default depends on variability, and for a
                    continuous state it is *false*

Conflating them is the fastest route to a false positive, and the InitSan that
already exists conflates them — it reads `start` and compares it to `min`/`max`
whatever `fixed` says. `xFromInitEq` in the probe model reads `start = 0.0`,
which is a *default*, and is actually initialized to -1 by an equation.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from ..physical.engine import constant_value
from .interval import INF, Interval


@dataclass(frozen=True)
class Provenance:
    """Why a variable has the range it has. Carried into every diagnostic."""

    source: str
    """declared-bound | fixed-start | parameter | initial-equation | propagated"""

    detail: str = ""

    def __str__(self) -> str:
        return f"{self.source}{': ' + self.detail if self.detail else ''}"


@dataclass
class Binding:
    interval: Interval
    why: list[Provenance] = field(default_factory=list)

    def refine(self, interval: Interval, why: Provenance) -> bool:
        """Intersect. Returns whether anything actually narrowed."""
        tightened = self.interval.meet(interval)
        if tightened == self.interval:
            return False
        self.interval = tightened
        self.why.append(why)
        return True


class InitialState:
    """Variable id -> the interval it can occupy at t = 0."""

    def __init__(self, model) -> None:
        self.model = model
        self.bindings: dict[int, Binding] = {}
        self.names: dict[int, str] = {v.id: v.name for v in model.variables}
        self._seed()

    # ── seeding ──────────────────────────────────────────────────────────────

    def _seed(self) -> None:
        for variable in self.model.variables:
            interval, why = self._declared(variable)
            self.bindings[variable.id] = Binding(interval, why)

    def _declared(self, variable) -> tuple[Interval, list[Provenance]]:
        why: list[Provenance] = []
        lo = constant_value(getattr(variable, "minimum", None))
        hi = constant_value(getattr(variable, "maximum", None))
        interval = Interval(lo if lo is not None else -INF,
                            hi if hi is not None else INF)
        if lo is not None or hi is not None:
            why.append(Provenance("declared-bound", f"{interval}"))

        # A parameter's binding is its value.
        if getattr(variable, "is_parameter", False):
            value = constant_value(getattr(variable, "binding", None))
            if value is not None:
                interval = interval.meet(Interval.point(value))
                why.append(Provenance("parameter", f"= {value:g}"))
                return interval, why

        # `start` constrains only when `fixed` is true. This is the distinction
        # the brief calls out and the existing InitSan misses.
        if getattr(variable, "fixed", None) is True:
            value = constant_value(getattr(variable, "start", None))
            if value is not None:
                interval = interval.meet(Interval.point(value))
                why.append(Provenance("fixed-start", f"start = {value:g}, fixed = true"))
        return interval, why

    # ── access ───────────────────────────────────────────────────────────────

    def interval(self, variable_id: int) -> Interval:
        binding = self.bindings.get(variable_id)
        return binding.interval if binding else Interval.unknown()

    def why(self, variable_id: int) -> list[Provenance]:
        binding = self.bindings.get(variable_id)
        return list(binding.why) if binding else []

    def refine(self, variable_id: int, interval: Interval, why: Provenance) -> bool:
        binding = self.bindings.setdefault(variable_id, Binding(Interval.unknown()))
        return binding.refine(interval, why)

    def name(self, variable_id: int) -> str:
        return self.names.get(variable_id, f"<{variable_id}>")

    @property
    def contradictions(self) -> list[int]:
        """Variables whose constraints cannot all hold."""
        return [i for i, b in self.bindings.items() if b.interval.is_empty]

    def summary(self) -> dict:
        constrained = [i for i, b in self.bindings.items() if not b.interval.is_unknown]
        return {
            "variables": len(self.bindings),
            "constrained": len(constrained),
            "points": sum(1 for b in self.bindings.values() if b.interval.is_point),
            "contradictions": len(self.contradictions),
        }
