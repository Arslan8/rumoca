# FINDING-01297: Not yet established as a bug or a false positive

| Field | Value |
|---|---|
| Verdict | unresolved |
| Scope / group | baseline-blocked |
| Model | Modelica.Electrical.Machines.Examples.DCMachines.DCPM_CurrentControlled |
| Target | dcpmData.La |
| Student classification | divisor-reachable-zero |
| Original report | [FINDING-dcpm-currentcontrolled-dcpmdata-la-intent.md](../../v2/bugs/FINDING-dcpm-currentcontrolled-dcpmdata-la-intent.md) — reviewed as `FINDING-01297-dcpm-currentcontrolled-dcpmdata-la.md`, which a later run renamed |
| Original SHA-256 | c20bfc169b571460eb05fc5c67af64edd9a46ddae5a3d0bf26530662fdda628c |

## What remains unresolved

The current Rumoca nominal run is tool-error, before any reported perturbation. This prevents causal attribution to this parameter. Source metadata was recovered, but none of the reviewed source proofs or counterexamples establishes this particular claim. A baseline failure/tool limitation is neither confirmation nor a false positive.

## Source evidence

Compiler/source-resolved declaration: `Electrical/Machines/Utilities/ParameterRecords/DcPermanentMagnetData.mo:28`. Role: `parameter`; binding: `0.0015`; effective min: `None`; effective max: `None`. 

[Electrical/Machines/Utilities/ParameterRecords/DcPermanentMagnetData.mo — source snapshot](../evidence/sources/dd335b6f66800523-DcPermanentMagnetData.mo)

```modelica
26:     "Temperature coefficient of armature resistance"
27:     annotation (Dialog(tab="Armature"));
28:   parameter SI.Inductance La=0.0015 "Armature inductance"
29:     annotation (Dialog(tab="Armature"));
30:   parameter Machines.Losses.FrictionParameters frictionParameters(PRef=0, wRef=
31:         wNominal) "Friction loss parameter record"
```


## Execution evidence

[Rumoca commands, return codes, integrity hashes, bounded output and metadata](../evidence/77b1c55854f32a4c.json). Baseline: **tool-error**.

No independent runtime override was executed for this target in this audit; this is not a pass.

## Recommended action

Resolve the intended parameter domain and enclosing equations; check inherited bounds, final/protected status, guards and aliases. Construct an otherwise-valid source-level witness, establish a clean baseline in a capable engine, then retranslate at the witness and compare with the runtime override. For equality claims use the actual partner value. Do not apply a blanket min>0 fix yet.

## Scope and limitations

A source-level verdict addresses the reported declaration/claim, not every possible connected system. Tests cover 0–0.5 seconds and are not a proof of long-run stability. Shared instances are not distinct root causes. A missing bound, timeout, compiler error or failed nominal run alone never counts as a verified bug or a false positive. Fixes are proposals; no library/compiler implementation was changed.

[Group and related reports](../groups/baseline-blocked.md) · [Index](../README.md)
