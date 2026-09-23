# FINDING-04625: IdealPump permits zero nominal speed then divides by it

| Field | Value |
|---|---|
| Verdict | confirmed |
| Scope / group | ideal-pump-speed |
| Model | Modelica.Thermal.FluidHeatFlow.Examples.PumpAndValve |
| Target | idealPump.wNominal |
| Student classification | divisor-reachable-zero |
| Original report | [FINDING-pumpandvalve-idealpump-wnominal-divzero-2.md](../../v2/bugs/FINDING-pumpandvalve-idealpump-wnominal-divzero-2.md) — reviewed as `FINDING-04625-pumpandvalve-idealpump-wnominal.md`, which a later run renamed |
| Original SHA-256 | c19bf6212df4f64d3ac81f9b5a53a4e858b1ebd280044d2ba7f836eea95b6f19 |

## Verification and root cause

IdealPump declares wNominal without a positive bound and evaluates both w/wNominal and a flow characteristic derived from it. Zero is admitted but undefined even though the low-actual-speed runtime branch is guarded; the nominal scale is evaluated before that branch can make it safe.

## Source evidence

Compiler/source-resolved declaration: `Thermal/FluidHeatFlow/Sources/IdealPump.mo:5`. Role: `parameter`; binding: `1`; effective min: `None`; effective max: `None`. 

[Thermal/FluidHeatFlow/Sources/IdealPump.mo — source snapshot](../evidence/sources/ecddbaceba7f68b2-IdealPump.mo)

```modelica
3: 
4:   extends FluidHeatFlow.BaseClasses.TwoPort(final tapT=1);
5:   parameter SI.AngularVelocity wNominal(start=1, displayUnit="rev/min")
6:     "Nominal speed"
7:       annotation(Dialog(group="Pump characteristic"));
8:   parameter SI.Pressure dp0(start=2)
```

[Thermal/FluidHeatFlow/Sources/IdealPump.mo — source snapshot](../evidence/sources/ecddbaceba7f68b2-IdealPump.mo)

```modelica
2: model IdealPump "Model of an ideal pump"
3: 
4:   extends FluidHeatFlow.BaseClasses.TwoPort(final tapT=1);
5:   parameter SI.AngularVelocity wNominal(start=1, displayUnit="rev/min")
6:     "Nominal speed"
7:       annotation(Dialog(group="Pump characteristic"));
8:   parameter SI.Pressure dp0(start=2)
9:     "Max. pressure increase @ V_flow=0"
10:       annotation(Dialog(group="Pump characteristic"));
11:   parameter SI.VolumeFlowRate V_flow0(start=2)
12:     "Max. volume flow rate @ dp=0"
13:       annotation(Dialog(group="Pump characteristic"));
14:   SI.AngularVelocity w=der(flange_a.phi) "Speed";
15: protected
16:   SI.Pressure dp1;
17:   SI.VolumeFlowRate V_flow1;
18: public
19:   Modelica.Mechanics.Rotational.Interfaces.Flange_a flange_a
20:     annotation (Placement(transformation(extent={{-10,-110},{10,-90}})));
21: equation
22:   // pump characteristic
23:   dp1 = dp0*sign(w/wNominal)*(w/wNominal)^2;
24:   V_flow1 = V_flow0*(w/wNominal);
25:   if noEvent(abs(w)<Modelica.Constants.small) then
26:     dp = 0;
27:     flange_a.tau = 0;
28:   else
29:     dp = -dp1*(1 - V_flow/V_flow1);
30:     flange_a.tau*w = -dp*V_flow;
31:   end if;
```


## Execution evidence

[Rumoca commands, return codes, integrity hashes, bounded output and metadata](../evidence/db1c40a3e361d88f.json). Baseline: **tool-error**.

No independent runtime override was executed for this target in this audit; this is not a pass.

## Proposed fix

Require wNominal>0 (or a documented nonzero signed convention) and assert it before pump-characteristic evaluation. Guard derived ratios so invalid configuration produces one clear parameter error.

## Fix validation

Test default, zero, negative according to the sign policy, near-zero positive, actual standstill w=0, and both flow directions.

## Scope and limitations

A source-level verdict addresses the reported declaration/claim, not every possible connected system. Tests cover 0–0.5 seconds and are not a proof of long-run stability. Shared instances are not distinct root causes. A missing bound, timeout, compiler error or failed nominal run alone never counts as a verified bug or a false positive. Fixes are proposals; no library/compiler implementation was changed.

[Group and related reports](../groups/ideal-pump-speed.md) · [Index](../README.md)
