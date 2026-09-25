"""Units for physical constants the compiler folded into bare literals.

[TOOLBUG-028](../../../../docs/toolbugs/TOOLBUG-028-constant-folding-discards-the-unit.md):
a reference to `Modelica.Constants.mu_0` reaches the bitcode as the literal
`1.25663706212e-06` with nothing recording that it is henries per metre. Any
dimensional analysis over such an expression is then unsound, and it fails in
the reporting direction — correct MSL code looks dimensionally inconsistent.

This recovers the unit by matching a literal's *exact* value against the
constants the library itself declares. That is a workaround for a lossy
artifact, not a repair of it, and the toolbug records the real fix.

Matching on value is safe here for one reason that does not generalise: these
are SI-defining constants, exact by definition since 2019, and their values are
not numbers anyone writes by accident. `pi`, `eps` and the other dimensionless
constants are deliberately excluded — recovering "dimensionless" changes
nothing, and matching `1.0` against anything would be reckless.
"""

from __future__ import annotations

import functools
import re
from pathlib import Path

from .dimension import Dimension, parse

#: Where MSL keeps its constants and the types that give them units.
_MSL = (Path(__file__).resolve().parents[4]
        / "target/msl/ModelicaStandardLibrary-4.1.0" / "Modelica 4.1.0")

#: `final constant SI.Permeability mu_0 = 1.25663706212e-6 "..."`
_CONSTANT = re.compile(
    r'constant\s+(?:SI|Modelica\.Units\.SI|NonSI)\.(\w+)\s+(\w+)\s*=\s*'
    r'([-+]?\d+\.?\d*(?:[eE][-+]?\d+)?)\s*[";]')

#: `type Permeability = Real (final quantity="...", final unit="H/m");`
_TYPE = re.compile(r'type\s+(\w+)\s*=\s*Real\s*\((.*?)\)\s*;', re.S)

#: SI-defining constants, used when the corpus is absent. Exact by definition
#: (SI 2019) rather than measured, so unlike a quantity/unit table this one
#: cannot fall behind the library — the library cannot change them either.
FALLBACK: dict[float, tuple[str, str]] = {
    1.25663706212e-6: ("mu_0", "H/m"),
    299792458.0: ("c", "m/s"),
    9.80665: ("g_n", "m/s2"),
    1.602176634e-19: ("q", "C"),
    6.62607015e-34: ("h", "J.s"),
    1.380649e-23: ("k", "J/K"),
    6.02214076e23: ("N_A", "1/mol"),
}


def _units_by_type(source: str) -> dict[str, str]:
    found = {}
    for match in _TYPE.finditer(source):
        unit = re.search(r'\bunit\s*=\s*"([^"]*)"', match.group(2))
        if unit:
            found[match.group(1)] = unit.group(1)
    return found


@functools.lru_cache(maxsize=1)
def table() -> dict[float, tuple[str, str]]:
    """`{value: (constant name, unit)}` for dimensional constants.

    Derived from the library when it is present, so a constant MSL adds or
    revises is picked up without editing this file.
    """
    constants = _MSL / "Constants.mo"
    units = _MSL / "Units.mo"
    if not (constants.is_file() and units.is_file()):
        return dict(FALLBACK)

    by_type = _units_by_type(units.read_text())
    found: dict[float, tuple[str, str]] = {}
    for type_name, name, literal in _CONSTANT.findall(constants.read_text()):
        unit = by_type.get(type_name)
        dimension = parse(unit) if unit else None
        # A dimensionless constant carries no information worth recovering,
        # and its value is likely to collide with an ordinary number.
        if dimension is None or dimension.dimensionless:
            continue
        try:
            value = float(literal)
        except ValueError:
            continue
        if value and value not in found:
            found[value] = (name, unit)
    return found or dict(FALLBACK)


def dimension_of_literal(value) -> Dimension | None:
    """The dimension of a literal that is exactly a known physical constant.

    None for every other number, which is the overwhelming majority: this
    speaks only when a value matches a constant exactly.
    """
    if not isinstance(value, float):
        return None
    entry = table().get(value)
    return parse(entry[1]) if entry else None


def name_of_literal(value) -> str | None:
    entry = table().get(value) if isinstance(value, float) else None
    return entry[0] if entry else None
