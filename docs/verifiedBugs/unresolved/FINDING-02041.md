# FINDING-02041: Not yet established as a bug or a false positive

| Field | Value |
|---|---|
| Verdict | unresolved |
| Scope / group | baseline-blocked |
| Model | Modelica.Electrical.Machines.Examples.InductionMachines.IMC_YD |
| Target | wLoad |
| Student classification | divisor-reachable-zero |
| Original report | `FINDING-02041-imc-yd-wload.md` — [withdrawn](../../v2/bugs/withdrawn.md); a later run no longer makes this claim |
| Original SHA-256 | 4adea60afd9249c68b55e5b3ad8a84746f43df3568f2d0448a9f8f0e4d4fd794 |

## What remains unresolved

The current Rumoca nominal run is tool-error, before any reported perturbation. This prevents causal attribution to this parameter. Source metadata was recovered, but none of the reviewed source proofs or counterexamples establishes this particular claim. A baseline failure/tool limitation is neither confirmation nor a false positive.

## Source evidence

Compiler/source-resolved declaration: `Electrical/Machines/Examples/InductionMachines/IMC_YD.mo:12`. Role: `parameter`; binding: `(((1440.45 * 2) * (2 * asin(1.0))) / 60)`; effective min: `None`; effective max: `None`. 

[Electrical/Machines/Examples/InductionMachines/IMC_YD.mo — source snapshot](../evidence/sources/644e7487e2bcb216-IMC_YD.mo)

```modelica
10:   parameter SI.Time tStart2=2.0 "Start time from Y to D";
11:   parameter SI.Torque TLoad=161.4 "Nominal load torque";
12:   parameter SI.AngularVelocity wLoad(displayUnit="rev/min")=
13:        1440.45*2*Modelica.Constants.pi/60 "Nominal load speed";
14:   parameter SI.Inertia JLoad=0.29
15:     "Load's moment of inertia";
```


## Execution evidence

[Rumoca commands, return codes, integrity hashes, bounded output and metadata](../evidence/f475b935ebf4281d.json). Baseline: **tool-error**.

No independent runtime override was executed for this target in this audit; this is not a pass.

## Recommended action

Resolve the intended parameter domain and enclosing equations; check inherited bounds, final/protected status, guards and aliases. Construct an otherwise-valid source-level witness, establish a clean baseline in a capable engine, then retranslate at the witness and compare with the runtime override. For equality claims use the actual partner value. Do not apply a blanket min>0 fix yet.

## Scope and limitations

A source-level verdict addresses the reported declaration/claim, not every possible connected system. Tests cover 0–0.5 seconds and are not a proof of long-run stability. Shared instances are not distinct root causes. A missing bound, timeout, compiler error or failed nominal run alone never counts as a verified bug or a false positive. Fixes are proposals; no library/compiler implementation was changed.

[Group and related reports](../groups/baseline-blocked.md) · [Index](../README.md)
