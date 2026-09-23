# FINDING-01617: Not yet established as a bug or a false positive

| Field | Value |
|---|---|
| Verdict | unresolved |
| Scope / group | baseline-blocked |
| Model | Modelica.Electrical.Machines.Examples.InductionMachines.IMC_Initialize |
| Target | JLoad |
| Student classification | physical-domain-unenforced |
| Original report | [FINDING-imc-initialize-jload-zerolimit.md](../../v2/bugs/FINDING-imc-initialize-jload-zerolimit.md) — reviewed as `FINDING-01617-imc-initialize-jload.md`, which a later run renamed |
| Original SHA-256 | 79eebddf9bce2d37e8359296169b97bf67544ae29526c73df17bba12272841a4 |

## What remains unresolved

The current Rumoca nominal run is tool-error, before any reported perturbation. This prevents causal attribution to this parameter. Source metadata was recovered, but none of the reviewed source proofs or counterexamples establishes this particular claim. A baseline failure/tool limitation is neither confirmation nor a false positive.

## Source evidence

Compiler/source-resolved declaration: `Electrical/Machines/Examples/InductionMachines/IMC_Initialize.mo:15`. Role: `parameter`; binding: `0.29`; effective min: `None`; effective max: `None`. 

[Electrical/Machines/Examples/InductionMachines/IMC_Initialize.mo — source snapshot](../evidence/sources/651bb07e402d90bc-IMC_Initialize.mo)

```modelica
13:   parameter SI.AngularVelocity wLoad(displayUnit="rev/min")=
14:        1440.45*2*Modelica.Constants.pi/60 "Nominal load speed";
15:   parameter SI.Inertia JLoad=0.29
16:     "Load's moment of inertia";
17:   Machines.BasicMachines.InductionMachines.IM_SquirrelCage aimc(
18:     p=aimcData.p,
```


## Execution evidence

[Rumoca commands, return codes, integrity hashes, bounded output and metadata](../evidence/6b09ecf975c03970.json). Baseline: **tool-error**.

No independent runtime override was executed for this target in this audit; this is not a pass.

## Recommended action

Resolve the intended parameter domain and enclosing equations; check inherited bounds, final/protected status, guards and aliases. Construct an otherwise-valid source-level witness, establish a clean baseline in a capable engine, then retranslate at the witness and compare with the runtime override. For equality claims use the actual partner value. Do not apply a blanket min>0 fix yet.

## Scope and limitations

A source-level verdict addresses the reported declaration/claim, not every possible connected system. Tests cover 0–0.5 seconds and are not a proof of long-run stability. Shared instances are not distinct root causes. A missing bound, timeout, compiler error or failed nominal run alone never counts as a verified bug or a false positive. Fixes are proposals; no library/compiler implementation was changed.

[Group and related reports](../groups/baseline-blocked.md) · [Index](../README.md)
