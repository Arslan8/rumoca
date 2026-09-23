# FINDING-05109: Vehicle exposes zero regularization speed to reciprocal equations

| Field | Value |
|---|---|
| Verdict | confirmed |
| Scope / group | vehicle-regularization-speed |
| Model | ModelicaTest.Translational.Vehicles |
| Target | vehicleRollInVar.vReg |
| Student classification | divisor-reachable-zero |
| Original report | `FINDING-05109-vehicles-vehiclerollinvar-vreg.md` — [withdrawn](../../v2/bugs/withdrawn.md); a later run no longer makes this claim |
| Original SHA-256 | c2d07c429b324245fe4febcdcd3727f45291cffae4848bbdf4c8045205a0264d |

## Verification and root cause

Vehicle declares vReg=1e-3 without propagating the positive bound of RollingResistance.v0, then passes final v0=vReg. Every regularization branch divides by v0. The outer parameter therefore appears to allow zero even though the consumer requires at least Modelica.Constants.eps.

## Source evidence

Compiler/source-resolved declaration: `Mechanics/Translational/Components/Vehicle.mo:21`. Role: `parameter`; binding: `0.001`; effective min: `None`; effective max: `None`. 

[Mechanics/Translational/Components/Vehicle.mo — source snapshot](../evidence/sources/037334fdb7d77239-Vehicle.mo)

```modelica
19:   parameter Real CrConstant=0.015 "Constant rolling resistance coefficient"
20:     annotation(Dialog(tab="Driving resistances", group="Rolling resistance", enable=not useCrInput));
21:   parameter SI.Velocity vReg=1e-3 "Velocity for regularization around 0"
22:     annotation(Dialog(tab="Driving resistances", group="Rolling resistance"));
23:   parameter Boolean useInclinationInput=false "Enable signal input for inclination"
24:     annotation(Dialog(tab="Driving resistances", group="Inclination resistance"));
```

[Mechanics/Translational/Components/Vehicle.mo — source snapshot](../evidence/sources/037334fdb7d77239-Vehicle.mo)

```modelica
17:   parameter Boolean useCrInput=false "Enable signal input for Cr"
18:     annotation(Dialog(tab="Driving resistances", group="Rolling resistance"));
19:   parameter Real CrConstant=0.015 "Constant rolling resistance coefficient"
20:     annotation(Dialog(tab="Driving resistances", group="Rolling resistance", enable=not useCrInput));
21:   parameter SI.Velocity vReg=1e-3 "Velocity for regularization around 0"
22:     annotation(Dialog(tab="Driving resistances", group="Rolling resistance"));
23:   parameter Boolean useInclinationInput=false "Enable signal input for inclination"
```

[Mechanics/Translational/Components/RollingResistance.mo — source snapshot](../evidence/sources/10590361b1409b76-RollingResistance.mo)

```modelica
12:   parameter Modelica.Blocks.Types.Regularization reg=Modelica.Blocks.Types.Regularization.Exp
13:     "Type of regularization" annotation(Evaluate=true);
14:   parameter SI.Velocity v0(final min=Modelica.Constants.eps)=0.1
15:     "Regularization below v0";
16:   SI.Velocity v
17:     "Velocity of flange with respect to support (= der(s))";
18:   SI.Force f_nominal "Nominal rolling resistance without regularization";
19:   Blocks.Interfaces.RealInput inclination = inclination_internal if useInclinationInput
20:     "Inclination=tan(angle)"
21:     annotation (Placement(transformation(extent={{-20,-20},{20,20}},
22:         origin={-120,60})));
23:   Blocks.Interfaces.RealInput cr = Cr_internal if useCrInput
24:     "Rolling resistance coefficient"
25:     annotation (Placement(transformation(extent={{-20,-20},{20,20}},
26:         origin={-120,-60})));
27: protected
28:   Real Cr_internal "Rolling resistance coefficient";
29:   Real inclination_internal "Inclination";
30: equation
31:   if not useCrInput then
32:     Cr_internal = CrConstant;
33:   end if;
34:   if not useInclinationInput then
35:     inclination_internal = inclinationConstant;
36:   end if;
37:   v = der(s);
38:   f_nominal = -Cr_internal*fWeight*cos(atan(inclination_internal));
39:   if reg==Modelica.Blocks.Types.Regularization.Exp then
40:     f = -f_nominal*(2/(1 + Modelica.Math.exp(-v/(0.01*v0)))-1);
41:   elseif reg==Modelica.Blocks.Types.Regularization.Sine then
42:     f = -f_nominal*smooth(1, (if abs(v)>=v0 then sign(v) else Modelica.Math.sin(pi/2*v/v0)));
43:   elseif reg==Modelica.Blocks.Types.Regularization.Linear then
44:     f = -f_nominal*(if abs(v)>=v0 then sign(v) else (v/v0));
45:   else//if reg==Modelica.Blocks.Types.Regularization.CoSine
46:     f = -f_nominal*(if abs(v)>=v0 then sign(v) else sign(v)*(1 - Modelica.Math.cos(pi/2*v/v0)));
```


## Execution evidence

[Rumoca commands, return codes, integrity hashes, bounded output and metadata](../evidence/e1997bd33cf0ed7f.json). Baseline: **tool-error**.

No independent runtime override was executed for this target in this audit; this is not a pass.

## Proposed fix

Mirror v0(final min=Modelica.Constants.eps) on Vehicle.vReg and add a clear assertion before constructing/evaluating regularization. Keep the exact positive bound consistent between wrapper and component.

## Fix validation

Test each Regularization enum at default, zero, negative and small positive vReg; invalid input must be rejected before exponent/division evaluation.

## Scope and limitations

A source-level verdict addresses the reported declaration/claim, not every possible connected system. Tests cover 0–0.5 seconds and are not a proof of long-run stability. Shared instances are not distinct root causes. A missing bound, timeout, compiler error or failed nominal run alone never counts as a verified bug or a false positive. Fixes are proposals; no library/compiler implementation was changed.

[Group and related reports](../groups/vehicle-regularization-speed.md) · [Index](../README.md)
