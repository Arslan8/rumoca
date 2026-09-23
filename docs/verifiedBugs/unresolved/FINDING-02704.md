# FINDING-02704: Not yet established as a bug or a false positive

| Field | Value |
|---|---|
| Verdict | unresolved |
| Scope / group | baseline-blocked |
| Model | Modelica.Electrical.Machines.Examples.Transformers.IMC_Transformer |
| Target | aimc.Lrsigma |
| Student classification | physical-domain-unenforced |
| Original report | [FINDING-imc-transformer-aimc-lrsigma-intent-2.md](../../v2/bugs/FINDING-imc-transformer-aimc-lrsigma-intent-2.md) — reviewed as `FINDING-02704-imc-transformer-aimc-lrsigma.md`, which a later run renamed |
| Original SHA-256 | da99a699005a7870ff0e199719dd2d36c5f64b629b9d32c55fae5e9401cdf9f1 |

## What remains unresolved

The current Rumoca nominal run is tool-error, before any reported perturbation. This prevents causal attribution to this parameter. Source metadata was recovered, but none of the reviewed source proofs or counterexamples establishes this particular claim. A baseline failure/tool limitation is neither confirmation nor a false positive.

## Source evidence

Compiler/source-resolved declaration: `Electrical/Machines/BasicMachines/InductionMachines/IM_SquirrelCage.mo:29`. Role: `parameter`; binding: `aimcData.Lrsigma`; effective min: `None`; effective max: `None`. 

[Electrical/Machines/BasicMachines/InductionMachines/IM_SquirrelCage.mo — source snapshot](../evidence/sources/d35e8ddc6d02c4da-IM_SquirrelCage.mo)

```modelica
27:         *fsNominal)) "Stator main field inductance per phase"
28:     annotation (Dialog(tab="Nominal resistances and inductances"));
29:   parameter SI.Inductance Lrsigma(start=3*ZsRef*(1 - sqrt(1 -
30:         0.0667))/(2*pi*fsNominal))
31:     "Rotor stray inductance per phase (equivalent three-phase winding)"
32:     annotation (Dialog(tab="Nominal resistances and inductances"));
```


## Execution evidence

[Rumoca commands, return codes, integrity hashes, bounded output and metadata](../evidence/1d64c76f1b77946f.json). Baseline: **tool-error**.

No independent runtime override was executed for this target in this audit; this is not a pass.

## Recommended action

Resolve the intended parameter domain and enclosing equations; check inherited bounds, final/protected status, guards and aliases. Construct an otherwise-valid source-level witness, establish a clean baseline in a capable engine, then retranslate at the witness and compare with the runtime override. For equality claims use the actual partner value. Do not apply a blanket min>0 fix yet.

## Scope and limitations

A source-level verdict addresses the reported declaration/claim, not every possible connected system. Tests cover 0–0.5 seconds and are not a proof of long-run stability. Shared instances are not distinct root causes. A missing bound, timeout, compiler error or failed nominal run alone never counts as a verified bug or a false positive. Fixes are proposals; no library/compiler implementation was changed.

[Group and related reports](../groups/baseline-blocked.md) · [Index](../README.md)
