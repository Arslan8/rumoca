# FINDING-01263: Not yet established as a bug or a false positive

| Field | Value |
|---|---|
| Verdict | unresolved |
| Scope / group | baseline-blocked |
| Model | Modelica.Electrical.Machines.Examples.DCMachines.DCPM_Cooling |
| Target | dTCoolant |
| Student classification | divisor-reachable-zero |
| Original report | `FINDING-01263-dcpm-cooling-dtcoolant.md` — [withdrawn](../../v2/bugs/withdrawn.md); a later run no longer makes this claim |
| Original SHA-256 | a1a2068083e04d9498487166919bb12828c55a5a588a024b60a86f18e3814e9c |

## What remains unresolved

The current Rumoca nominal run is tool-error, before any reported perturbation. This prevents causal attribution to this parameter. Source metadata was recovered, but none of the reviewed source proofs or counterexamples establishes this particular claim. A baseline failure/tool limitation is neither confirmation nor a false positive.

## Source evidence

Compiler/source-resolved declaration: `Electrical/Machines/Examples/DCMachines/DCPM_Cooling.mo:20`. Role: `parameter`; binding: `10`; effective min: `None`; effective max: `None`. 

[Electrical/Machines/Examples/DCMachines/DCPM_Cooling.mo — source snapshot](../evidence/sources/f148851cfdfd9dcf-DCPM_Cooling.mo)

```modelica
18:   final parameter SI.Temperature T0=293.15
19:     "Reference temperature 20 degC";
20:   final parameter SI.TemperatureDifference dTCoolant=10
21:     "Coolant's temperature rise";
22:   final parameter SI.TemperatureDifference dTArmature=dcpm.TaNominal
23:        - T0 - dTCoolant/2 "Armature's temperature rise over coolant";
```


## Execution evidence

[Rumoca commands, return codes, integrity hashes, bounded output and metadata](../evidence/2651adcda9432b0e.json). Baseline: **tool-error**.

No independent runtime override was executed for this target in this audit; this is not a pass.

## Recommended action

Resolve the intended parameter domain and enclosing equations; check inherited bounds, final/protected status, guards and aliases. Construct an otherwise-valid source-level witness, establish a clean baseline in a capable engine, then retranslate at the witness and compare with the runtime override. For equality claims use the actual partner value. Do not apply a blanket min>0 fix yet.

## Scope and limitations

A source-level verdict addresses the reported declaration/claim, not every possible connected system. Tests cover 0–0.5 seconds and are not a proof of long-run stability. Shared instances are not distinct root causes. A missing bound, timeout, compiler error or failed nominal run alone never counts as a verified bug or a false positive. Fixes are proposals; no library/compiler implementation was changed.

[Group and related reports](../groups/baseline-blocked.md) · [Index](../README.md)
