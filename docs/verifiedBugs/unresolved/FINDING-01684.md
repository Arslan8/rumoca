# FINDING-01684: Not yet established as a bug or a false positive

| Field | Value |
|---|---|
| Verdict | unresolved |
| Scope / group | baseline-blocked |
| Model | Modelica.Electrical.Machines.Examples.InductionMachines.IMC_InverterDrive |
| Target | inverter.GoffDiode |
| Student classification | physical-domain-unenforced |
| Original report | [FINDING-imc-inverterdrive-inverter-goffdiode-ruleoff.md](../../v2/bugs/FINDING-imc-inverterdrive-inverter-goffdiode-ruleoff.md) — reviewed as `FINDING-01684-imc-inverterdrive-inverter-goffdiode.md`, which a later run renamed |
| Original SHA-256 | 0ac61383c6cf945ebfd98e392ba7d5816184c9dc0925d9d9fdb39fbda26a7a8f |

## What remains unresolved

The current Rumoca nominal run is tool-error, before any reported perturbation. This prevents causal attribution to this parameter. Source metadata was recovered, but none of the reviewed source proofs or counterexamples establishes this particular claim. A baseline failure/tool limitation is neither confirmation nor a false positive.

## Source evidence

Compiler/source-resolved declaration: `Electrical/PowerConverters/DCAC/Polyphase2Level.mo:13`. Role: `parameter`; binding: `0.0001`; effective min: `None`; effective max: `None`. 

[Electrical/PowerConverters/DCAC/Polyphase2Level.mo — source snapshot](../evidence/sources/9267bcd7585aab4a-Polyphase2Level.mo)

```modelica
11:   parameter SI.Resistance RonDiode=1e-05
12:     "Diode closed resistance";
13:   parameter SI.Conductance GoffDiode=1e-05
14:     "Diode opened conductance";
15:   parameter SI.Voltage VkneeDiode=0 "Diode threshold voltage";
16:   // parameter Boolean useEnable "Enables enable signal connector";
```


## Execution evidence

[Rumoca commands, return codes, integrity hashes, bounded output and metadata](../evidence/f1b3b20d1746a2aa.json). Baseline: **tool-error**.

No independent runtime override was executed for this target in this audit; this is not a pass.

## Recommended action

Resolve the intended parameter domain and enclosing equations; check inherited bounds, final/protected status, guards and aliases. Construct an otherwise-valid source-level witness, establish a clean baseline in a capable engine, then retranslate at the witness and compare with the runtime override. For equality claims use the actual partner value. Do not apply a blanket min>0 fix yet.

## Scope and limitations

A source-level verdict addresses the reported declaration/claim, not every possible connected system. Tests cover 0–0.5 seconds and are not a proof of long-run stability. Shared instances are not distinct root causes. A missing bound, timeout, compiler error or failed nominal run alone never counts as a verified bug or a false positive. Fixes are proposals; no library/compiler implementation was changed.

[Group and related reports](../groups/baseline-blocked.md) · [Index](../README.md)
