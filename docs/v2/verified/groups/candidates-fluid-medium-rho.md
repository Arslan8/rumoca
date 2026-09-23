# Static/source-supported candidates: `fluid-medium-rho`

**16 report instances**

[Back to Static/source-supported candidates](../candidates.md) · [Overview](../README.md)

## Common decision rule

The Medium record gives rho no strictly-positive bound or assertion. FluidHeatFlow.BaseClasses.TwoPort evaluates V_flow=flowPort_a.m_flow/medium.rho. Therefore zero is admitted by the material record and makes the common consumer undefined. The report instances share this declaration-level defect; nominal models blocked in the current Rumoca runtime are not falsely described as independently simulated.

## Reports

| ID | Model | Target | Independent evidence | Student report |
|---|---|---|---|---|
| [FINDING-01406](../candidate/FINDING-01406.md) | Modelica.Electrical.Machines.Examples.DCMachines.DCPM_Cooling | `volumeFlow.medium.rho` | OMC: `witness-executes-cleanly` | [FINDING-dcpm-cooling-volumeflow-medium-rho-bound.md](../../bugs/FINDING-dcpm-cooling-volumeflow-medium-rho-bound.md) |
| [FINDING-01410](../candidate/FINDING-01410.md) | Modelica.Electrical.Machines.Examples.DCMachines.DCPM_Cooling | `cooling.medium.rho` | OMC: `witness-executes-cleanly` | [FINDING-dcpm-cooling-cooling-medium-rho-bound.md](../../bugs/FINDING-dcpm-cooling-cooling-medium-rho-bound.md) |
| [FINDING-04756](../candidate/FINDING-04756.md) | Modelica.Thermal.FluidHeatFlow.Examples.IndirectCooling | `outerMedium.rho` | OMC: `witness-executes-cleanly` | [FINDING-indirectcooling-outermedium-rho-bound.md](../../bugs/FINDING-indirectcooling-outermedium-rho-bound.md) |
| [FINDING-04757](../candidate/FINDING-04757.md) | Modelica.Thermal.FluidHeatFlow.Examples.IndirectCooling | `innerMedium.rho` | OMC: `witness-executes-cleanly` | [FINDING-indirectcooling-innermedium-rho-bound.md](../../bugs/FINDING-indirectcooling-innermedium-rho-bound.md) |
| [FINDING-04810](../candidate/FINDING-04810.md) | Modelica.Thermal.FluidHeatFlow.Examples.OneMass | `medium.rho` | OMC: `witness-executes-cleanly` | [FINDING-onemass-medium-rho-bound.md](../../bugs/FINDING-onemass-medium-rho-bound.md) |
| [FINDING-04838](../candidate/FINDING-04838.md) | Modelica.Thermal.FluidHeatFlow.Examples.ParallelCooling | `medium.rho` | OMC: `witness-executes-cleanly` | [FINDING-parallelcooling-medium-rho-bound.md](../../bugs/FINDING-parallelcooling-medium-rho-bound.md) |
| [FINDING-04880](../candidate/FINDING-04880.md) | Modelica.Thermal.FluidHeatFlow.Examples.ParallelPumpDropOut | `medium.rho` | OMC: `witness-executes-cleanly` | [FINDING-parallelpumpdropout-medium-rho-bound.md](../../bugs/FINDING-parallelpumpdropout-medium-rho-bound.md) |
| [FINDING-04924](../candidate/FINDING-04924.md) | Modelica.Thermal.FluidHeatFlow.Examples.PumpAndValve | `medium.rho` | OMC: `witness-executes-cleanly` | [FINDING-pumpandvalve-medium-rho-bound.md](../../bugs/FINDING-pumpandvalve-medium-rho-bound.md) |
| [FINDING-04968](../candidate/FINDING-04968.md) | Modelica.Thermal.FluidHeatFlow.Examples.PumpDropOut | `medium.rho` | OMC: `witness-executes-cleanly` | [FINDING-pumpdropout-medium-rho-bound.md](../../bugs/FINDING-pumpdropout-medium-rho-bound.md) |
| [FINDING-04995](../candidate/FINDING-04995.md) | Modelica.Thermal.FluidHeatFlow.Examples.SimpleCooling | `medium.rho` | OMC: `witness-executes-cleanly` | [FINDING-simplecooling-medium-rho-bound.md](../../bugs/FINDING-simplecooling-medium-rho-bound.md) |
| [FINDING-05020](../candidate/FINDING-05020.md) | Modelica.Thermal.FluidHeatFlow.Examples.TwoMass | `medium.rho` | OMC: `witness-executes-cleanly` | [FINDING-twomass-medium-rho-bound.md](../../bugs/FINDING-twomass-medium-rho-bound.md) |
| [FINDING-05072](../candidate/FINDING-05072.md) | Modelica.Thermal.FluidHeatFlow.Examples.TwoTanks | `pipe.medium.rho` | OMC: `witness-executes-cleanly` | [FINDING-twotanks-pipe-medium-rho-bound.md](../../bugs/FINDING-twotanks-pipe-medium-rho-bound.md) |
| [FINDING-05090](../candidate/FINDING-05090.md) | Modelica.Thermal.FluidHeatFlow.Examples.WaterPump | `idealPump.medium.rho` | OMC: `witness-executes-cleanly` | [FINDING-waterpump-idealpump-medium-rho-bound.md](../../bugs/FINDING-waterpump-idealpump-medium-rho-bound.md) |
| [FINDING-05094](../candidate/FINDING-05094.md) | Modelica.Thermal.FluidHeatFlow.Examples.WaterPump | `volumeFlowSensor.medium.rho` | OMC: `witness-executes-cleanly` | [FINDING-waterpump-volumeflowsensor-medium-rho-bound.md](../../bugs/FINDING-waterpump-volumeflowsensor-medium-rho-bound.md) |
| [FINDING-05100](../candidate/FINDING-05100.md) | Modelica.Thermal.FluidHeatFlow.Examples.WaterPump | `oneWayValve.medium.rho` | OMC: `witness-executes-cleanly` | [FINDING-waterpump-onewayvalve-medium-rho-bound.md](../../bugs/FINDING-waterpump-onewayvalve-medium-rho-bound.md) |
| [FINDING-05104](../candidate/FINDING-05104.md) | Modelica.Thermal.FluidHeatFlow.Examples.WaterPump | `pipe.medium.rho` | OMC: `witness-executes-cleanly` | [FINDING-waterpump-pipe-medium-rho-bound.md](../../bugs/FINDING-waterpump-pipe-medium-rho-bound.md) |
