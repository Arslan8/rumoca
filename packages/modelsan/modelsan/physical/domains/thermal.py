"""Thermal rules.

Absolute temperature is the one invariant here that must hold *at every instant*
rather than only at declaration: a model can start above absolute zero and be
driven below it by a bad heat flow. It is therefore the pack's runtime rule,
and a useful demonstration that the engine handles both kinds.
"""

from __future__ import annotations

from ..invariant import Comparison, Domain, Enforcement
from ..rules import QuantityRule, RulePack

THERMAL = Domain("thermal")

PACK = RulePack(
    domain=THERMAL,
    description="Heat-transfer quantities.",
    rules=[
        QuantityRule(
            rule_id="thermal.temperature.above_absolute_zero",
            domain=THERMAL,
            quantities=frozenset({"ThermodynamicTemperature", "Temperature"}),
            units=frozenset({"K"}),
            op=Comparison.GE, bound=0.0,
            origin="absolute temperature cannot be negative; below 0 K the "
                   "thermal equations lose physical meaning",
            reference="MLS Modelica.Units.SI.ThermodynamicTemperature",
            # State, not a design choice: it must hold throughout the run.
            enforcement=Enforcement.RUNTIME, severity="high",
        ),
        QuantityRule(
            rule_id="thermal.heat_capacity.positive",
            domain=THERMAL,
            quantities=frozenset({"HeatCapacity"}),
            units=frozenset({"J/K"}),
            op=Comparison.GT, bound=0.0,
            origin="C*dT = dQ; a non-positive heat capacity makes a body cool "
                   "when heated",
            enforcement=Enforcement.STATIC, parameters_only=True,
        ),
        QuantityRule(
            rule_id="thermal.conductance.positive",
            domain=THERMAL,
            quantities=frozenset({"ThermalConductance"}),
            units=frozenset({"W/K"}),
            op=Comparison.GT, bound=0.0,
            origin="heat flows from hot to cold; G <= 0 reverses the second law",
            enforcement=Enforcement.STATIC, parameters_only=True,
        ),
    ],
)
