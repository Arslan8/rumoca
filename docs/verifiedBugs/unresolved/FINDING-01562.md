# FINDING-01562: Not yet established as a bug or a false positive

| Field | Value |
|---|---|
| Verdict | unresolved |
| Scope / group | baseline-blocked |
| Model | Modelica.Electrical.Machines.Examples.InductionMachines.IMC_DCBraking |
| Target | imc.squirrelCageR.Rr |
| Student classification | physical-domain-unenforced |
| Original report | [FINDING-imc-dcbraking-imc-squirrelcager-rr-zerolimit.md](../../v2/bugs/FINDING-imc-dcbraking-imc-squirrelcager-rr-zerolimit.md) — reviewed as `FINDING-01562-imc-dcbraking-imc-squirrelcager-rr.md`, which a later run renamed |
| Original SHA-256 | e013fbaa115b331ba25df421c985cd7fc1a6c9245dc36986a29216917e68818b |

## What remains unresolved

The current Rumoca nominal run is tool-error, before any reported perturbation. This prevents causal attribution to this parameter. Source metadata was recovered, but none of the reviewed source proofs or counterexamples establishes this particular claim. A baseline failure/tool limitation is neither confirmation nor a false positive.

## Source evidence

Compiler/source-resolved declaration: `Electrical/Machines/BasicMachines/Components/SquirrelCage.mo:5`. Role: `parameter`; binding: `imcData.Rr`; effective min: `None`; effective max: `None`. 

[Electrical/Machines/BasicMachines/Components/SquirrelCage.mo — source snapshot](../evidence/sources/1ea4e9328c27e7ba-SquirrelCage.mo)

```modelica
3:   parameter SI.Inductance Lrsigma
4:     "Rotor stray inductance per phase translated to stator";
5:   parameter SI.Resistance Rr
6:     "Rotor resistance per phase translated to stator at T_ref";
7:   parameter SI.Temperature T_ref=293.15
8:     "Reference temperature";
```


## Execution evidence

[Rumoca commands, return codes, integrity hashes, bounded output and metadata](../evidence/489fdf592354cb9a.json). Baseline: **tool-error**.

No independent runtime override was executed for this target in this audit; this is not a pass.

## Recommended action

Resolve the intended parameter domain and enclosing equations; check inherited bounds, final/protected status, guards and aliases. Construct an otherwise-valid source-level witness, establish a clean baseline in a capable engine, then retranslate at the witness and compare with the runtime override. For equality claims use the actual partner value. Do not apply a blanket min>0 fix yet.

## Scope and limitations

A source-level verdict addresses the reported declaration/claim, not every possible connected system. Tests cover 0–0.5 seconds and are not a proof of long-run stability. Shared instances are not distinct root causes. A missing bound, timeout, compiler error or failed nominal run alone never counts as a verified bug or a false positive. Fixes are proposals; no library/compiler implementation was changed.

[Group and related reports](../groups/baseline-blocked.md) · [Index](../README.md)
