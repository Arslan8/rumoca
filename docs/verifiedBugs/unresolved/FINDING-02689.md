# FINDING-02689: Not yet established as a bug or a false positive

| Field | Value |
|---|---|
| Verdict | unresolved |
| Scope / group | baseline-blocked |
| Model | Modelica.Electrical.Machines.Examples.Transformers.IMC_Transformer |
| Target | JLoad |
| Student classification | physical-domain-unenforced |
| Original report | [FINDING-imc-transformer-jload-zerolimit-2.md](../../v2/bugs/FINDING-imc-transformer-jload-zerolimit-2.md) — reviewed as `FINDING-02689-imc-transformer-jload.md`, which a later run renamed |
| Original SHA-256 | 38e266e510e7b25c190b0ee30fbb81c7be0ae783c76997eb52c462d336608f37 |

## What remains unresolved

The current Rumoca nominal run is tool-error, before any reported perturbation. This prevents causal attribution to this parameter. Source metadata was recovered, but none of the reviewed source proofs or counterexamples establishes this particular claim. A baseline failure/tool limitation is neither confirmation nor a false positive.

## Source evidence

Compiler/source-resolved declaration: `Electrical/Machines/Examples/InductionMachines/IMC_Transformer.mo:15`. Role: `parameter`; binding: `0.29`; effective min: `None`; effective max: `None`. 

[Electrical/Machines/Examples/InductionMachines/IMC_Transformer.mo — source snapshot](../evidence/sources/636dfab7a1d6ef30-IMC_Transformer.mo)

```modelica
13:   parameter SI.AngularVelocity wLoad(displayUnit="rev/min")=
14:        1440.45*2*Modelica.Constants.pi/60 "Nominal load speed";
15:   parameter SI.Inertia JLoad=0.29
16:     "Load's moment of inertia";
17:   Machines.BasicMachines.InductionMachines.IM_SquirrelCage aimc(
18:     p=aimcData.p,
```


## Execution evidence

[Rumoca commands, return codes, integrity hashes, bounded output and metadata](../evidence/1d64c76f1b77946f.json). Baseline: **tool-error**.

No independent runtime override was executed for this target in this audit; this is not a pass.

## Recommended action

Resolve the intended parameter domain and enclosing equations; check inherited bounds, final/protected status, guards and aliases. Construct an otherwise-valid source-level witness, establish a clean baseline in a capable engine, then retranslate at the witness and compare with the runtime override. For equality claims use the actual partner value. Do not apply a blanket min>0 fix yet.

## Scope and limitations

A source-level verdict addresses the reported declaration/claim, not every possible connected system. Tests cover 0–0.5 seconds and are not a proof of long-run stability. Shared instances are not distinct root causes. A missing bound, timeout, compiler error or failed nominal run alone never counts as a verified bug or a false positive. Fixes are proposals; no library/compiler implementation was changed.

[Group and related reports](../groups/baseline-blocked.md) · [Index](../README.md)
