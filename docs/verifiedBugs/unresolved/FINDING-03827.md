# FINDING-03827: Not yet established as a bug or a false positive

| Field | Value |
|---|---|
| Verdict | unresolved |
| Scope / group | baseline-blocked |
| Model | Modelica.Magnetic.FluxTubes.Examples.SolenoidActuator.Components.AdvancedSolenoid |
| Target | rho_steel |
| Student classification | physical-bound-permits-zero |
| Original report | [FINDING-advancedsolenoid-rho-steel-zerolimit.md](../../v2/bugs/FINDING-advancedsolenoid-rho-steel-zerolimit.md) — reviewed as `FINDING-03827-advancedsolenoid-rho-steel.md`, which a later run renamed |
| Original SHA-256 | 08a9ed56356410b66d70b93070340e423d27e7c14b1848a9d4e91f69e6e90d61 |

## What remains unresolved

The current Rumoca nominal run is tool-error, before any reported perturbation. This prevents causal attribution to this parameter. Source metadata was recovered, but none of the reviewed source proofs or counterexamples establishes this particular claim. A baseline failure/tool limitation is neither confirmation nor a false positive.

## Source evidence

Compiler/source-resolved declaration: `Magnetic/FluxTubes/Examples/SolenoidActuator/Components/AdvancedSolenoid.mo:59`. Role: `parameter`; binding: `7853`; effective min: `0.0`; effective max: `None`. 

[Magnetic/FluxTubes/Examples/SolenoidActuator/Components/AdvancedSolenoid.mo — source snapshot](../evidence/sources/db2a7ffbdda4969b-AdvancedSolenoid.mo)

```modelica
57: 
58: protected
59:   parameter SI.Density rho_steel=7853
60:     "Density for calculation of armature mass from geometry";
61: 
62: public
```


## Execution evidence

[Rumoca commands, return codes, integrity hashes, bounded output and metadata](../evidence/2b15116b50ad0f74.json). Baseline: **tool-error**.

No independent runtime override was executed for this target in this audit; this is not a pass.

## Recommended action

Resolve the intended parameter domain and enclosing equations; check inherited bounds, final/protected status, guards and aliases. Construct an otherwise-valid source-level witness, establish a clean baseline in a capable engine, then retranslate at the witness and compare with the runtime override. For equality claims use the actual partner value. Do not apply a blanket min>0 fix yet.

## Scope and limitations

A source-level verdict addresses the reported declaration/claim, not every possible connected system. Tests cover 0–0.5 seconds and are not a proof of long-run stability. Shared instances are not distinct root causes. A missing bound, timeout, compiler error or failed nominal run alone never counts as a verified bug or a false positive. Fixes are proposals; no library/compiler implementation was changed.

[Group and related reports](../groups/baseline-blocked.md) · [Index](../README.md)
