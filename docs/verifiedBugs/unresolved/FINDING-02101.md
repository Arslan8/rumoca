# FINDING-02101: Not yet established as a bug or a false positive

| Field | Value |
|---|---|
| Verdict | unresolved |
| Scope / group | baseline-blocked |
| Model | Modelica.Electrical.Machines.Examples.InductionMachines.IMS_Start |
| Target | aimsData.Lrzero |
| Student classification | physical-domain-unenforced |
| Original report | [FINDING-ims-start-aimsdata-lrzero-zerolimit.md](../../v2/bugs/FINDING-ims-start-aimsdata-lrzero-zerolimit.md) — reviewed as `FINDING-02101-ims-start-aimsdata-lrzero.md`, which a later run renamed |
| Original SHA-256 | b590a00a423615990e0cda329405e3bc3c229e89a8d408f5582c8a3fdcb1d738 |

## What remains unresolved

The current Rumoca nominal run is tool-error, before any reported perturbation. This prevents causal attribution to this parameter. Source metadata was recovered, but none of the reviewed source proofs or counterexamples establishes this particular claim. A baseline failure/tool limitation is neither confirmation nor a false positive.

## Source evidence

Compiler/source-resolved declaration: `Electrical/Machines/Utilities/ParameterRecords/IM_SlipRingData.mo:16`. Role: `parameter`; binding: `(aimsData.Lrsigma / (aimsData.turnsRatio ^ 2))`; effective min: `None`; effective max: `None`. 

[Electrical/Machines/Utilities/ParameterRecords/IM_SlipRingData.mo — source snapshot](../evidence/sources/43598d6d883f8edf-IM_SlipRingData.mo)

```modelica
14:     "Ratio of common stray inductance / total stray inductance of rotor winding"
15:     annotation (Dialog(tab="Nominal resistances and inductances"));
16:   parameter SI.Inductance Lrzero=Lrsigma/turnsRatio^2
17:     "Rotor zero sequence inductance w.r.t. rotor side"
18:     annotation (Dialog(tab="Nominal resistances and inductances"));
19:   parameter SI.Resistance Rr=0.04/turnsRatio^2
```


## Execution evidence

[Rumoca commands, return codes, integrity hashes, bounded output and metadata](../evidence/2804e4f64ad6a33e.json). Baseline: **tool-error**.

No independent runtime override was executed for this target in this audit; this is not a pass.

## Recommended action

Resolve the intended parameter domain and enclosing equations; check inherited bounds, final/protected status, guards and aliases. Construct an otherwise-valid source-level witness, establish a clean baseline in a capable engine, then retranslate at the witness and compare with the runtime override. For equality claims use the actual partner value. Do not apply a blanket min>0 fix yet.

## Scope and limitations

A source-level verdict addresses the reported declaration/claim, not every possible connected system. Tests cover 0–0.5 seconds and are not a proof of long-run stability. Shared instances are not distinct root causes. A missing bound, timeout, compiler error or failed nominal run alone never counts as a verified bug or a false positive. Fixes are proposals; no library/compiler implementation was changed.

[Group and related reports](../groups/baseline-blocked.md) · [Index](../README.md)
