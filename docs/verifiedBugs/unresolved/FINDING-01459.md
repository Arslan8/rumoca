# FINDING-01459: Not yet established as a bug or a false positive

| Field | Value |
|---|---|
| Verdict | unresolved |
| Scope / group | baseline-blocked |
| Model | Modelica.Electrical.Machines.Examples.DCMachines.DCPM_withLosses |
| Target | dcpmData2.IaNominal |
| Student classification | divisor-reachable-zero |
| Original report | `FINDING-01459-dcpm-withlosses-dcpmdata2-ianominal.md` — [withdrawn](../../v2/bugs/withdrawn.md); a later run no longer makes this claim |
| Original SHA-256 | 41832e2b6706187d3eb3cf9eff5ee763643d92333d697811ee6cbd2935aa0916 |

## What remains unresolved

The current Rumoca nominal run is tool-error, before any reported perturbation. This prevents causal attribution to this parameter. Source metadata was recovered, but none of the reviewed source proofs or counterexamples establishes this particular claim. A baseline failure/tool limitation is neither confirmation nor a false positive.

## Source evidence

Compiler/source-resolved declaration: `Electrical/Machines/Utilities/ParameterRecords/DcPermanentMagnetData.mo:10`. Role: `parameter`; binding: `100`; effective min: `None`; effective max: `None`. 

[Electrical/Machines/Utilities/ParameterRecords/DcPermanentMagnetData.mo — source snapshot](../evidence/sources/dd335b6f66800523-DcPermanentMagnetData.mo)

```modelica
8:     "Nominal armature voltage"
9:     annotation (Dialog(tab="Nominal parameters"));
10:   parameter SI.Current IaNominal=100
11:     "Nominal armature current (>0..Motor, <0..Generator)"
12:     annotation (Dialog(tab="Nominal parameters"));
13:   parameter SI.AngularVelocity wNominal(displayUnit="rev/min")=
```


## Execution evidence

[Rumoca commands, return codes, integrity hashes, bounded output and metadata](../evidence/1255084b3c3934b8.json). Baseline: **tool-error**.

No independent runtime override was executed for this target in this audit; this is not a pass.

## Recommended action

Resolve the intended parameter domain and enclosing equations; check inherited bounds, final/protected status, guards and aliases. Construct an otherwise-valid source-level witness, establish a clean baseline in a capable engine, then retranslate at the witness and compare with the runtime override. For equality claims use the actual partner value. Do not apply a blanket min>0 fix yet.

## Scope and limitations

A source-level verdict addresses the reported declaration/claim, not every possible connected system. Tests cover 0–0.5 seconds and are not a proof of long-run stability. Shared instances are not distinct root causes. A missing bound, timeout, compiler error or failed nominal run alone never counts as a verified bug or a false positive. Fixes are proposals; no library/compiler implementation was changed.

[Group and related reports](../groups/baseline-blocked.md) · [Index](../README.md)
