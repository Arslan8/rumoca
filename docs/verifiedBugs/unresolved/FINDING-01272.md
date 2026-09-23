# FINDING-01272: Not yet established as a bug or a false positive

| Field | Value |
|---|---|
| Verdict | unresolved |
| Scope / group | baseline-blocked |
| Model | Modelica.Electrical.Machines.Examples.DCMachines.DCPM_CurrentControlled |
| Target | Ra |
| Student classification | physical-domain-unenforced |
| Original report | [FINDING-dcpm-currentcontrolled-ra-unbounded.md](../../v2/bugs/FINDING-dcpm-currentcontrolled-ra-unbounded.md) — reviewed as `FINDING-01272-dcpm-currentcontrolled-ra.md`, which a later run renamed |
| Original SHA-256 | 0eaf6604046266ec7f9a66fbc5d851229f9abc29d318d4d528c4adfb23202732 |

## What remains unresolved

The current Rumoca nominal run is tool-error, before any reported perturbation. This prevents causal attribution to this parameter. Source metadata was recovered, but none of the reviewed source proofs or counterexamples establishes this particular claim. A baseline failure/tool limitation is neither confirmation nor a false positive.

## Source evidence

Compiler/source-resolved declaration: `Electrical/Machines/Examples/DCMachines/DCPM_CurrentControlled.mo:8`. Role: `parameter`; binding: `Modelica.Electrical.Machines.Thermal.convertResistance(dcpmData.Ra, dcpmData.TaRef, dcpmData.alpha20a, dcpmData.TaNominal)`; effective min: `None`; effective max: `None`. 

[Electrical/Machines/Examples/DCMachines/DCPM_CurrentControlled.mo — source snapshot](../evidence/sources/7201d33bf2cce885-DCPM_CurrentControlled.mo)

```modelica
6:   parameter SI.AngularVelocity wLoad=dcpmData.wNominal "Nominal load torque";
7:   parameter SI.Inertia JLoad=dcpmData.Jr "Load's moment of inertia";
8:   parameter SI.Resistance Ra=Modelica.Electrical.Machines.Thermal.convertResistance(
9:     dcpmData.Ra,
10:     dcpmData.TaRef,
11:     dcpmData.alpha20a,
```


## Execution evidence

[Rumoca commands, return codes, integrity hashes, bounded output and metadata](../evidence/77b1c55854f32a4c.json). Baseline: **tool-error**.

No independent runtime override was executed for this target in this audit; this is not a pass.

## Recommended action

Resolve the intended parameter domain and enclosing equations; check inherited bounds, final/protected status, guards and aliases. Construct an otherwise-valid source-level witness, establish a clean baseline in a capable engine, then retranslate at the witness and compare with the runtime override. For equality claims use the actual partner value. Do not apply a blanket min>0 fix yet.

## Scope and limitations

A source-level verdict addresses the reported declaration/claim, not every possible connected system. Tests cover 0–0.5 seconds and are not a proof of long-run stability. Shared instances are not distinct root causes. A missing bound, timeout, compiler error or failed nominal run alone never counts as a verified bug or a false positive. Fixes are proposals; no library/compiler implementation was changed.

[Group and related reports](../groups/baseline-blocked.md) · [Index](../README.md)
