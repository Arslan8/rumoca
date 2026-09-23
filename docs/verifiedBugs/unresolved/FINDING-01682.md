# FINDING-01682: Not yet established as a bug or a false positive

| Field | Value |
|---|---|
| Verdict | unresolved |
| Scope / group | baseline-blocked |
| Model | Modelica.Electrical.Machines.Examples.InductionMachines.IMC_InverterDrive |
| Target | inverter.GoffTransistor |
| Student classification | physical-domain-unenforced |
| Original report | [FINDING-imc-inverterdrive-inverter-gofftransistor-ruleoff.md](../../v2/bugs/FINDING-imc-inverterdrive-inverter-gofftransistor-ruleoff.md) — reviewed as `FINDING-01682-imc-inverterdrive-inverter-gofftransistor.md`, which a later run renamed |
| Original SHA-256 | f3e89ffb8f09263bdc67f2d039d4e7c87c3ea8305bb4785d50fef4428d17e634 |

## What remains unresolved

The current Rumoca nominal run is tool-error, before any reported perturbation. This prevents causal attribution to this parameter. Source metadata was recovered, but none of the reviewed source proofs or counterexamples establishes this particular claim. A baseline failure/tool limitation is neither confirmation nor a false positive.

## Source evidence

Compiler/source-resolved declaration: `Electrical/PowerConverters/DCAC/Polyphase2Level.mo:7`. Role: `parameter`; binding: `0.0001`; effective min: `None`; effective max: `None`. 

[Electrical/PowerConverters/DCAC/Polyphase2Level.mo — source snapshot](../evidence/sources/9267bcd7585aab4a-Polyphase2Level.mo)

```modelica
5:   parameter SI.Resistance RonTransistor=1e-05
6:     "Transistor closed resistance";
7:   parameter SI.Conductance GoffTransistor=1e-05
8:     "Transistor opened conductance";
9:   parameter SI.Voltage VkneeTransistor=0
10:     "Transistor threshold voltage";
```


## Execution evidence

[Rumoca commands, return codes, integrity hashes, bounded output and metadata](../evidence/f1b3b20d1746a2aa.json). Baseline: **tool-error**.

No independent runtime override was executed for this target in this audit; this is not a pass.

## Recommended action

Resolve the intended parameter domain and enclosing equations; check inherited bounds, final/protected status, guards and aliases. Construct an otherwise-valid source-level witness, establish a clean baseline in a capable engine, then retranslate at the witness and compare with the runtime override. For equality claims use the actual partner value. Do not apply a blanket min>0 fix yet.

## Scope and limitations

A source-level verdict addresses the reported declaration/claim, not every possible connected system. Tests cover 0–0.5 seconds and are not a proof of long-run stability. Shared instances are not distinct root causes. A missing bound, timeout, compiler error or failed nominal run alone never counts as a verified bug or a false positive. Fixes are proposals; no library/compiler implementation was changed.

[Group and related reports](../groups/baseline-blocked.md) · [Index](../README.md)
