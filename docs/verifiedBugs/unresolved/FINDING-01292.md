# FINDING-01292: Not yet established as a bug or a false positive

| Field | Value |
|---|---|
| Verdict | unresolved |
| Scope / group | baseline-blocked |
| Model | Modelica.Electrical.Machines.Examples.DCMachines.DCPM_CurrentControlled |
| Target | dcpmData.Ra |
| Student classification | divisor-reachable-zero |
| Original report | [FINDING-dcpm-currentcontrolled-dcpmdata-ra-unbounded.md](../../v2/bugs/FINDING-dcpm-currentcontrolled-dcpmdata-ra-unbounded.md) — reviewed as `FINDING-01292-dcpm-currentcontrolled-dcpmdata-ra.md`, which a later run renamed |
| Original SHA-256 | af4ebce69c3f4007d250631a44e345edbd4bf3d3d4f359a74374dec5328bb0c3 |

## What remains unresolved

The current Rumoca nominal run is tool-error, before any reported perturbation. This prevents causal attribution to this parameter. Source metadata was recovered, but none of the reviewed source proofs or counterexamples establishes this particular claim. A baseline failure/tool limitation is neither confirmation nor a false positive.

## Source evidence

Compiler/source-resolved declaration: `Electrical/Machines/Utilities/ParameterRecords/DcPermanentMagnetData.mo:19`. Role: `parameter`; binding: `0.05`; effective min: `None`; effective max: `None`. 

[Electrical/Machines/Utilities/ParameterRecords/DcPermanentMagnetData.mo — source snapshot](../evidence/sources/dd335b6f66800523-DcPermanentMagnetData.mo)

```modelica
17:     "Nominal armature temperature"
18:     annotation (Dialog(tab="Nominal parameters"));
19:   parameter SI.Resistance Ra=0.05
20:     "Armature resistance at TaRef"
21:     annotation (Dialog(tab="Armature"));
22:   parameter SI.Temperature TaRef=293.15
```


## Execution evidence

[Rumoca commands, return codes, integrity hashes, bounded output and metadata](../evidence/77b1c55854f32a4c.json). Baseline: **tool-error**.

No independent runtime override was executed for this target in this audit; this is not a pass.

## Recommended action

Resolve the intended parameter domain and enclosing equations; check inherited bounds, final/protected status, guards and aliases. Construct an otherwise-valid source-level witness, establish a clean baseline in a capable engine, then retranslate at the witness and compare with the runtime override. For equality claims use the actual partner value. Do not apply a blanket min>0 fix yet.

## Scope and limitations

A source-level verdict addresses the reported declaration/claim, not every possible connected system. Tests cover 0–0.5 seconds and are not a proof of long-run stability. Shared instances are not distinct root causes. A missing bound, timeout, compiler error or failed nominal run alone never counts as a verified bug or a false positive. Fixes are proposals; no library/compiler implementation was changed.

[Group and related reports](../groups/baseline-blocked.md) · [Index](../README.md)
