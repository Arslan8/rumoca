# Zero mass is a massless algebraic component, not an intrinsic division

Group `zero-translational-mass` · 70 report instances · false-positives

The declared min is zero and the equation is m*a=flange_a.f+flange_b.f. At m=0 this becomes an algebraic force-balance constraint; the source does not divide by m. Independent controls retain m=0 and simulate after incompatible fixed initialization is removed. Some connected systems can be inconsistent, but the blanket strictly-positive attribution is false.

Correct the detector/adjudicator for this specific semantic case; do not impose a blanket strictly-positive bound on the library declaration.

Read the per-report evidence: members can share a declaration while having different runtime outcomes. Source-proof reuse is not a claim that every instance was independently simulated.

| ID | Model | Target |
|---|---|---|
| [FINDING-03769](../false-positives/FINDING-03769.md) | Modelica.Magnetic.FluxTubes.Examples.MovingCoilActuator.ArmatureStroke | `pmActuator.armature.mass.m` |
| [FINDING-03772](../false-positives/FINDING-03772.md) | Modelica.Magnetic.FluxTubes.Examples.MovingCoilActuator.ArmatureStroke | `pmLoad.m` |
| [FINDING-03781](../false-positives/FINDING-03781.md) | Modelica.Magnetic.FluxTubes.Examples.MovingCoilActuator.ArmatureStroke | `cActuator.armature.mass.m` |
| [FINDING-03785](../false-positives/FINDING-03785.md) | Modelica.Magnetic.FluxTubes.Examples.MovingCoilActuator.ArmatureStroke | `cLoad.m` |
| [FINDING-03801](../false-positives/FINDING-03801.md) | Modelica.Magnetic.FluxTubes.Examples.MovingCoilActuator.Components.ConstantActuator | `armature.mass.m` |
| [FINDING-03812](../false-positives/FINDING-03812.md) | Modelica.Magnetic.FluxTubes.Examples.MovingCoilActuator.Components.PermeanceActuator | `armature.mass.m` |
| [FINDING-03832](../false-positives/FINDING-03832.md) | Modelica.Magnetic.FluxTubes.Examples.SolenoidActuator.Components.AdvancedSolenoid | `armature.mass.m` |
| [FINDING-03865](../false-positives/FINDING-03865.md) | Modelica.Magnetic.FluxTubes.Examples.SolenoidActuator.Components.SimpleSolenoid | `armature.mass.m` |
| [FINDING-03888](../false-positives/FINDING-03888.md) | Modelica.Magnetic.FluxTubes.Examples.Utilities.TranslatoryArmatureAndStopper | `mass.m` |
| [FINDING-04406](../false-positives/FINDING-04406.md) | Modelica.Mechanics.Rotational.Examples.RollingWheel | `mass.m` |
| [FINDING-04417](../false-positives/FINDING-04417.md) | Modelica.Mechanics.Translational.Examples.Accelerate | `mass.m` |
| [FINDING-04419](../false-positives/FINDING-04419.md) | Modelica.Mechanics.Translational.Examples.CompareBrakingForce | `mass1.m` |
| [FINDING-04420](../false-positives/FINDING-04420.md) | Modelica.Mechanics.Translational.Examples.CompareBrakingForce | `mass2.m` |
| [FINDING-04421](../false-positives/FINDING-04421.md) | Modelica.Mechanics.Translational.Examples.CompareBrakingForce | `mass3.m` |
| [FINDING-04422](../false-positives/FINDING-04422.md) | Modelica.Mechanics.Translational.Examples.CompareBrakingForce | `mass4.m` |
| [FINDING-04425](../false-positives/FINDING-04425.md) | Modelica.Mechanics.Translational.Examples.Damper | `mass1.m` |
| [FINDING-04426](../false-positives/FINDING-04426.md) | Modelica.Mechanics.Translational.Examples.Damper | `mass2.m` |
| [FINDING-04427](../false-positives/FINDING-04427.md) | Modelica.Mechanics.Translational.Examples.Damper | `mass3.m` |
| [FINDING-04430](../false-positives/FINDING-04430.md) | Modelica.Mechanics.Translational.Examples.EddyCurrentBrake | `mass.m` |
| [FINDING-04437](../false-positives/FINDING-04437.md) | Modelica.Mechanics.Translational.Examples.ElastoGap | `mass1.m` |
| [FINDING-04440](../false-positives/FINDING-04440.md) | Modelica.Mechanics.Translational.Examples.ElastoGap | `mass2.m` |
| [FINDING-04443](../false-positives/FINDING-04443.md) | Modelica.Mechanics.Translational.Examples.GenerationOfFMUs | `directMass.mass.m` |
| [FINDING-04445](../false-positives/FINDING-04445.md) | Modelica.Mechanics.Translational.Examples.GenerationOfFMUs | `inverseMass.mass.m` |
| [FINDING-04449](../false-positives/FINDING-04449.md) | Modelica.Mechanics.Translational.Examples.GenerationOfFMUs | `mass2a.m` |
| [FINDING-04450](../false-positives/FINDING-04450.md) | Modelica.Mechanics.Translational.Examples.GenerationOfFMUs | `mass2b.m` |
| [FINDING-04453](../false-positives/FINDING-04453.md) | Modelica.Mechanics.Translational.Examples.GenerationOfFMUs | `mass3a.m` |
| [FINDING-04454](../false-positives/FINDING-04454.md) | Modelica.Mechanics.Translational.Examples.GenerationOfFMUs | `mass3b.m` |
| [FINDING-04456](../false-positives/FINDING-04456.md) | Modelica.Mechanics.Translational.Examples.InitialConditions | `m3.m` |
| [FINDING-04458](../false-positives/FINDING-04458.md) | Modelica.Mechanics.Translational.Examples.InitialConditions | `m4.m` |
| [FINDING-04460](../false-positives/FINDING-04460.md) | Modelica.Mechanics.Translational.Examples.InitialConditions | `m1.m` |
| [FINDING-04462](../false-positives/FINDING-04462.md) | Modelica.Mechanics.Translational.Examples.InitialConditions | `m2.m` |
| [FINDING-04463](../false-positives/FINDING-04463.md) | Modelica.Mechanics.Translational.Examples.Oscillator | `mass1.m` |
| [FINDING-04465](../false-positives/FINDING-04465.md) | Modelica.Mechanics.Translational.Examples.Oscillator | `mass2.m` |
| [FINDING-04469](../false-positives/FINDING-04469.md) | Modelica.Mechanics.Translational.Examples.PreLoad | `spool.m` |
| [FINDING-04470](../false-positives/FINDING-04470.md) | Modelica.Mechanics.Translational.Examples.PreLoad | `springPlateA.m` |
| [FINDING-04471](../false-positives/FINDING-04471.md) | Modelica.Mechanics.Translational.Examples.PreLoad | `springPlateB.m` |
| [FINDING-04475](../false-positives/FINDING-04475.md) | Modelica.Mechanics.Translational.Examples.Sensors | `mass.m` |
| [FINDING-04476](../false-positives/FINDING-04476.md) | Modelica.Mechanics.Translational.Examples.SignConvention | `mass1.m` |
| [FINDING-04477](../false-positives/FINDING-04477.md) | Modelica.Mechanics.Translational.Examples.SignConvention | `mass2.m` |
| [FINDING-04478](../false-positives/FINDING-04478.md) | Modelica.Mechanics.Translational.Examples.SignConvention | `mass3.m` |
| [FINDING-04480](../false-positives/FINDING-04480.md) | Modelica.Mechanics.Translational.Examples.Utilities.DirectMass | `mass.m` |
| [FINDING-04482](../false-positives/FINDING-04482.md) | Modelica.Mechanics.Translational.Examples.Utilities.InverseMass | `mass.m` |
| [FINDING-04490](../false-positives/FINDING-04490.md) | Modelica.Mechanics.Translational.Examples.WhyArrows | `mass1.m` |
| [FINDING-04492](../false-positives/FINDING-04492.md) | Modelica.Mechanics.Translational.Examples.WhyArrows | `inertia2.m` |
| [FINDING-05001](../false-positives/FINDING-05001.md) | ModelicaTest.Rotational.TestSpeed | `mass1.m` |
| [FINDING-05002](../false-positives/FINDING-05002.md) | ModelicaTest.Rotational.TestSpeed | `mass2.m` |
| [FINDING-05011](../false-positives/FINDING-05011.md) | ModelicaTest.Rotational.TestMove | `slidingMass.m` |
| [FINDING-05023](../false-positives/FINDING-05023.md) | ModelicaTest.Translational.AllComponents | `slidingMass.m` |
| [FINDING-05025](../false-positives/FINDING-05025.md) | ModelicaTest.Translational.AllComponents | `slidingMass1.m` |
| [FINDING-05027](../false-positives/FINDING-05027.md) | ModelicaTest.Translational.AllComponents | `slidingMass2.m` |
| [FINDING-05029](../false-positives/FINDING-05029.md) | ModelicaTest.Translational.AllComponents | `slidingMass3.m` |
| [FINDING-05030](../false-positives/FINDING-05030.md) | ModelicaTest.Translational.AllComponents | `slidingMass4.m` |
| [FINDING-05031](../false-positives/FINDING-05031.md) | ModelicaTest.Translational.AllComponents | `slidingMass5.m` |
| [FINDING-05032](../false-positives/FINDING-05032.md) | ModelicaTest.Translational.AllComponents | `slidingMass6.m` |
| [FINDING-05033](../false-positives/FINDING-05033.md) | ModelicaTest.Translational.AllComponents | `slidingMass7.m` |
| [FINDING-05035](../false-positives/FINDING-05035.md) | ModelicaTest.Translational.TestBraking | `mass1.m` |
| [FINDING-05036](../false-positives/FINDING-05036.md) | ModelicaTest.Translational.TestBraking | `mass2.m` |
| [FINDING-05037](../false-positives/FINDING-05037.md) | ModelicaTest.Translational.TestBraking | `mass3.m` |
| [FINDING-05038](../false-positives/FINDING-05038.md) | ModelicaTest.Translational.TestBraking | `mass4.m` |
| [FINDING-05039](../false-positives/FINDING-05039.md) | ModelicaTest.Translational.TestBraking | `mass5.m` |
| [FINDING-05041](../false-positives/FINDING-05041.md) | ModelicaTest.Translational.TestBraking | `mass6.m` |
| [FINDING-05055](../false-positives/FINDING-05055.md) | ModelicaTest.Translational.Vehicles | `vehicleDrag.mass.m` |
| [FINDING-05061](../false-positives/FINDING-05061.md) | ModelicaTest.Translational.Vehicles | `vehicleDragInConst.mass.m` |
| [FINDING-05067](../false-positives/FINDING-05067.md) | ModelicaTest.Translational.Vehicles | `vehicleDragInVar.mass.m` |
| [FINDING-05072](../false-positives/FINDING-05072.md) | ModelicaTest.Translational.Vehicles | `vehicleRoll.mass.m` |
| [FINDING-05077](../false-positives/FINDING-05077.md) | ModelicaTest.Translational.Vehicles | `vehicleRollInConst.mass.m` |
| [FINDING-05082](../false-positives/FINDING-05082.md) | ModelicaTest.Translational.Vehicles | `vehicleRollInVar.mass.m` |
| [FINDING-05087](../false-positives/FINDING-05087.md) | ModelicaTest.Translational.Vehicles | `vehicleInclination.mass.m` |
| [FINDING-05092](../false-positives/FINDING-05092.md) | ModelicaTest.Translational.Vehicles | `vehicleInclinationInConst.mass.m` |
| [FINDING-05097](../false-positives/FINDING-05097.md) | ModelicaTest.Translational.Vehicles | `vehicleInclinationInVar.mass.m` |
