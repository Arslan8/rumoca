# FINDING-05140: Not yet established as a bug or a false positive

| Field | Value |
|---|---|
| Verdict | unresolved |
| Scope / group | baseline-blocked |
| Model | RigidBody.Examples.QuadrotorSIL |
| Target | vehicle_mass |
| Student classification | divisor-reachable-zero |
| Original report | `FINDING-05140-quadrotorsil-vehicle-mass.md` — [withdrawn](../../v2/bugs/withdrawn.md); a later run no longer makes this claim |
| Original SHA-256 | 7b8b73f991ea8aae73079ed64bb41a6f7399cf1d3ccb1509869bd8ac6d72efae |

## What remains unresolved

The current Rumoca nominal run is tool-error, before any reported perturbation. This prevents causal attribution to this parameter. Source metadata was recovered, but none of the reviewed source proofs or counterexamples establishes this particular claim. A baseline failure/tool limitation is neither confirmation nor a false positive.

## Source evidence

Compiler/source-resolved declaration: `/data/mrumoca/rumoca/target/cmm/CMM-a642c381/RigidBody/Examples/QuadrotorSIL.mo:16`. Role: `parameter`; binding: `2.0`; effective min: `None`; effective max: `None`. 

[/data/mrumoca/rumoca/target/cmm/CMM-a642c381/RigidBody/Examples/QuadrotorSIL.mo — source snapshot](../evidence/sources/0ca83ee587091198-QuadrotorSIL.mo)

```modelica
14: 
15: model QuadrotorSIL
16:   parameter Real vehicle_mass = 2.0 "Total vehicle mass [kg]";
17:   parameter Real vehicle_ixx = 0.02166666666666667 "Body inertia xx [kg*m^2]";
18:   parameter Real vehicle_iyy = 0.02166666666666667 "Body inertia yy [kg*m^2]";
19:   parameter Real vehicle_izz = 0.04000000000000001 "Body inertia zz [kg*m^2]";
```


## Execution evidence

[Rumoca commands, return codes, integrity hashes, bounded output and metadata](../evidence/ddacc4c3b454e93f.json). Baseline: **tool-error**.

No independent runtime override was executed for this target in this audit; this is not a pass.

## Recommended action

Resolve the intended parameter domain and enclosing equations; check inherited bounds, final/protected status, guards and aliases. Construct an otherwise-valid source-level witness, establish a clean baseline in a capable engine, then retranslate at the witness and compare with the runtime override. For equality claims use the actual partner value. Do not apply a blanket min>0 fix yet.

## Scope and limitations

A source-level verdict addresses the reported declaration/claim, not every possible connected system. Tests cover 0–0.5 seconds and are not a proof of long-run stability. Shared instances are not distinct root causes. A missing bound, timeout, compiler error or failed nominal run alone never counts as a verified bug or a false positive. Fixes are proposals; no library/compiler implementation was changed.

[Group and related reports](../groups/baseline-blocked.md) · [Index](../README.md)
