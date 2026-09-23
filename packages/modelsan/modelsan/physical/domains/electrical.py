"""Electrical rules.

Scoped to *passive* components. A negative resistance is a real device — a
negative-impedance converter — so the claim is not "resistance is positive" but
"a passive resistor dissipates energy, so its resistance is positive".

Each rule therefore names the component role that establishes its premise and
the role that refutes it, and leaves the semantic binder to decide which
objects hold them. Matching on the declared quantity alone was not enough: it
reported `Nr.Ga = -0.76` in `ChuaCircuit` as a violation at the highest
confidence, quantity and unit both agreeing and both beside the point, on a
stock MSL example whose negative conductance is the device.

Where nothing is known about the declaring class the rules still fire on the
quantity, at the lower severity — a negative resistance is anomalous by
default, and only a positive statement to the contrary should silence it.
"""

from __future__ import annotations

from ..invariant import Comparison, Domain, Enforcement
from ..rules import RulePack, SemanticRule
from ...semantics import role as roles

ELECTRICAL = Domain("electrical")

PACK = RulePack(
    domain=ELECTRICAL,
    description="Passive electrical component parameters.",
    rules=[
        SemanticRule(
            rule_id="elec.resistance.positive",
            confirming_roles=frozenset({roles.PASSIVE_RESISTANCE}),
            excluded_roles=frozenset({roles.ACTIVE_RESISTANCE,
                                      roles.UNRESTRICTED_RESISTANCE,
                                      roles.MACHINE_WINDING_RESISTANCE}),
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
        SemanticRule(
            rule_id="elec.capacitance.positive",
            confirming_roles=frozenset({roles.PASSIVE_CAPACITANCE}),
            domain=ELECTRICAL,
            quantities=frozenset({"Capacitance"}),
            units=frozenset({"F"}),
            op=Comparison.GT, bound=0.0,
            origin="stored energy is C*v^2/2, which a negative capacitance "
                   "makes negative; C = 0 removes the state",
            reference="MSL Electrical.Analog.Basic.Capacitor",
            enforcement=Enforcement.STATIC, parameters_only=True,
        ),
        SemanticRule(
            rule_id="elec.inductance.positive",
            confirming_roles=frozenset({roles.PASSIVE_INDUCTANCE}),
            domain=ELECTRICAL,
            quantities=frozenset({"Inductance", "SelfInductance"}),
            units=frozenset({"H"}),
            op=Comparison.GT, bound=0.0,
            origin="stored energy is L*i^2/2; L = 0 turns the differential "
                   "equation into a constraint on voltage",
            reference="MSL Electrical.Analog.Basic.Inductor",
            enforcement=Enforcement.STATIC, parameters_only=True,
        ),
        SemanticRule(
            rule_id="elec.conductance.positive",
            confirming_roles=frozenset({roles.PASSIVE_CONDUCTANCE}),
            excluded_roles=frozenset({roles.ACTIVE_CONDUCTANCE,
                                      roles.UNRESTRICTED_CONDUCTANCE,
                                      roles.MACHINE_WINDING_CONDUCTANCE}),
            domain=ELECTRICAL,
            quantities=frozenset({"Conductance"}),
            units=frozenset({"S"}),
            op=Comparison.GT, bound=0.0,
            origin="the reciprocal of a passive resistance",
            enforcement=Enforcement.STATIC, parameters_only=True,
        ),
        # The third answer. A machine winding is copper: a negative resistance
        # is a defect and must still be reported, while zero is the ideal
        # lossless winding that the machine examples set on purpose. Neither
        # `> 0` nor "unrestricted" says that, which is why this rule exists
        # rather than another entry in one of the two existing lists.
        SemanticRule(
            rule_id="elec.machine_winding_resistance.non_negative",
            confirming_roles=frozenset({roles.MACHINE_WINDING_RESISTANCE}),
            excluded_roles=frozenset({roles.ACTIVE_RESISTANCE,
                                      roles.UNRESTRICTED_RESISTANCE}),
            domain=ELECTRICAL,
            quantities=frozenset(),
            units=frozenset(),
            op=Comparison.GE, bound=0.0,
            origin="a winding is copper; R < 0 is not a machine, and R = 0 is "
                   "the ideal lossless winding the examples use deliberately",
            reference="MSL Electrical.Machines.Utilities.ParameterRecords",
            enforcement=Enforcement.STATIC, parameters_only=True,
        ),
        SemanticRule(
            rule_id="elec.machine_winding_conductance.non_negative",
            confirming_roles=frozenset({roles.MACHINE_WINDING_CONDUCTANCE}),
            excluded_roles=frozenset({roles.ACTIVE_CONDUCTANCE,
                                      roles.UNRESTRICTED_CONDUCTANCE}),
            domain=ELECTRICAL,
            quantities=frozenset(),
            units=frozenset(),
            op=Comparison.GE, bound=0.0,
            origin="the reciprocal of a winding resistance, with the same "
                   "lossless limit at zero",
            enforcement=Enforcement.STATIC, parameters_only=True,
        ),
    ],
)
