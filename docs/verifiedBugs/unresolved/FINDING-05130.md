# FINDING-05130: Not yet established as a bug or a false positive

| Field | Value |
|---|---|
| Verdict | unresolved |
| Scope / group | baseline-blocked |
| Model | RigidBody.Examples.FixedWingPlant |
| Target | mass |
| Student classification | divisor-reachable-zero |
| Original report | [FINDING-fixedwingplant-mass-divzero.md](../../v2/bugs/FINDING-fixedwingplant-mass-divzero.md) — reviewed as `FINDING-05130-fixedwingplant-mass.md`, which a later run renamed |
| Original SHA-256 | 56351e4a2ed9b6bab71fe85890ec04787f2cc83e6a247d2935536c6350bc2161 |

## What remains unresolved

The current Rumoca nominal run is tool-error, before any reported perturbation. This prevents causal attribution to this parameter. Source metadata was recovered, but none of the reviewed source proofs or counterexamples establishes this particular claim. A baseline failure/tool limitation is neither confirmation nor a false positive.

## Source evidence

Compiler/source-resolved declaration: `/data/mrumoca/rumoca/target/cmm/CMM-a642c381/RigidBody/package.mo:3`. Role: `parameter`; binding: `5.5`; effective min: `None`; effective max: `None`. 

[/data/mrumoca/rumoca/target/cmm/CMM-a642c381/RigidBody/package.mo — source snapshot](../evidence/sources/e8b2bd080ef1d960-package.mo)

```modelica
1: package RigidBody
2:   partial model RigidBody6DOF
3:     parameter Real mass = 1.0 "Mass [kg]";
4:     parameter Real g = 9.8 "Gravity [m/s^2]";
5:     parameter Real ixx = 1.0 "Body inertia matrix xx entry [kg*m^2]";
6:     parameter Real iyy = 1.0 "Body inertia matrix yy entry [kg*m^2]";
```


## Execution evidence

[Rumoca commands, return codes, integrity hashes, bounded output and metadata](../evidence/ad6e9f5e9a6c9594.json). Baseline: **tool-error**.

No independent runtime override was executed for this target in this audit; this is not a pass.

## Recommended action

Resolve the intended parameter domain and enclosing equations; check inherited bounds, final/protected status, guards and aliases. Construct an otherwise-valid source-level witness, establish a clean baseline in a capable engine, then retranslate at the witness and compare with the runtime override. For equality claims use the actual partner value. Do not apply a blanket min>0 fix yet.

## Scope and limitations

A source-level verdict addresses the reported declaration/claim, not every possible connected system. Tests cover 0–0.5 seconds and are not a proof of long-run stability. Shared instances are not distinct root causes. A missing bound, timeout, compiler error or failed nominal run alone never counts as a verified bug or a false positive. Fixes are proposals; no library/compiler implementation was changed.

[Group and related reports](../groups/baseline-blocked.md) · [Index](../README.md)
