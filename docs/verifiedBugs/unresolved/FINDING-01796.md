# FINDING-01796: Not yet established as a bug or a false positive

| Field | Value |
|---|---|
| Verdict | unresolved |
| Scope / group | baseline-blocked |
| Model | Modelica.Electrical.Machines.Examples.InductionMachines.IMC_Steinmetz |
| Target | JLoad |
| Student classification | physical-domain-unenforced |
| Original report | [FINDING-imc-steinmetz-jload-zerolimit.md](../../v2/bugs/FINDING-imc-steinmetz-jload-zerolimit.md) — reviewed as `FINDING-01796-imc-steinmetz-jload.md`, which a later run renamed |
| Original SHA-256 | 7ffda43a1f750b6cf6ef6bf461bc2c08fa27f4951bee9bcc352ae2a4e2e9f0db |

## What remains unresolved

The current Rumoca nominal run is tool-error, before any reported perturbation. This prevents causal attribution to this parameter. Source metadata was recovered, but none of the reviewed source proofs or counterexamples establishes this particular claim. A baseline failure/tool limitation is neither confirmation nor a false positive.

## Source evidence

Compiler/source-resolved declaration: `Electrical/Machines/Examples/InductionMachines/IMC_Steinmetz.mo:20`. Role: `parameter`; binding: `0.29`; effective min: `None`; effective max: `None`. 

[Electrical/Machines/Examples/InductionMachines/IMC_Steinmetz.mo — source snapshot](../evidence/sources/39e3cc5c9f815c15-IMC_Steinmetz.mo)

```modelica
18:   parameter SI.AngularVelocity wLoad(displayUnit="rev/min")=
19:        1462.5*2*Modelica.Constants.pi/60 "Nominal load speed";
20:   parameter SI.Inertia JLoad=0.29
21:     "Load's moment of inertia";
22:   Machines.BasicMachines.InductionMachines.IM_SquirrelCage aimc(
23:     p=aimcData.p,
```


## Execution evidence

[Rumoca commands, return codes, integrity hashes, bounded output and metadata](../evidence/00227f080db37cf1.json). Baseline: **tool-error**.

No independent runtime override was executed for this target in this audit; this is not a pass.

## Recommended action

Resolve the intended parameter domain and enclosing equations; check inherited bounds, final/protected status, guards and aliases. Construct an otherwise-valid source-level witness, establish a clean baseline in a capable engine, then retranslate at the witness and compare with the runtime override. For equality claims use the actual partner value. Do not apply a blanket min>0 fix yet.

## Scope and limitations

A source-level verdict addresses the reported declaration/claim, not every possible connected system. Tests cover 0–0.5 seconds and are not a proof of long-run stability. Shared instances are not distinct root causes. A missing bound, timeout, compiler error or failed nominal run alone never counts as a verified bug or a false positive. Fixes are proposals; no library/compiler implementation was changed.

[Group and related reports](../groups/baseline-blocked.md) · [Index](../README.md)
