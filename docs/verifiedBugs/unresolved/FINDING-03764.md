# FINDING-03764: Not yet established as a bug or a false positive

| Field | Value |
|---|---|
| Verdict | unresolved |
| Scope / group | baseline-blocked |
| Model | Modelica.Magnetic.FluxTubes.Examples.MovingCoilActuator.ArmatureStroke |
| Target | pmActuator.c |
| Student classification | physical-domain-unenforced |
| Original report | [FINDING-armaturestroke-pmactuator-c-intent.md](../../v2/bugs/FINDING-armaturestroke-pmactuator-c-intent.md) — reviewed as `FINDING-03764-armaturestroke-pmactuator-c.md`, which a later run renamed |
| Original SHA-256 | 9954ee55f2da8397dac0c858949561de9c3048a144ff5ba76a4b6bae89fde7e3 |

## What remains unresolved

The current Rumoca nominal run is tool-error, before any reported perturbation. This prevents causal attribution to this parameter. Source metadata was recovered, but none of the reviewed source proofs or counterexamples establishes this particular claim. A baseline failure/tool limitation is neither confirmation nor a false positive.

## Source evidence

Compiler/source-resolved declaration: `Magnetic/FluxTubes/Examples/MovingCoilActuator/Components/PermeanceActuator.mo:32`. Role: `parameter`; binding: `100000000000.0`; effective min: `None`; effective max: `None`. 

[Magnetic/FluxTubes/Examples/MovingCoilActuator/Components/PermeanceActuator.mo — source snapshot](../evidence/sources/1142230a24c5b94d-PermeanceActuator.mo)

```modelica
30:     annotation (Dialog(group="Armature and stopper"));
31: 
32:   parameter SI.TranslationalSpringConstant c=1e11
33:     "Spring stiffness between impact partners"
34:     annotation (Dialog(group="Armature and stopper"));
35:   parameter SI.TranslationalDampingConstant d=400
```


## Execution evidence

[Rumoca commands, return codes, integrity hashes, bounded output and metadata](../evidence/086c556da894438a.json). Baseline: **tool-error**.

No independent runtime override was executed for this target in this audit; this is not a pass.

## Recommended action

Resolve the intended parameter domain and enclosing equations; check inherited bounds, final/protected status, guards and aliases. Construct an otherwise-valid source-level witness, establish a clean baseline in a capable engine, then retranslate at the witness and compare with the runtime override. For equality claims use the actual partner value. Do not apply a blanket min>0 fix yet.

## Scope and limitations

A source-level verdict addresses the reported declaration/claim, not every possible connected system. Tests cover 0–0.5 seconds and are not a proof of long-run stability. Shared instances are not distinct root causes. A missing bound, timeout, compiler error or failed nominal run alone never counts as a verified bug or a false positive. Fixes are proposals; no library/compiler implementation was changed.

[Group and related reports](../groups/baseline-blocked.md) · [Index](../README.md)
