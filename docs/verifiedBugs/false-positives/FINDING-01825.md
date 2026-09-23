# FINDING-01825: Zero leakage inductance is a supported ideal limit

| Field | Value |
|---|---|
| Verdict | false-positives |
| Scope / group | zero-machine-data-leakage |
| Model | Modelica.Electrical.Machines.Examples.InductionMachines.IMC_Steinmetz |
| Target | aimcData.Lszero |
| Student classification | physical-domain-unenforced |
| Original report | [FINDING-imc-steinmetz-aimcdata-lszero-intent.md](../../v2/bugs/FINDING-imc-steinmetz-aimcdata-lszero-intent.md) — reviewed as `FINDING-01825-imc-steinmetz-aimcdata-lszero.md`, which a later run renamed |
| Original SHA-256 | ce06bd0f907f1d50c599496b0aebaef18178801f711015109e76ea9af93b3b1b |

## Why this is a false positive

Lszero and Lssigma represent zero-sequence/stray inductance. They are forwarded to inductor equations that multiply derivatives by L; zero removes the leakage voltage drop. The Basic.Inductor contract explicitly permits zero. This does not excuse fsNominal=0 in the default formula, which is documented as a separate confirmed frequency bug.

## Source evidence

Compiler/source-resolved declaration: `Electrical/Machines/Utilities/ParameterRecords/InductionMachineData.mo:20`. Role: `parameter`; binding: `aimcData.Lssigma`; effective min: `None`; effective max: `None`. 

[Electrical/Machines/Utilities/ParameterRecords/InductionMachineData.mo — source snapshot](../evidence/sources/8d312108fd6330eb-InductionMachineData.mo)

```modelica
18:     annotation (Dialog(tab="Nominal resistances and inductances"));
19:   parameter Real effectiveStatorTurns=1 "Effective number of stator turns";
20:   parameter SI.Inductance Lszero=Lssigma
21:     "Stator zero sequence inductance"
22:     annotation (Dialog(tab="Nominal resistances and inductances"));
23:   parameter SI.Inductance Lssigma=3*(1 - sqrt(1 - 0.0667))/
```

[Electrical/Machines/Utilities/ParameterRecords/InductionMachineData.mo — source snapshot](../evidence/sources/8d312108fd6330eb-InductionMachineData.mo)

```modelica
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

[Rumoca commands, return codes, integrity hashes, bounded output and metadata](../evidence/00227f080db37cf1.json). Baseline: **tool-error**.

No independent runtime override was executed for this target in this audit; this is not a pass.

## Recommended action

Correct the detector/adjudicator for this specific semantic case; do not impose a blanket strictly-positive bound on the library declaration.

## Scope and limitations

A source-level verdict addresses the reported declaration/claim, not every possible connected system. Tests cover 0–0.5 seconds and are not a proof of long-run stability. Shared instances are not distinct root causes. A missing bound, timeout, compiler error or failed nominal run alone never counts as a verified bug or a false positive. Fixes are proposals; no library/compiler implementation was changed.

[Group and related reports](../groups/zero-machine-data-leakage.md) · [Index](../README.md)
