# FINDING-04895: Not yet established as a bug or a false positive

| Field | Value |
|---|---|
| Verdict | unresolved |
| Scope / group | baseline-blocked |
| Model | ModelicaTest.Electrical.Machines.SMPM_VoltageSourceWithLosses |
| Target | smpmData.frictionParameters.linear |
| Student classification | divisor-reachable-zero |
| Original report | `FINDING-04895-smpm-voltagesourcewithlosses-smpmdata-frictionparameters-linear.md` — [withdrawn](../../v2/bugs/withdrawn.md); a later run no longer makes this claim |
| Original SHA-256 | 61715e2db0aef7ccda915c56b019b619d25bec5bd91816a499ca47914d3ea0fb |

## What remains unresolved

The current Rumoca nominal run is tool-error, before any reported perturbation. This prevents causal attribution to this parameter. Source metadata was recovered, but none of the reviewed source proofs or counterexamples establishes this particular claim. A baseline failure/tool limitation is neither confirmation nor a false positive.

## Source evidence

Compiler/source-resolved declaration: `Electrical/Machines/Losses/FrictionParameters.mo:14`. Role: `parameter`; binding: `0.001`; effective min: `None`; effective max: `None`. 

[Electrical/Machines/Losses/FrictionParameters.mo — source snapshot](../evidence/sources/69521414f63c2e81-FrictionParameters.mo)

```modelica
12:        else PRef/wRef
13:     "Reference friction torque at reference angular velocity";
14:   final parameter Real linear=0.001
15:     "Linear angular velocity range with respect to reference angular velocity";
16:   final parameter SI.AngularVelocity wLinear=linear*wRef
17:     "Linear angular velocity range";
```


## Execution evidence

[Rumoca commands, return codes, integrity hashes, bounded output and metadata](../evidence/f5cf46ada0ef7a80.json). Baseline: **tool-error**.

No independent runtime override was executed for this target in this audit; this is not a pass.

## Recommended action

Resolve the intended parameter domain and enclosing equations; check inherited bounds, final/protected status, guards and aliases. Construct an otherwise-valid source-level witness, establish a clean baseline in a capable engine, then retranslate at the witness and compare with the runtime override. For equality claims use the actual partner value. Do not apply a blanket min>0 fix yet.

## Scope and limitations

A source-level verdict addresses the reported declaration/claim, not every possible connected system. Tests cover 0–0.5 seconds and are not a proof of long-run stability. Shared instances are not distinct root causes. A missing bound, timeout, compiler error or failed nominal run alone never counts as a verified bug or a false positive. Fixes are proposals; no library/compiler implementation was changed.

[Group and related reports](../groups/baseline-blocked.md) · [Index](../README.md)
