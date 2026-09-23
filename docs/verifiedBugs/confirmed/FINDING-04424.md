# FINDING-04424: Braking example fails to propagate positive speed-scale bounds

| Field | Value |
|---|---|
| Verdict | confirmed |
| Scope / group | braking-speed-scales |
| Model | Modelica.Mechanics.Translational.Examples.CompareBrakingForce |
| Target | v_nominal |
| Student classification | divisor-reachable-zero |
| Original report | `FINDING-04424-comparebrakingforce-v-nominal.md` — [withdrawn](../../v2/bugs/withdrawn.md); a later run no longer makes this claim |
| Original SHA-256 | fd13ff2860713cf30fa13844ca9cb45313528ada336f701cb547ac50013d6b84 |

## Verification and root cause

The outer example declares v_nominal without a positive bound and forwards it to force/torque sources whose corresponding parameter has min=Modelica.Constants.eps and appears in reciprocal normalization. Thus the example interface admits zero while every consumer requires a positive scale.

## Source evidence

Compiler/source-resolved declaration: `Mechanics/Translational/Examples/CompareBrakingForce.mo:7`. Role: `parameter`; binding: `100`; effective min: `None`; effective max: `None`. 

[Mechanics/Translational/Examples/CompareBrakingForce.mo — source snapshot](../evidence/sources/46d5f21a0434641a-CompareBrakingForce.mo)

```modelica
5:   parameter SI.Velocity v_start=100 "Initial speed of mass";
6:   parameter SI.Force f_nominal=100 "Nominal force";
7:   parameter SI.Velocity v_nominal=abs(v_start) "Nominal speed";
8:   parameter SI.Velocity v0=1 "Speed limit for regularization";
9:   Modelica.Mechanics.Translational.Components.Mass mass1(
10:     m=m,
```

[Mechanics/Translational/Examples/CompareBrakingForce.mo — source snapshot](../evidence/sources/46d5f21a0434641a-CompareBrakingForce.mo)

```modelica
2: model CompareBrakingForce "Compare different braking forces"
3:   extends Modelica.Icons.Example;
4:   parameter SI.Mass m=1 "Mass";
5:   parameter SI.Velocity v_start=100 "Initial speed of mass";
6:   parameter SI.Force f_nominal=100 "Nominal force";
7:   parameter SI.Velocity v_nominal=abs(v_start) "Nominal speed";
8:   parameter SI.Velocity v0=1 "Speed limit for regularization";
9:   Modelica.Mechanics.Translational.Components.Mass mass1(
10:     m=m,
11:     s(fixed=true, start=0),
12:     v(fixed=true, start=v_start))
13:     annotation (Placement(transformation(extent={{-10,50},{10,70}})));
14:   Modelica.Mechanics.Translational.Sources.SignForce signForce(
15:     f_nominal=-f_nominal,
16:     reg=Modelica.Blocks.Types.Regularization.Linear,
17:     v0=v0)   annotation (Placement(transformation(extent={{-40,50},{-20,70}})));
18:   Modelica.Mechanics.Translational.Components.Mass mass2(
19:     m=m,
20:     s(fixed=true, start=0),
21:     v(fixed=true, start=v_start))
22:     annotation (Placement(transformation(extent={{-10,10},{10,30}})));
23:   Modelica.Mechanics.Translational.Sources.LinearSpeedDependentForce
24:     linearSpeedDependentForce(
25:     f_nominal=-f_nominal,
26:     ForceDirection=false,
27:     v_nominal=v_nominal)
28:     annotation (Placement(transformation(extent={{-40,10},{-20,30}})));
```

[Mechanics/Translational/Sources/InverseSpeedDependentForce.mo — source snapshot](../evidence/sources/b3bbe2c8cc2f02e4-InverseSpeedDependentForce.mo)

```modelica
1: within Modelica.Mechanics.Translational.Sources;
2: model InverseSpeedDependentForce
3:   "Force reciprocal dependent on speed"
4:   extends Translational.Interfaces.PartialForce;
5:   parameter SI.Force f_nominal
6:     "Nominal force (if negative, torque is acting as load in positive direction of motion)";
7:   parameter Boolean ForceDirection=true
8:     "Same direction of force in both directions of motion";
9:   parameter SI.Velocity v_nominal(min=Modelica.Constants.eps)
10:     "Nominal speed";
11:   parameter SI.Velocity v0(final min=Modelica.Constants.eps, start=0.1)
12:     "Regularization below v0" annotation(Dialog(enable=not ForceDirection));
13:   SI.Velocity v
14:     "Velocity of flange with respect to support (= der(s))";
15: equation
16:   v = der(s);
17:   if ForceDirection then
18:     f = if abs(v)<v0 then -f_nominal*v_nominal/v0 else -f_nominal*v_nominal/abs(v);
19:   else
20:     f = if abs(v)<v0 then -f_nominal*v/v0 else -f_nominal*v_nominal/v;
21:   end if;
22:   annotation (
23:     Icon(
24:       coordinateSystem(
25:         preserveAspectRatio=true,
```


## Execution evidence

[Rumoca commands, return codes, integrity hashes, bounded output and metadata](../evidence/a87b7cf9305a618d.json). Baseline: **clean**.

| Probe | Outcome |
|---|---|
| `v_nominal=0` | reported-failure |

Diagnostic: solve-IR evaluation failed: algebraic projection did not converge at event boundary: worst scaled residual row=29 target=quadraticSpeedDependentForce.f value=-inf ratio=inf norm=inf row_scale=1.000000e0 scaled_tolerance=1.000000e-10

## Proposed fix

Mirror the child min=Modelica.Constants.eps attribute on v_nominal and assert it at the example boundary before source-component parameter evaluation.

## Fix validation

Test zero and small-positive regularization/nominal scales for every braking law, plus nominal stopping trajectories.

## Scope and limitations

A source-level verdict addresses the reported declaration/claim, not every possible connected system. Tests cover 0–0.5 seconds and are not a proof of long-run stability. Shared instances are not distinct root causes. A missing bound, timeout, compiler error or failed nominal run alone never counts as a verified bug or a false positive. Fixes are proposals; no library/compiler implementation was changed.

[Group and related reports](../groups/braking-speed-scales.md) · [Index](../README.md)
