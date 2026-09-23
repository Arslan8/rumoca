# FINDING-01153: Not yet established as a bug or a false positive

| Field | Value |
|---|---|
| Verdict | unresolved |
| Scope / group | baseline-blocked |
| Model | Modelica.Electrical.Machines.Examples.DCMachines.DC_CompareCharacteristics |
| Target | dcee.Le |
| Student classification | physical-domain-unenforced |
| Original report | [FINDING-dc-comparecharacteristics-dcee-le-intent.md](../../v2/bugs/FINDING-dc-comparecharacteristics-dcee-le-intent.md) — reviewed as `FINDING-01153-dc-comparecharacteristics-dcee-le.md`, which a later run renamed |
| Original SHA-256 | 899fcdb91aa820d629ad787c54b7b9bdb5745c921d34db62cb804e03d996ddf1 |

## What remains unresolved

The current Rumoca nominal run is tool-error, before any reported perturbation. This prevents causal attribution to this parameter. Source metadata was recovered, but none of the reviewed source proofs or counterexamples establishes this particular claim. A baseline failure/tool limitation is neither confirmation nor a false positive.

## Source evidence

Compiler/source-resolved declaration: `Electrical/Machines/BasicMachines/DCMachines/DC_ElectricalExcited.mo:33`. Role: `parameter`; binding: `dceeData.Le`; effective min: `None`; effective max: `None`. 

[Electrical/Machines/BasicMachines/DCMachines/DC_ElectricalExcited.mo — source snapshot](../evidence/sources/750c79fb852e1417-DC_ElectricalExcited.mo)

```modelica
31:     "Temperature coefficient of excitation resistance"
32:     annotation (Dialog(tab="Excitation"));
33:   parameter SI.Inductance Le(start=1)
34:     "Total field excitation inductance"
35:     annotation (Dialog(tab="Excitation"));
36:   parameter Real sigmae(
```


## Execution evidence

[Rumoca commands, return codes, integrity hashes, bounded output and metadata](../evidence/f15341d4427cc3e0.json). Baseline: **tool-error**.

No independent runtime override was executed for this target in this audit; this is not a pass.

## Recommended action

Resolve the intended parameter domain and enclosing equations; check inherited bounds, final/protected status, guards and aliases. Construct an otherwise-valid source-level witness, establish a clean baseline in a capable engine, then retranslate at the witness and compare with the runtime override. For equality claims use the actual partner value. Do not apply a blanket min>0 fix yet.

## Scope and limitations

A source-level verdict addresses the reported declaration/claim, not every possible connected system. Tests cover 0–0.5 seconds and are not a proof of long-run stability. Shared instances are not distinct root causes. A missing bound, timeout, compiler error or failed nominal run alone never counts as a verified bug or a false positive. Fixes are proposals; no library/compiler implementation was changed.

[Group and related reports](../groups/baseline-blocked.md) · [Index](../README.md)
