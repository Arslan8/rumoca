# Zero heat capacity is a no-storage algebraic limit

Group `zero-heat-capacity` · 31 report instances · false-positives

The source equation is C*der(T)=port.Q_flow, not division by C. At C=0 it imposes zero stored heat flow and removes the temperature state. Thus the missing/zero-bound claim does not by itself prove a defect; fixed starts or isolated thermal topologies may still become inconsistent. The two divisor-reach reports for this declaration remain unresolved separately because they make a different compiler-IR claim.

Correct the detector/adjudicator for this specific semantic case; do not impose a blanket strictly-positive bound on the library declaration.

Read the per-report evidence: members can share a declaration while having different runtime outcomes. Source-proof reuse is not a claim that every instance was independently simulated.

| ID | Model | Target |
|---|---|---|
| [DECL-0095](../false-positives/DECL-0095.md) | — | `C` |
| [FINDING-00264](../false-positives/FINDING-00264.md) | Modelica.Electrical.Analog.Examples.HeatingMOSInverter | `HeatCapacitor1.C` |
| [FINDING-00280](../false-positives/FINDING-00280.md) | Modelica.Electrical.Analog.Examples.HeatingNPN_NORGate | `HeatCapacitor1.C` |
| [FINDING-00312](../false-positives/FINDING-00312.md) | Modelica.Electrical.Analog.Examples.HeatingPNP_NORGate | `HeatCapacitor1.C` |
| [FINDING-00345](../false-positives/FINDING-00345.md) | Modelica.Electrical.Analog.Examples.HeatingRectifier | `HeatCapacitor1.C` |
| [FINDING-01236](../false-positives/FINDING-01236.md) | Modelica.Electrical.Machines.Examples.DCMachines.DCPM_Cooling | `armature.C` |
| [FINDING-01238](../false-positives/FINDING-01238.md) | Modelica.Electrical.Machines.Examples.DCMachines.DCPM_Cooling | `core.C` |
| [FINDING-04383](../false-positives/FINDING-04383.md) | Modelica.Mechanics.Rotational.Examples.EddyCurrentBrake | `heatCapacitor.C` |
| [FINDING-04431](../false-positives/FINDING-04431.md) | Modelica.Mechanics.Translational.Examples.EddyCurrentBrake | `heatCapacitor.C` |
| [FINDING-04504](../false-positives/FINDING-04504.md) | Modelica.Thermal.FluidHeatFlow.Examples.IndirectCooling | `heatCapacitor.C` |
| [FINDING-04543](../false-positives/FINDING-04543.md) | Modelica.Thermal.FluidHeatFlow.Examples.OneMass | `heatCapacitor.C` |
| [FINDING-04569](../false-positives/FINDING-04569.md) | Modelica.Thermal.FluidHeatFlow.Examples.ParallelCooling | `heatCapacitor1.C` |
| [FINDING-04570](../false-positives/FINDING-04570.md) | Modelica.Thermal.FluidHeatFlow.Examples.ParallelCooling | `heatCapacitor2.C` |
| [FINDING-04597](../false-positives/FINDING-04597.md) | Modelica.Thermal.FluidHeatFlow.Examples.ParallelPumpDropOut | `heatCapacitor1.C` |
| [FINDING-04598](../false-positives/FINDING-04598.md) | Modelica.Thermal.FluidHeatFlow.Examples.ParallelPumpDropOut | `heatCapacitor2.C` |
| [FINDING-04622](../false-positives/FINDING-04622.md) | Modelica.Thermal.FluidHeatFlow.Examples.PumpAndValve | `heatCapacitor.C` |
| [FINDING-04644](../false-positives/FINDING-04644.md) | Modelica.Thermal.FluidHeatFlow.Examples.PumpDropOut | `heatCapacitor.C` |
| [FINDING-04661](../false-positives/FINDING-04661.md) | Modelica.Thermal.FluidHeatFlow.Examples.SimpleCooling | `heatCapacitor.C` |
| [FINDING-04686](../false-positives/FINDING-04686.md) | Modelica.Thermal.FluidHeatFlow.Examples.TwoMass | `heatCapacitor1.C` |
| [FINDING-04688](../false-positives/FINDING-04688.md) | Modelica.Thermal.FluidHeatFlow.Examples.TwoMass | `heatCapacitor2.C` |
| [FINDING-04750](../false-positives/FINDING-04750.md) | Modelica.Thermal.HeatTransfer.Examples.ControlledTemperature | `heatCapacitor.C` |
| [FINDING-04756](../false-positives/FINDING-04756.md) | Modelica.Thermal.HeatTransfer.Examples.GenerationOfFMUs | `directCapacity.heatCapacitor.C` |
| [FINDING-04758](../false-positives/FINDING-04758.md) | Modelica.Thermal.HeatTransfer.Examples.GenerationOfFMUs | `inverseCapacity.mass.C` |
| [FINDING-04761](../false-positives/FINDING-04761.md) | Modelica.Thermal.HeatTransfer.Examples.GenerationOfFMUs | `capacitor3a.C` |
| [FINDING-04762](../false-positives/FINDING-04762.md) | Modelica.Thermal.HeatTransfer.Examples.GenerationOfFMUs | `capacitor3b.C` |
| [FINDING-04763](../false-positives/FINDING-04763.md) | Modelica.Thermal.HeatTransfer.Examples.TwoMasses | `mass1.C` |
| [FINDING-04764](../false-positives/FINDING-04764.md) | Modelica.Thermal.HeatTransfer.Examples.TwoMasses | `mass2.C` |
| [FINDING-04771](../false-positives/FINDING-04771.md) | Modelica.Thermal.HeatTransfer.Examples.Utilities.DirectCapacity | `heatCapacitor.C` |
| [FINDING-04773](../false-positives/FINDING-04773.md) | Modelica.Thermal.HeatTransfer.Examples.Utilities.InverseCapacity | `mass.C` |
| [FINDING-05019](../false-positives/FINDING-05019.md) | ModelicaTest.Rotational.TestBraking | `heatCapacitor.C` |
| [FINDING-05040](../false-positives/FINDING-05040.md) | ModelicaTest.Translational.TestBraking | `heatCapacitor.C` |
