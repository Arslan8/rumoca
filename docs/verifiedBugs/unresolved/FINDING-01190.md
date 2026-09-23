# FINDING-01190: Not yet established as a bug or a false positive

| Field | Value |
|---|---|
| Verdict | unresolved |
| Scope / group | baseline-blocked |
| Model | Modelica.Electrical.Machines.Examples.DCMachines.DC_CompareCharacteristics |
| Target | dcseData.sigmae |
| Student classification | divisor-reachable-zero |
| Original report | `FINDING-01190-dc-comparecharacteristics-dcsedata-sigmae.md` — [withdrawn](../../v2/bugs/withdrawn.md); a later run no longer makes this claim |
| Original SHA-256 | 52297110462fa8b01d62e7859e97512d39ae4b921e17fd80e209a7c26f43229b |

## What remains unresolved

The current Rumoca nominal run is tool-error, before any reported perturbation. This prevents causal attribution to this parameter. Source metadata was recovered, but none of the reviewed source proofs or counterexamples establishes this particular claim. A baseline failure/tool limitation is neither confirmation nor a false positive.

## Source evidence

Compiler/source-resolved declaration: `Electrical/Machines/Utilities/ParameterRecords/DcSeriesExcitedData.mo:17`. Role: `parameter`; binding: `0`; effective min: `0`; effective max: `0.99`. 

[Electrical/Machines/Utilities/ParameterRecords/DcSeriesExcitedData.mo — source snapshot](../evidence/sources/0074b7caf8e008ad-DcSeriesExcitedData.mo)

```modelica
15:     "Total field excitation inductance"
16:     annotation (Dialog(tab="Excitation"));
17:   parameter Real sigmae(
18:     min=0,
19:     max=0.99) = 0 "Stray fraction of total excitation inductance"
20:     annotation (Dialog(tab="Excitation"));
```


## Execution evidence

[Rumoca commands, return codes, integrity hashes, bounded output and metadata](../evidence/f15341d4427cc3e0.json). Baseline: **tool-error**.

No independent runtime override was executed for this target in this audit; this is not a pass.

## Recommended action

Resolve the intended parameter domain and enclosing equations; check inherited bounds, final/protected status, guards and aliases. Construct an otherwise-valid source-level witness, establish a clean baseline in a capable engine, then retranslate at the witness and compare with the runtime override. For equality claims use the actual partner value. Do not apply a blanket min>0 fix yet.

## Scope and limitations

A source-level verdict addresses the reported declaration/claim, not every possible connected system. Tests cover 0–0.5 seconds and are not a proof of long-run stability. Shared instances are not distinct root causes. A missing bound, timeout, compiler error or failed nominal run alone never counts as a verified bug or a false positive. Fixes are proposals; no library/compiler implementation was changed.

[Group and related reports](../groups/baseline-blocked.md) · [Index](../README.md)
