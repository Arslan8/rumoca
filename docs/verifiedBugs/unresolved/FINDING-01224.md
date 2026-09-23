# FINDING-01224: Not yet established as a bug or a false positive

| Field | Value |
|---|---|
| Verdict | unresolved |
| Scope / group | baseline-blocked |
| Model | Modelica.Electrical.Machines.Examples.DCMachines.DCPM_Cooling |
| Target | G_armature_core |
| Student classification | physical-domain-unenforced |
| Original report | [FINDING-dcpm-cooling-g-armature-core-zerolimit.md](../../v2/bugs/FINDING-dcpm-cooling-g-armature-core-zerolimit.md) — reviewed as `FINDING-01224-dcpm-cooling-g-armature-core.md`, which a later run renamed |
| Original SHA-256 | fce9786124cfd008e2d271fe8ae7bf84d16b8ffa14ae979ae4504ca7ec05f87b |

## What remains unresolved

The current Rumoca nominal run is tool-error, before any reported perturbation. This prevents causal attribution to this parameter. Source metadata was recovered, but none of the reviewed source proofs or counterexamples establishes this particular claim. A baseline failure/tool limitation is neither confirmation nor a false positive.

## Source evidence

Compiler/source-resolved declaration: `Electrical/Machines/Examples/DCMachines/DCPM_Cooling.mo:24`. Role: `parameter`; binding: `((2 * Losses) / dTArmature)`; effective min: `None`; effective max: `None`. 

[Electrical/Machines/Examples/DCMachines/DCPM_Cooling.mo — source snapshot](../evidence/sources/f148851cfdfd9dcf-DCPM_Cooling.mo)

```modelica
22:   final parameter SI.TemperatureDifference dTArmature=dcpm.TaNominal
23:        - T0 - dTCoolant/2 "Armature's temperature rise over coolant";
24:   parameter SI.ThermalConductance G_armature_core=2*Losses/
25:       dTArmature "Heat conductance armature - core";
26:   parameter SI.ThermalConductance G_core_cooling=2*Losses/
27:       dTArmature "Heat conductance core - cooling";
```


## Execution evidence

[Rumoca commands, return codes, integrity hashes, bounded output and metadata](../evidence/2651adcda9432b0e.json). Baseline: **tool-error**.

No independent runtime override was executed for this target in this audit; this is not a pass.

## Recommended action

Resolve the intended parameter domain and enclosing equations; check inherited bounds, final/protected status, guards and aliases. Construct an otherwise-valid source-level witness, establish a clean baseline in a capable engine, then retranslate at the witness and compare with the runtime override. For equality claims use the actual partner value. Do not apply a blanket min>0 fix yet.

## Scope and limitations

A source-level verdict addresses the reported declaration/claim, not every possible connected system. Tests cover 0–0.5 seconds and are not a proof of long-run stability. Shared instances are not distinct root causes. A missing bound, timeout, compiler error or failed nominal run alone never counts as a verified bug or a false positive. Fixes are proposals; no library/compiler implementation was changed.

[Group and related reports](../groups/baseline-blocked.md) · [Index](../README.md)
