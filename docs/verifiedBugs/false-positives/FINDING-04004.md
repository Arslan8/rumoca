# FINDING-04004: MultiBody spring mass/stiffness has an intentional zero limit

| Field | Value |
|---|---|
| Verdict | false-positives |
| Scope / group | zero-multibody-spring-option |
| Model | Modelica.Mechanics.MultiBody.Examples.Elementary.HeatLosses |
| Target | spring.c |
| Student classification | physical-bound-permits-zero |
| Original report | [FINDING-heatlosses-spring-c-intent.md](../../v2/bugs/FINDING-heatlosses-spring-c-intent.md) — reviewed as `FINDING-04004-heatlosses-spring-c.md`, which a later run renamed |
| Original SHA-256 | 7b12f7cbb70d154f9d8d670f461a3a074249f73090d0478c7cd9e1e80e764e88 |

## Why this is a false positive

c(min=0) is forwarded to the translational Spring equation f=c*(s_rel-s_rel0), so zero transmits no elastic force. The reported blanket positive-only constraint is inconsistent with these explicit component branches/equations.

## Source evidence

Compiler/source-resolved declaration: `Mechanics/MultiBody/Forces/Spring.mo:9`. Role: `parameter`; binding: `30`; effective min: `0`; effective max: `None`. 

[Mechanics/MultiBody/Forces/Spring.mo — source snapshot](../evidence/sources/ac522a4c4845a453-Spring.mo)

```modelica
7:     "= true, if point mass shall be visualized as sphere if animation=true and m>0";
8: 
9:   parameter SI.TranslationalSpringConstant c(final min=0) "Spring constant";
10:   parameter SI.Length s_unstretched=0 "Unstretched spring length";
11:   parameter SI.Mass m(min=0)=0
12:     "Spring mass located on the connection line between the origin of frame_a and the origin of frame_b";
```

[Mechanics/MultiBody/Forces/Spring.mo — source snapshot](../evidence/sources/ac522a4c4845a453-Spring.mo)

```modelica
5:   parameter Boolean animation=true "= true, if animation shall be enabled";
6:   parameter Boolean showMass=true
7:     "= true, if point mass shall be visualized as sphere if animation=true and m>0";
8: 
9:   parameter SI.TranslationalSpringConstant c(final min=0) "Spring constant";
10:   parameter SI.Length s_unstretched=0 "Unstretched spring length";
11:   parameter SI.Mass m(min=0)=0
12:     "Spring mass located on the connection line between the origin of frame_a and the origin of frame_b";
13:   parameter Real lengthFraction(
14:     min=0,
15:     max=1) = 0.5
16:     "Location of spring mass with respect to frame_a as a fraction of the distance from frame_a to frame_b (=0: at frame_a; =1: at frame_b)";
17:   input SI.Distance width=world.defaultForceWidth "Width of spring"
18:     annotation (Dialog(tab="Animation", group="if animation = true", enable=animation));
```

[Mechanics/MultiBody/Forces/Spring.mo — source snapshot](../evidence/sources/ac522a4c4845a453-Spring.mo)

```modelica
60:   Forces.LineForceWithMass lineForce(
61:     final animateLine=animation,
62:     final animateMass=showMass,
63:     final m=m,
64:     final lengthFraction=lengthFraction,
65:     final lineShapeType="spring",
66:     final lineShapeHeight=coilWidth*2,
67:     final lineShapeWidth=width,
68:     final lineShapeExtra=numberOfWindings,
69:     final lineShapeColor=color,
70:     final specularCoefficient=specularCoefficient,
71:     final massDiameter=massDiameter,
72:     final massColor=massColor,
73:     final s_small=s_small,
74:     final fixedRotationAtFrame_a=fixedRotationAtFrame_a,
75:     final fixedRotationAtFrame_b=fixedRotationAtFrame_b) annotation (Placement(transformation(extent={{-20,-20},{20,20}})));
76:   Modelica.Mechanics.Translational.Components.Spring spring(
77:      final s_rel0=s_unstretched,
78:      final c=c) annotation (Placement(transformation(extent={{-8,40},{12,60}})));
79: 
80: equation
81:   // Results
82:   r_rel_a = Frames.resolve2(frame_a.R, r_rel_0);
83:   e_a = r_rel_a/s;
84:   f = spring.f;
85:   length = lineForce.length;
86:   s = lineForce.s;
87:   r_rel_0 = lineForce.r_rel_0;
88:   e_rel_0 = lineForce.e_rel_0;
89: 
90:   connect(lineForce.frame_a, frame_a)
```


## Execution evidence

[Rumoca commands, return codes, integrity hashes, bounded output and metadata](../evidence/2c68b447bcac4844.json). Baseline: **tool-error**.

No independent runtime override was executed for this target in this audit; this is not a pass.

## Recommended action

Correct the detector/adjudicator for this specific semantic case; do not impose a blanket strictly-positive bound on the library declaration.

## Scope and limitations

A source-level verdict addresses the reported declaration/claim, not every possible connected system. Tests cover 0–0.5 seconds and are not a proof of long-run stability. Shared instances are not distinct root causes. A missing bound, timeout, compiler error or failed nominal run alone never counts as a verified bug or a false positive. Fixes are proposals; no library/compiler implementation was changed.

[Group and related reports](../groups/zero-multibody-spring-option.md) · [Index](../README.md)
