# FINDING-02703: Not yet established as a bug or a false positive

| Field | Value |
|---|---|
| Verdict | unresolved |
| Scope / group | baseline-blocked |
| Model | Modelica.Electrical.Machines.Examples.Transformers.IMC_Transformer |
| Target | aimc.Lm |
| Student classification | physical-domain-unenforced |
| Original report | [FINDING-imc-transformer-aimc-lm-intent-2.md](../../v2/bugs/FINDING-imc-transformer-aimc-lm-intent-2.md) — reviewed as `FINDING-02703-imc-transformer-aimc-lm.md`, which a later run renamed |
| Original SHA-256 | 3135e402c3e74944c3b888a73c8d43152c2d7313d6a89f822fb249a96ee5feb7 |

## What remains unresolved

The current Rumoca nominal run is tool-error, before any reported perturbation. This prevents causal attribution to this parameter. Source metadata was recovered, but none of the reviewed source proofs or counterexamples establishes this particular claim. A baseline failure/tool limitation is neither confirmation nor a false positive.

## Source evidence

Compiler/source-resolved declaration: `Electrical/Machines/BasicMachines/InductionMachines/IM_SquirrelCage.mo:26`. Role: `parameter`; binding: `aimcData.Lm`; effective min: `None`; effective max: `None`. 

[Electrical/Machines/BasicMachines/InductionMachines/IM_SquirrelCage.mo — source snapshot](../evidence/sources/d35e8ddc6d02c4da-IM_SquirrelCage.mo)

```modelica
24:     final m=m) annotation (Placement(transformation(extent={{-10,-10},{10,10}},
25:           rotation=270)));
26:   parameter SI.Inductance Lm(start=3*ZsRef*sqrt(1 - 0.0667)/(2*pi
27:         *fsNominal)) "Stator main field inductance per phase"
28:     annotation (Dialog(tab="Nominal resistances and inductances"));
29:   parameter SI.Inductance Lrsigma(start=3*ZsRef*(1 - sqrt(1 -
```


## Execution evidence

[Rumoca commands, return codes, integrity hashes, bounded output and metadata](../evidence/1d64c76f1b77946f.json). Baseline: **tool-error**.

No independent runtime override was executed for this target in this audit; this is not a pass.

## Recommended action

Resolve the intended parameter domain and enclosing equations; check inherited bounds, final/protected status, guards and aliases. Construct an otherwise-valid source-level witness, establish a clean baseline in a capable engine, then retranslate at the witness and compare with the runtime override. For equality claims use the actual partner value. Do not apply a blanket min>0 fix yet.

## Scope and limitations

A source-level verdict addresses the reported declaration/claim, not every possible connected system. Tests cover 0–0.5 seconds and are not a proof of long-run stability. Shared instances are not distinct root causes. A missing bound, timeout, compiler error or failed nominal run alone never counts as a verified bug or a false positive. Fixes are proposals; no library/compiler implementation was changed.

[Group and related reports](../groups/baseline-blocked.md) · [Index](../README.md)
