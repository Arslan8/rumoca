"""Automotive rules, written against roles rather than against model paths.

Nothing here names a variable. `automotive.wheel.radius` is what the rule
requires; which object fills it is the binder's problem, and in this domain it
is usually the user's answer — `rad/s` does not distinguish a wheel from a fan,
and no amount of metadata in the model will.

This is the separation the architecture turns on. The same pack applies to any
vehicle model from any vendor, because it never had to know how that vendor
spells its paths.
"""

from __future__ import annotations

from ...physical.invariant import Comparison, Domain, Enforcement
from ...physical.rules import RulePack, SemanticRule

AUTOMOTIVE = Domain("automotive")

PACK = RulePack(
    domain=AUTOMOTIVE,
    description="Vehicle-level invariants over bound semantic roles.",
    rules=[
        SemanticRule(
            rule_id="auto.wheel.radius.positive",
            domain=AUTOMOTIVE,
            # No quantity fallback: `Length` is shared by a wheel radius and
            # every other length in a vehicle, so there is nothing to fall back
            # *to*. This rule fires only on a bound role, which is the honest
            # position — without the binding, the checker does not know which
            # length is a wheel.
            quantities=frozenset(),
            confirming_roles=frozenset({"automotive.wheel.radius"}),
            op=Comparison.GT, bound=0.0,
            origin="a wheel has positive radius; a non-positive one makes the "
                   "speed-to-angular-velocity relation v = w*r degenerate or "
                   "sign-inverted",
            reference="vehicle dynamics, rolling radius",
            enforcement=Enforcement.STATIC, parameters_only=True,
            severity="high", confirmed_severity="high",
        ),
        SemanticRule(
            rule_id="auto.vehicle_speed.finite_non_negative",
            domain=AUTOMOTIVE,
            quantities=frozenset(),
            confirming_roles=frozenset({"automotive.vehicle_speed"}),
            op=Comparison.GE, bound=0.0,
            origin="a vehicle speed expressed as a magnitude is non-negative; "
                   "a signed longitudinal velocity should be declared as one",
            enforcement=Enforcement.RUNTIME,
            severity="medium", confirmed_severity="medium",
        ),
    ],
)
