# FINDING-03860: Not yet established as a bug or a false positive

| Field | Value |
|---|---|
| Verdict | unresolved |
| Scope / group | baseline-blocked |
| Model | Modelica.Magnetic.FluxTubes.Examples.SolenoidActuator.Components.SimpleSolenoid |
| Target | rho_steel |
| Student classification | physical-bound-permits-zero |
| Original report | [FINDING-simplesolenoid-rho-steel-zerolimit.md](../../v2/bugs/FINDING-simplesolenoid-rho-steel-zerolimit.md) — reviewed as `FINDING-03860-simplesolenoid-rho-steel.md`, which a later run renamed |
| Original SHA-256 | 9e228d0d7d1bf31be1c22f7d452a89494d9248427d746871bf3a158626145539 |

## What remains unresolved

The current Rumoca nominal run is tool-error, before any reported perturbation. This prevents causal attribution to this parameter. Source metadata was recovered, but none of the reviewed source proofs or counterexamples establishes this particular claim. A baseline failure/tool limitation is neither confirmation nor a false positive.

## Source evidence

Compiler/source-resolved declaration: `Magnetic/FluxTubes/Examples/SolenoidActuator/Components/SimpleSolenoid.mo:51`. Role: `parameter`; binding: `7853`; effective min: `0.0`; effective max: `None`. 

[Magnetic/FluxTubes/Examples/SolenoidActuator/Components/SimpleSolenoid.mo — source snapshot](../evidence/sources/781a69dd73dfb074-SimpleSolenoid.mo)

```modelica
49: 
50: protected
51:   parameter SI.Density rho_steel=7853
52:     "Density for calculation of armature mass from geometry";
53: 
54: public
```


## Execution evidence

[Rumoca commands, return codes, integrity hashes, bounded output and metadata](../evidence/58e9d70f53839800.json). Baseline: **tool-error**.

No independent runtime override was executed for this target in this audit; this is not a pass.

## Recommended action

Resolve the intended parameter domain and enclosing equations; check inherited bounds, final/protected status, guards and aliases. Construct an otherwise-valid source-level witness, establish a clean baseline in a capable engine, then retranslate at the witness and compare with the runtime override. For equality claims use the actual partner value. Do not apply a blanket min>0 fix yet.

## Scope and limitations

A source-level verdict addresses the reported declaration/claim, not every possible connected system. Tests cover 0–0.5 seconds and are not a proof of long-run stability. Shared instances are not distinct root causes. A missing bound, timeout, compiler error or failed nominal run alone never counts as a verified bug or a false positive. Fixes are proposals; no library/compiler implementation was changed.

[Group and related reports](../groups/baseline-blocked.md) · [Index](../README.md)
