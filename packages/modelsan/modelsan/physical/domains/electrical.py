"""Electrical rules.

Scoped to *passive* components. A negative resistance is a real device — a
negative-impedance converter — so the claim is not "resistance is positive" but
"a passive resistor dissipates energy, so its resistance is positive". The
distinction is why matching uses the declared quantity and the rules are
restricted to parameters rather than applied to every Ohm-valued signal.
"""

from __future__ import annotations

from ..invariant import Comparison, Domain, Enforcement
from ..rules import QuantityRule, RulePack

ELECTRICAL = Domain("electrical")

PACK = RulePack(
    domain=ELECTRICAL,
    description="Passive electrical component parameters.",
    rules=[
        QuantityRule(
            rule_id="elec.resistance.positive",
            domain=ELECTRICAL,
            quantities=frozenset({"Resistance"}),
            units=frozenset({"Ohm"}),
            op=Comparison.GT, bound=0.0,
            origin="a passive resistor dissipates energy; R <= 0 would make it "
                   "a source, and R = 0 removes the equation that determines "
                   "its current",
            reference="MSL Electrical.Analog.Basic.Resistor",
            enforcement=Enforcement.STATIC, parameters_only=True,
        ),
        QuantityRule(
            rule_id="elec.capacitance.positive",
            domain=ELECTRICAL,
            quantities=frozenset({"Capacitance"}),
            units=frozenset({"F"}),
            op=Comparison.GT, bound=0.0,
            origin="stored energy is C*v^2/2, which a negative capacitance "
                   "makes negative; C = 0 removes the state",
            reference="MSL Electrical.Analog.Basic.Capacitor",
            enforcement=Enforcement.STATIC, parameters_only=True,
        ),
        QuantityRule(
            rule_id="elec.inductance.positive",
            domain=ELECTRICAL,
            quantities=frozenset({"Inductance", "SelfInductance"}),
            units=frozenset({"H"}),
            op=Comparison.GT, bound=0.0,
            origin="stored energy is L*i^2/2; L = 0 turns the differential "
                   "equation into a constraint on voltage",
            reference="MSL Electrical.Analog.Basic.Inductor",
            enforcement=Enforcement.STATIC, parameters_only=True,
        ),
        QuantityRule(
            rule_id="elec.conductance.positive",
            domain=ELECTRICAL,
            quantities=frozenset({"Conductance"}),
            units=frozenset({"S"}),
            op=Comparison.GT, bound=0.0,
            origin="the reciprocal of a passive resistance",
            enforcement=Enforcement.STATIC, parameters_only=True,
        ),
    ],
)
