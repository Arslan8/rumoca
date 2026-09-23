"""Mechanical rules.

Damping is `>= 0` rather than `> 0` because a frictionless joint is a normal
idealisation, while a *negative* damper injects energy. Stiffness is `> 0`
because a zero-stiffness spring is not a spring — it is an absent constraint,
and MSL models that intend one omit the component.

Mass and inertia key on the declaring class as well as the quantity, and unlike
the electrical elements the stronger claim survives scrutiny: MSL documents
`Basic.Resistor`'s R as "allowed to be positive, zero, or negative" and grants
`Mass` and `Inertia` no such latitude. `Rotational.Components.Inertia.J`
declares `min=0` and cannot honour it, which is BUG-018.
"""

from __future__ import annotations

from ..invariant import Comparison, Domain, Enforcement
from ..rules import QuantityRule, RulePack, SemanticRule
from ...semantics import role as roles

MECHANICAL = Domain("mechanical")

PACK = RulePack(
    domain=MECHANICAL,
    description="Rigid-body and drive-train parameters.",
    rules=[
        SemanticRule(
            rule_id="mech.mass.positive",
            confirming_roles=frozenset({roles.TRANSLATIONAL_MASS}),
            domain=MECHANICAL,
            quantities=frozenset({"Mass"}),
            units=frozenset({"kg"}),
            op=Comparison.GT, bound=0.0,
            origin="m*a = f determines acceleration only for m > 0; negative "
                   "mass is not a physical body",
            reference="MSL Mechanics.Translational.Components.Mass",
            enforcement=Enforcement.STATIC, parameters_only=True,
        ),
        SemanticRule(
            rule_id="mech.inertia.positive",
            confirming_roles=frozenset({roles.ROTATIONAL_INERTIA}),
            domain=MECHANICAL,
            quantities=frozenset({"Inertia", "MomentOfInertia"}),
            units=frozenset({"kg.m2"}),
            op=Comparison.GT, bound=0.0,
            origin="the rotational analogue of mass; J = 0 leaves angular "
                   "acceleration undetermined",
            reference="MSL Mechanics.Rotational.Components.Inertia",
            enforcement=Enforcement.STATIC, parameters_only=True,
        ),
        QuantityRule(
            rule_id="mech.damping.non_negative",
            domain=MECHANICAL,
            quantities=frozenset({"TranslationalDampingConstant",
                                  "RotationalDampingConstant"}),
            op=Comparison.GE, bound=0.0,
            origin="a damper dissipates; d < 0 injects energy. Zero is a "
                   "legitimate frictionless idealisation, so the bound is >=",
            enforcement=Enforcement.STATIC, parameters_only=True,
        ),
        QuantityRule(
            rule_id="mech.stiffness.positive",
            domain=MECHANICAL,
            quantities=frozenset({"TranslationalSpringConstant",
                                  "RotationalSpringConstant"}),
            op=Comparison.GT, bound=0.0,
            origin="a spring with c <= 0 does not restore; c = 0 removes the "
                   "constraint the component exists to impose",
            enforcement=Enforcement.STATIC, parameters_only=True,
        ),
    ],
)
