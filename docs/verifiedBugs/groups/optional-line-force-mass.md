# The line-force point mass is explicitly optional

Group `optional-line-force-mass` · 10 report instances · false-positives

The parameter is declared m(min=0)=0 and described as a point mass on the connection line; animation is conditional on m>0. Zero is the default no-added-mass configuration, so flagging it as an invalid physical bound contradicts the model design.

Correct the detector/adjudicator for this specific semantic case; do not impose a blanket strictly-positive bound on the library declaration.

Read the per-report evidence: members can share a declaration while having different runtime outcomes. Source-proof reuse is not a claim that every instance was independently simulated.

| ID | Model | Target |
|---|---|---|
| [FINDING-03951](../false-positives/FINDING-03951.md) | Modelica.Mechanics.MultiBody.Examples.Elementary.FreeBody | `spring1.lineForce.m` |
| [FINDING-03970](../false-positives/FINDING-03970.md) | Modelica.Mechanics.MultiBody.Examples.Elementary.FreeBody | `spring2.lineForce.m` |
| [FINDING-03984](../false-positives/FINDING-03984.md) | Modelica.Mechanics.MultiBody.Examples.Elementary.HeatLosses | `spring1.lineForce.m` |
| [FINDING-04006](../false-positives/FINDING-04006.md) | Modelica.Mechanics.MultiBody.Examples.Elementary.HeatLosses | `spring.lineForce.m` |
| [FINDING-04027](../false-positives/FINDING-04027.md) | Modelica.Mechanics.MultiBody.Examples.Elementary.InitSpringConstant | `spring.lineForce.m` |
| [FINDING-04121](../false-positives/FINDING-04121.md) | Modelica.Mechanics.MultiBody.Examples.Elementary.PointGravityWithPointMasses | `spring.lineForce.m` |
| [FINDING-04127](../false-positives/FINDING-04127.md) | Modelica.Mechanics.MultiBody.Examples.Elementary.SpringWithMass | `spring.lineForce.m` |
| [FINDING-04149](../false-positives/FINDING-04149.md) | Modelica.Mechanics.MultiBody.Examples.Elementary.ThreeSprings | `spring1.lineForce.m` |
| [FINDING-04153](../false-positives/FINDING-04153.md) | Modelica.Mechanics.MultiBody.Examples.Elementary.ThreeSprings | `spring2.lineForce.m` |
| [FINDING-04157](../false-positives/FINDING-04157.md) | Modelica.Mechanics.MultiBody.Examples.Elementary.ThreeSprings | `spring3.lineForce.m` |
