# FINDING-01575: Zero stator leakage inductance is supported

| Field | Value |
|---|---|
| Verdict | false-positives |
| Scope / group | ideal-stator-leakage |
| Model | Modelica.Electrical.Machines.Examples.InductionMachines.IMC_DOL |
| Target | aimc.Lssigma |
| Student classification | physical-domain-unenforced |
| Original report | [FINDING-imc-dol-aimc-lssigma-intent.md](../../v2/bugs/FINDING-imc-dol-aimc-lssigma-intent.md) — reviewed as `FINDING-01575-imc-dol-aimc-lssigma.md`, which a later run renamed |
| Original SHA-256 | 48b936d31a3033e8e68b360d0e5d2ea3da0b47ed1a8837f7eab6fb7a6cca86fd |

## Why this is a false positive

Lszero and Lssigma are passed to scalar/space-phasor inductors whose equations multiply current derivatives by L. Zero is the ideal no-leakage voltage-drop limit; there is no intrinsic reciprocal. The separate fsNominal-derived default formula can still require a positive nominal frequency.

## Source evidence

Compiler/source-resolved declaration: `Electrical/Machines/Interfaces/PartialBasicInductionMachine.mo:23`. Role: `parameter`; binding: `aimcData.Lssigma`; effective min: `None`; effective max: `None`. 

[Electrical/Machines/Interfaces/PartialBasicInductionMachine.mo — source snapshot](../evidence/sources/9baf5b1d5152b001-PartialBasicInductionMachine.mo)

```modelica
21:     "Stator zero sequence inductance"
22:     annotation (Dialog(tab="Nominal resistances and inductances"));
23:   parameter SI.Inductance Lssigma(start=3*ZsRef*(1 - sqrt(1 -
24:         0.0667))/(2*pi*fsNominal)) "Stator stray inductance per phase"
25:     annotation (Dialog(tab="Nominal resistances and inductances"));
26:   extends PartialBasicMachine(
```

[Electrical/Machines/Interfaces/PartialBasicInductionMachine.mo — source snapshot](../evidence/sources/9baf5b1d5152b001-PartialBasicInductionMachine.mo)

```modelica
15:     "Reference temperature of stator resistance"
16:     annotation (Dialog(tab="Nominal resistances and inductances"));
17:   parameter Machines.Thermal.LinearTemperatureCoefficient20 alpha20s(start=0)
18:     "Temperature coefficient of stator resistance at 20 degC"
19:     annotation (Dialog(tab="Nominal resistances and inductances"));
20:   parameter SI.Inductance Lszero=Lssigma
21:     "Stator zero sequence inductance"
22:     annotation (Dialog(tab="Nominal resistances and inductances"));
23:   parameter SI.Inductance Lssigma(start=3*ZsRef*(1 - sqrt(1 -
24:         0.0667))/(2*pi*fsNominal)) "Stator stray inductance per phase"
25:     annotation (Dialog(tab="Nominal resistances and inductances"));
```

[Electrical/Machines/Interfaces/PartialBasicInductionMachine.mo — source snapshot](../evidence/sources/9baf5b1d5152b001-PartialBasicInductionMachine.mo)

```modelica
76:     final useHeatPort=true,
77:     final T=fill(TsRef, m)) annotation (Placement(transformation(extent={{
78:             60,70},{40,90}})));
79:   Machines.BasicMachines.Components.Inductor lssigma(final L=fill(Lssigma, 2))
80:     annotation (Placement(transformation(
81:         extent={{-10,-10},{10,10}},
82:         rotation=270,
83:         origin={20,20})));
84:   Modelica.Electrical.Analog.Basic.Inductor lszero(final L=Lszero)
85:     annotation (Placement(transformation(extent={{0,40},{-20,60}})));
86:   Machines.Losses.InductionMachines.Core statorCore(
```

[Electrical/Analog/Basic/Inductor.mo — source snapshot](../evidence/sources/fff3148b5c6bf96b-Inductor.mo)

```modelica
2: model Inductor "Ideal linear electrical inductor"
3:   extends Interfaces.OnePort(i(start=0));
4:   parameter SI.Inductance L(start=1) "Inductance";
5: 
6: equation
7:   L*der(i) = v;
8:   annotation (
9:     Documentation(info="<html>
10: <p>The linear inductor connects the branch voltage <em>v</em> with the branch current <em>i</em> by <em>v = L * di/dt</em>. The Inductance <em>L</em> is allowed to be positive, or zero.</p>
11: 
```


## Execution evidence

[Rumoca commands, return codes, integrity hashes, bounded output and metadata](../evidence/3bb307101f6982f2.json). Baseline: **tool-error**.

No independent runtime override was executed for this target in this audit; this is not a pass.

## Recommended action

Correct the detector/adjudicator for this specific semantic case; do not impose a blanket strictly-positive bound on the library declaration.

## Scope and limitations

A source-level verdict addresses the reported declaration/claim, not every possible connected system. Tests cover 0–0.5 seconds and are not a proof of long-run stability. Shared instances are not distinct root causes. A missing bound, timeout, compiler error or failed nominal run alone never counts as a verified bug or a false positive. Fixes are proposals; no library/compiler implementation was changed.

[Group and related reports](../groups/ideal-stator-leakage.md) · [Index](../README.md)
