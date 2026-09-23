# FINDING-03826: Not yet established as a bug or a false positive

| Field | Value |
|---|---|
| Verdict | unresolved |
| Scope / group | baseline-blocked |
| Model | Modelica.Magnetic.FluxTubes.Examples.SolenoidActuator.Components.AdvancedSolenoid |
| Target | d |
| Student classification | physical-domain-unenforced |
| Original report | [FINDING-advancedsolenoid-d-intent.md](../../v2/bugs/FINDING-advancedsolenoid-d-intent.md) — reviewed as `FINDING-03826-advancedsolenoid-d.md`, which a later run renamed |
| Original SHA-256 | b901e27047cb146cdbc19dd94dca2c9e9537f08137714a682a64af5e889f0856 |

## What remains unresolved

The current Rumoca nominal run is tool-error, before any reported perturbation. This prevents causal attribution to this parameter. Source metadata was recovered, but none of the reviewed source proofs or counterexamples establishes this particular claim. A baseline failure/tool limitation is neither confirmation nor a false positive.

## Source evidence

Compiler/source-resolved declaration: `Magnetic/FluxTubes/Examples/SolenoidActuator/Components/AdvancedSolenoid.mo:41`. Role: `parameter`; binding: `400`; effective min: `None`; effective max: `None`. 

[Magnetic/FluxTubes/Examples/SolenoidActuator/Components/AdvancedSolenoid.mo — source snapshot](../evidence/sources/db2a7ffbdda4969b-AdvancedSolenoid.mo)

```modelica
39:     "Spring stiffness between impact partners"
40:     annotation (Dialog(group="Armature and stopper"));
41:   parameter SI.TranslationalDampingConstant d=400
42:     "Damping coefficient between impact partners"
43:     annotation (Dialog(group="Armature and stopper"));
44:   parameter SI.Position x_min=0.25e-3
```


## Execution evidence

[Rumoca commands, return codes, integrity hashes, bounded output and metadata](../evidence/2b15116b50ad0f74.json). Baseline: **tool-error**.

No independent runtime override was executed for this target in this audit; this is not a pass.

## Recommended action

Resolve the intended parameter domain and enclosing equations; check inherited bounds, final/protected status, guards and aliases. Construct an otherwise-valid source-level witness, establish a clean baseline in a capable engine, then retranslate at the witness and compare with the runtime override. For equality claims use the actual partner value. Do not apply a blanket min>0 fix yet.

## Scope and limitations

A source-level verdict addresses the reported declaration/claim, not every possible connected system. Tests cover 0–0.5 seconds and are not a proof of long-run stability. Shared instances are not distinct root causes. A missing bound, timeout, compiler error or failed nominal run alone never counts as a verified bug or a false positive. Fixes are proposals; no library/compiler implementation was changed.

[Group and related reports](../groups/baseline-blocked.md) · [Index](../README.md)
