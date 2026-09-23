# FINDING-05088: Vehicle parameter has a multiplicative zero limit

| Field | Value |
|---|---|
| Verdict | false-positives |
| Scope / group | vehicle-zero-idealization |
| Model | ModelicaTest.Translational.Vehicles |
| Target | vehicleInclinationInConst.m |
| Student classification | physical-bound-permits-zero |
| Original report | [FINDING-vehicles-vehicleinclinationinconst-m-zerolimit.md](../../v2/bugs/FINDING-vehicles-vehicleinclinationinconst-m-zerolimit.md) — reviewed as `FINDING-05088-vehicles-vehicleinclinationinconst-m.md`, which a later run renamed |
| Original SHA-256 | 59614ae11eb146a7603e55a6c10758d6da7f1017c5967ed5e66e603b0964eaf5 |

## Why this is a false positive

m is passed to Translational.Mass and used in force balance. At zero it removes that inertia or aerodynamic term; the Vehicle source does not divide by it. A physical production vehicle has positive values, but this component also supports idealized/lumped configurations, so a blanket strictly-positive sanitizer finding is not a verified bug.

## Source evidence

Compiler/source-resolved declaration: `Mechanics/Translational/Components/Vehicle.mo:3`. Role: `parameter`; binding: `1200`; effective min: `0`; effective max: `None`. 

[Mechanics/Translational/Components/Vehicle.mo — source snapshot](../evidence/sources/037334fdb7d77239-Vehicle.mo)

```modelica
1: within Modelica.Mechanics.Translational.Components;
2: model Vehicle "Simple vehicle model"
3:   parameter SI.Mass m "Total mass of vehicle";
4:   parameter SI.Acceleration g=Modelica.Constants.g_n "Constant gravity acceleration";
5:   parameter SI.Inertia J "Total rotational inertia of drive train";
6:   parameter SI.Length R "Wheel radius";
```

[Mechanics/Translational/Components/Vehicle.mo — source snapshot](../evidence/sources/037334fdb7d77239-Vehicle.mo)

```modelica
2: model Vehicle "Simple vehicle model"
3:   parameter SI.Mass m "Total mass of vehicle";
4:   parameter SI.Acceleration g=Modelica.Constants.g_n "Constant gravity acceleration";
5:   parameter SI.Inertia J "Total rotational inertia of drive train";
6:   parameter SI.Length R "Wheel radius";
7:   parameter SI.Area A(start=1) "Cross section of vehicle"
8:     annotation(Dialog(tab="Driving resistances", group="Drag resistance"));
9:   parameter Real Cd(start=0.5) "Drag resistance coefficient"
10:     annotation(Dialog(tab="Driving resistances", group="Drag resistance"));
11:   parameter SI.Density rho=1.2 "Density of air"
12:     annotation(Dialog(tab="Driving resistances", group="Drag resistance"));
13:   parameter Boolean useWindInput=false "Enable signal input for wind velocity"
14:     annotation(Dialog(tab="Driving resistances", group="Drag resistance"));
15:   parameter SI.Velocity vWindConstant=0 "Constant wind velocity"
16:     annotation(Dialog(tab="Driving resistances", group="Drag resistance", enable=not useWindInput));
17:   parameter Boolean useCrInput=false "Enable signal input for Cr"
18:     annotation(Dialog(tab="Driving resistances", group="Rolling resistance"));
19:   parameter Real CrConstant=0.015 "Constant rolling resistance coefficient"
20:     annotation(Dialog(tab="Driving resistances", group="Rolling resistance", enable=not useCrInput));
21:   parameter SI.Velocity vReg=1e-3 "Velocity for regularization around 0"
22:     annotation(Dialog(tab="Driving resistances", group="Rolling resistance"));
23:   parameter Boolean useInclinationInput=false "Enable signal input for inclination"
24:     annotation(Dialog(tab="Driving resistances", group="Inclination resistance"));
25:   parameter Real inclinationConstant=0 "Constant inclination = tan(angle)"
26:     annotation(Dialog(tab="Driving resistances", group="Inclination resistance", enable=not useInclinationInput));
27:   SI.Position s(displayUnit="km", start=0)=mass.s "Position of vehicle";
28:   SI.Velocity v(displayUnit="km/h", start=0)=mass.v "Velocity of vehicle";
29:   SI.Acceleration a=mass.a "Acceleration of vehicle";
30: protected
31:   constant SI.Velocity vRef=1 "Reference velocity for air drag";
32: public
33:   Sources.QuadraticSpeedDependentForce fDrag(
34:     final useSupport=true,
35:     final f_nominal=-Cd*A*rho*vRef^2/2,
36:     final ForceDirection=false,
```


## Execution evidence

[Rumoca commands, return codes, integrity hashes, bounded output and metadata](../evidence/e1997bd33cf0ed7f.json). Baseline: **tool-error**.

No independent runtime override was executed for this target in this audit; this is not a pass.

## Recommended action

Correct the detector/adjudicator for this specific semantic case; do not impose a blanket strictly-positive bound on the library declaration.

## Scope and limitations

A source-level verdict addresses the reported declaration/claim, not every possible connected system. Tests cover 0–0.5 seconds and are not a proof of long-run stability. Shared instances are not distinct root causes. A missing bound, timeout, compiler error or failed nominal run alone never counts as a verified bug or a false positive. Fixes are proposals; no library/compiler implementation was changed.

[Group and related reports](../groups/vehicle-zero-idealization.md) · [Index](../README.md)
