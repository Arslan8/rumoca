# FINDING-01746: Not yet established as a bug or a false positive

| Field | Value |
|---|---|
| Verdict | unresolved |
| Scope / group | baseline-blocked |
| Model | Modelica.Electrical.Machines.Examples.InductionMachines.IMC_InverterDrive |
| Target | fNominal |
| Student classification | divisor-reachable-zero |
| Original report | `FINDING-01746-imc-inverterdrive-fnominal.md` — [withdrawn](../../v2/bugs/withdrawn.md); a later run no longer makes this claim |
| Original SHA-256 | 53f5996e629e03d5dc12f8601f8da074c171f742214a58ff500815164de74f76 |

## What remains unresolved

The current Rumoca nominal run is tool-error, before any reported perturbation. This prevents causal attribution to this parameter. Source metadata was recovered, but none of the reviewed source proofs or counterexamples establishes this particular claim. A baseline failure/tool limitation is neither confirmation nor a false positive.

## Source evidence

Compiler/source-resolved declaration: `Electrical/Machines/Examples/InductionMachines/IMC_InverterDrive.mo:10`. Role: `parameter`; binding: `50`; effective min: `None`; effective max: `None`. 

[Electrical/Machines/Examples/InductionMachines/IMC_InverterDrive.mo — source snapshot](../evidence/sources/35d82484be6d95ca-IMC_InverterDrive.mo)

```modelica
8:   parameter SI.Voltage VNominal=400
9:     "Nominal RMS voltage per phase";
10:   parameter SI.Frequency fNominal=50 "Nominal frequency";
11:   parameter SI.Resistance RGrid=10e-3 "Grid choke resistance";
12:   parameter SI.Inductance LGrid=500e-6 "Grid choke inductance";
13:   parameter SI.Voltage VDC=factorY2DC(m)*VNominal/sqrt(3) "Theoretical DC voltage";
```


## Execution evidence

[Rumoca commands, return codes, integrity hashes, bounded output and metadata](../evidence/f1b3b20d1746a2aa.json). Baseline: **tool-error**.

No independent runtime override was executed for this target in this audit; this is not a pass.

## Recommended action

Resolve the intended parameter domain and enclosing equations; check inherited bounds, final/protected status, guards and aliases. Construct an otherwise-valid source-level witness, establish a clean baseline in a capable engine, then retranslate at the witness and compare with the runtime override. For equality claims use the actual partner value. Do not apply a blanket min>0 fix yet.

## Scope and limitations

A source-level verdict addresses the reported declaration/claim, not every possible connected system. Tests cover 0–0.5 seconds and are not a proof of long-run stability. Shared instances are not distinct root causes. A missing bound, timeout, compiler error or failed nominal run alone never counts as a verified bug or a false positive. Fixes are proposals; no library/compiler implementation was changed.

[Group and related reports](../groups/baseline-blocked.md) · [Index](../README.md)
