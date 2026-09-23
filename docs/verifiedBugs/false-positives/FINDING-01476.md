# FINDING-01476: Zero optional leakage inductance is intentional

| Field | Value |
|---|---|
| Verdict | false-positives |
| Scope / group | zero-stray-inductance |
| Model | Modelica.Electrical.Machines.Examples.DCMachines.DCSE_SinglePhase |
| Target | dcse.Lesigma |
| Student classification | physical-invariant-violated |
| Original report | [FINDING-dcse-singlephase-dcse-lesigma-zerolimit.md](../../v2/bugs/FINDING-dcse-singlephase-dcse-lesigma-zerolimit.md) — reviewed as `FINDING-01476-dcse-singlephase-dcse-lesigma.md`, which a later run renamed |
| Original SHA-256 | edfbbe0542573758904c52025192785b085d070ecbcb314b89cff0b5b676adbc |

## Why this is a false positive

The derived stray inductance is Lesigma=Le*sigmae; sigmae=0 represents no stray part. It is passed into InductorDC, whose equation is v=if quasiStatic then 0 else L*der(i). At L=0 the element has zero voltage drop; it is not an unconditional source-level 1/L. A default zero optional leakage term is not an invariant violation.

## Source evidence

Compiler/source-resolved declaration: `Electrical/Machines/BasicMachines/DCMachines/DC_SeriesExcited.mo:86`. Role: `parameter`; binding: `(dcse.Le * dcse.sigmae)`; effective min: `None`; effective max: `None`. 

[Electrical/Machines/BasicMachines/DCMachines/DC_SeriesExcited.mo — source snapshot](../evidence/sources/d5e46cdc01821f26-DC_SeriesExcited.mo)

```modelica
84:   final parameter SI.Inductance Lme=Le*(1 - sigmae)
85:     "Main part of excitation inductance";
86:   final parameter SI.Inductance Lesigma=Le*sigmae
87:     "Stray part of excitation inductance" annotation (Evaluate=true);
88: equation
89:   connect(airGapDC.pin_ap, la.n) annotation (Line(
```

[Electrical/Machines/BasicMachines/Components/InductorDC.mo — source snapshot](../evidence/sources/72ab8f755e24ff0e-InductorDC.mo)

```modelica
5:   parameter SI.Inductance L(start=1) "Inductance";
6:   parameter Boolean quasiStatic(start=false)
7:     "No electrical transients if true" annotation (Evaluate=true);
8: equation
9:   v = if quasiStatic then 0 else L*der(i);
```

[Electrical/Machines/BasicMachines/DCMachines/DC_SeriesExcited.mo — source snapshot](../evidence/sources/d5e46cdc01821f26-DC_SeriesExcited.mo)

```modelica
84:   final parameter SI.Inductance Lme=Le*(1 - sigmae)
85:     "Main part of excitation inductance";
86:   final parameter SI.Inductance Lesigma=Le*sigmae
87:     "Stray part of excitation inductance" annotation (Evaluate=true);
88: equation
89:   connect(airGapDC.pin_ap, la.n) annotation (Line(
```


## Execution evidence

[Rumoca commands, return codes, integrity hashes, bounded output and metadata](../evidence/f00103fd4bc29b1a.json). Baseline: **tool-error**.

No independent runtime override was executed for this target in this audit; this is not a pass.

## Recommended action

Correct the detector/adjudicator for this specific semantic case; do not impose a blanket strictly-positive bound on the library declaration.

## Scope and limitations

A source-level verdict addresses the reported declaration/claim, not every possible connected system. Tests cover 0–0.5 seconds and are not a proof of long-run stability. Shared instances are not distinct root causes. A missing bound, timeout, compiler error or failed nominal run alone never counts as a verified bug or a false positive. Fixes are proposals; no library/compiler implementation was changed.

[Group and related reports](../groups/zero-stray-inductance.md) · [Index](../README.md)
