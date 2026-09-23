# FINDING-01353: Not yet established as a bug or a false positive

| Field | Value |
|---|---|
| Verdict | unresolved |
| Scope / group | baseline-blocked |
| Model | Modelica.Electrical.Machines.Examples.DCMachines.DCPM_QuasiStatic |
| Target | JLoad |
| Student classification | physical-domain-unenforced |
| Original report | [FINDING-dcpm-quasistatic-jload-zerolimit.md](../../v2/bugs/FINDING-dcpm-quasistatic-jload-zerolimit.md) — reviewed as `FINDING-01353-dcpm-quasistatic-jload.md`, which a later run renamed |
| Original SHA-256 | 92130b6175769b26db51c94341f890e397c8ae5807c73e3a8015f7cf5b313d9c |

## What remains unresolved

The current Rumoca nominal run is tool-error, before any reported perturbation. This prevents causal attribution to this parameter. Source metadata was recovered, but none of the reviewed source proofs or counterexamples establishes this particular claim. A baseline failure/tool limitation is neither confirmation nor a false positive.

## Source evidence

Compiler/source-resolved declaration: `Electrical/Machines/Examples/DCMachines/DCPM_QuasiStatic.mo:10`. Role: `parameter`; binding: `0.15`; effective min: `None`; effective max: `None`. 

[Electrical/Machines/Examples/DCMachines/DCPM_QuasiStatic.mo — source snapshot](../evidence/sources/fb656f6c6c2ccae4-DCPM_QuasiStatic.mo)

```modelica
8:       Modelica.Units.Conversions.from_rpm(1500) "No-load speed";
9:   parameter SI.Torque TLoad=63.66 "Nominal load torque";
10:   parameter SI.Inertia JLoad=0.15
11:     "Load's moment of inertia";
12:   Machines.BasicMachines.DCMachines.DC_PermanentMagnet dcpm1(
13:     VaNominal=dcpmData.VaNominal,
```


## Execution evidence

[Rumoca commands, return codes, integrity hashes, bounded output and metadata](../evidence/aea5ee8f9a92fcb1.json). Baseline: **tool-error**.

No independent runtime override was executed for this target in this audit; this is not a pass.

## Recommended action

Resolve the intended parameter domain and enclosing equations; check inherited bounds, final/protected status, guards and aliases. Construct an otherwise-valid source-level witness, establish a clean baseline in a capable engine, then retranslate at the witness and compare with the runtime override. For equality claims use the actual partner value. Do not apply a blanket min>0 fix yet.

## Scope and limitations

A source-level verdict addresses the reported declaration/claim, not every possible connected system. Tests cover 0–0.5 seconds and are not a proof of long-run stability. Shared instances are not distinct root causes. A missing bound, timeout, compiler error or failed nominal run alone never counts as a verified bug or a false positive. Fixes are proposals; no library/compiler implementation was changed.

[Group and related reports](../groups/baseline-blocked.md) · [Index](../README.md)
