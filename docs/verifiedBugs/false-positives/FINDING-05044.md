# FINDING-05044: Zero effective drag area switches off aerodynamic drag

| Field | Value |
|---|---|
| Verdict | false-positives |
| Scope / group | disabled-drag |
| Model | ModelicaTest.Translational.Vehicles |
| Target | vehicleRoll.A |
| Student classification | physical-invariant-violated |
| Original report | [FINDING-vehicles-vehicleroll-a-zerolimit.md](../../v2/bugs/FINDING-vehicles-vehicleroll-a-zerolimit.md) — reviewed as `FINDING-05044-vehicles-vehicleroll-a.md`, which a later run renamed |
| Original SHA-256 | eb1d2589ace2464b18f320f381fb4255e7a9f18b1f2701c34c1addf95df5566f |

## Why this is a false positive

Here A enters f_nominal=-Cd*A*rho*vRef^2/2 as a multiplier; the speed normalization uses the separate protected vRef=1. A=0 is a no-aerodynamic-drag configuration, not a zero geometric divisor. The reported invariant is too broad for this effective coefficient.

## Source evidence

Compiler/source-resolved declaration: `Mechanics/Translational/Components/Vehicle.mo:7`. Role: `parameter`; binding: `0`; effective min: `None`; effective max: `None`. 

[Mechanics/Translational/Components/Vehicle.mo — source snapshot](../evidence/sources/037334fdb7d77239-Vehicle.mo)

```modelica
5:   parameter SI.Inertia J "Total rotational inertia of drive train";
6:   parameter SI.Length R "Wheel radius";
7:   parameter SI.Area A(start=1) "Cross section of vehicle"
8:     annotation(Dialog(tab="Driving resistances", group="Drag resistance"));
9:   parameter Real Cd(start=0.5) "Drag resistance coefficient"
10:     annotation(Dialog(tab="Driving resistances", group="Drag resistance"));
```

[Mechanics/Translational/Components/Vehicle.mo — source snapshot](../evidence/sources/037334fdb7d77239-Vehicle.mo)

```modelica
30: protected
31:   constant SI.Velocity vRef=1 "Reference velocity for air drag";
32: public
33:   Sources.QuadraticSpeedDependentForce fDrag(
34:     final useSupport=true,
35:     final f_nominal=-Cd*A*rho*vRef^2/2,
36:     final ForceDirection=false,
37:     final v_nominal=vRef) "Drag resistance"
```


## Execution evidence

[Rumoca commands, return codes, integrity hashes, bounded output and metadata](../evidence/e1997bd33cf0ed7f.json). Baseline: **tool-error**.

No independent runtime override was executed for this target in this audit; this is not a pass.

## Recommended action

Correct the detector/adjudicator for this specific semantic case; do not impose a blanket strictly-positive bound on the library declaration.

## Scope and limitations

A source-level verdict addresses the reported declaration/claim, not every possible connected system. Tests cover 0–0.5 seconds and are not a proof of long-run stability. Shared instances are not distinct root causes. A missing bound, timeout, compiler error or failed nominal run alone never counts as a verified bug or a false positive. Fixes are proposals; no library/compiler implementation was changed.

[Group and related reports](../groups/disabled-drag.md) · [Index](../README.md)
