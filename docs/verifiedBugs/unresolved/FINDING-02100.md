# FINDING-02100: Not yet established as a bug or a false positive

| Field | Value |
|---|---|
| Verdict | unresolved |
| Scope / group | baseline-blocked |
| Model | Modelica.Electrical.Machines.Examples.InductionMachines.IMS_Start |
| Target | aimsData.Lrsigma |
| Student classification | physical-domain-unenforced |
| Original report | [FINDING-ims-start-aimsdata-lrsigma-intent.md](../../v2/bugs/FINDING-ims-start-aimsdata-lrsigma-intent.md) — reviewed as `FINDING-02100-ims-start-aimsdata-lrsigma.md`, which a later run renamed |
| Original SHA-256 | 501244a046bbf7f189ba2aa0c48e5676251edb5d5abe3f972de998e2fd538ff3 |

## What remains unresolved

The current Rumoca nominal run is tool-error, before any reported perturbation. This prevents causal attribution to this parameter. Source metadata was recovered, but none of the reviewed source proofs or counterexamples establishes this particular claim. A baseline failure/tool limitation is neither confirmation nor a false positive.

## Source evidence

Compiler/source-resolved declaration: `Electrical/Machines/Utilities/ParameterRecords/IM_SlipRingData.mo:9`. Role: `parameter`; binding: `(((3 * (1 - sqrt((1 - 0.0667)))) / ((2 * (2 * asin(1.0))) * aimsData.fsNominal)) / (aimsData.turnsRatio ^ 2))`; effective min: `None`; effective max: `None`. 

[Electrical/Machines/Utilities/ParameterRecords/IM_SlipRingData.mo — source snapshot](../evidence/sources/43598d6d883f8edf-IM_SlipRingData.mo)

```modelica
7:       fsNominal) "Stator main field inductance per phase"
8:     annotation (Dialog(tab="Nominal resistances and inductances"));
9:   parameter SI.Inductance Lrsigma=3*(1 - sqrt(1 - 0.0667))/
10:       (2*pi*fsNominal)/turnsRatio^2
11:     "Rotor stray inductance per phase w.r.t. rotor side"
12:     annotation (Dialog(tab="Nominal resistances and inductances"));
```


## Execution evidence

[Rumoca commands, return codes, integrity hashes, bounded output and metadata](../evidence/2804e4f64ad6a33e.json). Baseline: **tool-error**.

No independent runtime override was executed for this target in this audit; this is not a pass.

## Recommended action

Resolve the intended parameter domain and enclosing equations; check inherited bounds, final/protected status, guards and aliases. Construct an otherwise-valid source-level witness, establish a clean baseline in a capable engine, then retranslate at the witness and compare with the runtime override. For equality claims use the actual partner value. Do not apply a blanket min>0 fix yet.

## Scope and limitations

A source-level verdict addresses the reported declaration/claim, not every possible connected system. Tests cover 0–0.5 seconds and are not a proof of long-run stability. Shared instances are not distinct root causes. A missing bound, timeout, compiler error or failed nominal run alone never counts as a verified bug or a false positive. Fixes are proposals; no library/compiler implementation was changed.

[Group and related reports](../groups/baseline-blocked.md) · [Index](../README.md)
