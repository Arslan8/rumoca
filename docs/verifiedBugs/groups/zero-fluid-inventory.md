# Zero stored fluid mass is explicitly supported

Group `zero-fluid-inventory` · 33 report instances · false-positives

TwoPort explicitly documents that m=0 neglects the temperature transient. Its equation uses if m>small then m*medium.cv*der(T) else an algebraic zero-storage energy balance. Zero is handled by a dedicated branch; a blanket strictly-positive mass rule is contrary to the component contract.

Correct the detector/adjudicator for this specific semantic case; do not impose a blanket strictly-positive bound on the library declaration.

Read the per-report evidence: members can share a declaration while having different runtime outcomes. Source-proof reuse is not a claim that every instance was independently simulated.

| ID | Model | Target |
|---|---|---|
| [FINDING-01243](../false-positives/FINDING-01243.md) | Modelica.Electrical.Machines.Examples.DCMachines.DCPM_Cooling | `volumeFlow.m` |
| [FINDING-01247](../false-positives/FINDING-01247.md) | Modelica.Electrical.Machines.Examples.DCMachines.DCPM_Cooling | `cooling.m` |
| [FINDING-04498](../false-positives/FINDING-04498.md) | Modelica.Thermal.FluidHeatFlow.Examples.IndirectCooling | `outerPump.m` |
| [FINDING-04506](../false-positives/FINDING-04506.md) | Modelica.Thermal.FluidHeatFlow.Examples.IndirectCooling | `pipe1.m` |
| [FINDING-04512](../false-positives/FINDING-04512.md) | Modelica.Thermal.FluidHeatFlow.Examples.IndirectCooling | `innerPump.m` |
| [FINDING-04516](../false-positives/FINDING-04516.md) | Modelica.Thermal.FluidHeatFlow.Examples.IndirectCooling | `outerPipe.m` |
| [FINDING-04520](../false-positives/FINDING-04520.md) | Modelica.Thermal.FluidHeatFlow.Examples.IndirectCooling | `innerPipe.m` |
| [FINDING-04534](../false-positives/FINDING-04534.md) | Modelica.Thermal.FluidHeatFlow.Examples.OneMass | `pump.m` |
| [FINDING-04538](../false-positives/FINDING-04538.md) | Modelica.Thermal.FluidHeatFlow.Examples.OneMass | `pipe.m` |
| [FINDING-04552](../false-positives/FINDING-04552.md) | Modelica.Thermal.FluidHeatFlow.Examples.ParallelCooling | `pump.m` |
| [FINDING-04556](../false-positives/FINDING-04556.md) | Modelica.Thermal.FluidHeatFlow.Examples.ParallelCooling | `pipe1.m` |
| [FINDING-04560](../false-positives/FINDING-04560.md) | Modelica.Thermal.FluidHeatFlow.Examples.ParallelCooling | `pipe2.m` |
| [FINDING-04564](../false-positives/FINDING-04564.md) | Modelica.Thermal.FluidHeatFlow.Examples.ParallelCooling | `pipe3.m` |
| [FINDING-04580](../false-positives/FINDING-04580.md) | Modelica.Thermal.FluidHeatFlow.Examples.ParallelPumpDropOut | `pump.m` |
| [FINDING-04584](../false-positives/FINDING-04584.md) | Modelica.Thermal.FluidHeatFlow.Examples.ParallelPumpDropOut | `pipe1.m` |
| [FINDING-04588](../false-positives/FINDING-04588.md) | Modelica.Thermal.FluidHeatFlow.Examples.ParallelPumpDropOut | `pipe2.m` |
| [FINDING-04592](../false-positives/FINDING-04592.md) | Modelica.Thermal.FluidHeatFlow.Examples.ParallelPumpDropOut | `pipe3.m` |
| [FINDING-04608](../false-positives/FINDING-04608.md) | Modelica.Thermal.FluidHeatFlow.Examples.PumpAndValve | `idealPump.m` |
| [FINDING-04612](../false-positives/FINDING-04612.md) | Modelica.Thermal.FluidHeatFlow.Examples.PumpAndValve | `valve.m` |
| [FINDING-04617](../false-positives/FINDING-04617.md) | Modelica.Thermal.FluidHeatFlow.Examples.PumpAndValve | `pipe.m` |
| [FINDING-04635](../false-positives/FINDING-04635.md) | Modelica.Thermal.FluidHeatFlow.Examples.PumpDropOut | `pump.m` |
| [FINDING-04639](../false-positives/FINDING-04639.md) | Modelica.Thermal.FluidHeatFlow.Examples.PumpDropOut | `pipe.m` |
| [FINDING-04652](../false-positives/FINDING-04652.md) | Modelica.Thermal.FluidHeatFlow.Examples.SimpleCooling | `pump.m` |
| [FINDING-04656](../false-positives/FINDING-04656.md) | Modelica.Thermal.FluidHeatFlow.Examples.SimpleCooling | `pipe.m` |
| [FINDING-04669](../false-positives/FINDING-04669.md) | Modelica.Thermal.FluidHeatFlow.Examples.TwoMass | `pump.m` |
| [FINDING-04673](../false-positives/FINDING-04673.md) | Modelica.Thermal.FluidHeatFlow.Examples.TwoMass | `pipe1.m` |
| [FINDING-04677](../false-positives/FINDING-04677.md) | Modelica.Thermal.FluidHeatFlow.Examples.TwoMass | `pipe2.m` |
| [FINDING-04681](../false-positives/FINDING-04681.md) | Modelica.Thermal.FluidHeatFlow.Examples.TwoMass | `pipe3.m` |
| [FINDING-04702](../false-positives/FINDING-04702.md) | Modelica.Thermal.FluidHeatFlow.Examples.TwoTanks | `pipe.m` |
| [FINDING-04715](../false-positives/FINDING-04715.md) | Modelica.Thermal.FluidHeatFlow.Examples.WaterPump | `idealPump.m` |
| [FINDING-04719](../false-positives/FINDING-04719.md) | Modelica.Thermal.FluidHeatFlow.Examples.WaterPump | `volumeFlowSensor.m` |
| [FINDING-04725](../false-positives/FINDING-04725.md) | Modelica.Thermal.FluidHeatFlow.Examples.WaterPump | `oneWayValve.m` |
| [FINDING-04729](../false-positives/FINDING-04729.md) | Modelica.Thermal.FluidHeatFlow.Examples.WaterPump | `pipe.m` |
