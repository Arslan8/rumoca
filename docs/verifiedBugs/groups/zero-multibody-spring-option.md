# MultiBody spring mass/stiffness has an intentional zero limit

Group `zero-multibody-spring-option` · 20 report instances · false-positives

c(min=0) is forwarded to the translational Spring equation f=c*(s_rel-s_rel0), so zero transmits no elastic force. The reported blanket positive-only constraint is inconsistent with these explicit component branches/equations.

Correct the detector/adjudicator for this specific semantic case; do not impose a blanket strictly-positive bound on the library declaration.

Read the per-report evidence: members can share a declaration while having different runtime outcomes. Source-proof reuse is not a claim that every instance was independently simulated.

| ID | Model | Target |
|---|---|---|
| [FINDING-03949](../false-positives/FINDING-03949.md) | Modelica.Mechanics.MultiBody.Examples.Elementary.FreeBody | `spring1.c` |
| [FINDING-03950](../false-positives/FINDING-03950.md) | Modelica.Mechanics.MultiBody.Examples.Elementary.FreeBody | `spring1.m` |
| [FINDING-03968](../false-positives/FINDING-03968.md) | Modelica.Mechanics.MultiBody.Examples.Elementary.FreeBody | `spring2.c` |
| [FINDING-03969](../false-positives/FINDING-03969.md) | Modelica.Mechanics.MultiBody.Examples.Elementary.FreeBody | `spring2.m` |
| [FINDING-03982](../false-positives/FINDING-03982.md) | Modelica.Mechanics.MultiBody.Examples.Elementary.HeatLosses | `spring1.c` |
| [FINDING-03983](../false-positives/FINDING-03983.md) | Modelica.Mechanics.MultiBody.Examples.Elementary.HeatLosses | `spring1.m` |
| [FINDING-04004](../false-positives/FINDING-04004.md) | Modelica.Mechanics.MultiBody.Examples.Elementary.HeatLosses | `spring.c` |
| [FINDING-04005](../false-positives/FINDING-04005.md) | Modelica.Mechanics.MultiBody.Examples.Elementary.HeatLosses | `spring.m` |
| [FINDING-04025](../false-positives/FINDING-04025.md) | Modelica.Mechanics.MultiBody.Examples.Elementary.InitSpringConstant | `spring.c` |
| [FINDING-04026](../false-positives/FINDING-04026.md) | Modelica.Mechanics.MultiBody.Examples.Elementary.InitSpringConstant | `spring.m` |
| [FINDING-04119](../false-positives/FINDING-04119.md) | Modelica.Mechanics.MultiBody.Examples.Elementary.PointGravityWithPointMasses | `spring.c` |
| [FINDING-04120](../false-positives/FINDING-04120.md) | Modelica.Mechanics.MultiBody.Examples.Elementary.PointGravityWithPointMasses | `spring.m` |
| [FINDING-04125](../false-positives/FINDING-04125.md) | Modelica.Mechanics.MultiBody.Examples.Elementary.SpringWithMass | `spring.c` |
| [FINDING-04126](../false-positives/FINDING-04126.md) | Modelica.Mechanics.MultiBody.Examples.Elementary.SpringWithMass | `spring.m` |
| [FINDING-04147](../false-positives/FINDING-04147.md) | Modelica.Mechanics.MultiBody.Examples.Elementary.ThreeSprings | `spring1.c` |
| [FINDING-04148](../false-positives/FINDING-04148.md) | Modelica.Mechanics.MultiBody.Examples.Elementary.ThreeSprings | `spring1.m` |
| [FINDING-04151](../false-positives/FINDING-04151.md) | Modelica.Mechanics.MultiBody.Examples.Elementary.ThreeSprings | `spring2.c` |
| [FINDING-04152](../false-positives/FINDING-04152.md) | Modelica.Mechanics.MultiBody.Examples.Elementary.ThreeSprings | `spring2.m` |
| [FINDING-04155](../false-positives/FINDING-04155.md) | Modelica.Mechanics.MultiBody.Examples.Elementary.ThreeSprings | `spring3.c` |
| [FINDING-04156](../false-positives/FINDING-04156.md) | Modelica.Mechanics.MultiBody.Examples.Elementary.ThreeSprings | `spring3.m` |
