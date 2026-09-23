# FINDING-04630: The friction denominator is protected by an ordering assertion

| Field | Value |
|---|---|
| Verdict | false-positives |
| Scope / group | asserted-friction-flow-order |
| Model | Modelica.Thermal.FluidHeatFlow.Examples.PumpAndValve |
| Target | pipe.V_flowNominal |
| Student classification | divisor-reachable-zero |
| Original report | [FINDING-pumpandvalve-pipe-v-flownominal-divzero.md](../../v2/bugs/FINDING-pumpandvalve-pipe-v-flownominal-divzero.md) — reviewed as `FINDING-04630-pumpandvalve-pipe-v-flownominal.md`, which a later run renamed |
| Original SHA-256 | f24231347a4b53d19d0f51e5728794437d0bd6412535406a0146514fb994b92c |

## Why this is a false positive

The only difference denominator is (V_flowNominal-V_flowLaminar)^2. V_flowLaminar has min=Modelica.Constants.small, and the initial algorithm asserts V_flowNominal>V_flowLaminar before computing k. Consequently V_flowNominal cannot be zero or equal to the laminar value in an admissible initialization. The detector ignored the inherited positive bound and relational assertion.

## Source evidence

Compiler/source-resolved declaration: `Thermal/FluidHeatFlow/BaseClasses/SimpleFriction.mo:9`. Role: `parameter`; binding: `1`; effective min: `None`; effective max: `None`. 

[Thermal/FluidHeatFlow/BaseClasses/SimpleFriction.mo — source snapshot](../evidence/sources/cab059d1a725c12e-SimpleFriction.mo)

```modelica
7:     "Laminar pressure drop"
8:     annotation(Dialog(group="Simple friction"));
9:   parameter SI.VolumeFlowRate V_flowNominal(start=1)
10:     "Nominal volume flow"
11:     annotation(Dialog(group="Simple friction"));
12:   parameter SI.Pressure dpNominal(start=1)
```

[Thermal/FluidHeatFlow/BaseClasses/SimpleFriction.mo — source snapshot](../evidence/sources/cab059d1a725c12e-SimpleFriction.mo)

```modelica
2: partial model SimpleFriction "Simple friction model"
3:   parameter SI.VolumeFlowRate V_flowLaminar(min=Modelica.Constants.small, start=0.1)
4:     "Laminar volume flow"
5:     annotation(Dialog(group="Simple friction"));
6:   parameter SI.Pressure dpLaminar(start=0.1)
7:     "Laminar pressure drop"
8:     annotation(Dialog(group="Simple friction"));
9:   parameter SI.VolumeFlowRate V_flowNominal(start=1)
10:     "Nominal volume flow"
11:     annotation(Dialog(group="Simple friction"));
12:   parameter SI.Pressure dpNominal(start=1)
13:     "Nominal pressure drop"
14:     annotation(Dialog(group="Simple friction"));
15:   parameter Real frictionLoss(min=0, max=1) = 0
16:     "Part of friction losses fed to medium"
17:     annotation(Dialog(group="Simple friction"));
18:   SI.Pressure pressureDrop;
19:   SI.VolumeFlowRate volumeFlow;
20:   SI.Power Q_friction;
21: protected
22:   parameter SI.Pressure dpNomMin=dpLaminar/V_flowLaminar*V_flowNominal;
23:   parameter Real k(final unit="Pa.s2/m6", fixed=false);
24: initial algorithm
25:   assert(V_flowNominal>V_flowLaminar,
26:     "SimpleFriction: V_flowNominal has to be > V_flowLaminar!");
27:   assert(dpNominal>=dpNomMin,
28:     "SimpleFriction: dpNominal has to be > dpLaminar/V_flowLaminar*V_flowNominal!");
29:   k:=(dpNominal - dpNomMin)/(V_flowNominal - V_flowLaminar)^2;
```


## Execution evidence

[Rumoca commands, return codes, integrity hashes, bounded output and metadata](../evidence/db1c40a3e361d88f.json). Baseline: **tool-error**.

No independent runtime override was executed for this target in this audit; this is not a pass.

## Recommended action

Correct the detector/adjudicator for this specific semantic case; do not impose a blanket strictly-positive bound on the library declaration.

## Scope and limitations

A source-level verdict addresses the reported declaration/claim, not every possible connected system. Tests cover 0–0.5 seconds and are not a proof of long-run stability. Shared instances are not distinct root causes. A missing bound, timeout, compiler error or failed nominal run alone never counts as a verified bug or a false positive. Fixes are proposals; no library/compiler implementation was changed.

[Group and related reports](../groups/asserted-friction-flow-order.md) · [Index](../README.md)
