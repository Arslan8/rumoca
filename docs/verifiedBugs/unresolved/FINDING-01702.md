# FINDING-01702: Not yet established as a bug or a false positive

| Field | Value |
|---|---|
| Verdict | unresolved |
| Scope / group | baseline-blocked |
| Model | Modelica.Electrical.Machines.Examples.InductionMachines.IMC_InverterDrive |
| Target | inverter.transistor_n.Goff |
| Student classification | physical-domain-unenforced |
| Original report | [FINDING-imc-inverterdrive-inverter-transistor-n-goff-ruleoff.md](../../v2/bugs/FINDING-imc-inverterdrive-inverter-transistor-n-goff-ruleoff.md) — reviewed as `FINDING-01702-imc-inverterdrive-inverter-transistor-n-goff.md`, which a later run renamed |
| Original SHA-256 | a5aeacce0b08244f4f9db4335858e3b941ed861173733b239a0a925d247cfb1a |

## What remains unresolved

The current Rumoca nominal run is tool-error, before any reported perturbation. This prevents causal attribution to this parameter. Source metadata was recovered, but none of the reviewed source proofs or counterexamples establishes this particular claim. A baseline failure/tool limitation is neither confirmation nor a false positive.

## Source evidence

Compiler/source-resolved declaration: `Electrical/Polyphase/Ideal/IdealGTOThyristor.mo:6`. Role: `parameter`; binding: `fill(inverter.GoffTransistor, inverter.m)`; effective min: `zeros(3)`; effective max: `None`. 

[Electrical/Polyphase/Ideal/IdealGTOThyristor.mo — source snapshot](../evidence/sources/4a077a8df07fb74c-IdealGTOThyristor.mo)

```modelica
4:   parameter SI.Resistance Ron[m](final min=zeros(m), start=
5:         fill(1e-5, m)) "Closed thyristor resistance";
6:   parameter SI.Conductance Goff[m](final min=zeros(m), start=
7:         fill(1e-5, m)) "Opened thyristor conductance";
8:   parameter SI.Voltage Vknee[m](final min=zeros(m), start=
9:         zeros(m)) "Threshold voltage";
```


## Execution evidence

[Rumoca commands, return codes, integrity hashes, bounded output and metadata](../evidence/f1b3b20d1746a2aa.json). Baseline: **tool-error**.

No independent runtime override was executed for this target in this audit; this is not a pass.

## Recommended action

Resolve the intended parameter domain and enclosing equations; check inherited bounds, final/protected status, guards and aliases. Construct an otherwise-valid source-level witness, establish a clean baseline in a capable engine, then retranslate at the witness and compare with the runtime override. For equality claims use the actual partner value. Do not apply a blanket min>0 fix yet.

## Scope and limitations

A source-level verdict addresses the reported declaration/claim, not every possible connected system. Tests cover 0–0.5 seconds and are not a proof of long-run stability. Shared instances are not distinct root causes. A missing bound, timeout, compiler error or failed nominal run alone never counts as a verified bug or a false positive. Fixes are proposals; no library/compiler implementation was changed.

[Group and related reports](../groups/baseline-blocked.md) · [Index](../README.md)
