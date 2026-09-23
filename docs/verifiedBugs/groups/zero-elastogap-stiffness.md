# Zero ElastoGap stiffness is handled without division

Group `zero-elastogap-stiffness` · 21 report instances · false-positives

c has min=0 and only forms f_ref=c*s_ref. The normalization divides by the separately positive s_ref, not by c; at c=0 the contact spring force is zero and the limiter keeps damping force within that zero spring force. The reported strict-positivity rule confuses a multiplier with a divisor.

Correct the detector/adjudicator for this specific semantic case; do not impose a blanket strictly-positive bound on the library declaration.

Read the per-report evidence: members can share a declaration while having different runtime outcomes. Source-proof reuse is not a claim that every instance was independently simulated.

| ID | Model | Target |
|---|---|---|
| [FINDING-03770](../false-positives/FINDING-03770.md) | Modelica.Magnetic.FluxTubes.Examples.MovingCoilActuator.ArmatureStroke | `pmActuator.armature.stopper_xMax.c` |
| [FINDING-03771](../false-positives/FINDING-03771.md) | Modelica.Magnetic.FluxTubes.Examples.MovingCoilActuator.ArmatureStroke | `pmActuator.armature.stopper_xMin.c` |
| [FINDING-03782](../false-positives/FINDING-03782.md) | Modelica.Magnetic.FluxTubes.Examples.MovingCoilActuator.ArmatureStroke | `cActuator.armature.stopper_xMax.c` |
| [FINDING-03783](../false-positives/FINDING-03783.md) | Modelica.Magnetic.FluxTubes.Examples.MovingCoilActuator.ArmatureStroke | `cActuator.armature.stopper_xMin.c` |
| [FINDING-03802](../false-positives/FINDING-03802.md) | Modelica.Magnetic.FluxTubes.Examples.MovingCoilActuator.Components.ConstantActuator | `armature.stopper_xMax.c` |
| [FINDING-03803](../false-positives/FINDING-03803.md) | Modelica.Magnetic.FluxTubes.Examples.MovingCoilActuator.Components.ConstantActuator | `armature.stopper_xMin.c` |
| [FINDING-03813](../false-positives/FINDING-03813.md) | Modelica.Magnetic.FluxTubes.Examples.MovingCoilActuator.Components.PermeanceActuator | `armature.stopper_xMax.c` |
| [FINDING-03814](../false-positives/FINDING-03814.md) | Modelica.Magnetic.FluxTubes.Examples.MovingCoilActuator.Components.PermeanceActuator | `armature.stopper_xMin.c` |
| [FINDING-03833](../false-positives/FINDING-03833.md) | Modelica.Magnetic.FluxTubes.Examples.SolenoidActuator.Components.AdvancedSolenoid | `armature.stopper_xMax.c` |
| [FINDING-03834](../false-positives/FINDING-03834.md) | Modelica.Magnetic.FluxTubes.Examples.SolenoidActuator.Components.AdvancedSolenoid | `armature.stopper_xMin.c` |
| [FINDING-03866](../false-positives/FINDING-03866.md) | Modelica.Magnetic.FluxTubes.Examples.SolenoidActuator.Components.SimpleSolenoid | `armature.stopper_xMax.c` |
| [FINDING-03867](../false-positives/FINDING-03867.md) | Modelica.Magnetic.FluxTubes.Examples.SolenoidActuator.Components.SimpleSolenoid | `armature.stopper_xMin.c` |
| [FINDING-03889](../false-positives/FINDING-03889.md) | Modelica.Magnetic.FluxTubes.Examples.Utilities.TranslatoryArmatureAndStopper | `stopper_xMax.c` |
| [FINDING-03890](../false-positives/FINDING-03890.md) | Modelica.Magnetic.FluxTubes.Examples.Utilities.TranslatoryArmatureAndStopper | `stopper_xMin.c` |
| [FINDING-04438](../false-positives/FINDING-04438.md) | Modelica.Mechanics.Translational.Examples.ElastoGap | `elastoGap1.c` |
| [FINDING-04439](../false-positives/FINDING-04439.md) | Modelica.Mechanics.Translational.Examples.ElastoGap | `elastoGap2.c` |
| [FINDING-04467](../false-positives/FINDING-04467.md) | Modelica.Mechanics.Translational.Examples.PreLoad | `innerContactA.c` |
| [FINDING-04468](../false-positives/FINDING-04468.md) | Modelica.Mechanics.Translational.Examples.PreLoad | `innerContactB.c` |
| [FINDING-04473](../false-positives/FINDING-04473.md) | Modelica.Mechanics.Translational.Examples.PreLoad | `outerContactA.c` |
| [FINDING-04474](../false-positives/FINDING-04474.md) | Modelica.Mechanics.Translational.Examples.PreLoad | `outerContactB.c` |
| [FINDING-05028](../false-positives/FINDING-05028.md) | ModelicaTest.Translational.AllComponents | `elastoGap.c` |
