# FINDING-03808: Not yet established as a bug or a false positive

| Field | Value |
|---|---|
| Verdict | unresolved |
| Scope / group | baseline-blocked |
| Model | Modelica.Magnetic.FluxTubes.Examples.MovingCoilActuator.Components.PermeanceActuator |
| Target | d |
| Student classification | physical-domain-unenforced |
| Original report | [FINDING-permeanceactuator-d-intent.md](../../v2/bugs/FINDING-permeanceactuator-d-intent.md) — reviewed as `FINDING-03808-permeanceactuator-d.md`, which a later run renamed |
| Original SHA-256 | a20bb17729c374ef7b6fff661230f02d1c34fad07266b0c8744aefb5401baa1b |

## What remains unresolved

The current Rumoca nominal run is tool-error, before any reported perturbation. This prevents causal attribution to this parameter. Source metadata was recovered, but none of the reviewed source proofs or counterexamples establishes this particular claim. A baseline failure/tool limitation is neither confirmation nor a false positive.

## Source evidence

Compiler/source-resolved declaration: `Magnetic/FluxTubes/Examples/MovingCoilActuator/Components/PermeanceActuator.mo:35`. Role: `parameter`; binding: `400`; effective min: `None`; effective max: `None`. 

[Magnetic/FluxTubes/Examples/MovingCoilActuator/Components/PermeanceActuator.mo — source snapshot](../evidence/sources/1142230a24c5b94d-PermeanceActuator.mo)

```modelica
33:     "Spring stiffness between impact partners"
34:     annotation (Dialog(group="Armature and stopper"));
35:   parameter SI.TranslationalDampingConstant d=400
36:     "Damping coefficient between impact partners"
37:     annotation (Dialog(group="Armature and stopper"));
38:   parameter SI.Position x_min=-4e-3
```


## Execution evidence

[Rumoca commands, return codes, integrity hashes, bounded output and metadata](../evidence/c8968c8735add08a.json). Baseline: **tool-error**.

No independent runtime override was executed for this target in this audit; this is not a pass.

## Recommended action

Resolve the intended parameter domain and enclosing equations; check inherited bounds, final/protected status, guards and aliases. Construct an otherwise-valid source-level witness, establish a clean baseline in a capable engine, then retranslate at the witness and compare with the runtime override. For equality claims use the actual partner value. Do not apply a blanket min>0 fix yet.

## Scope and limitations

A source-level verdict addresses the reported declaration/claim, not every possible connected system. Tests cover 0–0.5 seconds and are not a proof of long-run stability. Shared instances are not distinct root causes. A missing bound, timeout, compiler error or failed nominal run alone never counts as a verified bug or a false positive. Fixes are proposals; no library/compiler implementation was changed.

[Group and related reports](../groups/baseline-blocked.md) · [Index](../README.md)
