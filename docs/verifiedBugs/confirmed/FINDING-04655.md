# FINDING-04655: Zero medium density enters an unguarded division

| Field | Value |
|---|---|
| Verdict | confirmed |
| Scope / group | fluid-medium-rho |
| Model | Modelica.Thermal.FluidHeatFlow.Examples.SimpleCooling |
| Target | pipe.medium.rho |
| Student classification | physical-bound-permits-zero |
| Original report | [FINDING-simplecooling-pipe-medium-rho-intent.md](../../v2/bugs/FINDING-simplecooling-pipe-medium-rho-intent.md) — reviewed as `FINDING-04655-simplecooling-pipe-medium-rho.md`, which a later run renamed |
| Original SHA-256 | 1e8de1bd2bdcefc8a9e56fd2df114971845524989e3ffe442f3d523c8f08ce55 |

## Verification and root cause

The Medium record gives rho no strictly-positive bound or assertion. FluidHeatFlow.BaseClasses.TwoPort evaluates V_flow=flowPort_a.m_flow/medium.rho. Therefore zero is admitted by the material record and makes the common consumer undefined. The report instances share this declaration-level defect; nominal models blocked in the current Rumoca runtime are not falsely described as independently simulated.

## Source evidence

Compiler/source-resolved declaration: `Thermal/FluidHeatFlow/Media/Medium.mo:4`. Role: `parameter`; binding: `medium.rho`; effective min: `0.0`; effective max: `None`. 

[Thermal/FluidHeatFlow/Media/Medium.mo — source snapshot](../evidence/sources/9758e96ec7e20ef4-Medium.mo)

```modelica
2: record Medium "Record containing media properties"
3:   extends Modelica.Icons.Record;
4:   parameter SI.Density rho = 1 "Density";
5:   parameter SI.SpecificHeatCapacity cp = 1
6:     "Specific heat capacity at constant pressure";
7:   parameter SI.SpecificHeatCapacity cv = 1
```

[Thermal/FluidHeatFlow/Media/Medium.mo — source snapshot](../evidence/sources/9758e96ec7e20ef4-Medium.mo)

```modelica
2: record Medium "Record containing media properties"
3:   extends Modelica.Icons.Record;
4:   parameter SI.Density rho = 1 "Density";
5:   parameter SI.SpecificHeatCapacity cp = 1
6:     "Specific heat capacity at constant pressure";
7:   parameter SI.SpecificHeatCapacity cv = 1
8:     "Specific heat capacity at constant volume";
9:   parameter SI.ThermalConductivity lambda = 1
10:     "Thermal conductivity";
11:   parameter SI.KinematicViscosity nu = 1
12:     "Kinematic viscosity";
```

[Thermal/FluidHeatFlow/BaseClasses/TwoPort.mo — source snapshot](../evidence/sources/04f0a49d716ce1bd-TwoPort.mo)

```modelica
29:     annotation (Placement(transformation(extent={{-110,-10},{-90,10}})));
30:   FluidHeatFlow.Interfaces.FlowPort_b flowPort_b(final medium=medium)
31:     annotation (Placement(transformation(extent={{90,-10},{110,10}})));
32: equation
33:   dp=flowPort_a.p - flowPort_b.p;
34:   V_flow=flowPort_a.m_flow/medium.rho;
35:   T_a=flowPort_a.h/medium.cp;
36:   T_b=flowPort_b.h/medium.cp;
37:   dT=if noEvent(V_flow>=0) then T-T_a else T_b-T;
38:   h = medium.cp*T;
39:   T_q = T  - noEvent(sign(V_flow))*(1 - tapT)*dT;
40:   // mass balance
41:   flowPort_a.m_flow + flowPort_b.m_flow = 0;
42:   // energy balance
```


## Execution evidence

[Rumoca commands, return codes, integrity hashes, bounded output and metadata](../evidence/6d3b81c4641884a5.json). Baseline: **clean**.

| Probe | Outcome |
|---|---|
| `pipe.medium.rho=0` | clean |

## Proposed fix

Require and validate medium.rho>0 at the medium/TwoPort contract, and guard evaluation so an actionable material-domain error occurs before division. Prefer a reusable medium-property validation function or assertion; do not clamp a nonphysical zero to epsilon.

## Fix validation

Test the default medium, zero and negative rho, and a small positive value in a minimal TwoPort descendant. Both flow directions must retain finite temperature/volume-flow calculations.

## Scope and limitations

A source-level verdict addresses the reported declaration/claim, not every possible connected system. Tests cover 0–0.5 seconds and are not a proof of long-run stability. Shared instances are not distinct root causes. A missing bound, timeout, compiler error or failed nominal run alone never counts as a verified bug or a false positive. Fixes are proposals; no library/compiler implementation was changed.

[Group and related reports](../groups/fluid-medium-rho.md) · [Index](../README.md)
