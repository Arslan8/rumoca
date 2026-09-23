# FINDING-04442: Not yet established as a bug or a false positive

| Field | Value |
|---|---|
| Verdict | unresolved |
| Scope / group | baseline-blocked |
| Model | Modelica.Mechanics.Translational.Examples.GenerationOfFMUs |
| Target | directMass.m |
| Student classification | physical-bound-permits-zero |
| Original report | [FINDING-generationoffmus-directmass-m-intent.md](../../v2/bugs/FINDING-generationoffmus-directmass-m-intent.md) — reviewed as `FINDING-04442-generationoffmus-directmass-m.md`, which a later run renamed |
| Original SHA-256 | 873bb3259fbd25973cdf3b68ab38fd5678e033ff98f43c438cf495b1178ed101 |

## What remains unresolved

The current Rumoca nominal run is tool-error, before any reported perturbation. This prevents causal attribution to this parameter. Source metadata was recovered, but none of the reviewed source proofs or counterexamples establishes this particular claim. A baseline failure/tool limitation is neither confirmation nor a false positive.

## Source evidence

Compiler/source-resolved declaration: `Mechanics/Translational/Examples/Utilities/DirectMass.mo:4`. Role: `parameter`; binding: `1.1`; effective min: `0`; effective max: `None`. 

[Mechanics/Translational/Examples/Utilities/DirectMass.mo — source snapshot](../evidence/sources/d1cdaae289b7b0b6-DirectMass.mo)

```modelica
2: model DirectMass "Input/output block of a direct mass model"
3:   extends Modelica.Blocks.Icons.Block;
4:   parameter SI.Mass m(min=0)=1 "Mass";
5:   Modelica.Mechanics.Translational.Components.Mass mass(
6:     m=m,
7:     s(start=0, fixed=true),
```


## Execution evidence

[Rumoca commands, return codes, integrity hashes, bounded output and metadata](../evidence/6d8ae00caaf62637.json). Baseline: **tool-error**.

No independent runtime override was executed for this target in this audit; this is not a pass.

## Recommended action

Resolve the intended parameter domain and enclosing equations; check inherited bounds, final/protected status, guards and aliases. Construct an otherwise-valid source-level witness, establish a clean baseline in a capable engine, then retranslate at the witness and compare with the runtime override. For equality claims use the actual partner value. Do not apply a blanket min>0 fix yet.

## Scope and limitations

A source-level verdict addresses the reported declaration/claim, not every possible connected system. Tests cover 0–0.5 seconds and are not a proof of long-run stability. Shared instances are not distinct root causes. A missing bound, timeout, compiler error or failed nominal run alone never counts as a verified bug or a false positive. Fixes are proposals; no library/compiler implementation was changed.

[Group and related reports](../groups/baseline-blocked.md) · [Index](../README.md)
