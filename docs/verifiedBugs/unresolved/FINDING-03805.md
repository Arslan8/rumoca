# FINDING-03805: Not yet established as a bug or a false positive

| Field | Value |
|---|---|
| Verdict | unresolved |
| Scope / group | baseline-blocked |
| Model | Modelica.Magnetic.FluxTubes.Examples.MovingCoilActuator.Components.PermeanceActuator |
| Target | R |
| Student classification | physical-domain-unenforced |
| Original report | [FINDING-permeanceactuator-r-zerolimit.md](../../v2/bugs/FINDING-permeanceactuator-r-zerolimit.md) — reviewed as `FINDING-03805-permeanceactuator-r.md`, which a later run renamed |
| Original SHA-256 | e0cbca257a3d87bac411408e0a889bf7668108c3fa997a189e2eadf9d11e2186 |

## What remains unresolved

The current Rumoca nominal run is tool-error, before any reported perturbation. This prevents causal attribution to this parameter. Source metadata was recovered, but none of the reviewed source proofs or counterexamples establishes this particular claim. A baseline failure/tool limitation is neither confirmation nor a false positive.

## Source evidence

Compiler/source-resolved declaration: `Magnetic/FluxTubes/Examples/MovingCoilActuator/Components/PermeanceActuator.mo:8`. Role: `parameter`; binding: `2.86`; effective min: `None`; effective max: `None`. 

[Magnetic/FluxTubes/Examples/MovingCoilActuator/Components/PermeanceActuator.mo — source snapshot](../evidence/sources/1142230a24c5b94d-PermeanceActuator.mo)

```modelica
6:           "Parameters", groupImage=
7:           "modelica://Modelica/Resources/Images/Magnetic/FluxTubes/Examples/MovingCoilActuator/MovingCoilActuator_dimensions.png"));
8:   parameter SI.Resistance R=2.86 "Coil resistance";
9: 
10:   parameter SI.Radius r_core=12.5e-3
11:     "Radius of ferromagnetic stator core";
```


## Execution evidence

[Rumoca commands, return codes, integrity hashes, bounded output and metadata](../evidence/c8968c8735add08a.json). Baseline: **tool-error**.

No independent runtime override was executed for this target in this audit; this is not a pass.

## Recommended action

Resolve the intended parameter domain and enclosing equations; check inherited bounds, final/protected status, guards and aliases. Construct an otherwise-valid source-level witness, establish a clean baseline in a capable engine, then retranslate at the witness and compare with the runtime override. For equality claims use the actual partner value. Do not apply a blanket min>0 fix yet.

## Scope and limitations

A source-level verdict addresses the reported declaration/claim, not every possible connected system. Tests cover 0–0.5 seconds and are not a proof of long-run stability. Shared instances are not distinct root causes. A missing bound, timeout, compiler error or failed nominal run alone never counts as a verified bug or a false positive. Fixes are proposals; no library/compiler implementation was changed.

[Group and related reports](../groups/baseline-blocked.md) · [Index](../README.md)
