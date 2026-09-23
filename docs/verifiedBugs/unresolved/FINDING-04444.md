# FINDING-04444: Not yet established as a bug or a false positive

| Field | Value |
|---|---|
| Verdict | unresolved |
| Scope / group | baseline-blocked |
| Model | Modelica.Mechanics.Translational.Examples.GenerationOfFMUs |
| Target | inverseMass.m |
| Student classification | physical-bound-permits-zero |
| Original report | [FINDING-generationoffmus-inversemass-m-intent.md](../../v2/bugs/FINDING-generationoffmus-inversemass-m-intent.md) — reviewed as `FINDING-04444-generationoffmus-inversemass-m.md`, which a later run renamed |
| Original SHA-256 | 428527174a193925fa519517a8f6baf3ac6b1b9ed553d2226bb5f3a0a2b5a546 |

## What remains unresolved

The current Rumoca nominal run is tool-error, before any reported perturbation. This prevents causal attribution to this parameter. Source metadata was recovered, but none of the reviewed source proofs or counterexamples establishes this particular claim. A baseline failure/tool limitation is neither confirmation nor a false positive.

## Source evidence

Compiler/source-resolved declaration: `Mechanics/Translational/Examples/Utilities/InverseMass.mo:4`. Role: `parameter`; binding: `2.2`; effective min: `0`; effective max: `None`. 

[Mechanics/Translational/Examples/Utilities/InverseMass.mo — source snapshot](../evidence/sources/40c5b16cc77cf73c-InverseMass.mo)

```modelica
2: model InverseMass "Input/output block of an inverse mass model"
3:   extends Modelica.Blocks.Icons.Block;
4:   parameter SI.Mass m=1 "Mass";
5:   Modelica.Mechanics.Translational.Components.Mass mass(
6:     m=m)           annotation (Placement(transformation(extent={{-10,
7:             -10},{10,10}})));
```


## Execution evidence

[Rumoca commands, return codes, integrity hashes, bounded output and metadata](../evidence/6d8ae00caaf62637.json). Baseline: **tool-error**.

No independent runtime override was executed for this target in this audit; this is not a pass.

## Recommended action

Resolve the intended parameter domain and enclosing equations; check inherited bounds, final/protected status, guards and aliases. Construct an otherwise-valid source-level witness, establish a clean baseline in a capable engine, then retranslate at the witness and compare with the runtime override. For equality claims use the actual partner value. Do not apply a blanket min>0 fix yet.

## Scope and limitations

A source-level verdict addresses the reported declaration/claim, not every possible connected system. Tests cover 0–0.5 seconds and are not a proof of long-run stability. Shared instances are not distinct root causes. A missing bound, timeout, compiler error or failed nominal run alone never counts as a verified bug or a false positive. Fixes are proposals; no library/compiler implementation was changed.

[Group and related reports](../groups/baseline-blocked.md) · [Index](../README.md)
