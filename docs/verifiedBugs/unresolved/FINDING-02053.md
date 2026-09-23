# FINDING-02053: Not yet established as a bug or a false positive

| Field | Value |
|---|---|
| Verdict | unresolved |
| Scope / group | baseline-blocked |
| Model | Modelica.Electrical.Machines.Examples.InductionMachines.IMS_Start |
| Target | Rstart |
| Student classification | physical-domain-unenforced |
| Original report | [FINDING-ims-start-rstart-intent.md](../../v2/bugs/FINDING-ims-start-rstart-intent.md) — reviewed as `FINDING-02053-ims-start-rstart.md`, which a later run renamed |
| Original SHA-256 | 238db61abbba8d0ea01d4dd461797f68516a8a2919509890c5cebb3910caa71e |

## What remains unresolved

The current Rumoca nominal run is tool-error, before any reported perturbation. This prevents causal attribution to this parameter. Source metadata was recovered, but none of the reviewed source proofs or counterexamples establishes this particular claim. A baseline failure/tool limitation is neither confirmation nor a false positive.

## Source evidence

Compiler/source-resolved declaration: `Electrical/Machines/Examples/InductionMachines/IMS_Start.mo:9`. Role: `parameter`; binding: `(0.16 / (aimsData.turnsRatio ^ 2))`; effective min: `None`; effective max: `None`. 

[Electrical/Machines/Examples/InductionMachines/IMS_Start.mo — source snapshot](../evidence/sources/439faf5a498dc64f-IMS_Start.mo)

```modelica
7:   parameter SI.Frequency fNominal=50 "Nominal frequency";
8:   parameter SI.Time tStart1=0.1 "Start time";
9:   parameter SI.Resistance Rstart=0.16/aimsData.turnsRatio^2
10:     "Starting resistance";
11:   parameter SI.Time tStart2=1.0
12:     "Start time of shorting starting resistance";
```


## Execution evidence

[Rumoca commands, return codes, integrity hashes, bounded output and metadata](../evidence/2804e4f64ad6a33e.json). Baseline: **tool-error**.

No independent runtime override was executed for this target in this audit; this is not a pass.

## Recommended action

Resolve the intended parameter domain and enclosing equations; check inherited bounds, final/protected status, guards and aliases. Construct an otherwise-valid source-level witness, establish a clean baseline in a capable engine, then retranslate at the witness and compare with the runtime override. For equality claims use the actual partner value. Do not apply a blanket min>0 fix yet.

## Scope and limitations

A source-level verdict addresses the reported declaration/claim, not every possible connected system. Tests cover 0–0.5 seconds and are not a proof of long-run stability. Shared instances are not distinct root causes. A missing bound, timeout, compiler error or failed nominal run alone never counts as a verified bug or a false positive. Fixes are proposals; no library/compiler implementation was changed.

[Group and related reports](../groups/baseline-blocked.md) · [Index](../README.md)
