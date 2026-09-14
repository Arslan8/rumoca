"""Analysis tells the fuzzer where to look; it does not drive the search.

A hint is advice with a reason attached. The fuzzer decides whether to take it,
in what order, and how to combine hints — which is what keeps analysis and
search independent enough to change separately.
"""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True)
class FuzzHint:
    """Values worth trying for one target, and why."""

    target: str
    values: tuple[float, ...]
    reason: str
    source: str = ""
    """Which analysis or sanitizer emitted it, for attributing what worked."""

    # DAE anchors, so a finding produced from this hint can point at the
    # expression or variable that motivated it.
    expression_ids: tuple[int, ...] = field(default_factory=tuple)
    variable_ids: tuple[int, ...] = field(default_factory=tuple)

    def __str__(self) -> str:
        vals = ", ".join(f"{v:g}" for v in self.values)
        return f"{self.target} in [{vals}] — {self.reason}"


def merge(hints: list[FuzzHint]) -> list[FuzzHint]:
    """Combine hints for the same target, keeping every distinct value.

    Two analyses often flag the same parameter for different reasons — a
    divisor that is also a vanishing coefficient. Both reasons are worth
    keeping; the values should be tried once.
    """
    grouped: dict[str, FuzzHint] = {}
    for hint in hints:
        existing = grouped.get(hint.target)
        if existing is None:
            grouped[hint.target] = hint
            continue
        values = tuple(dict.fromkeys(existing.values + hint.values))
        grouped[hint.target] = FuzzHint(
            target=hint.target,
            values=values,
            reason=f"{existing.reason}; {hint.reason}",
            source=f"{existing.source},{hint.source}".strip(","),
            expression_ids=tuple(dict.fromkeys(
                existing.expression_ids + hint.expression_ids)),
            variable_ids=tuple(dict.fromkeys(
                existing.variable_ids + hint.variable_ids)),
        )
    return list(grouped.values())
