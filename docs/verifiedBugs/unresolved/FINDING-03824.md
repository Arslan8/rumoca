# FINDING-03824: Not yet established as a bug or a false positive

| Field | Value |
|---|---|
| Verdict | unresolved |
| Scope / group | baseline-blocked |
| Model | Modelica.Magnetic.FluxTubes.Examples.SolenoidActuator.Components.AdvancedSolenoid |
| Target | C_par |
| Student classification | physical-bound-permits-zero |
| Original report | [FINDING-advancedsolenoid-c-par-zerolimit.md](../../v2/bugs/FINDING-advancedsolenoid-c-par-zerolimit.md) — reviewed as `FINDING-03824-advancedsolenoid-c-par.md`, which a later run renamed |
| Original SHA-256 | 1e3709dfa2920d3999db493c51c22883d0aa42185a902673820db683eed2802a |

## What remains unresolved

The current Rumoca nominal run is tool-error, before any reported perturbation. This prevents causal attribution to this parameter. Source metadata was recovered, but none of the reviewed source proofs or counterexamples establishes this particular claim. A baseline failure/tool limitation is neither confirmation nor a false positive.

## Source evidence

Compiler/source-resolved declaration: `Magnetic/FluxTubes/Examples/SolenoidActuator/Components/AdvancedSolenoid.mo:11`. Role: `parameter`; binding: `1e-09`; effective min: `0`; effective max: `None`. 

[Magnetic/FluxTubes/Examples/SolenoidActuator/Components/AdvancedSolenoid.mo — source snapshot](../evidence/sources/db2a7ffbdda4969b-AdvancedSolenoid.mo)

```modelica
9:   parameter SI.Resistance R_par=1e5
10:     "Resistance parallel to the coil, in series to C_par";
11:   parameter SI.Capacitance C_par=1e-9
12:     "Capacitance parallel to the coil, in series to R_par";
13: 
14:   //yoke
```


## Execution evidence

[Rumoca commands, return codes, integrity hashes, bounded output and metadata](../evidence/2b15116b50ad0f74.json). Baseline: **tool-error**.

No independent runtime override was executed for this target in this audit; this is not a pass.

## Recommended action

Resolve the intended parameter domain and enclosing equations; check inherited bounds, final/protected status, guards and aliases. Construct an otherwise-valid source-level witness, establish a clean baseline in a capable engine, then retranslate at the witness and compare with the runtime override. For equality claims use the actual partner value. Do not apply a blanket min>0 fix yet.

## Scope and limitations

A source-level verdict addresses the reported declaration/claim, not every possible connected system. Tests cover 0–0.5 seconds and are not a proof of long-run stability. Shared instances are not distinct root causes. A missing bound, timeout, compiler error or failed nominal run alone never counts as a verified bug or a false positive. Fixes are proposals; no library/compiler implementation was changed.

[Group and related reports](../groups/baseline-blocked.md) · [Index](../README.md)
