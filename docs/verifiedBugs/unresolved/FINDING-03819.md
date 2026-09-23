# FINDING-03819: Not yet established as a bug or a false positive

| Field | Value |
|---|---|
| Verdict | unresolved |
| Scope / group | baseline-blocked |
| Model | Modelica.Magnetic.FluxTubes.Examples.MovingCoilActuator.Components.PermeanceActuator |
| Target | material.alpha_Br |
| Student classification | divisor-reachable-zero |
| Original report | `FINDING-03819-permeanceactuator-material-alpha-br.md` — [withdrawn](../../v2/bugs/withdrawn.md); a later run no longer makes this claim |
| Original SHA-256 | 14036e05ae8ab82d34ce978ea09d7d0be86da43017c45a972abddd41b3c95ef2 |

## What remains unresolved

The current Rumoca nominal run is tool-error, before any reported perturbation. This prevents causal attribution to this parameter. Source metadata was recovered, but none of the reviewed source proofs or counterexamples establishes this particular claim. A baseline failure/tool limitation is neither confirmation nor a false positive.

## Source evidence

Compiler/source-resolved declaration: `Magnetic/FluxTubes/Material/HardMagnetic/BaseData.mo:10`. Role: `parameter`; binding: `0`; effective min: `None`; effective max: `None`. 

[Magnetic/FluxTubes/Material/HardMagnetic/BaseData.mo — source snapshot](../evidence/sources/72a5ba9004272a6d-BaseData.mo)

```modelica
8:     "Remanence at reference temperature";
9:   parameter SI.Temperature T_ref=293.15 "Reference temperature";
10:   parameter SI.LinearTemperatureCoefficient alpha_Br=0
11:     "Temperature coefficient of remanence at reference temperature";
12: 
13:   parameter SI.Temperature T_op=293.15 "Operating temperature";
```


## Execution evidence

[Rumoca commands, return codes, integrity hashes, bounded output and metadata](../evidence/c8968c8735add08a.json). Baseline: **tool-error**.

No independent runtime override was executed for this target in this audit; this is not a pass.

## Recommended action

Resolve the intended parameter domain and enclosing equations; check inherited bounds, final/protected status, guards and aliases. Construct an otherwise-valid source-level witness, establish a clean baseline in a capable engine, then retranslate at the witness and compare with the runtime override. For equality claims use the actual partner value. Do not apply a blanket min>0 fix yet.

## Scope and limitations

A source-level verdict addresses the reported declaration/claim, not every possible connected system. Tests cover 0–0.5 seconds and are not a proof of long-run stability. Shared instances are not distinct root causes. A missing bound, timeout, compiler error or failed nominal run alone never counts as a verified bug or a false positive. Fixes are proposals; no library/compiler implementation was changed.

[Group and related reports](../groups/baseline-blocked.md) · [Index](../README.md)
