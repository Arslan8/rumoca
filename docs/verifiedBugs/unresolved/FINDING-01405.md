# FINDING-01405: Not yet established as a bug or a false positive

| Field | Value |
|---|---|
| Verdict | unresolved |
| Scope / group | baseline-blocked |
| Model | Modelica.Electrical.Machines.Examples.DCMachines.DCPM_Temperature |
| Target | JLoad |
| Student classification | physical-domain-unenforced |
| Original report | [FINDING-dcpm-temperature-jload-zerolimit.md](../../v2/bugs/FINDING-dcpm-temperature-jload-zerolimit.md) — reviewed as `FINDING-01405-dcpm-temperature-jload.md`, which a later run renamed |
| Original SHA-256 | 19f662eb832fbcb82a020b9bd45cc599e99c9176906730a2661046ec89b2fb12 |

## What remains unresolved

The current Rumoca nominal run is tool-error, before any reported perturbation. This prevents causal attribution to this parameter. Source metadata was recovered, but none of the reviewed source proofs or counterexamples establishes this particular claim. A baseline failure/tool limitation is neither confirmation nor a false positive.

## Source evidence

Compiler/source-resolved declaration: `Electrical/Machines/Examples/DCMachines/DCPM_Temperature.mo:10`. Role: `parameter`; binding: `0.15`; effective min: `None`; effective max: `None`. 

[Electrical/Machines/Examples/DCMachines/DCPM_Temperature.mo — source snapshot](../evidence/sources/bec4cc5921f02d47-DCPM_Temperature.mo)

```modelica
8:       Modelica.Units.Conversions.from_rpm(1500) "No-load speed";
9:   parameter SI.Torque TLoad=63.66 "Nominal load torque";
10:   parameter SI.Inertia JLoad=0.15
11:     "Load's moment of inertia";
12:   Machines.BasicMachines.DCMachines.DC_PermanentMagnet dcpm(
13:     wMechanical(start=w0, fixed=true),
```


## Execution evidence

[Rumoca commands, return codes, integrity hashes, bounded output and metadata](../evidence/f6a744925526df08.json). Baseline: **tool-error**.

No independent runtime override was executed for this target in this audit; this is not a pass.

## Recommended action

Resolve the intended parameter domain and enclosing equations; check inherited bounds, final/protected status, guards and aliases. Construct an otherwise-valid source-level witness, establish a clean baseline in a capable engine, then retranslate at the witness and compare with the runtime override. For equality claims use the actual partner value. Do not apply a blanket min>0 fix yet.

## Scope and limitations

A source-level verdict addresses the reported declaration/claim, not every possible connected system. Tests cover 0–0.5 seconds and are not a proof of long-run stability. Shared instances are not distinct root causes. A missing bound, timeout, compiler error or failed nominal run alone never counts as a verified bug or a false positive. Fixes are proposals; no library/compiler implementation was changed.

[Group and related reports](../groups/baseline-blocked.md) · [Index](../README.md)
