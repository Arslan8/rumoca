# FINDING-01214: Not yet established as a bug or a false positive

| Field | Value |
|---|---|
| Verdict | unresolved |
| Scope / group | baseline-blocked |
| Model | Modelica.Electrical.Machines.Examples.DCMachines.DCEE_Start |
| Target | dceeData.Le |
| Student classification | physical-domain-unenforced |
| Original report | [FINDING-dcee-start-dceedata-le-intent.md](../../v2/bugs/FINDING-dcee-start-dceedata-le-intent.md) — reviewed as `FINDING-01214-dcee-start-dceedata-le.md`, which a later run renamed |
| Original SHA-256 | 692041e27edab4f253ad016189d8ee98c31cc37642ede295735e32d9e405404b |

## What remains unresolved

The current Rumoca nominal run is tool-error, before any reported perturbation. This prevents causal attribution to this parameter. Source metadata was recovered, but none of the reviewed source proofs or counterexamples establishes this particular claim. A baseline failure/tool limitation is neither confirmation nor a false positive.

## Source evidence

Compiler/source-resolved declaration: `Electrical/Machines/Utilities/ParameterRecords/DcElectricalExcitedData.mo:15`. Role: `parameter`; binding: `1`; effective min: `None`; effective max: `None`. 

[Electrical/Machines/Utilities/ParameterRecords/DcElectricalExcitedData.mo — source snapshot](../evidence/sources/3a099b39d59294ff-DcElectricalExcitedData.mo)

```modelica
13:     "Temperature coefficient of excitation resistance"
14:     annotation (Dialog(tab="Excitation"));
15:   parameter SI.Inductance Le=1
16:     "Total field excitation inductance"
17:     annotation (Dialog(tab="Excitation"));
18:   parameter Real sigmae(
```


## Execution evidence

[Rumoca commands, return codes, integrity hashes, bounded output and metadata](../evidence/038fc081f23c709d.json). Baseline: **tool-error**.

No independent runtime override was executed for this target in this audit; this is not a pass.

## Recommended action

Resolve the intended parameter domain and enclosing equations; check inherited bounds, final/protected status, guards and aliases. Construct an otherwise-valid source-level witness, establish a clean baseline in a capable engine, then retranslate at the witness and compare with the runtime override. For equality claims use the actual partner value. Do not apply a blanket min>0 fix yet.

## Scope and limitations

A source-level verdict addresses the reported declaration/claim, not every possible connected system. Tests cover 0–0.5 seconds and are not a proof of long-run stability. Shared instances are not distinct root causes. A missing bound, timeout, compiler error or failed nominal run alone never counts as a verified bug or a false positive. Fixes are proposals; no library/compiler implementation was changed.

[Group and related reports](../groups/baseline-blocked.md) · [Index](../README.md)
