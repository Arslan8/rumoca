# FINDING-05136: Not yet established as a bug or a false positive

| Field | Value |
|---|---|
| Verdict | unresolved |
| Scope / group | baseline-blocked |
| Model | RigidBody.Examples.RoverPlant |
| Target | vertical_tau |
| Student classification | divisor-reachable-zero |
| Original report | [FINDING-roverplant-vertical-tau-divzero.md](../../v2/bugs/FINDING-roverplant-vertical-tau-divzero.md) — reviewed as `FINDING-05136-roverplant-vertical-tau.md`, which a later run renamed |
| Original SHA-256 | 4d48844ff3a561a3cfb85119312ba5900aac4c09b4b3f17093ba86142d0ae813 |

## What remains unresolved

The current Rumoca nominal run is tool-error, before any reported perturbation. This prevents causal attribution to this parameter. Source metadata was recovered, but none of the reviewed source proofs or counterexamples establishes this particular claim. A baseline failure/tool limitation is neither confirmation nor a false positive.

## Source evidence

Compiler/source-resolved declaration: `/data/mrumoca/rumoca/target/cmm/CMM-a642c381/RigidBody/Examples/RoverPlant.mo:21`. Role: `parameter`; binding: `0.05`; effective min: `None`; effective max: `None`. 

[/data/mrumoca/rumoca/target/cmm/CMM-a642c381/RigidBody/Examples/RoverPlant.mo — source snapshot](../evidence/sources/f499cee1062a8819-RoverPlant.mo)

```modelica
19:   parameter Real yaw_tau = 0.25 "Yaw-rate response time [s]";
20:   parameter Real side_tau = 0.12 "Lateral velocity damping time [s]";
21:   parameter Real vertical_tau = 0.05 "Vertical velocity damping time [s]";
22:   parameter Real height_tau = 0.08 "Ground-height correction time [s]";
23:   parameter Real mag_world_ned[3] = {0.21, 0.0, 0.45} "Mag field NED [Gauss]";
24:   parameter Real R_FRD_FLU[3, 3] = [
```


## Execution evidence

[Rumoca commands, return codes, integrity hashes, bounded output and metadata](../evidence/8525c747c098f5ee.json). Baseline: **tool-error**.

No independent runtime override was executed for this target in this audit; this is not a pass.

## Recommended action

Resolve the intended parameter domain and enclosing equations; check inherited bounds, final/protected status, guards and aliases. Construct an otherwise-valid source-level witness, establish a clean baseline in a capable engine, then retranslate at the witness and compare with the runtime override. For equality claims use the actual partner value. Do not apply a blanket min>0 fix yet.

## Scope and limitations

A source-level verdict addresses the reported declaration/claim, not every possible connected system. Tests cover 0–0.5 seconds and are not a proof of long-run stability. Shared instances are not distinct root causes. A missing bound, timeout, compiler error or failed nominal run alone never counts as a verified bug or a false positive. Fixes are proposals; no library/compiler implementation was changed.

[Group and related reports](../groups/baseline-blocked.md) · [Index](../README.md)
