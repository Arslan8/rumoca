# Zero stiffness/damping disables one parallel force term

Group `zero-spring-damper-term` · 6 report instances · false-positives

The equations are f_c=c*(s_rel-s_rel0), f_d=d*v_rel and f=f_c+f_d. Both parameters are multipliers with min=0; zero cleanly removes the corresponding elastic or dissipative term. It is not an intrinsic division or invalid bound.

Correct the detector/adjudicator for this specific semantic case; do not impose a blanket strictly-positive bound on the library declaration.

Read the per-report evidence: members can share a declaration while having different runtime outcomes. Source-proof reuse is not a claim that every instance was independently simulated.

| ID | Model | Target |
|---|---|---|
| [FINDING-04429](../false-positives/FINDING-04429.md) | Modelica.Mechanics.Translational.Examples.Damper | `springDamper3.c` |
| [FINDING-04435](../false-positives/FINDING-04435.md) | Modelica.Mechanics.Translational.Examples.ElastoGap | `springDamper1.c` |
| [FINDING-04436](../false-positives/FINDING-04436.md) | Modelica.Mechanics.Translational.Examples.ElastoGap | `springDamper2.c` |
| [FINDING-04457](../false-positives/FINDING-04457.md) | Modelica.Mechanics.Translational.Examples.InitialConditions | `sd2.c` |
| [FINDING-04461](../false-positives/FINDING-04461.md) | Modelica.Mechanics.Translational.Examples.InitialConditions | `sd1.c` |
| [FINDING-05026](../false-positives/FINDING-05026.md) | ModelicaTest.Translational.AllComponents | `springDamper.c` |
