# Zero medium specific heat capacity enters an unguarded division

Group `fluid-medium-cp` · 23 report instances · confirmed

The Medium record gives cp no strictly-positive bound or assertion. FluidHeatFlow.BaseClasses.TwoPort evaluates T_a=flowPort_a.h/medium.cp and T_b=flowPort_b.h/medium.cp. Therefore zero is admitted by the material record and makes the common consumer undefined. The report instances share this declaration-level defect; nominal models blocked in the current Rumoca runtime are not falsely described as independently simulated.

Require and validate medium.cp>0 at the medium/TwoPort contract, and guard evaluation so an actionable material-domain error occurs before division. Prefer a reusable medium-property validation function or assertion; do not clamp a nonphysical zero to epsilon.

Read the per-report evidence: members can share a declaration while having different runtime outcomes. Source-proof reuse is not a claim that every instance was independently simulated.

| ID | Model | Target |
|---|---|---|
| [DECL-0890](../confirmed/DECL-0890.md) | — | `cp` |
| [FINDING-01256](../confirmed/FINDING-01256.md) | Modelica.Electrical.Machines.Examples.DCMachines.DCPM_Cooling | `inlet.medium.cp` |
| [FINDING-01258](../confirmed/FINDING-01258.md) | Modelica.Electrical.Machines.Examples.DCMachines.DCPM_Cooling | `volumeFlow.medium.cp` |
| [FINDING-01260](../confirmed/FINDING-01260.md) | Modelica.Electrical.Machines.Examples.DCMachines.DCPM_Cooling | `cooling.medium.cp` |
| [FINDING-01261](../confirmed/FINDING-01261.md) | Modelica.Electrical.Machines.Examples.DCMachines.DCPM_Cooling | `outlet.medium.cp` |
| [FINDING-04523](../confirmed/FINDING-04523.md) | Modelica.Thermal.FluidHeatFlow.Examples.IndirectCooling | `outerMedium.cp` |
| [FINDING-04526](../confirmed/FINDING-04526.md) | Modelica.Thermal.FluidHeatFlow.Examples.IndirectCooling | `innerMedium.cp` |
| [FINDING-04545](../confirmed/FINDING-04545.md) | Modelica.Thermal.FluidHeatFlow.Examples.OneMass | `medium.cp` |
| [FINDING-04571](../confirmed/FINDING-04571.md) | Modelica.Thermal.FluidHeatFlow.Examples.ParallelCooling | `medium.cp` |
| [FINDING-04599](../confirmed/FINDING-04599.md) | Modelica.Thermal.FluidHeatFlow.Examples.ParallelPumpDropOut | `medium.cp` |
| [FINDING-04623](../confirmed/FINDING-04623.md) | Modelica.Thermal.FluidHeatFlow.Examples.PumpAndValve | `medium.cp` |
| [FINDING-04645](../confirmed/FINDING-04645.md) | Modelica.Thermal.FluidHeatFlow.Examples.PumpDropOut | `medium.cp` |
| [FINDING-04662](../confirmed/FINDING-04662.md) | Modelica.Thermal.FluidHeatFlow.Examples.SimpleCooling | `medium.cp` |
| [FINDING-04690](../confirmed/FINDING-04690.md) | Modelica.Thermal.FluidHeatFlow.Examples.TwoMass | `medium.cp` |
| [FINDING-04705](../confirmed/FINDING-04705.md) | Modelica.Thermal.FluidHeatFlow.Examples.TwoTanks | `openTank1.medium.cp` |
| [FINDING-04707](../confirmed/FINDING-04707.md) | Modelica.Thermal.FluidHeatFlow.Examples.TwoTanks | `openTank2.medium.cp` |
| [FINDING-04710](../confirmed/FINDING-04710.md) | Modelica.Thermal.FluidHeatFlow.Examples.TwoTanks | `pipe.medium.cp` |
| [FINDING-04736](../confirmed/FINDING-04736.md) | Modelica.Thermal.FluidHeatFlow.Examples.WaterPump | `ambient1.medium.cp` |
| [FINDING-04738](../confirmed/FINDING-04738.md) | Modelica.Thermal.FluidHeatFlow.Examples.WaterPump | `idealPump.medium.cp` |
| [FINDING-04741](../confirmed/FINDING-04741.md) | Modelica.Thermal.FluidHeatFlow.Examples.WaterPump | `volumeFlowSensor.medium.cp` |
| [FINDING-04743](../confirmed/FINDING-04743.md) | Modelica.Thermal.FluidHeatFlow.Examples.WaterPump | `oneWayValve.medium.cp` |
| [FINDING-04747](../confirmed/FINDING-04747.md) | Modelica.Thermal.FluidHeatFlow.Examples.WaterPump | `pipe.medium.cp` |
| [FINDING-04748](../confirmed/FINDING-04748.md) | Modelica.Thermal.FluidHeatFlow.Examples.WaterPump | `ambient2.medium.cp` |
