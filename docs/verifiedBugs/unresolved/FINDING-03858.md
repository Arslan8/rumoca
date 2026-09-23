# FINDING-03858: Not yet established as a bug or a false positive

| Field | Value |
|---|---|
| Verdict | unresolved |
| Scope / group | baseline-blocked |
| Model | Modelica.Magnetic.FluxTubes.Examples.SolenoidActuator.Components.SimpleSolenoid |
| Target | c |
| Student classification | physical-domain-unenforced |
| Original report | [FINDING-simplesolenoid-c-intent.md](../../v2/bugs/FINDING-simplesolenoid-c-intent.md) — reviewed as `FINDING-03858-simplesolenoid-c.md`, which a later run renamed |
| Original SHA-256 | a30300facfda9205512711787bc3fd80a584ff7ce1f695bbba10eac95cbc2b69 |

## What remains unresolved

The current Rumoca nominal run is tool-error, before any reported perturbation. This prevents causal attribution to this parameter. Source metadata was recovered, but none of the reviewed source proofs or counterexamples establishes this particular claim. A baseline failure/tool limitation is neither confirmation nor a false positive.

## Source evidence

Compiler/source-resolved declaration: `Magnetic/FluxTubes/Examples/SolenoidActuator/Components/SimpleSolenoid.mo:34`. Role: `parameter`; binding: `100000000000.0`; effective min: `None`; effective max: `None`. 

[Magnetic/FluxTubes/Examples/SolenoidActuator/Components/SimpleSolenoid.mo — source snapshot](../evidence/sources/781a69dd73dfb074-SimpleSolenoid.mo)

```modelica
32:   parameter SI.Length l_arm=26e-3 "Armature length"
33:     annotation (Dialog(group="Armature and stopper"));
34:   parameter SI.TranslationalSpringConstant c=1e11
35:     "Spring stiffness between impact partners"
36:     annotation (Dialog(group="Armature and stopper"));
37:   parameter SI.TranslationalDampingConstant d=400
```


## Execution evidence

[Rumoca commands, return codes, integrity hashes, bounded output and metadata](../evidence/58e9d70f53839800.json). Baseline: **tool-error**.

No independent runtime override was executed for this target in this audit; this is not a pass.

## Recommended action

Resolve the intended parameter domain and enclosing equations; check inherited bounds, final/protected status, guards and aliases. Construct an otherwise-valid source-level witness, establish a clean baseline in a capable engine, then retranslate at the witness and compare with the runtime override. For equality claims use the actual partner value. Do not apply a blanket min>0 fix yet.

## Scope and limitations

A source-level verdict addresses the reported declaration/claim, not every possible connected system. Tests cover 0–0.5 seconds and are not a proof of long-run stability. Shared instances are not distinct root causes. A missing bound, timeout, compiler error or failed nominal run alone never counts as a verified bug or a false positive. Fixes are proposals; no library/compiler implementation was changed.

[Group and related reports](../groups/baseline-blocked.md) · [Index](../README.md)
