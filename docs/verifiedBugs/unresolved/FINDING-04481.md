# FINDING-04481: Not yet established as a bug or a false positive

| Field | Value |
|---|---|
| Verdict | unresolved |
| Scope / group | baseline-blocked |
| Model | Modelica.Mechanics.Translational.Examples.Utilities.InverseMass |
| Target | m |
| Student classification | physical-bound-permits-zero |
| Original report | [FINDING-inversemass-m-zerolimit.md](../../v2/bugs/FINDING-inversemass-m-zerolimit.md) — reviewed as `FINDING-04481-inversemass-m.md`, which a later run renamed |
| Original SHA-256 | 5bf34e82099137fcdff9d63ebbdaefd702ca60d9ce51daa85c2af53e65a0fd32 |

## What remains unresolved

The current Rumoca nominal run is tool-error, before any reported perturbation. This prevents causal attribution to this parameter. Source metadata was recovered, but none of the reviewed source proofs or counterexamples establishes this particular claim. A baseline failure/tool limitation is neither confirmation nor a false positive.

## Source evidence

Compiler/source-resolved declaration: `Mechanics/Translational/Examples/Utilities/InverseMass.mo:4`. Role: `parameter`; binding: `1`; effective min: `0`; effective max: `None`. 

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

[Rumoca commands, return codes, integrity hashes, bounded output and metadata](../evidence/1b584f2d4d8bbc53.json). Baseline: **tool-error**.

No independent runtime override was executed for this target in this audit; this is not a pass.

## Recommended action

Resolve the intended parameter domain and enclosing equations; check inherited bounds, final/protected status, guards and aliases. Construct an otherwise-valid source-level witness, establish a clean baseline in a capable engine, then retranslate at the witness and compare with the runtime override. For equality claims use the actual partner value. Do not apply a blanket min>0 fix yet.

## Scope and limitations

A source-level verdict addresses the reported declaration/claim, not every possible connected system. Tests cover 0–0.5 seconds and are not a proof of long-run stability. Shared instances are not distinct root causes. A missing bound, timeout, compiler error or failed nominal run alone never counts as a verified bug or a false positive. Fixes are proposals; no library/compiler implementation was changed.

[Group and related reports](../groups/baseline-blocked.md) · [Index](../README.md)
