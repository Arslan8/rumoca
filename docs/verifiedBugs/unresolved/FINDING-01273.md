# FINDING-01273: Not yet established as a bug or a false positive

| Field | Value |
|---|---|
| Verdict | unresolved |
| Scope / group | baseline-blocked |
| Model | Modelica.Electrical.Machines.Examples.DCMachines.DCPM_CurrentControlled |
| Target | k |
| Student classification | physical-domain-unenforced |
| Original report | [FINDING-dcpm-currentcontrolled-k-intent.md](../../v2/bugs/FINDING-dcpm-currentcontrolled-k-intent.md) — reviewed as `FINDING-01273-dcpm-currentcontrolled-k.md`, which a later run renamed |
| Original SHA-256 | 6b47040419f6f247b95922744fc72ac4bb7258f852667941cca29e2355c48150 |

## What remains unresolved

The current Rumoca nominal run is tool-error, before any reported perturbation. This prevents causal attribution to this parameter. Source metadata was recovered, but none of the reviewed source proofs or counterexamples establishes this particular claim. A baseline failure/tool limitation is neither confirmation nor a false positive.

## Source evidence

Compiler/source-resolved declaration: `Electrical/Machines/Examples/DCMachines/DCPM_CurrentControlled.mo:16`. Role: `parameter`; binding: `((Ra * Ta) / (2 * Ts))`; effective min: `None`; effective max: `None`. 

[Electrical/Machines/Examples/DCMachines/DCPM_CurrentControlled.mo — source snapshot](../evidence/sources/7201d33bf2cce885-DCPM_CurrentControlled.mo)

```modelica
14:   parameter SI.Time Ta=dcpmData.La/Ra "Armature time constant";
15:   parameter SI.Time Ts=1e-3 "Dead time of inverter";
16:   parameter SI.Resistance k=Ra*Ta/(2*Ts) "Current controller proportional gain";
17:   parameter SI.Time Ti=Ta "Current controller integral time constant";
18:   parameter SI.MagneticFlux kPhi=ViNominal/dcpmData.wNominal "Voltage constant";
19:   Machines.BasicMachines.DCMachines.DC_PermanentMagnet dcpm(
```


## Execution evidence

[Rumoca commands, return codes, integrity hashes, bounded output and metadata](../evidence/77b1c55854f32a4c.json). Baseline: **tool-error**.

No independent runtime override was executed for this target in this audit; this is not a pass.

## Recommended action

Resolve the intended parameter domain and enclosing equations; check inherited bounds, final/protected status, guards and aliases. Construct an otherwise-valid source-level witness, establish a clean baseline in a capable engine, then retranslate at the witness and compare with the runtime override. For equality claims use the actual partner value. Do not apply a blanket min>0 fix yet.

## Scope and limitations

A source-level verdict addresses the reported declaration/claim, not every possible connected system. Tests cover 0–0.5 seconds and are not a proof of long-run stability. Shared instances are not distinct root causes. A missing bound, timeout, compiler error or failed nominal run alone never counts as a verified bug or a false positive. Fixes are proposals; no library/compiler implementation was changed.

[Group and related reports](../groups/baseline-blocked.md) · [Index](../README.md)
