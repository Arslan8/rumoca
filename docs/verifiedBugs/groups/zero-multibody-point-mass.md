# PointMass permits a massless algebraic point

Group `zero-multibody-point-mass` · 10 report instances · false-positives

PointMass declares m(min=0), and its force equation multiplies acceleration/gravity by m. At zero it becomes a force-balance/kinematic connection rather than dividing by mass. A surrounding free-state formulation may need different state selection, but the component declaration is not intrinsically invalid.

Correct the detector/adjudicator for this specific semantic case; do not impose a blanket strictly-positive bound on the library declaration.

Read the per-report evidence: members can share a declaration while having different runtime outcomes. Source-proof reuse is not a claim that every instance was independently simulated.

| ID | Model | Target |
|---|---|---|
| [FINDING-04059](../false-positives/FINDING-04059.md) | Modelica.Mechanics.MultiBody.Examples.Elementary.PointGravityWithPointMasses2 | `pointMass1.m` |
| [FINDING-04060](../false-positives/FINDING-04060.md) | Modelica.Mechanics.MultiBody.Examples.Elementary.PointGravityWithPointMasses2 | `pointMass2.m` |
| [FINDING-04061](../false-positives/FINDING-04061.md) | Modelica.Mechanics.MultiBody.Examples.Elementary.PointGravityWithPointMasses2 | `pointMass3.m` |
| [FINDING-04062](../false-positives/FINDING-04062.md) | Modelica.Mechanics.MultiBody.Examples.Elementary.PointGravityWithPointMasses2 | `pointMass4.m` |
| [FINDING-04063](../false-positives/FINDING-04063.md) | Modelica.Mechanics.MultiBody.Examples.Elementary.PointGravityWithPointMasses2 | `pointMass5.m` |
| [FINDING-04064](../false-positives/FINDING-04064.md) | Modelica.Mechanics.MultiBody.Examples.Elementary.PointGravityWithPointMasses2 | `pointMass6.m` |
| [FINDING-04115](../false-positives/FINDING-04115.md) | Modelica.Mechanics.MultiBody.Examples.Elementary.PointGravityWithPointMasses | `body1.m` |
| [FINDING-04116](../false-positives/FINDING-04116.md) | Modelica.Mechanics.MultiBody.Examples.Elementary.PointGravityWithPointMasses | `body2.m` |
| [FINDING-04117](../false-positives/FINDING-04117.md) | Modelica.Mechanics.MultiBody.Examples.Elementary.PointGravityWithPointMasses | `body3.m` |
| [FINDING-04118](../false-positives/FINDING-04118.md) | Modelica.Mechanics.MultiBody.Examples.Elementary.PointGravityWithPointMasses | `body4.m` |
