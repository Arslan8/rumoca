# FINDING-05021: Not yet established as a bug or a false positive

| Field | Value |
|---|---|
| Verdict | unresolved |
| Scope / group | baseline-blocked |
| Model | ModelicaTest.Rotational.TestBraking |
| Target | eddyCurrentTorque.TRef |
| Student classification | divisor-reachable-zero |
| Original report | `FINDING-05021-testbraking-eddycurrenttorque-tref.md` — [withdrawn](../../v2/bugs/withdrawn.md); a later run no longer makes this claim |
| Original SHA-256 | aa2d95337c6998b0d1bbc3c1983dc80893aff214fac5a3b656b9bec10a1ad674 |

## What remains unresolved

The current Rumoca nominal run is tool-error, before any reported perturbation. This prevents causal attribution to this parameter. Source metadata was recovered, but none of the reviewed source proofs or counterexamples establishes this particular claim. A baseline failure/tool limitation is neither confirmation nor a false positive.

## Source evidence

Compiler/source-resolved declaration: `Mechanics/Rotational/Sources/EddyCurrentTorque.mo:10`. Role: `parameter`; binding: `293.15`; effective min: `0.0`; effective max: `None`. 

[Mechanics/Rotational/Sources/EddyCurrentTorque.mo — source snapshot](../evidence/sources/60f7c3193866c90e-EddyCurrentTorque.mo)

```modelica
8:   parameter SI.AngularVelocity w_nominal(min=Modelica.Constants.eps)
9:     "Nominal speed (leads to maximum torque) at reference temperature";
10:   parameter SI.Temperature TRef(start=293.15)
11:     "Reference temperature";
12:   parameter
13:     Modelica.Electrical.Machines.Thermal.LinearTemperatureCoefficient20
```


## Execution evidence

[Rumoca commands, return codes, integrity hashes, bounded output and metadata](../evidence/b729a64ec1e6d0d5.json). Baseline: **tool-error**.

No independent runtime override was executed for this target in this audit; this is not a pass.

## Recommended action

Resolve the intended parameter domain and enclosing equations; check inherited bounds, final/protected status, guards and aliases. Construct an otherwise-valid source-level witness, establish a clean baseline in a capable engine, then retranslate at the witness and compare with the runtime override. For equality claims use the actual partner value. Do not apply a blanket min>0 fix yet.

## Scope and limitations

A source-level verdict addresses the reported declaration/claim, not every possible connected system. Tests cover 0–0.5 seconds and are not a proof of long-run stability. Shared instances are not distinct root causes. A missing bound, timeout, compiler error or failed nominal run alone never counts as a verified bug or a false positive. Fixes are proposals; no library/compiler implementation was changed.

[Group and related reports](../groups/baseline-blocked.md) · [Index](../README.md)
