# FINDING-01531: Not yet established as a bug or a false positive

| Field | Value |
|---|---|
| Verdict | unresolved |
| Scope / group | baseline-blocked |
| Model | Modelica.Electrical.Machines.Examples.DCMachines.DCSE_Start |
| Target | dcseData.Le |
| Student classification | divisor-reachable-zero |
| Original report | [FINDING-dcse-start-dcsedata-le-zerolimit.md](../../v2/bugs/FINDING-dcse-start-dcsedata-le-zerolimit.md) — reviewed as `FINDING-01531-dcse-start-dcsedata-le.md`, which a later run renamed |
| Original SHA-256 | 537d6c629b8a17a222f1a0c4de27bf34115665399df723db45632ca1e1b34c0f |

## What remains unresolved

The current Rumoca nominal run is tool-error, before any reported perturbation. This prevents causal attribution to this parameter. Source metadata was recovered, but none of the reviewed source proofs or counterexamples establishes this particular claim. A baseline failure/tool limitation is neither confirmation nor a false positive.

## Source evidence

Compiler/source-resolved declaration: `Electrical/Machines/Utilities/ParameterRecords/DcSeriesExcitedData.mo:14`. Role: `parameter`; binding: `0.0005`; effective min: `None`; effective max: `None`. 

[Electrical/Machines/Utilities/ParameterRecords/DcSeriesExcitedData.mo — source snapshot](../evidence/sources/0074b7caf8e008ad-DcSeriesExcitedData.mo)

```modelica
12:     "Temperature coefficient of excitation resistance"
13:     annotation (Dialog(tab="Excitation"));
14:   parameter SI.Inductance Le=0.0005
15:     "Total field excitation inductance"
16:     annotation (Dialog(tab="Excitation"));
17:   parameter Real sigmae(
```


## Execution evidence

[Rumoca commands, return codes, integrity hashes, bounded output and metadata](../evidence/40df0fa91f83b25d.json). Baseline: **tool-error**.

No independent runtime override was executed for this target in this audit; this is not a pass.

## Recommended action

Resolve the intended parameter domain and enclosing equations; check inherited bounds, final/protected status, guards and aliases. Construct an otherwise-valid source-level witness, establish a clean baseline in a capable engine, then retranslate at the witness and compare with the runtime override. For equality claims use the actual partner value. Do not apply a blanket min>0 fix yet.

## Scope and limitations

A source-level verdict addresses the reported declaration/claim, not every possible connected system. Tests cover 0–0.5 seconds and are not a proof of long-run stability. Shared instances are not distinct root causes. A missing bound, timeout, compiler error or failed nominal run alone never counts as a verified bug or a false positive. Fixes are proposals; no library/compiler implementation was changed.

[Group and related reports](../groups/baseline-blocked.md) · [Index](../README.md)
