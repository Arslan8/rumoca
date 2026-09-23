# FINDING-02054: Not yet established as a bug or a false positive

| Field | Value |
|---|---|
| Verdict | unresolved |
| Scope / group | baseline-blocked |
| Model | Modelica.Electrical.Machines.Examples.InductionMachines.IMS_Start |
| Target | JLoad |
| Student classification | physical-domain-unenforced |
| Original report | [FINDING-ims-start-jload-zerolimit.md](../../v2/bugs/FINDING-ims-start-jload-zerolimit.md) — reviewed as `FINDING-02054-ims-start-jload.md`, which a later run renamed |
| Original SHA-256 | 9a1e07595fcfb286073e9125eb6912e0199392d835ca2a4f2273679f5c7ac057 |

## What remains unresolved

The current Rumoca nominal run is tool-error, before any reported perturbation. This prevents causal attribution to this parameter. Source metadata was recovered, but none of the reviewed source proofs or counterexamples establishes this particular claim. A baseline failure/tool limitation is neither confirmation nor a false positive.

## Source evidence

Compiler/source-resolved declaration: `Electrical/Machines/Examples/InductionMachines/IMS_Start.mo:16`. Role: `parameter`; binding: `0.29`; effective min: `None`; effective max: `None`. 

[Electrical/Machines/Examples/InductionMachines/IMS_Start.mo — source snapshot](../evidence/sources/439faf5a498dc64f-IMS_Start.mo)

```modelica
14:   parameter SI.AngularVelocity wLoad(displayUnit="rev/min")=
15:        1440.45*2*Modelica.Constants.pi/60 "Nominal load speed";
16:   parameter SI.Inertia JLoad=0.29
17:     "Load's moment of inertia";
18:   Machines.BasicMachines.InductionMachines.IM_SlipRing aims(
19:     p=aimsData.p,
```


## Execution evidence

[Rumoca commands, return codes, integrity hashes, bounded output and metadata](../evidence/2804e4f64ad6a33e.json). Baseline: **tool-error**.

No independent runtime override was executed for this target in this audit; this is not a pass.

## Recommended action

Resolve the intended parameter domain and enclosing equations; check inherited bounds, final/protected status, guards and aliases. Construct an otherwise-valid source-level witness, establish a clean baseline in a capable engine, then retranslate at the witness and compare with the runtime override. For equality claims use the actual partner value. Do not apply a blanket min>0 fix yet.

## Scope and limitations

A source-level verdict addresses the reported declaration/claim, not every possible connected system. Tests cover 0–0.5 seconds and are not a proof of long-run stability. Shared instances are not distinct root causes. A missing bound, timeout, compiler error or failed nominal run alone never counts as a verified bug or a false positive. Fixes are proposals; no library/compiler implementation was changed.

[Group and related reports](../groups/baseline-blocked.md) · [Index](../README.md)
