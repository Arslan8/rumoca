# FINDING-01558: Not yet established as a bug or a false positive

| Field | Value |
|---|---|
| Verdict | unresolved |
| Scope / group | baseline-blocked |
| Model | Modelica.Electrical.Machines.Examples.InductionMachines.IMC_DCBraking |
| Target | imc.Lm |
| Student classification | physical-domain-unenforced |
| Original report | [FINDING-imc-dcbraking-imc-lm-intent.md](../../v2/bugs/FINDING-imc-dcbraking-imc-lm-intent.md) — reviewed as `FINDING-01558-imc-dcbraking-imc-lm.md`, which a later run renamed |
| Original SHA-256 | 013641f5741a97bae8414b9657ba383d038e77b18fbf05baecddf44806043264 |

## What remains unresolved

The current Rumoca nominal run is tool-error, before any reported perturbation. This prevents causal attribution to this parameter. Source metadata was recovered, but none of the reviewed source proofs or counterexamples establishes this particular claim. A baseline failure/tool limitation is neither confirmation nor a false positive.

## Source evidence

Compiler/source-resolved declaration: `Electrical/Machines/BasicMachines/InductionMachines/IM_SquirrelCage.mo:26`. Role: `parameter`; binding: `imcData.Lm`; effective min: `None`; effective max: `None`. 

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

[Rumoca commands, return codes, integrity hashes, bounded output and metadata](../evidence/489fdf592354cb9a.json). Baseline: **tool-error**.

No independent runtime override was executed for this target in this audit; this is not a pass.

## Recommended action

Resolve the intended parameter domain and enclosing equations; check inherited bounds, final/protected status, guards and aliases. Construct an otherwise-valid source-level witness, establish a clean baseline in a capable engine, then retranslate at the witness and compare with the runtime override. For equality claims use the actual partner value. Do not apply a blanket min>0 fix yet.

## Scope and limitations

A source-level verdict addresses the reported declaration/claim, not every possible connected system. Tests cover 0–0.5 seconds and are not a proof of long-run stability. Shared instances are not distinct root causes. A missing bound, timeout, compiler error or failed nominal run alone never counts as a verified bug or a false positive. Fixes are proposals; no library/compiler implementation was changed.

[Group and related reports](../groups/baseline-blocked.md) · [Index](../README.md)
