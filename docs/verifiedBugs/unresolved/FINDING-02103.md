# FINDING-02103: Not yet established as a bug or a false positive

| Field | Value |
|---|---|
| Verdict | unresolved |
| Scope / group | baseline-blocked |
| Model | Modelica.Electrical.Machines.Examples.InductionMachines.IMS_Start |
| Target | wLoad |
| Student classification | divisor-reachable-zero |
| Original report | `FINDING-02103-ims-start-wload.md` — [withdrawn](../../v2/bugs/withdrawn.md); a later run no longer makes this claim |
| Original SHA-256 | f1acd53727ab3d24b479cde5b03d6728c953a98032ba65345187d95cd1bc5d5d |

## What remains unresolved

The current Rumoca nominal run is tool-error, before any reported perturbation. This prevents causal attribution to this parameter. Source metadata was recovered, but none of the reviewed source proofs or counterexamples establishes this particular claim. A baseline failure/tool limitation is neither confirmation nor a false positive.

## Source evidence

Compiler/source-resolved declaration: `Electrical/Machines/Examples/InductionMachines/IMS_Start.mo:14`. Role: `parameter`; binding: `(((1440.45 * 2) * (2 * asin(1.0))) / 60)`; effective min: `None`; effective max: `None`. 

[Electrical/Machines/Examples/InductionMachines/IMS_Start.mo — source snapshot](../evidence/sources/439faf5a498dc64f-IMS_Start.mo)

```modelica
12:     "Start time of shorting starting resistance";
13:   parameter SI.Torque TLoad=161.4 "Nominal load torque";
14:   parameter SI.AngularVelocity wLoad(displayUnit="rev/min")=
15:        1440.45*2*Modelica.Constants.pi/60 "Nominal load speed";
16:   parameter SI.Inertia JLoad=0.29
17:     "Load's moment of inertia";
```


## Execution evidence

[Rumoca commands, return codes, integrity hashes, bounded output and metadata](../evidence/2804e4f64ad6a33e.json). Baseline: **tool-error**.

No independent runtime override was executed for this target in this audit; this is not a pass.

## Recommended action

Resolve the intended parameter domain and enclosing equations; check inherited bounds, final/protected status, guards and aliases. Construct an otherwise-valid source-level witness, establish a clean baseline in a capable engine, then retranslate at the witness and compare with the runtime override. For equality claims use the actual partner value. Do not apply a blanket min>0 fix yet.

## Scope and limitations

A source-level verdict addresses the reported declaration/claim, not every possible connected system. Tests cover 0–0.5 seconds and are not a proof of long-run stability. Shared instances are not distinct root causes. A missing bound, timeout, compiler error or failed nominal run alone never counts as a verified bug or a false positive. Fixes are proposals; no library/compiler implementation was changed.

[Group and related reports](../groups/baseline-blocked.md) · [Index](../README.md)
