# Zero MultiBody visualization fraction divides geometry by zero

Group `multibody-visual-scale` · 34 report instances · confirmed

World exposes this parameter without a positive bound, while default body/frame dimensions divide a length by it. Zero is therefore admitted and makes animation geometry undefined. Although visual rather than physical dynamics, it is a real unguarded parameter-domain defect.

Add a meaningful strictly-positive lower bound and explicit assertion for the fraction before dependent animation dimensions are evaluated. Keep animation=false paths lazy so unused visualization settings need not block physical simulation.

Read the per-report evidence: members can share a declaration while having different runtime outcomes. Source-proof reuse is not a claim that every instance was independently simulated.

| ID | Model | Target |
|---|---|---|
| [FINDING-03919](../confirmed/FINDING-03919.md) | Modelica.Mechanics.MultiBody.Examples.Elementary.DoublePendulumInitTip | `world.defaultFrameDiameterFraction` |
| [FINDING-03920](../confirmed/FINDING-03920.md) | Modelica.Mechanics.MultiBody.Examples.Elementary.DoublePendulumInitTip | `world.defaultWidthFraction` |
| [FINDING-03947](../confirmed/FINDING-03947.md) | Modelica.Mechanics.MultiBody.Examples.Elementary.DoublePendulum | `world.defaultFrameDiameterFraction` |
| [FINDING-03948](../confirmed/FINDING-03948.md) | Modelica.Mechanics.MultiBody.Examples.Elementary.DoublePendulum | `world.defaultWidthFraction` |
| [FINDING-03972](../confirmed/FINDING-03972.md) | Modelica.Mechanics.MultiBody.Examples.Elementary.FreeBody | `world.defaultFrameDiameterFraction` |
| [FINDING-03973](../confirmed/FINDING-03973.md) | Modelica.Mechanics.MultiBody.Examples.Elementary.FreeBody | `world.defaultWidthFraction` |
| [FINDING-04008](../confirmed/FINDING-04008.md) | Modelica.Mechanics.MultiBody.Examples.Elementary.HeatLosses | `world.defaultFrameDiameterFraction` |
| [FINDING-04009](../confirmed/FINDING-04009.md) | Modelica.Mechanics.MultiBody.Examples.Elementary.HeatLosses | `world.defaultWidthFraction` |
| [FINDING-04029](../confirmed/FINDING-04029.md) | Modelica.Mechanics.MultiBody.Examples.Elementary.InitSpringConstant | `world.defaultFrameDiameterFraction` |
| [FINDING-04030](../confirmed/FINDING-04030.md) | Modelica.Mechanics.MultiBody.Examples.Elementary.InitSpringConstant | `world.defaultWidthFraction` |
| [FINDING-04039](../confirmed/FINDING-04039.md) | Modelica.Mechanics.MultiBody.Examples.Elementary.Pendulum | `world.defaultFrameDiameterFraction` |
| [FINDING-04040](../confirmed/FINDING-04040.md) | Modelica.Mechanics.MultiBody.Examples.Elementary.Pendulum | `world.defaultWidthFraction` |
| [FINDING-04057](../confirmed/FINDING-04057.md) | Modelica.Mechanics.MultiBody.Examples.Elementary.PointGravity | `world.defaultFrameDiameterFraction` |
| [FINDING-04058](../confirmed/FINDING-04058.md) | Modelica.Mechanics.MultiBody.Examples.Elementary.PointGravity | `world.defaultWidthFraction` |
| [FINDING-04113](../confirmed/FINDING-04113.md) | Modelica.Mechanics.MultiBody.Examples.Elementary.PointGravityWithPointMasses2 | `world.defaultWidthFraction` |
| [FINDING-04114](../confirmed/FINDING-04114.md) | Modelica.Mechanics.MultiBody.Examples.Elementary.PointGravityWithPointMasses2 | `world.defaultFrameDiameterFraction` |
| [FINDING-04123](../confirmed/FINDING-04123.md) | Modelica.Mechanics.MultiBody.Examples.Elementary.PointGravityWithPointMasses | `world.defaultFrameDiameterFraction` |
| [FINDING-04124](../confirmed/FINDING-04124.md) | Modelica.Mechanics.MultiBody.Examples.Elementary.PointGravityWithPointMasses | `world.defaultWidthFraction` |
| [FINDING-04137](../confirmed/FINDING-04137.md) | Modelica.Mechanics.MultiBody.Examples.Elementary.SpringWithMass | `world.defaultFrameDiameterFraction` |
| [FINDING-04138](../confirmed/FINDING-04138.md) | Modelica.Mechanics.MultiBody.Examples.Elementary.SpringWithMass | `world.defaultWidthFraction` |
| [FINDING-04159](../confirmed/FINDING-04159.md) | Modelica.Mechanics.MultiBody.Examples.Elementary.ThreeSprings | `world.defaultFrameDiameterFraction` |
| [FINDING-04160](../confirmed/FINDING-04160.md) | Modelica.Mechanics.MultiBody.Examples.Elementary.ThreeSprings | `world.defaultWidthFraction` |
| [FINDING-04169](../confirmed/FINDING-04169.md) | Modelica.Mechanics.MultiBody.Examples.Elementary.UserDefinedGravityField | `world.defaultFrameDiameterFraction` |
| [FINDING-04170](../confirmed/FINDING-04170.md) | Modelica.Mechanics.MultiBody.Examples.Elementary.UserDefinedGravityField | `world.defaultWidthFraction` |
| [FINDING-04223](../confirmed/FINDING-04223.md) | Modelica.Mechanics.MultiBody.Examples.Loops.PlanarFourbar | `world.defaultFrameDiameterFraction` |
| [FINDING-04224](../confirmed/FINDING-04224.md) | Modelica.Mechanics.MultiBody.Examples.Loops.PlanarFourbar | `world.defaultWidthFraction` |
| [FINDING-04246](../confirmed/FINDING-04246.md) | Modelica.Mechanics.MultiBody.Examples.Rotational3DEffects.BevelGear1D | `world.defaultFrameDiameterFraction` |
| [FINDING-04247](../confirmed/FINDING-04247.md) | Modelica.Mechanics.MultiBody.Examples.Rotational3DEffects.BevelGear1D | `world.defaultWidthFraction` |
| [FINDING-04369](../confirmed/FINDING-04369.md) | Modelica.Mechanics.MultiBody.Examples.Systems.RobotR3.Utilities.MechanicalStructure | `world.defaultFrameDiameterFraction` |
| [FINDING-04370](../confirmed/FINDING-04370.md) | Modelica.Mechanics.MultiBody.Examples.Systems.RobotR3.Utilities.MechanicalStructure | `world.defaultWidthFraction` |
| [FINDING-04997](../confirmed/FINDING-04997.md) | ModelicaTest.MultiBody.WorldGroundVisualization | `world.defaultFrameDiameterFraction` |
| [FINDING-04998](../confirmed/FINDING-04998.md) | ModelicaTest.MultiBody.WorldGroundVisualization | `world.defaultWidthFraction` |
| [FINDING-05012](../confirmed/FINDING-05012.md) | ModelicaTest.Rotational.TestMove | `world.defaultFrameDiameterFraction` |
| [FINDING-05013](../confirmed/FINDING-05013.md) | ModelicaTest.Rotational.TestMove | `world.defaultWidthFraction` |
