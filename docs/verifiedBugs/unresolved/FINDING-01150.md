# FINDING-01150: Not yet established as a bug or a false positive

| Field | Value |
|---|---|
| Verdict | unresolved |
| Scope / group | baseline-blocked |
| Model | Modelica.Electrical.Machines.Examples.DCMachines.DC_CompareCharacteristics |
| Target | dceeData.Re |
| Student classification | physical-domain-unenforced |
| Original report | [FINDING-dc-comparecharacteristics-dceedata-re-unbounded.md](../../v2/bugs/FINDING-dc-comparecharacteristics-dceedata-re-unbounded.md) — reviewed as `FINDING-01150-dc-comparecharacteristics-dceedata-re.md`, which a later run renamed |
| Original SHA-256 | 49a3126b70628154bd4d0225475c4aeffc6ddc1165e5ad367e34eaadd521661d |

## What remains unresolved

The current Rumoca nominal run is tool-error, before any reported perturbation. This prevents causal attribution to this parameter. Source metadata was recovered, but none of the reviewed source proofs or counterexamples establishes this particular claim. A baseline failure/tool limitation is neither confirmation nor a false positive.

## Source evidence

Compiler/source-resolved declaration: `Electrical/Machines/Utilities/ParameterRecords/DcElectricalExcitedData.mo:6`. Role: `parameter`; binding: `100`; effective min: `None`; effective max: `None`. 

[Electrical/Machines/Utilities/ParameterRecords/DcElectricalExcitedData.mo — source snapshot](../evidence/sources/3a099b39d59294ff-DcElectricalExcitedData.mo)

```modelica
4:   parameter SI.Current IeNominal=1
5:     "Nominal excitation current" annotation (Dialog(tab="Excitation"));
6:   parameter SI.Resistance Re=100
7:     "Field excitation resistance at TeRef"
8:     annotation (Dialog(tab="Excitation"));
9:   parameter SI.Temperature TeRef=293.15
```


## Execution evidence

[Rumoca commands, return codes, integrity hashes, bounded output and metadata](../evidence/f15341d4427cc3e0.json). Baseline: **tool-error**.

No independent runtime override was executed for this target in this audit; this is not a pass.

## Recommended action

Resolve the intended parameter domain and enclosing equations; check inherited bounds, final/protected status, guards and aliases. Construct an otherwise-valid source-level witness, establish a clean baseline in a capable engine, then retranslate at the witness and compare with the runtime override. For equality claims use the actual partner value. Do not apply a blanket min>0 fix yet.

## Scope and limitations

A source-level verdict addresses the reported declaration/claim, not every possible connected system. Tests cover 0–0.5 seconds and are not a proof of long-run stability. Shared instances are not distinct root causes. A missing bound, timeout, compiler error or failed nominal run alone never counts as a verified bug or a false positive. Fixes are proposals; no library/compiler implementation was changed.

[Group and related reports](../groups/baseline-blocked.md) · [Index](../README.md)
