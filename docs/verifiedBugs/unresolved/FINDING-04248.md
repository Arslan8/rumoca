# FINDING-04248: Not yet established as a bug or a false positive

| Field | Value |
|---|---|
| Verdict | unresolved |
| Scope / group | baseline-blocked |
| Model | Modelica.Mechanics.MultiBody.Examples.Systems.RobotR3.Utilities.MechanicalStructure |
| Target | mLoad |
| Student classification | physical-bound-permits-zero |
| Original report | [FINDING-mechanicalstructure-mload-intent.md](../../v2/bugs/FINDING-mechanicalstructure-mload-intent.md) — reviewed as `FINDING-04248-mechanicalstructure-mload.md`, which a later run renamed |
| Original SHA-256 | 986c5cb6b14f09e7780d234e44340e8a80b22cfff73777918da98bf5fefb609d |

## What remains unresolved

The current Rumoca nominal run is tool-error, before any reported perturbation. This prevents causal attribution to this parameter. Source metadata was recovered, but none of the reviewed source proofs or counterexamples establishes this particular claim. A baseline failure/tool limitation is neither confirmation nor a false positive.

## Source evidence

Compiler/source-resolved declaration: `Mechanics/MultiBody/Examples/Systems/RobotR3/Utilities/MechanicalStructure.mo:7`. Role: `parameter`; binding: `15`; effective min: `0`; effective max: `None`. 

[Mechanics/MultiBody/Examples/Systems/RobotR3/Utilities/MechanicalStructure.mo — source snapshot](../evidence/sources/d38be6c61cc89b4c-MechanicalStructure.mo)

```modelica
5: 
6:   parameter Boolean animation=true "= true, if animation shall be enabled";
7:   parameter SI.Mass mLoad(min=0)=15 "Mass of load";
8:   parameter SI.Position rLoad[3]={0,0.25,0}
9:     "Distance from last flange to load mass";
10:   parameter SI.Acceleration g=9.81 "Gravity acceleration";
```


## Execution evidence

[Rumoca commands, return codes, integrity hashes, bounded output and metadata](../evidence/24c9ba888f1f8278.json). Baseline: **tool-error**.

No independent runtime override was executed for this target in this audit; this is not a pass.

## Recommended action

Resolve the intended parameter domain and enclosing equations; check inherited bounds, final/protected status, guards and aliases. Construct an otherwise-valid source-level witness, establish a clean baseline in a capable engine, then retranslate at the witness and compare with the runtime override. For equality claims use the actual partner value. Do not apply a blanket min>0 fix yet.

## Scope and limitations

A source-level verdict addresses the reported declaration/claim, not every possible connected system. Tests cover 0–0.5 seconds and are not a proof of long-run stability. Shared instances are not distinct root causes. A missing bound, timeout, compiler error or failed nominal run alone never counts as a verified bug or a false positive. Fixes are proposals; no library/compiler implementation was changed.

[Group and related reports](../groups/baseline-blocked.md) · [Index](../README.md)
