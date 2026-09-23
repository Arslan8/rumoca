# FINDING-04381: Braking example fails to propagate positive speed-scale bounds

| Field | Value |
|---|---|
| Verdict | confirmed |
| Scope / group | braking-speed-scales |
| Model | Modelica.Mechanics.Rotational.Examples.CompareBrakingTorque |
| Target | w_nominal |
| Student classification | divisor-reachable-zero |
| Original report | `FINDING-04381-comparebrakingtorque-w-nominal.md` — [withdrawn](../../v2/bugs/withdrawn.md); a later run no longer makes this claim |
| Original SHA-256 | 35a0a88e9546190410c06113cf6397b1afce8ab5effaf787b79728a66c787da7 |

## Verification and root cause

The outer example declares w_nominal without a positive bound and forwards it to force/torque sources whose corresponding parameter has min=Modelica.Constants.eps and appears in reciprocal normalization. Thus the example interface admits zero while every consumer requires a positive scale.

## Source evidence

Compiler/source-resolved declaration: `Mechanics/Rotational/Examples/CompareBrakingTorque.mo:7`. Role: `parameter`; binding: `100`; effective min: `None`; effective max: `None`. 

[Mechanics/Rotational/Examples/CompareBrakingTorque.mo — source snapshot](../evidence/sources/4a146eb70f1f35af-CompareBrakingTorque.mo)

```modelica
5:   parameter SI.AngularVelocity w_start=100 "Initial speed of inertia";
6:   parameter SI.Torque tau_nominal=100 "Nominal torque";
7:   parameter SI.AngularVelocity w_nominal=abs(w_start) "Nominal speed";
8:   parameter SI.AngularVelocity w0=1 "Speed limit for regularization";
9:   Modelica.Mechanics.Rotational.Components.Inertia inertia1(
10:     J=J,
```

[Mechanics/Rotational/Examples/CompareBrakingTorque.mo — source snapshot](../evidence/sources/4a146eb70f1f35af-CompareBrakingTorque.mo)

```modelica
2: model CompareBrakingTorque "Compare different braking torques"
3:   extends Modelica.Icons.Example;
4:   parameter SI.Inertia J=1 "Moment of inertia";
5:   parameter SI.AngularVelocity w_start=100 "Initial speed of inertia";
6:   parameter SI.Torque tau_nominal=100 "Nominal torque";
7:   parameter SI.AngularVelocity w_nominal=abs(w_start) "Nominal speed";
8:   parameter SI.AngularVelocity w0=1 "Speed limit for regularization";
9:   Modelica.Mechanics.Rotational.Components.Inertia inertia1(
10:     J=J,
11:     phi(fixed=true, start=0),
12:     w(fixed=true, start=w_start))
13:     annotation (Placement(transformation(extent={{-10,50},{10,70}})));
14:   Modelica.Mechanics.Rotational.Sources.SignTorque signTorque(
15:     tau_nominal=-tau_nominal,
16:     reg=Modelica.Blocks.Types.Regularization.Linear,
17:     w0=w0)   annotation (Placement(transformation(extent={{-40,50},{-20,70}})));
18:   Modelica.Mechanics.Rotational.Components.Inertia inertia2(
19:     J=J,
20:     phi(fixed=true, start=0),
21:     w(fixed=true, start=w_start))
22:     annotation (Placement(transformation(extent={{-10,10},{10,30}})));
23:   Modelica.Mechanics.Rotational.Sources.LinearSpeedDependentTorque
24:     linearSpeedDependentTorque(
25:     tau_nominal=-tau_nominal,
26:     TorqueDirection=false,
27:     w_nominal=w_nominal)
28:     annotation (Placement(transformation(extent={{-40,10},{-20,30}})));
```

[Mechanics/Rotational/Sources/InverseSpeedDependentTorque.mo — source snapshot](../evidence/sources/70145ddeed7f1ac7-InverseSpeedDependentTorque.mo)

```modelica
1: within Modelica.Mechanics.Rotational.Sources;
2: model InverseSpeedDependentTorque
3:   "Torque reciprocal dependent on speed"
4:   extends Rotational.Interfaces.PartialTorque;
5:   import Modelica.Constants.pi;
6:   parameter SI.Torque tau_nominal
7:     "Nominal torque (if negative, torque is acting as load in positive direction of rotation)";
8:   parameter Boolean TorqueDirection=true
9:     "Same direction of torque in both directions of rotation";
10:   parameter SI.AngularVelocity w_nominal(min=Modelica.Constants.eps)
11:     "Nominal speed";
12:   parameter SI.AngularVelocity w0(final min=Modelica.Constants.eps, start=0.1)
13:     "Regularization below w0" annotation(Dialog(enable=not TorqueDirection));
14:   SI.AngularVelocity w
15:     "Angular velocity of flange with respect to support (= der(phi))";
16:   SI.Torque tau
17:     "Accelerating torque acting at flange (= -flange.tau)";
18: equation
19:   w = der(phi);
20:   tau = -flange.tau;
21:   if TorqueDirection then
22:     tau = if abs(w)<w0 then tau_nominal*w_nominal/w0 else tau_nominal*w_nominal/abs(w);
23:   else
24:     tau = if abs(w)<w0 then tau_nominal*w/w0 else tau_nominal*w_nominal/w;
25:   end if;
```


## Execution evidence

[Rumoca commands, return codes, integrity hashes, bounded output and metadata](../evidence/fe3161ba002311e0.json). Baseline: **clean**.

| Probe | Outcome |
|---|---|
| `w_nominal=0` | reported-failure |

Diagnostic: solve-IR evaluation failed: algebraic projection did not converge at event boundary: worst scaled residual row=29 target=quadraticSpeedDependentTorque.tau value=inf ratio=inf norm=inf row_scale=1.000000e0 scaled_tolerance=1.000000e-10

## Proposed fix

Mirror the child min=Modelica.Constants.eps attribute on w_nominal and assert it at the example boundary before source-component parameter evaluation.

## Fix validation

Test zero and small-positive regularization/nominal scales for every braking law, plus nominal stopping trajectories.

## Scope and limitations

A source-level verdict addresses the reported declaration/claim, not every possible connected system. Tests cover 0–0.5 seconds and are not a proof of long-run stability. Shared instances are not distinct root causes. A missing bound, timeout, compiler error or failed nominal run alone never counts as a verified bug or a false positive. Fixes are proposals; no library/compiler implementation was changed.

[Group and related reports](../groups/braking-speed-scales.md) · [Index](../README.md)
