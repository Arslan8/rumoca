# FINDING-01987: Not yet established as a bug or a false positive

| Field | Value |
|---|---|
| Verdict | unresolved |
| Scope / group | baseline-blocked |
| Model | Modelica.Electrical.Machines.Examples.InductionMachines.IMC_YD |
| Target | JLoad |
| Student classification | physical-domain-unenforced |
| Original report | [FINDING-imc-yd-jload-zerolimit.md](../../v2/bugs/FINDING-imc-yd-jload-zerolimit.md) — reviewed as `FINDING-01987-imc-yd-jload.md`, which a later run renamed |
| Original SHA-256 | 999c2ea75868372ec89a1ef86e56b750aa48a0d80efa0459b78eb0a04a009fd8 |

## What remains unresolved

The current Rumoca nominal run is tool-error, before any reported perturbation. This prevents causal attribution to this parameter. Source metadata was recovered, but none of the reviewed source proofs or counterexamples establishes this particular claim. A baseline failure/tool limitation is neither confirmation nor a false positive.

## Source evidence

Compiler/source-resolved declaration: `Electrical/Machines/Examples/InductionMachines/IMC_YD.mo:14`. Role: `parameter`; binding: `0.29`; effective min: `None`; effective max: `None`. 

[Electrical/Machines/Examples/InductionMachines/IMC_YD.mo — source snapshot](../evidence/sources/644e7487e2bcb216-IMC_YD.mo)

```modelica
12:   parameter SI.AngularVelocity wLoad(displayUnit="rev/min")=
13:        1440.45*2*Modelica.Constants.pi/60 "Nominal load speed";
14:   parameter SI.Inertia JLoad=0.29
15:     "Load's moment of inertia";
16:   Machines.BasicMachines.InductionMachines.IM_SquirrelCage aimc(
17:     p=aimcData.p,
```


## Execution evidence

[Rumoca commands, return codes, integrity hashes, bounded output and metadata](../evidence/f475b935ebf4281d.json). Baseline: **tool-error**.

No independent runtime override was executed for this target in this audit; this is not a pass.

## Recommended action

Resolve the intended parameter domain and enclosing equations; check inherited bounds, final/protected status, guards and aliases. Construct an otherwise-valid source-level witness, establish a clean baseline in a capable engine, then retranslate at the witness and compare with the runtime override. For equality claims use the actual partner value. Do not apply a blanket min>0 fix yet.

## Scope and limitations

A source-level verdict addresses the reported declaration/claim, not every possible connected system. Tests cover 0–0.5 seconds and are not a proof of long-run stability. Shared instances are not distinct root causes. A missing bound, timeout, compiler error or failed nominal run alone never counts as a verified bug or a false positive. Fixes are proposals; no library/compiler implementation was changed.

[Group and related reports](../groups/baseline-blocked.md) · [Index](../README.md)
