# FINDING-04380: Braking example fails to propagate positive speed-scale bounds

| Field | Value |
|---|---|
| Verdict | confirmed |
| Scope / group | braking-speed-scales |
| Model | Modelica.Mechanics.Rotational.Examples.CompareBrakingTorque |
| Target | w0 |
| Student classification | divisor-reachable-zero |
| Original report | `FINDING-04380-comparebrakingtorque-w0.md` — [withdrawn](../../v2/bugs/withdrawn.md); a later run no longer makes this claim |
| Original SHA-256 | 71036653d89744ac83fe4ebef6268216f706ed1ce6e020c2b0e934a1b7658fe4 |

## Verification and root cause

The outer example declares w0 without a positive bound and forwards it to force/torque sources whose corresponding parameter has min=Modelica.Constants.eps and appears in reciprocal normalization. Thus the example interface admits zero while every consumer requires a positive scale.

## Source evidence

Compiler/source-resolved declaration: `Mechanics/Rotational/Examples/CompareBrakingTorque.mo:8`. Role: `parameter`; binding: `1`; effective min: `None`; effective max: `None`. 

[Mechanics/Rotational/Examples/CompareBrakingTorque.mo — source snapshot](../evidence/sources/4a146eb70f1f35af-CompareBrakingTorque.mo)

```modelica
6:   parameter SI.Torque tau_nominal=100 "Nominal torque";
7:   parameter SI.AngularVelocity w_nominal=abs(w_start) "Nominal speed";
8:   parameter SI.AngularVelocity w0=1 "Speed limit for regularization";
9:   Modelica.Mechanics.Rotational.Components.Inertia inertia1(
10:     J=J,
11:     phi(fixed=true, start=0),
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

[Mechanics/Rotational/Sources/SignTorque.mo — source snapshot](../evidence/sources/40ffd3998043d48a-SignTorque.mo)

```modelica
1: within Modelica.Mechanics.Rotational.Sources;
2: model SignTorque "Constant torque changing sign with speed"
3:   extends Rotational.Interfaces.PartialTorque;
4:   import Modelica.Constants.pi;
5:   parameter SI.Torque tau_nominal
6:     "Nominal torque (if negative, torque is acting as load)";
7:   parameter Modelica.Blocks.Types.Regularization reg=Modelica.Blocks.Types.Regularization.Exp
8:     "Type of regularization" annotation(Evaluate=true);
9:   parameter SI.AngularVelocity w0(final min=Modelica.Constants.eps, start=0.1)
10:     "Regularization below w0";
11:   SI.AngularVelocity w
12:     "Angular velocity of flange with respect to support (= der(phi))";
13:   SI.Torque tau
14:     "Accelerating torque acting at flange (= -flange.tau)";
15: equation
16:   w = der(phi);
17:   tau = -flange.tau;
18:   if reg==Modelica.Blocks.Types.Regularization.Exp then
19:     tau = tau_nominal*(2/(1 + Modelica.Math.exp(-w/(0.01*w0)))-1);
20:   elseif reg==Modelica.Blocks.Types.Regularization.Sine then
21:     tau = tau_nominal*smooth(1, (if abs(w)>=w0 then sign(w) else Modelica.Math.sin(pi/2*w/w0)));
22:   elseif reg==Modelica.Blocks.Types.Regularization.Linear then
23:     tau = tau_nominal*(if abs(w)>=w0 then sign(w) else (w/w0));
24:   else//if reg==Modelica.Blocks.Types.Regularization.CoSine
25:     tau = tau_nominal*(if abs(w)>=w0 then sign(w) else sign(w)*(1 - Modelica.Math.cos(pi/2*w/w0)));
```


## Execution evidence

[Rumoca commands, return codes, integrity hashes, bounded output and metadata](../evidence/fe3161ba002311e0.json). Baseline: **clean**.

| Probe | Outcome |
|---|---|
| `w0=0` | reported-failure |

Diagnostic: diffsol-bdf advance exhaustion failed: ODE solver error: Step size is too small at time = 0.4999677459280067

## Proposed fix

Mirror the child min=Modelica.Constants.eps attribute on w0 and assert it at the example boundary before source-component parameter evaluation.

## Fix validation

Test zero and small-positive regularization/nominal scales for every braking law, plus nominal stopping trajectories.

## Scope and limitations

A source-level verdict addresses the reported declaration/claim, not every possible connected system. Tests cover 0–0.5 seconds and are not a proof of long-run stability. Shared instances are not distinct root causes. A missing bound, timeout, compiler error or failed nominal run alone never counts as a verified bug or a false positive. Fixes are proposals; no library/compiler implementation was changed.

[Group and related reports](../groups/braking-speed-scales.md) · [Index](../README.md)
