# FINDING-01856: Not yet established as a bug or a false positive

| Field | Value |
|---|---|
| Verdict | unresolved |
| Scope / group | baseline-blocked |
| Model | Modelica.Electrical.Machines.Examples.InductionMachines.IMC_Transformer |
| Target | aimc.squirrelCageR.Lrsigma |
| Student classification | physical-domain-unenforced |
| Original report | [FINDING-imc-transformer-aimc-squirrelcager-lrsigma-zerolimit.md](../../v2/bugs/FINDING-imc-transformer-aimc-squirrelcager-lrsigma-zerolimit.md) — reviewed as `FINDING-01856-imc-transformer-aimc-squirrelcager-lrsigma.md`, which a later run renamed |
| Original SHA-256 | a89d7264a857ad1ca90760b0a1b0ebb55f0a5a8460fc1f8621eaef08aa9900c1 |

## What remains unresolved

The current Rumoca nominal run is tool-error, before any reported perturbation. This prevents causal attribution to this parameter. Source metadata was recovered, but none of the reviewed source proofs or counterexamples establishes this particular claim. A baseline failure/tool limitation is neither confirmation nor a false positive.

## Source evidence

Compiler/source-resolved declaration: `Electrical/Machines/BasicMachines/Components/SquirrelCage.mo:3`. Role: `parameter`; binding: `aimcData.Lrsigma`; effective min: `None`; effective max: `None`. 

[Electrical/Machines/BasicMachines/Components/SquirrelCage.mo — source snapshot](../evidence/sources/1ea4e9328c27e7ba-SquirrelCage.mo)

```modelica
1: within Modelica.Electrical.Machines.BasicMachines.Components;
2: model SquirrelCage "Squirrel Cage"
3:   parameter SI.Inductance Lrsigma
4:     "Rotor stray inductance per phase translated to stator";
5:   parameter SI.Resistance Rr
6:     "Rotor resistance per phase translated to stator at T_ref";
```


## Execution evidence

[Rumoca commands, return codes, integrity hashes, bounded output and metadata](../evidence/ea078e37b0773dc4.json). Baseline: **tool-error**.

No independent runtime override was executed for this target in this audit; this is not a pass.

## Recommended action

Resolve the intended parameter domain and enclosing equations; check inherited bounds, final/protected status, guards and aliases. Construct an otherwise-valid source-level witness, establish a clean baseline in a capable engine, then retranslate at the witness and compare with the runtime override. For equality claims use the actual partner value. Do not apply a blanket min>0 fix yet.

## Scope and limitations

A source-level verdict addresses the reported declaration/claim, not every possible connected system. Tests cover 0–0.5 seconds and are not a proof of long-run stability. Shared instances are not distinct root causes. A missing bound, timeout, compiler error or failed nominal run alone never counts as a verified bug or a false positive. Fixes are proposals; no library/compiler implementation was changed.

[Group and related reports](../groups/baseline-blocked.md) · [Index](../README.md)
