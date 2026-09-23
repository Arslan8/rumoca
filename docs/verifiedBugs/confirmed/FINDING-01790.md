# FINDING-01790: Zero nominal frequency divides induction-machine data

| Field | Value |
|---|---|
| Verdict | confirmed |
| Scope / group | induction-data-frequency |
| Model | Modelica.Electrical.Machines.Examples.InductionMachines.IMC_Inverter |
| Target | aimcData.fsNominal |
| Student classification | divisor-reachable-zero |
| Original report | [FINDING-imc-inverter-aimcdata-fsnominal-divzero-2.md](../../v2/bugs/FINDING-imc-inverter-aimcdata-fsnominal-divzero-2.md) — reviewed as `FINDING-01790-imc-inverter-aimcdata-fsnominal.md`, which a later run renamed |
| Original SHA-256 | 04eba60978fdce4c9e20aea4516bf798bdd333b180b2dec63a21952dff17e536 |

## Verification and root cause

InductionMachineData leaves fsNominal without a positive bound, while Lssigma divides by 2*pi*fsNominal and multiple loss-reference angular velocities are proportional to it. The direct Lssigma binding is undefined at zero. The report instances share this record defect; tool-blocked full machines are not counted as successful runtime reproductions.

## Source evidence

Compiler/source-resolved declaration: `Electrical/Machines/Utilities/ParameterRecords/InductionMachineData.mo:9`. Role: `parameter`; binding: `50`; effective min: `None`; effective max: `None`. 

[Electrical/Machines/Utilities/ParameterRecords/InductionMachineData.mo — source snapshot](../evidence/sources/8d312108fd6330eb-InductionMachineData.mo)

```modelica
7:   parameter SI.Inertia Js=Jr "Stator's moment of inertia";
8:   parameter Integer p(min=1) = 2 "Number of pole pairs (Integer)";
9:   parameter SI.Frequency fsNominal=50 "Nominal frequency";
10:   parameter SI.Resistance Rs=0.03
11:     "Stator resistance per phase at TRef"
12:     annotation (Dialog(tab="Nominal resistances and inductances"));
```

[Electrical/Machines/Utilities/ParameterRecords/InductionMachineData.mo — source snapshot](../evidence/sources/8d312108fd6330eb-InductionMachineData.mo)

```modelica
4:   import Modelica.Constants.pi;
5:   parameter Integer m=3 "Number of phases" annotation(Evaluate=true);
6:   parameter SI.Inertia Jr=0.29 "Rotor's moment of inertia";
7:   parameter SI.Inertia Js=Jr "Stator's moment of inertia";
8:   parameter Integer p(min=1) = 2 "Number of pole pairs (Integer)";
9:   parameter SI.Frequency fsNominal=50 "Nominal frequency";
10:   parameter SI.Resistance Rs=0.03
11:     "Stator resistance per phase at TRef"
12:     annotation (Dialog(tab="Nominal resistances and inductances"));
13:   parameter SI.Temperature TsRef=293.15
14:     "Reference temperature of stator resistance"
15:     annotation (Dialog(tab="Nominal resistances and inductances"));
16:   parameter Machines.Thermal.LinearTemperatureCoefficient20 alpha20s=0
17:     "Temperature coefficient of stator resistance at 20 degC"
18:     annotation (Dialog(tab="Nominal resistances and inductances"));
19:   parameter Real effectiveStatorTurns=1 "Effective number of stator turns";
20:   parameter SI.Inductance Lszero=Lssigma
21:     "Stator zero sequence inductance"
22:     annotation (Dialog(tab="Nominal resistances and inductances"));
23:   parameter SI.Inductance Lssigma=3*(1 - sqrt(1 - 0.0667))/
24:       (2*pi*fsNominal) "Stator stray inductance per phase"
25:     annotation (Dialog(tab="Nominal resistances and inductances"));
```

[Electrical/Machines/Utilities/ParameterRecords/InductionMachineData.mo — source snapshot](../evidence/sources/8d312108fd6330eb-InductionMachineData.mo)

```modelica
26:   parameter Real ratioCommonStatorLeakage(final min=0, final max=1)=1
27:     "Ratio of common stray inductance / total stray inductance of stator winding"
28:     annotation (Dialog(tab="Nominal resistances and inductances"));
29:   parameter Machines.Losses.FrictionParameters frictionParameters(PRef=0, wRef=
30:         2*pi*fsNominal/p) "Friction loss parameter record"
31:     annotation (Dialog(tab="Losses"));
32:   parameter Machines.Losses.CoreParameters statorCoreParameters(
33:     m=m,
34:     PRef=0,
35:     VRef=100,
36:     wRef=2*pi*fsNominal)
37:     "Stator core loss parameter record; all parameters refer to stator side"
38:     annotation (Dialog(tab="Losses"));
39:   parameter Machines.Losses.StrayLoadParameters strayLoadParameters(
40:     PRef=0,
41:     IRef=100,
42:     wRef=2*pi*fsNominal/p) "Stray load losses" annotation (Dialog(tab="Losses"));
```


## Execution evidence

[Rumoca commands, return codes, integrity hashes, bounded output and metadata](../evidence/8e3358d86efa2aa5.json). Baseline: **tool-error**.

No independent runtime override was executed for this target in this audit; this is not a pass.

## Proposed fix

Set a meaningful positive lower bound on fsNominal and validate fsNominal>0 before derived data bindings are evaluated. If DC/zero-frequency machine data are needed, provide a separate formulation rather than evaluating the AC per-unit conversion at zero.

## Fix validation

Project the actual record in a minimal model at nominal, zero, negative, and small positive fsNominal; invalid values must report the frequency domain before derived inductance evaluation.

## Scope and limitations

A source-level verdict addresses the reported declaration/claim, not every possible connected system. Tests cover 0–0.5 seconds and are not a proof of long-run stability. Shared instances are not distinct root causes. A missing bound, timeout, compiler error or failed nominal run alone never counts as a verified bug or a false positive. Fixes are proposals; no library/compiler implementation was changed.

[Group and related reports](../groups/induction-data-frequency.md) · [Index](../README.md)
