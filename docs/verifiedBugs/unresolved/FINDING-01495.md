# FINDING-01495: Not yet established as a bug or a false positive

| Field | Value |
|---|---|
| Verdict | unresolved |
| Scope / group | baseline-blocked |
| Model | Modelica.Electrical.Machines.Examples.DCMachines.DCSE_SinglePhase |
| Target | dcseData.Re |
| Student classification | physical-domain-unenforced |
| Original report | [FINDING-dcse-singlephase-dcsedata-re-unbounded.md](../../v2/bugs/FINDING-dcse-singlephase-dcsedata-re-unbounded.md) — reviewed as `FINDING-01495-dcse-singlephase-dcsedata-re.md`, which a later run renamed |
| Original SHA-256 | 58a694750d66c2e6f82e9b0f8801b4462634ad74e8051f7271fd97184445acb6 |

## What remains unresolved

The current Rumoca nominal run is tool-error, before any reported perturbation. This prevents causal attribution to this parameter. Source metadata was recovered, but none of the reviewed source proofs or counterexamples establishes this particular claim. A baseline failure/tool limitation is neither confirmation nor a false positive.

## Source evidence

Compiler/source-resolved declaration: `Electrical/Machines/Utilities/ParameterRecords/DcSeriesExcitedData.mo:5`. Role: `parameter`; binding: `0.01`; effective min: `None`; effective max: `None`. 

[Electrical/Machines/Utilities/ParameterRecords/DcSeriesExcitedData.mo — source snapshot](../evidence/sources/0074b7caf8e008ad-DcSeriesExcitedData.mo)

```modelica
3:   extends DcPermanentMagnetData(wNominal=1410*2*pi/60);
4:   import Modelica.Constants.pi;
5:   parameter SI.Resistance Re=0.01
6:     "Series excitation resistance at TeRef"
7:     annotation (Dialog(tab="Excitation"));
8:   parameter SI.Temperature TeRef=293.15
```


## Execution evidence

[Rumoca commands, return codes, integrity hashes, bounded output and metadata](../evidence/f00103fd4bc29b1a.json). Baseline: **tool-error**.

No independent runtime override was executed for this target in this audit; this is not a pass.

## Recommended action

Resolve the intended parameter domain and enclosing equations; check inherited bounds, final/protected status, guards and aliases. Construct an otherwise-valid source-level witness, establish a clean baseline in a capable engine, then retranslate at the witness and compare with the runtime override. For equality claims use the actual partner value. Do not apply a blanket min>0 fix yet.

## Scope and limitations

A source-level verdict addresses the reported declaration/claim, not every possible connected system. Tests cover 0–0.5 seconds and are not a proof of long-run stability. Shared instances are not distinct root causes. A missing bound, timeout, compiler error or failed nominal run alone never counts as a verified bug or a false positive. Fixes are proposals; no library/compiler implementation was changed.

[Group and related reports](../groups/baseline-blocked.md) · [Index](../README.md)
