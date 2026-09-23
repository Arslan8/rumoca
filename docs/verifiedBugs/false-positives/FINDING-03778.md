# FINDING-03778: Armature example delegates to zero-capable mechanical terms

| Field | Value |
|---|---|
| Verdict | false-positives |
| Scope / group | armature-zero-mechanical-term |
| Model | Modelica.Magnetic.FluxTubes.Examples.MovingCoilActuator.ArmatureStroke |
| Target | cActuator.armature.m |
| Student classification | physical-bound-permits-zero |
| Original report | [FINDING-armaturestroke-cactuator-armature-m-intent.md](../../v2/bugs/FINDING-armaturestroke-cactuator-armature-m-intent.md) — reviewed as `FINDING-03778-armaturestroke-cactuator-armature-m.md`, which a later run renamed |
| Original SHA-256 | 4201e045dfafc957920a9ed49c4a95bae95d5313cfebb8eaed6988b4c97a29c1 |

## Why this is a false positive

m is passed to Translational.Mass, while c and d are passed to ElastoGap. Their source equations use mass, stiffness and damping multiplicatively; zero removes inertia/contact stiffness/damping rather than serving as a divisor. A stopper simulation may become underconstrained or physically unhelpful, but the blanket strictly-positive arithmetic claim is not established.

## Source evidence

Compiler/source-resolved declaration: `Magnetic/FluxTubes/Examples/Utilities/TranslatoryArmatureAndStopper.mo:7`. Role: `parameter`; binding: `cActuator.m_a`; effective min: `0`; effective max: `None`. 

[Magnetic/FluxTubes/Examples/Utilities/TranslatoryArmatureAndStopper.mo — source snapshot](../evidence/sources/88ef39eae81704e0-TranslatoryArmatureAndStopper.mo)

```modelica
5:   parameter SI.Length L(start=0)
6:     "Length of component from left flange to right flange (= flange_b.s - flange_a.s)";
7:   parameter SI.Mass m(start=1) "Armature mass";
8: 
9:   parameter SI.TranslationalSpringConstant c(start=1e11)
10:     "Spring stiffness between impact partners";
```

[Magnetic/FluxTubes/Examples/Utilities/TranslatoryArmatureAndStopper.mo — source snapshot](../evidence/sources/88ef39eae81704e0-TranslatoryArmatureAndStopper.mo)

```modelica
5:   parameter SI.Length L(start=0)
6:     "Length of component from left flange to right flange (= flange_b.s - flange_a.s)";
7:   parameter SI.Mass m(start=1) "Armature mass";
8: 
9:   parameter SI.TranslationalSpringConstant c(start=1e11)
10:     "Spring stiffness between impact partners";
11:   parameter SI.TranslationalDampingConstant d(start=2e7)
12:     "Damping coefficient between impact partners";
13:   parameter Real n(final min=1) = 2
14:     "Exponent of spring forces (f_c = c*|s_rel|^n)"
15:     annotation (Evaluate=true);
16: 
17:   parameter SI.Position x_max(start=10e-3)
18:     "Position of stopper at maximum armature position";
19:   parameter SI.Position x_min(start=0)
20:     "Position of stopper at minimum armature position";
21:   SI.Position s(start=0)
22:     "Absolute position of center of component (= flange_a.s + L/2)";
23:   SI.Velocity v(start=0)
24:     "Absolute velocity of components (= der(s))";
25:   SI.Acceleration a(start=0)
26:     "Absolute acceleration of components (= der(v))";
27:   Modelica.Mechanics.Translational.Components.Mass mass(final L=L, final
28:       m=m) annotation (Placement(transformation(extent={{-10,-10},{10,10}})));
29:   Modelica.Mechanics.Translational.Interfaces.Flange_a flange_a
30:     annotation (Placement(transformation(extent={{-110,-10},{-90,10}})));
31:   Modelica.Mechanics.Translational.Interfaces.Flange_b flange_b
32:     annotation (Placement(transformation(extent={{90,-10},{110,10}})));
33:   Modelica.Mechanics.Translational.Components.Fixed limit_xMin(s0=x_min)
34:     annotation (Placement(transformation(extent={{-80,-50},{-60,-30}})));
35:   Modelica.Mechanics.Translational.Components.Fixed limit_xMax(s0=x_max)
36:     annotation (Placement(transformation(extent={{60,-50},{80,-30}})));
37:   Modelica.Mechanics.Translational.Components.ElastoGap stopper_xMax(
38:     final c=c,
39:     final d=d,
40:     final n=n,
41:     final s_rel0=0) annotation (Placement(transformation(extent={{50,-30},
42:             {70,-10}})));
43:   Modelica.Mechanics.Translational.Components.ElastoGap stopper_xMin(
44:     final c=c,
45:     final d=d,
```


## Execution evidence

[Rumoca commands, return codes, integrity hashes, bounded output and metadata](../evidence/086c556da894438a.json). Baseline: **tool-error**.

No independent runtime override was executed for this target in this audit; this is not a pass.

## Recommended action

Correct the detector/adjudicator for this specific semantic case; do not impose a blanket strictly-positive bound on the library declaration.

## Scope and limitations

A source-level verdict addresses the reported declaration/claim, not every possible connected system. Tests cover 0–0.5 seconds and are not a proof of long-run stability. Shared instances are not distinct root causes. A missing bound, timeout, compiler error or failed nominal run alone never counts as a verified bug or a false positive. Fixes are proposals; no library/compiler implementation was changed.

[Group and related reports](../groups/armature-zero-mechanical-term.md) · [Index](../README.md)
