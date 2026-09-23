# Zero rotational stiffness/damping disables one torque term

Group `zero-rotational-spring-damper` · 2 report instances · false-positives

The component torque is the sum of c*phi_rel and d*w_rel terms. c and d have min=0 and are multipliers, so zero cleanly removes elasticity or damping; it is not an unguarded divisor.

Correct the detector/adjudicator for this specific semantic case; do not impose a blanket strictly-positive bound on the library declaration.

Read the per-report evidence: members can share a declaration while having different runtime outcomes. Source-proof reuse is not a claim that every instance was independently simulated.

| ID | Model | Target |
|---|---|---|
| [FINDING-04371](../false-positives/FINDING-04371.md) | Modelica.Mechanics.Rotational.Examples.Backlash | `springDamper.c` |
| [FINDING-04390](../false-positives/FINDING-04390.md) | Modelica.Mechanics.Rotational.Examples.ElasticBearing | `springDamper.c` |
