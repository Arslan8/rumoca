# FINDING-02213: Not yet established as a bug or a false positive

| Field | Value |
|---|---|
| Verdict | unresolved |
| Scope / group | baseline-blocked |
| Model | Modelica.Electrical.Machines.Examples.SynchronousMachines.SMEE_Generator |
| Target | smee.damperCage.Lrsigmaq |
| Student classification | physical-domain-unenforced |
| Original report | [FINDING-smee-generator-smee-dampercage-lrsigmaq-zerolimit.md](../../v2/bugs/FINDING-smee-generator-smee-dampercage-lrsigmaq-zerolimit.md) — reviewed as `FINDING-02213-smee-generator-smee-dampercage-lrsigmaq.md`, which a later run renamed |
| Original SHA-256 | 3d9d9274c15c5d59ec6236454184b2e237b12bb8fcfd29b83d1bbad04a8699b9 |

## What remains unresolved

The current Rumoca nominal run is tool-error, before any reported perturbation. This prevents causal attribution to this parameter. Source metadata was recovered, but none of the reviewed source proofs or counterexamples establishes this particular claim. A baseline failure/tool limitation is neither confirmation nor a false positive.

## Source evidence

Compiler/source-resolved declaration: `Electrical/Machines/BasicMachines/Components/DamperCage.mo:5`. Role: `parameter`; binding: `smeeData.Lrsigmaq`; effective min: `None`; effective max: `None`. 

[Electrical/Machines/BasicMachines/Components/DamperCage.mo — source snapshot](../evidence/sources/a430d3c774d76eaf-DamperCage.mo)

```modelica
3:   parameter SI.Inductance Lrsigmad
4:     "Stray inductance in d-axis per phase translated to stator";
5:   parameter SI.Inductance Lrsigmaq
6:     "Stray inductance in q-axis per phase translated to stator";
7:   parameter SI.Resistance Rrd
8:     "Resistance in d-axis per phase translated to stator at T_ref";
```


## Execution evidence

[Rumoca commands, return codes, integrity hashes, bounded output and metadata](../evidence/4d376a5cb19be7de.json). Baseline: **tool-error**.

No independent runtime override was executed for this target in this audit; this is not a pass.

## Recommended action

Resolve the intended parameter domain and enclosing equations; check inherited bounds, final/protected status, guards and aliases. Construct an otherwise-valid source-level witness, establish a clean baseline in a capable engine, then retranslate at the witness and compare with the runtime override. For equality claims use the actual partner value. Do not apply a blanket min>0 fix yet.

## Scope and limitations

A source-level verdict addresses the reported declaration/claim, not every possible connected system. Tests cover 0–0.5 seconds and are not a proof of long-run stability. Shared instances are not distinct root causes. A missing bound, timeout, compiler error or failed nominal run alone never counts as a verified bug or a false positive. Fixes are proposals; no library/compiler implementation was changed.

[Group and related reports](../groups/baseline-blocked.md) · [Index](../README.md)
