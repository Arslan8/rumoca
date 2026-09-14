"""Fluid and hydraulic rules.

Pressure is `>= 0` only because these quantities are *absolute* pressures. A
pressure *difference* is legitimately signed, and MSL types them separately
(`AbsolutePressure` vs `PressureDifference`), which is exactly why matching on
the declared quantity rather than the unit matters here: both are Pa.
"""

from __future__ import annotations

from ..invariant import Comparison, Domain, Enforcement
from ..rules import QuantityRule, RulePack

FLUID = Domain("fluid")

PACK = RulePack(
    domain=FLUID,
    description="Fluid state and geometry.",
    rules=[
        QuantityRule(
            rule_id="fluid.density.positive",
            domain=FLUID,
            quantities=frozenset({"Density"}),
            units=frozenset({"kg/m3"}),
            op=Comparison.GT, bound=0.0,
            origin="mass per volume of a real fluid; density appears as a "
                   "divisor throughout the Fluid library",
            enforcement=Enforcement.EITHER, severity="high",
        ),
        QuantityRule(
            rule_id="fluid.absolute_pressure.non_negative",
            domain=FLUID,
            quantities=frozenset({"AbsolutePressure"}),
            units=frozenset({"Pa"}),
            op=Comparison.GE, bound=0.0,
            origin="an absolute pressure is measured from vacuum. A pressure "
                   "*difference* is signed and is a different quantity",
            enforcement=Enforcement.RUNTIME,
        ),
        QuantityRule(
            rule_id="fluid.viscosity.non_negative",
            domain=FLUID,
            quantities=frozenset({"DynamicViscosity", "KinematicViscosity"}),
            op=Comparison.GE, bound=0.0,
            origin="viscosity resists shear; negative viscosity would amplify it",
            enforcement=Enforcement.EITHER,
        ),
        QuantityRule(
            rule_id="fluid.area.positive",
            domain=FLUID,
            quantities=frozenset({"Area", "CrossSection"}),
            units=frozenset({"m2"}),
            op=Comparison.GT, bound=0.0,
            origin="a flow cross-section is a divisor in every velocity "
                   "relation; zero area admits no flow and divides by zero",
            enforcement=Enforcement.STATIC, parameters_only=True,
        ),
    ],
)
