# FINDING-04116: PointMass permits a massless algebraic point

| Field | Value |
|---|---|
| Verdict | false-positives |
| Scope / group | zero-multibody-point-mass |
| Model | Modelica.Mechanics.MultiBody.Examples.Elementary.PointGravityWithPointMasses |
| Target | body2.m |
| Student classification | physical-bound-permits-zero |
| Original report | [FINDING-pointgravitywithpointmasses-body2-m-zerolimit.md](../../v2/bugs/FINDING-pointgravitywithpointmasses-body2-m-zerolimit.md) — reviewed as `FINDING-04116-pointgravitywithpointmasses-body2-m.md`, which a later run renamed |
| Original SHA-256 | 1008302938b47b7ad08f84e6205f845f5c6375bc57c6e274fd1752a0d8883962 |

## Why this is a false positive

PointMass declares m(min=0), and its force equation multiplies acceleration/gravity by m. At zero it becomes a force-balance/kinematic connection rather than dividing by mass. A surrounding free-state formulation may need different state selection, but the component declaration is not intrinsically invalid.

## Source evidence

Compiler/source-resolved declaration: `Mechanics/MultiBody/Parts/PointMass.mo:11`. Role: `parameter`; binding: `1`; effective min: `0`; effective max: `None`. 

[Mechanics/MultiBody/Parts/PointMass.mo — source snapshot](../evidence/sources/d51c87cb698a4e2c-PointMass.mo)

```modelica
9:   parameter Boolean animation=true
10:     "= true, if animation shall be enabled (show sphere)";
11:   parameter SI.Mass m(min=0) "Mass of mass point";
12:   input SI.Diameter sphereDiameter=world.defaultBodyDiameter
13:     "Diameter of sphere" annotation (Dialog(
14:       tab="Animation",
```

[Mechanics/MultiBody/Parts/PointMass.mo — source snapshot](../evidence/sources/d51c87cb698a4e2c-PointMass.mo)

```modelica
2: model PointMass
3:   "Rigid body where body rotation and inertia tensor is neglected (6 potential states)"
4: 
5:   import Modelica.Mechanics.MultiBody.Types;
6:   Interfaces.Frame_a frame_a
7:     "Coordinate system fixed at center of mass point" annotation (Placement(
8:         transformation(extent={{-16,-16},{16,16}})));
9:   parameter Boolean animation=true
10:     "= true, if animation shall be enabled (show sphere)";
11:   parameter SI.Mass m(min=0) "Mass of mass point";
12:   input SI.Diameter sphereDiameter=world.defaultBodyDiameter
```

[Mechanics/MultiBody/Parts/PointMass.mo — source snapshot](../evidence/sources/d51c87cb698a4e2c-PointMass.mo)

```modelica
80: 
81:   // Newton equation: f = m*(a-g)
82:   r_0 = frame_a.r_0;
83:   v_0 = der(r_0);
84:   a_0 = der(v_0);
85:   frame_a.f = m*Frames.resolve2(frame_a.R, a_0 - world.gravityAcceleration(
86:     r_0));
87:   annotation (Icon(coordinateSystem(
88:         preserveAspectRatio=true,
89:         extent={{-100,-100},{100,100}}), graphics={
90:         Text(
```


## Execution evidence

[Rumoca commands, return codes, integrity hashes, bounded output and metadata](../evidence/3545c46140c559ad.json). Baseline: **tool-error**.

No independent runtime override was executed for this target in this audit; this is not a pass.

## Recommended action

Correct the detector/adjudicator for this specific semantic case; do not impose a blanket strictly-positive bound on the library declaration.

## Scope and limitations

A source-level verdict addresses the reported declaration/claim, not every possible connected system. Tests cover 0–0.5 seconds and are not a proof of long-run stability. Shared instances are not distinct root causes. A missing bound, timeout, compiler error or failed nominal run alone never counts as a verified bug or a false positive. Fixes are proposals; no library/compiler implementation was changed.

[Group and related reports](../groups/zero-multibody-point-mass.md) · [Index](../README.md)
