# FINDING-03735: Not yet established as a bug or a false positive

| Field | Value |
|---|---|
| Verdict | unresolved |
| Scope / group | baseline-blocked |
| Model | Modelica.Magnetic.FluxTubes.Examples.BasicExamples.SaturatedInductor |
| Target | r_mAirPar.l |
| Student classification | divisor-reachable-zero |
| Original report | [FINDING-saturatedinductor-r-mairpar-l-divzero.md](../../v2/bugs/FINDING-saturatedinductor-r-mairpar-l-divzero.md) — reviewed as `FINDING-03735-saturatedinductor-r-mairpar-l.md`, which a later run renamed |
| Original SHA-256 | 0dd329b932a361d7dc63f4ce7d001729ea106d1c4ffb5610a33476962094bc03 |

## What remains unresolved

The current Rumoca nominal run is tool-error, before any reported perturbation. This prevents causal attribution to this parameter. Source metadata was recovered, but none of the reviewed source proofs or counterexamples establishes this particular claim. A baseline failure/tool limitation is neither confirmation nor a false positive.

## Source evidence

Compiler/source-resolved declaration: `Magnetic/FluxTubes/Shapes/FixedShape/Cuboid.mo:8`. Role: `parameter`; binding: `0.0001`; effective min: `None`; effective max: `None`. 

[Magnetic/FluxTubes/Shapes/FixedShape/Cuboid.mo — source snapshot](../evidence/sources/226c49f8c68f4957-Cuboid.mo)

```modelica
6:   extends Modelica.Magnetic.FluxTubes.Icons.Cuboid;
7: 
8:   parameter SI.Length l=0.01 "Length in direction of flux" annotation (
9:       Dialog(group="Fixed geometry", groupImage=
10:           "modelica://Modelica/Resources/Images/Magnetic/FluxTubes/Shapes/CuboidParallelFlux.png"));
11:   parameter SI.Length a=0.01 "Width of rectangular cross-section"
```


## Execution evidence

[Rumoca commands, return codes, integrity hashes, bounded output and metadata](../evidence/988d11293665b0c9.json). Baseline: **tool-error**.

No independent runtime override was executed for this target in this audit; this is not a pass.

## Recommended action

Resolve the intended parameter domain and enclosing equations; check inherited bounds, final/protected status, guards and aliases. Construct an otherwise-valid source-level witness, establish a clean baseline in a capable engine, then retranslate at the witness and compare with the runtime override. For equality claims use the actual partner value. Do not apply a blanket min>0 fix yet.

## Scope and limitations

A source-level verdict addresses the reported declaration/claim, not every possible connected system. Tests cover 0–0.5 seconds and are not a proof of long-run stability. Shared instances are not distinct root causes. A missing bound, timeout, compiler error or failed nominal run alone never counts as a verified bug or a false positive. Fixes are proposals; no library/compiler implementation was changed.

[Group and related reports](../groups/baseline-blocked.md) · [Index](../README.md)
