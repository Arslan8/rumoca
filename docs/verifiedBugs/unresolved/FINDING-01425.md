# FINDING-01425: Not yet established as a bug or a false positive

| Field | Value |
|---|---|
| Verdict | unresolved |
| Scope / group | baseline-blocked |
| Model | Modelica.Electrical.Machines.Examples.DCMachines.DCPM_withLosses |
| Target | JLoad |
| Student classification | physical-domain-unenforced |
| Original report | [FINDING-dcpm-withlosses-jload-zerolimit.md](../../v2/bugs/FINDING-dcpm-withlosses-jload-zerolimit.md) — reviewed as `FINDING-01425-dcpm-withlosses-jload.md`, which a later run renamed |
| Original SHA-256 | 952b0a41bf6bf21a58d9b7851ac4b6d20b1d2d98b65ec49e2255a54c28333ac2 |

## What remains unresolved

The current Rumoca nominal run is tool-error, before any reported perturbation. This prevents causal attribution to this parameter. Source metadata was recovered, but none of the reviewed source proofs or counterexamples establishes this particular claim. A baseline failure/tool limitation is neither confirmation nor a false positive.

## Source evidence

Compiler/source-resolved declaration: `Electrical/Machines/Examples/DCMachines/DCPM_withLosses.mo:16`. Role: `parameter`; binding: `0.15`; effective min: `None`; effective max: `None`. 

[Electrical/Machines/Examples/DCMachines/DCPM_withLosses.mo — source snapshot](../evidence/sources/697c8494e65e1638-DCPM_withLosses.mo)

```modelica
14:   parameter SI.AngularVelocity wLoad2=1417.5*2*pi/60
15:     "Nominal load speed";
16:   parameter SI.Inertia JLoad=0.15
17:     "Load's moment of inertia";
18:   Machines.BasicMachines.DCMachines.DC_PermanentMagnet dcpm1(
19:     VaNominal=dcpmData1.VaNominal,
```


## Execution evidence

[Rumoca commands, return codes, integrity hashes, bounded output and metadata](../evidence/1255084b3c3934b8.json). Baseline: **tool-error**.

No independent runtime override was executed for this target in this audit; this is not a pass.

## Recommended action

Resolve the intended parameter domain and enclosing equations; check inherited bounds, final/protected status, guards and aliases. Construct an otherwise-valid source-level witness, establish a clean baseline in a capable engine, then retranslate at the witness and compare with the runtime override. For equality claims use the actual partner value. Do not apply a blanket min>0 fix yet.

## Scope and limitations

A source-level verdict addresses the reported declaration/claim, not every possible connected system. Tests cover 0–0.5 seconds and are not a proof of long-run stability. Shared instances are not distinct root causes. A missing bound, timeout, compiler error or failed nominal run alone never counts as a verified bug or a false positive. Fixes are proposals; no library/compiler implementation was changed.

[Group and related reports](../groups/baseline-blocked.md) · [Index](../README.md)
