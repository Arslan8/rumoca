# FINDING-03797: Not yet established as a bug or a false positive

| Field | Value |
|---|---|
| Verdict | unresolved |
| Scope / group | baseline-blocked |
| Model | Modelica.Magnetic.FluxTubes.Examples.MovingCoilActuator.Components.ConstantActuator |
| Target | d |
| Student classification | physical-domain-unenforced |
| Original report | [FINDING-constantactuator-d-intent.md](../../v2/bugs/FINDING-constantactuator-d-intent.md) — reviewed as `FINDING-03797-constantactuator-d.md`, which a later run renamed |
| Original SHA-256 | 5a41470bcb9091fa605c9774a2260617e9d15c08cb6f52bf8eafa8238c4b3312 |

## What remains unresolved

The current Rumoca nominal run is reported-failure, before any reported perturbation. This prevents causal attribution to this parameter. Source metadata was recovered, but none of the reviewed source proofs or counterexamples establishes this particular claim. A baseline failure/tool limitation is neither confirmation nor a false positive.

## Source evidence

Compiler/source-resolved declaration: `Magnetic/FluxTubes/Examples/MovingCoilActuator/Components/ConstantActuator.mo:13`. Role: `parameter`; binding: `400`; effective min: `None`; effective max: `None`. 

[Magnetic/FluxTubes/Examples/MovingCoilActuator/Components/ConstantActuator.mo — source snapshot](../evidence/sources/38e251a55a83ff04-ConstantActuator.mo)

```modelica
11:     "Spring stiffness between impact partners"
12:     annotation (Dialog(group="Armature and stopper"));
13:   parameter SI.TranslationalDampingConstant d=400
14:     "Damping coefficient between impact partners"
15:     annotation (Dialog(group="Armature and stopper"));
16:   parameter SI.Position x_min=-4e-3 "Minimum armature position"
```


## Execution evidence

[Rumoca commands, return codes, integrity hashes, bounded output and metadata](../evidence/3b733d5e48ddac51.json). Baseline: **reported-failure**.

No independent runtime override was executed for this target in this audit; this is not a pass.

## Recommended action

Resolve the intended parameter domain and enclosing equations; check inherited bounds, final/protected status, guards and aliases. Construct an otherwise-valid source-level witness, establish a clean baseline in a capable engine, then retranslate at the witness and compare with the runtime override. For equality claims use the actual partner value. Do not apply a blanket min>0 fix yet.

## Scope and limitations

A source-level verdict addresses the reported declaration/claim, not every possible connected system. Tests cover 0–0.5 seconds and are not a proof of long-run stability. Shared instances are not distinct root causes. A missing bound, timeout, compiler error or failed nominal run alone never counts as a verified bug or a false positive. Fixes are proposals; no library/compiler implementation was changed.

[Group and related reports](../groups/baseline-blocked.md) · [Index](../README.md)
