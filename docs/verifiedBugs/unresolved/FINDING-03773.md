# FINDING-03773: Not yet established as a bug or a false positive

| Field | Value |
|---|---|
| Verdict | unresolved |
| Scope / group | baseline-blocked |
| Model | Modelica.Magnetic.FluxTubes.Examples.MovingCoilActuator.ArmatureStroke |
| Target | cActuator.R |
| Student classification | physical-domain-unenforced |
| Original report | [FINDING-armaturestroke-cactuator-r-zerolimit.md](../../v2/bugs/FINDING-armaturestroke-cactuator-r-zerolimit.md) — reviewed as `FINDING-03773-armaturestroke-cactuator-r.md`, which a later run renamed |
| Original SHA-256 | 62c548b82c113e5840e03424c04dafe2b6c59fa86c14109801a56e3da643630d |

## What remains unresolved

The current Rumoca nominal run is tool-error, before any reported perturbation. This prevents causal attribution to this parameter. Source metadata was recovered, but none of the reviewed source proofs or counterexamples establishes this particular claim. A baseline failure/tool limitation is neither confirmation nor a false positive.

## Source evidence

Compiler/source-resolved declaration: `Magnetic/FluxTubes/Examples/MovingCoilActuator/Components/ConstantActuator.mo:6`. Role: `parameter`; binding: `2.86`; effective min: `None`; effective max: `None`. 

[Magnetic/FluxTubes/Examples/MovingCoilActuator/Components/ConstantActuator.mo — source snapshot](../evidence/sources/38e251a55a83ff04-ConstantActuator.mo)

```modelica
4: 
5:   parameter SI.ElectricalForceConstant k=3.88 "Converter constant";
6:   parameter SI.Resistance R=2.86 "Coil resistance";
7:   parameter SI.Inductance L=0.0051 "Coil inductance at mid-stroke";
8:   parameter SI.Mass m_a=0.012 "Armature mass"
9:     annotation (Dialog(group="Armature and stopper"));
```


## Execution evidence

[Rumoca commands, return codes, integrity hashes, bounded output and metadata](../evidence/086c556da894438a.json). Baseline: **tool-error**.

No independent runtime override was executed for this target in this audit; this is not a pass.

## Recommended action

Resolve the intended parameter domain and enclosing equations; check inherited bounds, final/protected status, guards and aliases. Construct an otherwise-valid source-level witness, establish a clean baseline in a capable engine, then retranslate at the witness and compare with the runtime override. For equality claims use the actual partner value. Do not apply a blanket min>0 fix yet.

## Scope and limitations

A source-level verdict addresses the reported declaration/claim, not every possible connected system. Tests cover 0–0.5 seconds and are not a proof of long-run stability. Shared instances are not distinct root causes. A missing bound, timeout, compiler error or failed nominal run alone never counts as a verified bug or a false positive. Fixes are proposals; no library/compiler implementation was changed.

[Group and related reports](../groups/baseline-blocked.md) · [Index](../README.md)
