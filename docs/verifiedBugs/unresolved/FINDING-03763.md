# FINDING-03763: Not yet established as a bug or a false positive

| Field | Value |
|---|---|
| Verdict | unresolved |
| Scope / group | baseline-blocked |
| Model | Modelica.Magnetic.FluxTubes.Examples.MovingCoilActuator.ArmatureStroke |
| Target | pmActuator.m_a |
| Student classification | physical-bound-permits-zero |
| Original report | [FINDING-armaturestroke-pmactuator-m-a-intent.md](../../v2/bugs/FINDING-armaturestroke-pmactuator-m-a-intent.md) — reviewed as `FINDING-03763-armaturestroke-pmactuator-m-a.md`, which a later run renamed |
| Original SHA-256 | 052a77945b0f4fa1593232088212bf5285dcce6a032a785beb6d62626c64ab28 |

## What remains unresolved

The current Rumoca nominal run is tool-error, before any reported perturbation. This prevents causal attribution to this parameter. Source metadata was recovered, but none of the reviewed source proofs or counterexamples establishes this particular claim. A baseline failure/tool limitation is neither confirmation nor a false positive.

## Source evidence

Compiler/source-resolved declaration: `Magnetic/FluxTubes/Examples/MovingCoilActuator/Components/PermeanceActuator.mo:29`. Role: `parameter`; binding: `0.012`; effective min: `0`; effective max: `None`. 

[Magnetic/FluxTubes/Examples/MovingCoilActuator/Components/PermeanceActuator.mo — source snapshot](../evidence/sources/1142230a24c5b94d-PermeanceActuator.mo)

```modelica
27:     annotation (choicesAllMatching=true, Dialog(group="Material"));
28: 
29:   parameter SI.Mass m_a=0.012 "Mass of armature"
30:     annotation (Dialog(group="Armature and stopper"));
31: 
32:   parameter SI.TranslationalSpringConstant c=1e11
```


## Execution evidence

[Rumoca commands, return codes, integrity hashes, bounded output and metadata](../evidence/086c556da894438a.json). Baseline: **tool-error**.

No independent runtime override was executed for this target in this audit; this is not a pass.

## Recommended action

Resolve the intended parameter domain and enclosing equations; check inherited bounds, final/protected status, guards and aliases. Construct an otherwise-valid source-level witness, establish a clean baseline in a capable engine, then retranslate at the witness and compare with the runtime override. For equality claims use the actual partner value. Do not apply a blanket min>0 fix yet.

## Scope and limitations

A source-level verdict addresses the reported declaration/claim, not every possible connected system. Tests cover 0–0.5 seconds and are not a proof of long-run stability. Shared instances are not distinct root causes. A missing bound, timeout, compiler error or failed nominal run alone never counts as a verified bug or a false positive. Fixes are proposals; no library/compiler implementation was changed.

[Group and related reports](../groups/baseline-blocked.md) · [Index](../README.md)
