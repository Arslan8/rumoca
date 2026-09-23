# FINDING-05131: Not yet established as a bug or a false positive

| Field | Value |
|---|---|
| Verdict | unresolved |
| Scope / group | baseline-blocked |
| Model | RigidBody.Examples.RoverPlant |
| Target | max_speed |
| Student classification | divisor-reachable-zero |
| Original report | [FINDING-roverplant-max-speed-divzero.md](../../v2/bugs/FINDING-roverplant-max-speed-divzero.md) — reviewed as `FINDING-05131-roverplant-max-speed.md`, which a later run renamed |
| Original SHA-256 | 12494d91f230907cd033840cb39be5cec424ec243d8f8d3842934e80f4eb5799 |

## What remains unresolved

The current Rumoca nominal run is tool-error, before any reported perturbation. This prevents causal attribution to this parameter. Source metadata was recovered, but none of the reviewed source proofs or counterexamples establishes this particular claim. A baseline failure/tool limitation is neither confirmation nor a false positive.

## Source evidence

Compiler/source-resolved declaration: `/data/mrumoca/rumoca/target/cmm/CMM-a642c381/RigidBody/Examples/RoverPlant.mo:16`. Role: `parameter`; binding: `8.0`; effective min: `None`; effective max: `None`. 

[/data/mrumoca/rumoca/target/cmm/CMM-a642c381/RigidBody/Examples/RoverPlant.mo — source snapshot](../evidence/sources/f499cee1062a8819-RoverPlant.mo)

```modelica
14: 
15:   parameter Real wheel_radius = 0.15 "Wheel radius [m]";
16:   parameter Real max_speed = 8.0 "Maximum forward speed [m/s]";
17:   parameter Real max_yaw_rate = 1.2 "Maximum yaw rate [rad/s]";
18:   parameter Real speed_tau = 0.35 "Longitudinal speed response time [s]";
19:   parameter Real yaw_tau = 0.25 "Yaw-rate response time [s]";
```


## Execution evidence

[Rumoca commands, return codes, integrity hashes, bounded output and metadata](../evidence/8525c747c098f5ee.json). Baseline: **tool-error**.

No independent runtime override was executed for this target in this audit; this is not a pass.

## Recommended action

Resolve the intended parameter domain and enclosing equations; check inherited bounds, final/protected status, guards and aliases. Construct an otherwise-valid source-level witness, establish a clean baseline in a capable engine, then retranslate at the witness and compare with the runtime override. For equality claims use the actual partner value. Do not apply a blanket min>0 fix yet.

## Scope and limitations

A source-level verdict addresses the reported declaration/claim, not every possible connected system. Tests cover 0–0.5 seconds and are not a proof of long-run stability. Shared instances are not distinct root causes. A missing bound, timeout, compiler error or failed nominal run alone never counts as a verified bug or a false positive. Fixes are proposals; no library/compiler implementation was changed.

[Group and related reports](../groups/baseline-blocked.md) · [Index](../README.md)
