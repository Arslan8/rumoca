# FINDING-03828: Not yet established as a bug or a false positive

| Field | Value |
|---|---|
| Verdict | unresolved |
| Scope / group | baseline-blocked |
| Model | Modelica.Magnetic.FluxTubes.Examples.SolenoidActuator.Components.AdvancedSolenoid |
| Target | g_mAirWork.A |
| Student classification | physical-domain-unenforced |
| Original report | [FINDING-advancedsolenoid-g-mairwork-a-unbounded.md](../../v2/bugs/FINDING-advancedsolenoid-g-mairwork-a-unbounded.md) — reviewed as `FINDING-03828-advancedsolenoid-g-mairwork-a.md`, which a later run renamed |
| Original SHA-256 | 4fe95943151df8e4cd6efb0d8341b995117d98f7e3ebeb2b4353478a1b83005c |

## What remains unresolved

The current Rumoca nominal run is tool-error, before any reported perturbation. This prevents causal attribution to this parameter. Source metadata was recovered, but none of the reviewed source proofs or counterexamples establishes this particular claim. A baseline failure/tool limitation is neither confirmation nor a false positive.

## Source evidence

Compiler/source-resolved declaration: `Magnetic/FluxTubes/Shapes/Force/HollowCylinderAxialFlux.mo:16`. Role: `parameter`; binding: `((2 * asin(1.0)) * ((g_mAirWork.r_o ^ 2) - (g_mAirWork.r_i ^ 2)))`; effective min: `None`; effective max: `None`. 

[Magnetic/FluxTubes/Shapes/Force/HollowCylinderAxialFlux.mo — source snapshot](../evidence/sources/c9f1afd879f2df78-HollowCylinderAxialFlux.mo)

```modelica
14: 
15: protected
16:   parameter SI.Area A=pi*(r_o^2 - r_i^2)
17:     "Cross-sectional area orthogonal to direction of flux";
18: 
19: equation
```


## Execution evidence

[Rumoca commands, return codes, integrity hashes, bounded output and metadata](../evidence/2b15116b50ad0f74.json). Baseline: **tool-error**.

No independent runtime override was executed for this target in this audit; this is not a pass.

## Recommended action

Resolve the intended parameter domain and enclosing equations; check inherited bounds, final/protected status, guards and aliases. Construct an otherwise-valid source-level witness, establish a clean baseline in a capable engine, then retranslate at the witness and compare with the runtime override. For equality claims use the actual partner value. Do not apply a blanket min>0 fix yet.

## Scope and limitations

A source-level verdict addresses the reported declaration/claim, not every possible connected system. Tests cover 0–0.5 seconds and are not a proof of long-run stability. Shared instances are not distinct root causes. A missing bound, timeout, compiler error or failed nominal run alone never counts as a verified bug or a false positive. Fixes are proposals; no library/compiler implementation was changed.

[Group and related reports](../groups/baseline-blocked.md) · [Index](../README.md)
