# FINDING-05139: Not yet established as a bug or a false positive

| Field | Value |
|---|---|
| Verdict | unresolved |
| Scope / group | baseline-blocked |
| Model | RigidBody.Examples.QuadrotorSIL |
| Target | motor_tau_eps |
| Student classification | divisor-reachable-zero |
| Original report | `FINDING-05139-quadrotorsil-motor-tau-eps.md` — [withdrawn](../../v2/bugs/withdrawn.md); a later run no longer makes this claim |
| Original SHA-256 | d943e34ea63221bbfeeae203619365f2ab61f3d373bc350da68c0bce7218ce42 |

## What remains unresolved

The current Rumoca nominal run is tool-error, before any reported perturbation. This prevents causal attribution to this parameter. Source metadata was recovered, but none of the reviewed source proofs or counterexamples establishes this particular claim. A baseline failure/tool limitation is neither confirmation nor a false positive.

## Source evidence

Compiler/source-resolved declaration: `/data/mrumoca/rumoca/target/cmm/CMM-a642c381/RigidBody/Examples/QuadrotorSIL.mo:68`. Role: `parameter`; binding: `1.0`; effective min: `None`; effective max: `None`. 

[/data/mrumoca/rumoca/target/cmm/CMM-a642c381/RigidBody/Examples/QuadrotorSIL.mo — source snapshot](../evidence/sources/0ca83ee587091198-QuadrotorSIL.mo)

```modelica
66:   parameter Real tau_up = 0.0125 "Motor spin-up time constant [s]";
67:   parameter Real tau_down = 0.025 "Motor spin-down time constant [s]";
68:   parameter Real motor_tau_eps = 1.0 "Smooth transition width for asymmetric motor lag [rad/s]";
69:   parameter Real motor_moment_map[3, 4] = [
70:     -d,   d,   d,  -d;
71:     -d,   d,  -d,   d;
```


## Execution evidence

[Rumoca commands, return codes, integrity hashes, bounded output and metadata](../evidence/ddacc4c3b454e93f.json). Baseline: **tool-error**.

No independent runtime override was executed for this target in this audit; this is not a pass.

## Recommended action

Resolve the intended parameter domain and enclosing equations; check inherited bounds, final/protected status, guards and aliases. Construct an otherwise-valid source-level witness, establish a clean baseline in a capable engine, then retranslate at the witness and compare with the runtime override. For equality claims use the actual partner value. Do not apply a blanket min>0 fix yet.

## Scope and limitations

A source-level verdict addresses the reported declaration/claim, not every possible connected system. Tests cover 0–0.5 seconds and are not a proof of long-run stability. Shared instances are not distinct root causes. A missing bound, timeout, compiler error or failed nominal run alone never counts as a verified bug or a false positive. Fixes are proposals; no library/compiler implementation was changed.

[Group and related reports](../groups/baseline-blocked.md) · [Index](../README.md)
