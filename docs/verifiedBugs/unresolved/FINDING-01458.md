# FINDING-01458: Not yet established as a bug or a false positive

| Field | Value |
|---|---|
| Verdict | unresolved |
| Scope / group | baseline-blocked |
| Model | Modelica.Electrical.Machines.Examples.DCMachines.DCPM_withLosses |
| Target | wLoad1 |
| Student classification | divisor-reachable-zero |
| Original report | `FINDING-01458-dcpm-withlosses-wload1.md` — [withdrawn](../../v2/bugs/withdrawn.md); a later run no longer makes this claim |
| Original SHA-256 | c1a9ac0a1dd1e3dff9d27690833c64ca1aa3f1ffe2c85deee21ab41b7ee2d748 |

## What remains unresolved

The current Rumoca nominal run is tool-error, before any reported perturbation. This prevents causal attribution to this parameter. Source metadata was recovered, but none of the reviewed source proofs or counterexamples establishes this particular claim. A baseline failure/tool limitation is neither confirmation nor a false positive.

## Source evidence

Compiler/source-resolved declaration: `Electrical/Machines/Examples/DCMachines/DCPM_withLosses.mo:11`. Role: `parameter`; binding: `(((1425 * 2) * (2 * asin(1.0))) / 60)`; effective min: `None`; effective max: `None`. 

[Electrical/Machines/Examples/DCMachines/DCPM_withLosses.mo — source snapshot](../evidence/sources/697c8494e65e1638-DCPM_withLosses.mo)

```modelica
9:   parameter SI.Time tRamp=0.8 "Armature voltage ramp";
10:   parameter SI.Torque TLoad1=63.66 "Nominal load torque";
11:   parameter SI.AngularVelocity wLoad1=1425*2*pi/60
12:     "Nominal load speed";
13:   parameter SI.Torque TLoad2=61.30 "Nominal load torque";
14:   parameter SI.AngularVelocity wLoad2=1417.5*2*pi/60
```


## Execution evidence

[Rumoca commands, return codes, integrity hashes, bounded output and metadata](../evidence/1255084b3c3934b8.json). Baseline: **tool-error**.

No independent runtime override was executed for this target in this audit; this is not a pass.

## Recommended action

Resolve the intended parameter domain and enclosing equations; check inherited bounds, final/protected status, guards and aliases. Construct an otherwise-valid source-level witness, establish a clean baseline in a capable engine, then retranslate at the witness and compare with the runtime override. For equality claims use the actual partner value. Do not apply a blanket min>0 fix yet.

## Scope and limitations

A source-level verdict addresses the reported declaration/claim, not every possible connected system. Tests cover 0–0.5 seconds and are not a proof of long-run stability. Shared instances are not distinct root causes. A missing bound, timeout, compiler error or failed nominal run alone never counts as a verified bug or a false positive. Fixes are proposals; no library/compiler implementation was changed.

[Group and related reports](../groups/baseline-blocked.md) · [Index](../README.md)
