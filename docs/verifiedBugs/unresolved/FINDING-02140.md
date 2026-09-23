# FINDING-02140: Not yet established as a bug or a false positive

| Field | Value |
|---|---|
| Verdict | unresolved |
| Scope / group | baseline-blocked |
| Model | Modelica.Electrical.Machines.Examples.SynchronousMachines.SMEE_DOL |
| Target | smee.damperCage.Lrsigmad |
| Student classification | physical-domain-unenforced |
| Original report | [FINDING-smee-dol-smee-dampercage-lrsigmad-zerolimit.md](../../v2/bugs/FINDING-smee-dol-smee-dampercage-lrsigmad-zerolimit.md) — reviewed as `FINDING-02140-smee-dol-smee-dampercage-lrsigmad.md`, which a later run renamed |
| Original SHA-256 | 67e293a6780e530b74ec8ad5d3fbef64fe4963c84686fea20ab6b1a9af623c92 |

## What remains unresolved

The current Rumoca nominal run is tool-error, before any reported perturbation. This prevents causal attribution to this parameter. Source metadata was recovered, but none of the reviewed source proofs or counterexamples establishes this particular claim. A baseline failure/tool limitation is neither confirmation nor a false positive.

## Source evidence

Compiler/source-resolved declaration: `Electrical/Machines/BasicMachines/Components/DamperCage.mo:3`. Role: `parameter`; binding: `smeeData.Lrsigmad`; effective min: `None`; effective max: `None`. 

[Electrical/Machines/BasicMachines/Components/DamperCage.mo — source snapshot](../evidence/sources/a430d3c774d76eaf-DamperCage.mo)

```modelica
1: within Modelica.Electrical.Machines.BasicMachines.Components;
2: model DamperCage "Squirrel Cage"
3:   parameter SI.Inductance Lrsigmad
4:     "Stray inductance in d-axis per phase translated to stator";
5:   parameter SI.Inductance Lrsigmaq
6:     "Stray inductance in q-axis per phase translated to stator";
```


## Execution evidence

[Rumoca commands, return codes, integrity hashes, bounded output and metadata](../evidence/60c0c577a4240961.json). Baseline: **tool-error**.

No independent runtime override was executed for this target in this audit; this is not a pass.

## Recommended action

Resolve the intended parameter domain and enclosing equations; check inherited bounds, final/protected status, guards and aliases. Construct an otherwise-valid source-level witness, establish a clean baseline in a capable engine, then retranslate at the witness and compare with the runtime override. For equality claims use the actual partner value. Do not apply a blanket min>0 fix yet.

## Scope and limitations

A source-level verdict addresses the reported declaration/claim, not every possible connected system. Tests cover 0–0.5 seconds and are not a proof of long-run stability. Shared instances are not distinct root causes. A missing bound, timeout, compiler error or failed nominal run alone never counts as a verified bug or a false positive. Fixes are proposals; no library/compiler implementation was changed.

[Group and related reports](../groups/baseline-blocked.md) · [Index](../README.md)
