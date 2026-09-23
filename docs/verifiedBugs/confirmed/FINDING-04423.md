# FINDING-04423: Braking example fails to propagate positive speed-scale bounds

| Field | Value |
|---|---|
| Verdict | confirmed |
| Scope / group | braking-speed-scales |
| Model | Modelica.Mechanics.Translational.Examples.CompareBrakingForce |
| Target | v0 |
| Student classification | divisor-reachable-zero |
| Original report | `FINDING-04423-comparebrakingforce-v0.md` — [withdrawn](../../v2/bugs/withdrawn.md); a later run no longer makes this claim |
| Original SHA-256 | 49f44df5dc236ecd3462b6c75eb604966410a2d6362e26d401cccba3bbe81371 |

## Verification and root cause

The outer example declares v0 without a positive bound and forwards it to force/torque sources whose corresponding parameter has min=Modelica.Constants.eps and appears in reciprocal normalization. Thus the example interface admits zero while every consumer requires a positive scale.

## Source evidence

Compiler/source-resolved declaration: `Mechanics/Translational/Examples/CompareBrakingForce.mo:8`. Role: `parameter`; binding: `1`; effective min: `None`; effective max: `None`. 

[Mechanics/Translational/Examples/CompareBrakingForce.mo — source snapshot](../evidence/sources/46d5f21a0434641a-CompareBrakingForce.mo)

```modelica
6:   parameter SI.Force f_nominal=100 "Nominal force";
7:   parameter SI.Velocity v_nominal=abs(v_start) "Nominal speed";
8:   parameter SI.Velocity v0=1 "Speed limit for regularization";
9:   Modelica.Mechanics.Translational.Components.Mass mass1(
10:     m=m,
11:     s(fixed=true, start=0),
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

[Mechanics/Translational/Sources/SignForce.mo — source snapshot](../evidence/sources/d6ed5ac679b1c5fb-SignForce.mo)

```modelica
1: within Modelica.Mechanics.Translational.Sources;
2: model SignForce "Constant force changing sign with speed"
3:   extends Modelica.Mechanics.Translational.Interfaces.PartialForce;
4:   import Modelica.Constants.pi;
5:   parameter SI.Force f_nominal
6:     "Nominal force (if negative, force is acting as load)";
7:   parameter Modelica.Blocks.Types.Regularization reg=Modelica.Blocks.Types.Regularization.Exp
8:     "Type of regularization" annotation(Evaluate=true);
9:   parameter SI.Velocity v0(final min=Modelica.Constants.eps, start=0.1)
10:     "Regularization below v0";
11:   SI.Velocity v
12:     "Velocity of flange with respect to support (= der(s))";
13: equation
14:   v = der(s);
15:   if reg==Modelica.Blocks.Types.Regularization.Exp then
16:     f = -f_nominal*(2/(1 + Modelica.Math.exp(-v/(0.01*v0)))-1);
17:   elseif reg==Modelica.Blocks.Types.Regularization.Sine then
18:     f = -f_nominal*smooth(1, (if abs(v)>=v0 then sign(v) else Modelica.Math.sin(pi/2*v/v0)));
19:   elseif reg==Modelica.Blocks.Types.Regularization.Linear then
20:     f = -f_nominal*(if abs(v)>=v0 then sign(v) else (v/v0));
21:   else//if reg==Modelica.Blocks.Types.Regularization.CoSine
22:     f = -f_nominal*(if abs(v)>=v0 then sign(v) else sign(v)*(1 - Modelica.Math.cos(pi/2*v/v0)));
23:   end if;
24:   annotation (
25:     Icon(coordinateSystem(preserveAspectRatio=true, extent={{-100,
```


## Execution evidence

[Rumoca commands, return codes, integrity hashes, bounded output and metadata](../evidence/a87b7cf9305a618d.json). Baseline: **clean**.

| Probe | Outcome |
|---|---|
| `v0=0` | reported-failure |

Diagnostic: diffsol-bdf advance exhaustion failed: ODE solver error: Step size is too small at time = 0.4999677459280067

## Proposed fix

Mirror the child min=Modelica.Constants.eps attribute on v0 and assert it at the example boundary before source-component parameter evaluation.

## Fix validation

Test zero and small-positive regularization/nominal scales for every braking law, plus nominal stopping trajectories.

## Scope and limitations

A source-level verdict addresses the reported declaration/claim, not every possible connected system. Tests cover 0–0.5 seconds and are not a proof of long-run stability. Shared instances are not distinct root causes. A missing bound, timeout, compiler error or failed nominal run alone never counts as a verified bug or a false positive. Fixes are proposals; no library/compiler implementation was changed.

[Group and related reports](../groups/braking-speed-scales.md) · [Index](../README.md)
