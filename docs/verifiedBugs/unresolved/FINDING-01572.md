# FINDING-01572: Not yet established as a bug or a false positive

| Field | Value |
|---|---|
| Verdict | unresolved |
| Scope / group | baseline-blocked |
| Model | Modelica.Electrical.Machines.Examples.InductionMachines.IMC_DOL |
| Target | JLoad |
| Student classification | physical-domain-unenforced |
| Original report | [FINDING-imc-dol-jload-zerolimit.md](../../v2/bugs/FINDING-imc-dol-jload-zerolimit.md) — reviewed as `FINDING-01572-imc-dol-jload.md`, which a later run renamed |
| Original SHA-256 | 0b96f7de69f683a24be8d865ff99f48c6f31e5a379d30e687b8fe72d097aeb33 |

## What remains unresolved

The current Rumoca nominal run is tool-error, before any reported perturbation. This prevents causal attribution to this parameter. Source metadata was recovered, but none of the reviewed source proofs or counterexamples establishes this particular claim. A baseline failure/tool limitation is neither confirmation nor a false positive.

## Source evidence

Compiler/source-resolved declaration: `Electrical/Machines/Examples/InductionMachines/IMC_DOL.mo:13`. Role: `parameter`; binding: `0.29`; effective min: `None`; effective max: `None`. 

[Electrical/Machines/Examples/InductionMachines/IMC_DOL.mo — source snapshot](../evidence/sources/407dd2b64107b7f2-IMC_DOL.mo)

```modelica
11:   parameter SI.AngularVelocity wLoad(displayUnit="rev/min")=
12:        1440.45*2*Modelica.Constants.pi/60 "Nominal load speed";
13:   parameter SI.Inertia JLoad=0.29
14:     "Load's moment of inertia";
15:   Machines.BasicMachines.InductionMachines.IM_SquirrelCage aimc(
16:     p=aimcData.p,
```


## Execution evidence

[Rumoca commands, return codes, integrity hashes, bounded output and metadata](../evidence/3bb307101f6982f2.json). Baseline: **tool-error**.

No independent runtime override was executed for this target in this audit; this is not a pass.

## Recommended action

Resolve the intended parameter domain and enclosing equations; check inherited bounds, final/protected status, guards and aliases. Construct an otherwise-valid source-level witness, establish a clean baseline in a capable engine, then retranslate at the witness and compare with the runtime override. For equality claims use the actual partner value. Do not apply a blanket min>0 fix yet.

## Scope and limitations

A source-level verdict addresses the reported declaration/claim, not every possible connected system. Tests cover 0–0.5 seconds and are not a proof of long-run stability. Shared instances are not distinct root causes. A missing bound, timeout, compiler error or failed nominal run alone never counts as a verified bug or a false positive. Fixes are proposals; no library/compiler implementation was changed.

[Group and related reports](../groups/baseline-blocked.md) · [Index](../README.md)
