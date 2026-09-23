# FINDING-03774: Not yet established as a bug or a false positive

| Field | Value |
|---|---|
| Verdict | unresolved |
| Scope / group | baseline-blocked |
| Model | Modelica.Magnetic.FluxTubes.Examples.MovingCoilActuator.ArmatureStroke |
| Target | cActuator.L |
| Student classification | physical-domain-unenforced |
| Original report | [FINDING-armaturestroke-cactuator-l-zerolimit.md](../../v2/bugs/FINDING-armaturestroke-cactuator-l-zerolimit.md) — reviewed as `FINDING-03774-armaturestroke-cactuator-l.md`, which a later run renamed |
| Original SHA-256 | 5de45c5b357db6c5666e6996c096fdae6d11e129c7f5376bf1d777ca733394b8 |

## What remains unresolved

The current Rumoca nominal run is tool-error, before any reported perturbation. This prevents causal attribution to this parameter. Source metadata was recovered, but none of the reviewed source proofs or counterexamples establishes this particular claim. A baseline failure/tool limitation is neither confirmation nor a false positive.

## Source evidence

Compiler/source-resolved declaration: `Magnetic/FluxTubes/Examples/MovingCoilActuator/Components/ConstantActuator.mo:7`. Role: `parameter`; binding: `0.0051`; effective min: `None`; effective max: `None`. 

[Magnetic/FluxTubes/Examples/MovingCoilActuator/Components/ConstantActuator.mo — source snapshot](../evidence/sources/38e251a55a83ff04-ConstantActuator.mo)

```modelica
5:   parameter SI.ElectricalForceConstant k=3.88 "Converter constant";
6:   parameter SI.Resistance R=2.86 "Coil resistance";
7:   parameter SI.Inductance L=0.0051 "Coil inductance at mid-stroke";
8:   parameter SI.Mass m_a=0.012 "Armature mass"
9:     annotation (Dialog(group="Armature and stopper"));
10:   parameter SI.TranslationalSpringConstant c=1e11
```


## Execution evidence

[Rumoca commands, return codes, integrity hashes, bounded output and metadata](../evidence/086c556da894438a.json). Baseline: **tool-error**.

No independent runtime override was executed for this target in this audit; this is not a pass.

## Recommended action

Resolve the intended parameter domain and enclosing equations; check inherited bounds, final/protected status, guards and aliases. Construct an otherwise-valid source-level witness, establish a clean baseline in a capable engine, then retranslate at the witness and compare with the runtime override. For equality claims use the actual partner value. Do not apply a blanket min>0 fix yet.

## Scope and limitations

A source-level verdict addresses the reported declaration/claim, not every possible connected system. Tests cover 0–0.5 seconds and are not a proof of long-run stability. Shared instances are not distinct root causes. A missing bound, timeout, compiler error or failed nominal run alone never counts as a verified bug or a false positive. Fixes are proposals; no library/compiler implementation was changed.

[Group and related reports](../groups/baseline-blocked.md) · [Index](../README.md)
