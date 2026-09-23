"""SI dimensions, parsed from the unit strings MSL already declares.

A dimension is the exponent vector over the seven SI base units. Two quantities
can be added only if their vectors are equal, which makes `v + t` a defect no
physical argument is needed to settle — the strongest kind of claim this
project has, by its own precision data.

Unit syntax is MLS §19.1: a product of factors separated by `.`, a single `/`
for the denominator, integer exponents written as a suffix.

    "m"        "kg.m2"      "N.m/s"      "1/s"      "W/(m2.K)"
"""

from __future__ import annotations

import re
from dataclasses import dataclass

#: kg, m, s, A, K, mol, cd
BASE = ("kg", "m", "s", "A", "K", "mol", "cd")


@dataclass(frozen=True)
class Dimension:
    exponents: tuple[int, ...] = (0,) * 7

    def __mul__(self, other: "Dimension") -> "Dimension":
        return Dimension(tuple(a + b for a, b in zip(self.exponents, other.exponents)))

    def __truediv__(self, other: "Dimension") -> "Dimension":
        return Dimension(tuple(a - b for a, b in zip(self.exponents, other.exponents)))

    def power(self, n: int) -> "Dimension":
        return Dimension(tuple(a * n for a in self.exponents))

    @property
    def dimensionless(self) -> bool:
        return not any(self.exponents)

    def __str__(self) -> str:
        parts = [f"{b}{e if e != 1 else ''}" for b, e in zip(BASE, self.exponents) if e]
        return ".".join(parts) if parts else "1"


ONE = Dimension()

#: Derived units MSL uses, in base terms. Only those that actually appear —
#: an incomplete table is fine because an unknown unit yields *no claim*,
#: whereas a wrong entry would yield a wrong one.
DERIVED: dict[str, Dimension] = {
    "kg": Dimension((1, 0, 0, 0, 0, 0, 0)),
    "m": Dimension((0, 1, 0, 0, 0, 0, 0)),
    "s": Dimension((0, 0, 1, 0, 0, 0, 0)),
    "A": Dimension((0, 0, 0, 1, 0, 0, 0)),
    "K": Dimension((0, 0, 0, 0, 1, 0, 0)),
    "mol": Dimension((0, 0, 0, 0, 0, 1, 0)),
    "cd": Dimension((0, 0, 0, 0, 0, 0, 1)),
    "rad": ONE, "sr": ONE, "1": ONE,
    "N": Dimension((1, 1, -2, 0, 0, 0, 0)),
    "J": Dimension((1, 2, -2, 0, 0, 0, 0)),
    "W": Dimension((1, 2, -3, 0, 0, 0, 0)),
    "Pa": Dimension((1, -1, -2, 0, 0, 0, 0)),
    "Hz": Dimension((0, 0, -1, 0, 0, 0, 0)),
    "C": Dimension((0, 0, 1, 1, 0, 0, 0)),
    "V": Dimension((1, 2, -3, -1, 0, 0, 0)),
    "F": Dimension((-1, -2, 4, 2, 0, 0, 0)),
    "Ohm": Dimension((1, 2, -3, -2, 0, 0, 0)),
    "S": Dimension((-1, -2, 3, 2, 0, 0, 0)),
    "Wb": Dimension((1, 2, -2, -1, 0, 0, 0)),
    "T": Dimension((1, 0, -2, -1, 0, 0, 0)),
    "H": Dimension((1, 2, -2, -2, 0, 0, 0)),
    "degC": Dimension((0, 0, 0, 0, 1, 0, 0)),
    "lm": Dimension((0, 0, 0, 0, 0, 0, 1)),
    "lx": Dimension((0, -2, 0, 0, 0, 0, 1)),
    "Bq": Dimension((0, 0, -1, 0, 0, 0, 0)),
    "Gy": Dimension((0, 2, -2, 0, 0, 0, 0)),
    "Sv": Dimension((0, 2, -2, 0, 0, 0, 0)),
    "kat": Dimension((0, 0, -1, 0, 0, 1, 0)),
}

_FACTOR = re.compile(r"^([A-Za-z]+)(-?\d+)?$")


def parse(unit: str | None) -> Dimension | None:
    """The dimension of an MLS §19.1 unit string, or None if it is not one.

    `None` is returned for anything unrecognised rather than a guess, because a
    wrong dimension produces a wrong finding and an absent one produces
    silence. Silence is the right failure here.
    """
    if not unit:
        return None
    text = unit.strip()
    if not text or text == "1":
        return ONE

    # A leading numeric factor carries no dimension: "1/s", "100/m".
    numerator, _, denominator = text.partition("/")
    total = ONE
    for part, sign in ((numerator, 1), (denominator, -1)):
        part = part.strip().strip("()")
        if not part:
            continue
        for factor in part.split("."):
            factor = factor.strip()
            if not factor or factor.lstrip("-").isdigit():
                continue  # a pure number scales, it does not dimension
            found = _FACTOR.match(factor)
            if not found:
                return None
            symbol, exponent = found.group(1), int(found.group(2) or 1)
            base = DERIVED.get(symbol)
            if base is None:
                base = _with_prefix(symbol)
            if base is None:
                return None
            total = total * base.power(exponent * sign)
    return total


#: SI prefixes, which change magnitude and not dimension.
_PREFIXES = ("da", "h", "k", "M", "G", "T", "P", "E", "Z", "Y",
             "d", "c", "m", "u", "n", "p", "f", "a", "z", "y")


def _with_prefix(symbol: str) -> Dimension | None:
    for prefix in sorted(_PREFIXES, key=len, reverse=True):
        if symbol.startswith(prefix) and len(symbol) > len(prefix):
            base = DERIVED.get(symbol[len(prefix):])
            if base is not None:
                return base
    return None
