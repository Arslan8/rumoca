# Zero stiffness is a force-free spring limit

Group `zero-spring-stiffness` · 25 report instances · false-positives

The constitutive equation multiplies displacement by c (f=c*(s_rel-s_rel0) or tau=c*(phi_rel-phi_rel0)). At c=0 it transmits no elastic force; there is no reciprocal and the declaration intentionally has min=0. A disconnected or under-constrained surrounding mechanism is topology-specific, not proof that the component bound is defective.

Correct the detector/adjudicator for this specific semantic case; do not impose a blanket strictly-positive bound on the library declaration.

Read the per-report evidence: members can share a declaration while having different runtime outcomes. Source-proof reuse is not a claim that every instance was independently simulated.

| ID | Model | Target |
|---|---|---|
| [FINDING-03952](../false-positives/FINDING-03952.md) | Modelica.Mechanics.MultiBody.Examples.Elementary.FreeBody | `spring1.spring.c` |
| [FINDING-03971](../false-positives/FINDING-03971.md) | Modelica.Mechanics.MultiBody.Examples.Elementary.FreeBody | `spring2.spring.c` |
| [FINDING-03985](../false-positives/FINDING-03985.md) | Modelica.Mechanics.MultiBody.Examples.Elementary.HeatLosses | `spring1.spring.c` |
| [FINDING-04007](../false-positives/FINDING-04007.md) | Modelica.Mechanics.MultiBody.Examples.Elementary.HeatLosses | `spring.spring.c` |
| [FINDING-04028](../false-positives/FINDING-04028.md) | Modelica.Mechanics.MultiBody.Examples.Elementary.InitSpringConstant | `spring.spring.c` |
| [FINDING-04122](../false-positives/FINDING-04122.md) | Modelica.Mechanics.MultiBody.Examples.Elementary.PointGravityWithPointMasses | `spring.spring.c` |
| [FINDING-04128](../false-positives/FINDING-04128.md) | Modelica.Mechanics.MultiBody.Examples.Elementary.SpringWithMass | `spring.spring.c` |
| [FINDING-04150](../false-positives/FINDING-04150.md) | Modelica.Mechanics.MultiBody.Examples.Elementary.ThreeSprings | `spring1.spring.c` |
| [FINDING-04154](../false-positives/FINDING-04154.md) | Modelica.Mechanics.MultiBody.Examples.Elementary.ThreeSprings | `spring2.spring.c` |
| [FINDING-04158](../false-positives/FINDING-04158.md) | Modelica.Mechanics.MultiBody.Examples.Elementary.ThreeSprings | `spring3.spring.c` |
| [FINDING-04389](../false-positives/FINDING-04389.md) | Modelica.Mechanics.Rotational.Examples.ElasticBearing | `spring.c` |
| [FINDING-04397](../false-positives/FINDING-04397.md) | Modelica.Mechanics.Rotational.Examples.FirstGrounded | `spring.c` |
| [FINDING-04403](../false-positives/FINDING-04403.md) | Modelica.Mechanics.Rotational.Examples.First | `spring.c` |
| [FINDING-04416](../false-positives/FINDING-04416.md) | Modelica.Mechanics.Rotational.Examples.Utilities.Spring | `spring.c` |
| [FINDING-04428](../false-positives/FINDING-04428.md) | Modelica.Mechanics.Translational.Examples.Damper | `spring2.c` |
| [FINDING-04452](../false-positives/FINDING-04452.md) | Modelica.Mechanics.Translational.Examples.GenerationOfFMUs | `spring.spring.c` |
| [FINDING-04455](../false-positives/FINDING-04455.md) | Modelica.Mechanics.Translational.Examples.InitialConditions | `s2.c` |
| [FINDING-04459](../false-positives/FINDING-04459.md) | Modelica.Mechanics.Translational.Examples.InitialConditions | `s1.c` |
| [FINDING-04464](../false-positives/FINDING-04464.md) | Modelica.Mechanics.Translational.Examples.Oscillator | `spring1.c` |
| [FINDING-04466](../false-positives/FINDING-04466.md) | Modelica.Mechanics.Translational.Examples.Oscillator | `spring2.c` |
| [FINDING-04472](../false-positives/FINDING-04472.md) | Modelica.Mechanics.Translational.Examples.PreLoad | `spring.c` |
| [FINDING-04488](../false-positives/FINDING-04488.md) | Modelica.Mechanics.Translational.Examples.Utilities.Spring | `spring.c` |
| [FINDING-04489](../false-positives/FINDING-04489.md) | Modelica.Mechanics.Translational.Examples.WhyArrows | `spring1.c` |
| [FINDING-04491](../false-positives/FINDING-04491.md) | Modelica.Mechanics.Translational.Examples.WhyArrows | `spring2.c` |
| [FINDING-05024](../false-positives/FINDING-05024.md) | ModelicaTest.Translational.AllComponents | `spring.c` |
