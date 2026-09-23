# FINDING-04744: OneWayValve divides by unconstrained nominal scales

| Field | Value |
|---|---|
| Verdict | confirmed |
| Scope / group | one-way-valve-scales |
| Model | Modelica.Thermal.FluidHeatFlow.Examples.WaterPump |
| Target | oneWayValve.V_flowNominal |
| Student classification | divisor-reachable-zero |
| Original report | [FINDING-waterpump-onewayvalve-v-flownominal-divunresolved.md](../../v2/bugs/FINDING-waterpump-onewayvalve-v-flownominal-divunresolved.md) — reviewed as `FINDING-04744-waterpump-onewayvalve-v-flownominal.md`, which a later run renamed |
| Original SHA-256 | d726e869a5d3bda993264c26d60dfba17b01cbd058ab13ce54fb7871d31ac6f7 |

## Verification and root cause

The valve declares V_flowNominal and dpNominal without positive bounds, then evaluates dpForward/V_flowNominal and V_flowBackward/dpNominal in its piecewise constitutive equations. Either zero scale is directly undefined.

## Source evidence

Compiler/source-resolved declaration: `Thermal/FluidHeatFlow/Components/OneWayValve.mo:5`. Role: `parameter`; binding: `0.18`; effective min: `None`; effective max: `None`. 

[Thermal/FluidHeatFlow/Components/OneWayValve.mo — source snapshot](../evidence/sources/adeec05d6061d86a-OneWayValve.mo)

```modelica
3:   extends FluidHeatFlow.BaseClasses.TwoPort(m(start=0), final tapT=1);
4: 
5:   parameter SI.VolumeFlowRate V_flowNominal(start=1) "Nominal volume flow rate (forward)";
6:   parameter SI.Pressure dpForward(displayUnit="bar")=1e-6 "Pressure drop at nominal flow (forward)";
7:   parameter SI.Pressure dpNominal(displayUnit="bar", start=1e5) "Nominal pressure (backward)";
8:   parameter SI.VolumeFlowRate V_flowBackward(start=1E-6) "Leakage volume flow rate (backward)";
```

[Thermal/FluidHeatFlow/Components/OneWayValve.mo — source snapshot](../evidence/sources/adeec05d6061d86a-OneWayValve.mo)

```modelica
2: model OneWayValve "Simple one-way valve"
3:   extends FluidHeatFlow.BaseClasses.TwoPort(m(start=0), final tapT=1);
4: 
5:   parameter SI.VolumeFlowRate V_flowNominal(start=1) "Nominal volume flow rate (forward)";
6:   parameter SI.Pressure dpForward(displayUnit="bar")=1e-6 "Pressure drop at nominal flow (forward)";
7:   parameter SI.Pressure dpNominal(displayUnit="bar", start=1e5) "Nominal pressure (backward)";
8:   parameter SI.VolumeFlowRate V_flowBackward(start=1E-6) "Leakage volume flow rate (backward)";
9:   parameter Real frictionLoss(min=0, max=1, start=0)
10:     "Part of friction losses fed to medium";
11:   Boolean backward(start=true) "State forward=false / backward=true";
12: protected
13:   Real s(start=0, final unit="1")
14:     "Auxiliary variable for actual position on the valve characteristic";
15:   /* s < 0: backward, leakage flow
16:          s > 0: forward, small pressure drop */
17:   constant SI.VolumeFlowRate unitVolumeFlowRate = 1;
18:   constant SI.Pressure unitPressureDrop = 1;
19: equation
20:   backward = s<0;
21:   dp     = (s*unitVolumeFlowRate)*(if backward then 1 else dpForward/V_flowNominal);
22:   V_flow = (s*unitPressureDrop)  *(if backward then V_flowBackward/dpNominal else 1);
23:   Q_flow = frictionLoss*V_flow*dp;
24: annotation (Documentation(info="<html>
25: <p>Simple one-way valve, comparable to the electrical <a href=\"modelica://Modelica.Electrical.Analog.Ideal.IdealDiode\">ideal diode</a> model.</p>
```


## Execution evidence

[Rumoca commands, return codes, integrity hashes, bounded output and metadata](../evidence/73c04f9c1ce524a6.json). Baseline: **clean**.

| Probe | Outcome |
|---|---|
| `oneWayValve.V_flowNominal=0` | clean |

## Proposed fix

Require and assert strictly positive nominal flow magnitude and nominal backward pressure before forming the slopes. If signed configuration is intended, separate direction from positive magnitudes rather than allowing a zero denominator.

## Fix validation

Test nominal flow in both directions, each zero independently, negative sign-policy cases, and small positive scales with finite slopes.

## Scope and limitations

A source-level verdict addresses the reported declaration/claim, not every possible connected system. Tests cover 0–0.5 seconds and are not a proof of long-run stability. Shared instances are not distinct root causes. A missing bound, timeout, compiler error or failed nominal run alone never counts as a verified bug or a false positive. Fixes are proposals; no library/compiler implementation was changed.

[Group and related reports](../groups/one-way-valve-scales.md) · [Index](../README.md)
