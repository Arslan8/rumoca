# FINDING-04612: Zero stored fluid mass is explicitly supported

| Field | Value |
|---|---|
| Verdict | false-positives |
| Scope / group | zero-fluid-inventory |
| Model | Modelica.Thermal.FluidHeatFlow.Examples.PumpAndValve |
| Target | valve.m |
| Student classification | physical-bound-permits-zero |
| Original report | [FINDING-pumpandvalve-valve-m-zerolimit.md](../../v2/bugs/FINDING-pumpandvalve-valve-m-zerolimit.md) — reviewed as `FINDING-04612-pumpandvalve-valve-m.md`, which a later run renamed |
| Original SHA-256 | 0c355fe09d8978ca7f7cd8787989dbe764375f2c71f7fbd18a1ce35413dfb876 |

## Why this is a false positive

TwoPort explicitly documents that m=0 neglects the temperature transient. Its equation uses if m>small then m*medium.cv*der(T) else an algebraic zero-storage energy balance. Zero is handled by a dedicated branch; a blanket strictly-positive mass rule is contrary to the component contract.

## Source evidence

Compiler/source-resolved declaration: `Thermal/FluidHeatFlow/BaseClasses/TwoPort.mo:5`. Role: `parameter`; binding: `0`; effective min: `0`; effective max: `None`. 

[Thermal/FluidHeatFlow/BaseClasses/TwoPort.mo — source snapshot](../evidence/sources/04f0a49d716ce1bd-TwoPort.mo)

```modelica
3:   parameter FluidHeatFlow.Media.Medium medium=FluidHeatFlow.Media.Medium()
4:     "Medium in the component" annotation (choicesAllMatching=true);
5:   parameter SI.Mass m(start=1) "Mass of medium";
6:   parameter SI.Temperature T0(start=293.15, displayUnit="degC")
7:     "Initial temperature of medium"
8:     annotation(Dialog(enable=m>Modelica.Constants.small));
```

[Thermal/FluidHeatFlow/BaseClasses/TwoPort.mo — source snapshot](../evidence/sources/04f0a49d716ce1bd-TwoPort.mo)

```modelica
2: partial model TwoPort "Partial model of two port"
3:   parameter FluidHeatFlow.Media.Medium medium=FluidHeatFlow.Media.Medium()
4:     "Medium in the component" annotation (choicesAllMatching=true);
5:   parameter SI.Mass m(start=1) "Mass of medium";
6:   parameter SI.Temperature T0(start=293.15, displayUnit="degC")
7:     "Initial temperature of medium"
8:     annotation(Dialog(enable=m>Modelica.Constants.small));
9:   parameter Boolean T0fixed=false
10:     "Initial temperature guess value or fixed"
11:   annotation(choices(checkBox=true),Dialog(enable=m>Modelica.Constants.small));
12:   parameter Real tapT(final min=0, final max=1)=1
```

[Thermal/FluidHeatFlow/BaseClasses/TwoPort.mo — source snapshot](../evidence/sources/04f0a49d716ce1bd-TwoPort.mo)

```modelica
43:   if m>Modelica.Constants.small then
44:     flowPort_a.H_flow + flowPort_b.H_flow + Q_flow = m*medium.cv*der(T);
45:   else
46:     flowPort_a.H_flow + flowPort_b.H_flow + Q_flow = 0;
47:   end if;
48:   // mass flow a->b mixing rule at a, energy flow at b defined by medium's temperature
49:   // mass flow b->a mixing rule at b, energy flow at a defined by medium's temperature
50:   flowPort_a.H_flow = semiLinear(flowPort_a.m_flow,flowPort_a.h,h);
51:   flowPort_b.H_flow = semiLinear(flowPort_b.m_flow,flowPort_b.h,h);
52: annotation (Documentation(info="<html>
53: <p>Partial model with two flowPorts.</p>
54: <p>Possible heat exchange with the ambient is defined by Q_flow; setting this = 0 means no energy exchange.</p>
55: <p>
56: Setting parameter m (mass of medium within pipe) to zero
57: leads to neglect of temperature transient cv*m*der(T).</p>
58: <p>Mixing rule is applied.</p>
59: <p>Parameter 0 &lt; tapT &lt; 1 defines temperature of heatPort between medium's inlet and outlet temperature.</p>
60: </html>"));
61: end TwoPort;
```


## Execution evidence

[Rumoca commands, return codes, integrity hashes, bounded output and metadata](../evidence/db1c40a3e361d88f.json). Baseline: **tool-error**.

No independent runtime override was executed for this target in this audit; this is not a pass.

## Recommended action

Correct the detector/adjudicator for this specific semantic case; do not impose a blanket strictly-positive bound on the library declaration.

## Scope and limitations

A source-level verdict addresses the reported declaration/claim, not every possible connected system. Tests cover 0–0.5 seconds and are not a proof of long-run stability. Shared instances are not distinct root causes. A missing bound, timeout, compiler error or failed nominal run alone never counts as a verified bug or a false positive. Fixes are proposals; no library/compiler implementation was changed.

[Group and related reports](../groups/zero-fluid-inventory.md) · [Index](../README.md)
