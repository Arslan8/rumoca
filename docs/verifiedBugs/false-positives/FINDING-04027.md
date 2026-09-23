# FINDING-04027: The line-force point mass is explicitly optional

| Field | Value |
|---|---|
| Verdict | false-positives |
| Scope / group | optional-line-force-mass |
| Model | Modelica.Mechanics.MultiBody.Examples.Elementary.InitSpringConstant |
| Target | spring.lineForce.m |
| Student classification | physical-bound-permits-zero |
| Original report | [FINDING-initspringconstant-spring-lineforce-m-zerolimit.md](../../v2/bugs/FINDING-initspringconstant-spring-lineforce-m-zerolimit.md) — reviewed as `FINDING-04027-initspringconstant-spring-lineforce-m.md`, which a later run renamed |
| Original SHA-256 | fef73bbe5de74a3f92ae9a8ec77bc3bd8131b109a4ef2dc020b7e8e03ecc5d61 |

## Why this is a false positive

The parameter is declared m(min=0)=0 and described as a point mass on the connection line; animation is conditional on m>0. Zero is the default no-added-mass configuration, so flagging it as an invalid physical bound contradicts the model design.

## Source evidence

Compiler/source-resolved declaration: `Mechanics/MultiBody/Forces/LineForceWithMass.mo:23`. Role: `parameter`; binding: `spring.m`; effective min: `0`; effective max: `None`. 

[Mechanics/MultiBody/Forces/LineForceWithMass.mo — source snapshot](../evidence/sources/0f7d15b92e261c66-LineForceWithMass.mo)

```modelica
21:   parameter Boolean animateMass=true
22:     "= true, if point mass shall be visualized as sphere provided m > 0";
23:   parameter SI.Mass m(min=0)=0
24:     "Mass of point mass on the connection line between the origin of frame_a and the origin of frame_b";
25:   parameter Real lengthFraction(
26:     unit="1",
```

[Mechanics/MultiBody/Forces/LineForceWithMass.mo — source snapshot](../evidence/sources/0f7d15b92e261c66-LineForceWithMass.mo)

```modelica
18: 
19:   parameter Boolean animateLine=true
20:     "= true, if a line shape between frame_a and frame_b shall be visualized";
21:   parameter Boolean animateMass=true
22:     "= true, if point mass shall be visualized as sphere provided m > 0";
23:   parameter SI.Mass m(min=0)=0
24:     "Mass of point mass on the connection line between the origin of frame_a and the origin of frame_b";
25:   parameter Real lengthFraction(
26:     unit="1",
27:     min=0,
28:     max=1) = 0.5
29:     "Location of point mass with respect to frame_a as a fraction of the distance from frame_a to frame_b";
30:   input Types.SpecularCoefficient specularCoefficient = world.defaultSpecularCoefficient
31:     "Reflection of ambient light (= 0: light is completely absorbed)"
```


## Execution evidence

[Rumoca commands, return codes, integrity hashes, bounded output and metadata](../evidence/508f21cda8e8f472.json). Baseline: **tool-error**.

No independent runtime override was executed for this target in this audit; this is not a pass.

## Recommended action

Correct the detector/adjudicator for this specific semantic case; do not impose a blanket strictly-positive bound on the library declaration.

## Scope and limitations

A source-level verdict addresses the reported declaration/claim, not every possible connected system. Tests cover 0–0.5 seconds and are not a proof of long-run stability. Shared instances are not distinct root causes. A missing bound, timeout, compiler error or failed nominal run alone never counts as a verified bug or a false positive. Fixes are proposals; no library/compiler implementation was changed.

[Group and related reports](../groups/optional-line-force-mass.md) · [Index](../README.md)
