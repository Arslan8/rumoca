# FINDING-02581: Not yet established as a bug or a false positive

| Field | Value |
|---|---|
| Verdict | unresolved |
| Scope / group | baseline-blocked |
| Model | Modelica.Electrical.Machines.Examples.SynchronousMachines.SMR_DOL |
| Target | smr.damperCage.Lrsigmad |
| Student classification | physical-domain-unenforced |
| Original report | [FINDING-smr-dol-smr-dampercage-lrsigmad-zerolimit.md](../../v2/bugs/FINDING-smr-dol-smr-dampercage-lrsigmad-zerolimit.md) — reviewed as `FINDING-02581-smr-dol-smr-dampercage-lrsigmad.md`, which a later run renamed |
| Original SHA-256 | 713370e0f9390501ce6df890c1c344f61726df59aebf83916bd10ddd7a633ba3 |

## What remains unresolved

The current Rumoca nominal run is tool-error, before any reported perturbation. This prevents causal attribution to this parameter. Source metadata was recovered, but none of the reviewed source proofs or counterexamples establishes this particular claim. A baseline failure/tool limitation is neither confirmation nor a false positive.

## Source evidence

Compiler/source-resolved declaration: `Electrical/Machines/BasicMachines/Components/DamperCage.mo:3`. Role: `parameter`; binding: `smrData.Lrsigmad`; effective min: `None`; effective max: `None`. 

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

[Rumoca commands, return codes, integrity hashes, bounded output and metadata](../evidence/c3f17a08fd4d3c9d.json). Baseline: **tool-error**.

No independent runtime override was executed for this target in this audit; this is not a pass.

## Recommended action

Resolve the intended parameter domain and enclosing equations; check inherited bounds, final/protected status, guards and aliases. Construct an otherwise-valid source-level witness, establish a clean baseline in a capable engine, then retranslate at the witness and compare with the runtime override. For equality claims use the actual partner value. Do not apply a blanket min>0 fix yet.

## Scope and limitations

A source-level verdict addresses the reported declaration/claim, not every possible connected system. Tests cover 0–0.5 seconds and are not a proof of long-run stability. Shared instances are not distinct root causes. A missing bound, timeout, compiler error or failed nominal run alone never counts as a verified bug or a false positive. Fixes are proposals; no library/compiler implementation was changed.

[Group and related reports](../groups/baseline-blocked.md) · [Index](../README.md)
