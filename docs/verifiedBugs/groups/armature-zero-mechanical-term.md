# Armature example delegates to zero-capable mechanical terms

Group `armature-zero-mechanical-term` · 21 report instances · false-positives

m is passed to Translational.Mass, while c and d are passed to ElastoGap. Their source equations use mass, stiffness and damping multiplicatively; zero removes inertia/contact stiffness/damping rather than serving as a divisor. A stopper simulation may become underconstrained or physically unhelpful, but the blanket strictly-positive arithmetic claim is not established.

Correct the detector/adjudicator for this specific semantic case; do not impose a blanket strictly-positive bound on the library declaration.

Read the per-report evidence: members can share a declaration while having different runtime outcomes. Source-proof reuse is not a claim that every instance was independently simulated.

| ID | Model | Target |
|---|---|---|
| [FINDING-03766](../false-positives/FINDING-03766.md) | Modelica.Magnetic.FluxTubes.Examples.MovingCoilActuator.ArmatureStroke | `pmActuator.armature.m` |
| [FINDING-03767](../false-positives/FINDING-03767.md) | Modelica.Magnetic.FluxTubes.Examples.MovingCoilActuator.ArmatureStroke | `pmActuator.armature.c` |
| [FINDING-03768](../false-positives/FINDING-03768.md) | Modelica.Magnetic.FluxTubes.Examples.MovingCoilActuator.ArmatureStroke | `pmActuator.armature.d` |
| [FINDING-03778](../false-positives/FINDING-03778.md) | Modelica.Magnetic.FluxTubes.Examples.MovingCoilActuator.ArmatureStroke | `cActuator.armature.m` |
| [FINDING-03779](../false-positives/FINDING-03779.md) | Modelica.Magnetic.FluxTubes.Examples.MovingCoilActuator.ArmatureStroke | `cActuator.armature.c` |
| [FINDING-03780](../false-positives/FINDING-03780.md) | Modelica.Magnetic.FluxTubes.Examples.MovingCoilActuator.ArmatureStroke | `cActuator.armature.d` |
| [FINDING-03798](../false-positives/FINDING-03798.md) | Modelica.Magnetic.FluxTubes.Examples.MovingCoilActuator.Components.ConstantActuator | `armature.m` |
| [FINDING-03799](../false-positives/FINDING-03799.md) | Modelica.Magnetic.FluxTubes.Examples.MovingCoilActuator.Components.ConstantActuator | `armature.c` |
| [FINDING-03800](../false-positives/FINDING-03800.md) | Modelica.Magnetic.FluxTubes.Examples.MovingCoilActuator.Components.ConstantActuator | `armature.d` |
| [FINDING-03809](../false-positives/FINDING-03809.md) | Modelica.Magnetic.FluxTubes.Examples.MovingCoilActuator.Components.PermeanceActuator | `armature.m` |
| [FINDING-03810](../false-positives/FINDING-03810.md) | Modelica.Magnetic.FluxTubes.Examples.MovingCoilActuator.Components.PermeanceActuator | `armature.c` |
| [FINDING-03811](../false-positives/FINDING-03811.md) | Modelica.Magnetic.FluxTubes.Examples.MovingCoilActuator.Components.PermeanceActuator | `armature.d` |
| [FINDING-03829](../false-positives/FINDING-03829.md) | Modelica.Magnetic.FluxTubes.Examples.SolenoidActuator.Components.AdvancedSolenoid | `armature.m` |
| [FINDING-03830](../false-positives/FINDING-03830.md) | Modelica.Magnetic.FluxTubes.Examples.SolenoidActuator.Components.AdvancedSolenoid | `armature.c` |
| [FINDING-03831](../false-positives/FINDING-03831.md) | Modelica.Magnetic.FluxTubes.Examples.SolenoidActuator.Components.AdvancedSolenoid | `armature.d` |
| [FINDING-03862](../false-positives/FINDING-03862.md) | Modelica.Magnetic.FluxTubes.Examples.SolenoidActuator.Components.SimpleSolenoid | `armature.m` |
| [FINDING-03863](../false-positives/FINDING-03863.md) | Modelica.Magnetic.FluxTubes.Examples.SolenoidActuator.Components.SimpleSolenoid | `armature.c` |
| [FINDING-03864](../false-positives/FINDING-03864.md) | Modelica.Magnetic.FluxTubes.Examples.SolenoidActuator.Components.SimpleSolenoid | `armature.d` |
| [FINDING-03885](../false-positives/FINDING-03885.md) | Modelica.Magnetic.FluxTubes.Examples.Utilities.TranslatoryArmatureAndStopper | `m` |
| [FINDING-03886](../false-positives/FINDING-03886.md) | Modelica.Magnetic.FluxTubes.Examples.Utilities.TranslatoryArmatureAndStopper | `c` |
| [FINDING-03887](../false-positives/FINDING-03887.md) | Modelica.Magnetic.FluxTubes.Examples.Utilities.TranslatoryArmatureAndStopper | `d` |
