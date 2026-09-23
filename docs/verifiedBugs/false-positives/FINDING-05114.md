# FINDING-05114: vRef is a protected nonzero constant

| Field | Value |
|---|---|
| Verdict | false-positives |
| Scope / group | fixed-vehicle-reference-speed |
| Model | ModelicaTest.Translational.Vehicles |
| Target | vehicleInclinationInVar.vRef |
| Student classification | divisor-reachable-zero |
| Original report | `FINDING-05114-vehicles-vehicleinclinationinvar-vref.md` — [withdrawn](../../v2/bugs/withdrawn.md); a later run no longer makes this claim |
| Original SHA-256 | 7c187336dfdf1f60c02d189ee6f3b58f9010517b62a9e50915665d72ba1e3f71 |

## Why this is a false positive

Vehicle declares protected constant SI.Velocity vRef=1. It is an immutable unit/reference scale passed into the drag component and cannot reach zero through model parameter modification. The report lost constant/protected role information.

## Source evidence

Compiler/source-resolved declaration: `Mechanics/Translational/Components/Vehicle.mo:31`. Role: `constant`; binding: `1`; effective min: `None`; effective max: `None`. 

[Mechanics/Translational/Components/Vehicle.mo — source snapshot](../evidence/sources/037334fdb7d77239-Vehicle.mo)

```modelica
29:   SI.Acceleration a=mass.a "Acceleration of vehicle";
30: protected
31:   constant SI.Velocity vRef=1 "Reference velocity for air drag";
32: public
33:   Sources.QuadraticSpeedDependentForce fDrag(
34:     final useSupport=true,
```

[Mechanics/Translational/Components/Vehicle.mo — source snapshot](../evidence/sources/037334fdb7d77239-Vehicle.mo)

```modelica
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
37:     final v_nominal=vRef) "Drag resistance"
```


## Execution evidence

[Rumoca commands, return codes, integrity hashes, bounded output and metadata](../evidence/e1997bd33cf0ed7f.json). Baseline: **tool-error**.

No independent runtime override was executed for this target in this audit; this is not a pass.

## Recommended action

Correct the detector/adjudicator for this specific semantic case; do not impose a blanket strictly-positive bound on the library declaration.

## Scope and limitations

A source-level verdict addresses the reported declaration/claim, not every possible connected system. Tests cover 0–0.5 seconds and are not a proof of long-run stability. Shared instances are not distinct root causes. A missing bound, timeout, compiler error or failed nominal run alone never counts as a verified bug or a false positive. Fixes are proposals; no library/compiler implementation was changed.

[Group and related reports](../groups/fixed-vehicle-reference-speed.md) · [Index](../README.md)
