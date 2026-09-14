"""Mathematical domain constraints for Modelica operations.

Each entry answers one question: *what must be true for this operation to
produce a real, finite number?* That condition is the property ModelSan hunts
for a counterexample to.

The table is deliberately small and exact. An operation whose domain is the
whole real line is absent rather than listed as "always safe", so adding an
operation later cannot accidentally inherit a permissive default.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Domain:
    """A validity condition on one argument of an operation."""

    operation: str
    argument: int
    """Which argument is constrained, 0-based."""
    condition: str
    """Requirement with ``{}`` standing for the constrained argument."""
    why: str
    """What goes wrong when it is violated."""

    def describe(self, rendered: str) -> str:
        # `{}` rather than a letter: substituting "x" corrupts any rendering
        # that happens to contain an x, which most expression text does.
        return self.condition.format(rendered)


# Binary operators, keyed by the bitcode operator name.
BINARY_DOMAINS = {
    "divide": Domain(
        "divide",
        argument=1,
        condition="{} != 0",
        why="division by zero yields inf or nan",
    ),
    # a^b is real-valued for negative a only at integer b; a==0 with b<0 diverges.
    "power": Domain(
        "power",
        argument=0,
        condition="{} >= 0 unless the exponent is an integer",
        why="a negative base with a fractional exponent has no real result",
    ),
}

# Pure built-ins, keyed by the Modelica spelling bitcode records.
BUILTIN_DOMAINS = {
    "sqrt": Domain("sqrt", 0, "{} >= 0", "the square root of a negative number is not real"),
    "log": Domain("log", 0, "{} > 0", "log of zero diverges; log of a negative is not real"),
    "log10": Domain("log10", 0, "{} > 0", "log10 of zero diverges; log10 of a negative is not real"),
    "asin": Domain("asin", 0, "-1 <= {} <= 1", "asin outside [-1, 1] is not real"),
    "acos": Domain("acos", 0, "-1 <= {} <= 1", "acos outside [-1, 1] is not real"),
    "div": Domain("div", 1, "{} != 0", "integer division by zero"),
    "mod": Domain("mod", 1, "{} != 0", "modulo by zero"),
    "rem": Domain("rem", 1, "{} != 0", "remainder by zero"),
    # tan diverges at odd multiples of pi/2; it is representable but unbounded.
    "tan": Domain("tan", 0, "{} != pi/2 + k*pi", "tan diverges at odd multiples of pi/2"),
}


def domain_for_binary(op: str) -> Domain | None:
    return BINARY_DOMAINS.get(op)


def domain_for_builtin(name: str) -> Domain | None:
    return BUILTIN_DOMAINS.get(name)
