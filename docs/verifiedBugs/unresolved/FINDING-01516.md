# FINDING-01516: Not yet established as a bug or a false positive

| Field | Value |
|---|---|
| Verdict | unresolved |
| Scope / group | baseline-blocked |
| Model | Modelica.Electrical.Machines.Examples.DCMachines.DCSE_Start |
| Target | dcse.Re |
| Student classification | physical-domain-unenforced |
| Original report | [FINDING-dcse-start-dcse-re-unbounded.md](../../v2/bugs/FINDING-dcse-start-dcse-re-unbounded.md) — reviewed as `FINDING-01516-dcse-start-dcse-re.md`, which a later run renamed |
| Original SHA-256 | 9dbb382a61f8523c883ea3dea85b2dcc4bc8057a3ade996a7522cb6b78762a05 |

## What remains unresolved

The current Rumoca nominal run is tool-error, before any reported perturbation. This prevents causal attribution to this parameter. Source metadata was recovered, but none of the reviewed source proofs or counterexamples establishes this particular claim. A baseline failure/tool limitation is neither confirmation nor a false positive.

## Source evidence

Compiler/source-resolved declaration: `Electrical/Machines/BasicMachines/DCMachines/DC_SeriesExcited.mo:26`. Role: `parameter`; binding: `dcseData.Re`; effective min: `None`; effective max: `None`. 

[Electrical/Machines/BasicMachines/DCMachines/DC_SeriesExcited.mo — source snapshot](../evidence/sources/d5e46cdc01821f26-DC_SeriesExcited.mo)

```modelica
24:         lossPowerSeriesExcitation=re.LossPower),
25:     core(final w=airGapDC.w));
26:   parameter SI.Resistance Re(start=0.01)
27:     "Series excitation resistance at TeRef"
28:     annotation (Dialog(tab="Excitation"));
29:   parameter SI.Temperature TeRef(start=293.15)
```


## Execution evidence

[Rumoca commands, return codes, integrity hashes, bounded output and metadata](../evidence/40df0fa91f83b25d.json). Baseline: **tool-error**.

No independent runtime override was executed for this target in this audit; this is not a pass.

## Recommended action

Resolve the intended parameter domain and enclosing equations; check inherited bounds, final/protected status, guards and aliases. Construct an otherwise-valid source-level witness, establish a clean baseline in a capable engine, then retranslate at the witness and compare with the runtime override. For equality claims use the actual partner value. Do not apply a blanket min>0 fix yet.

## Scope and limitations

A source-level verdict addresses the reported declaration/claim, not every possible connected system. Tests cover 0–0.5 seconds and are not a proof of long-run stability. Shared instances are not distinct root causes. A missing bound, timeout, compiler error or failed nominal run alone never counts as a verified bug or a false positive. Fixes are proposals; no library/compiler implementation was changed.

[Group and related reports](../groups/baseline-blocked.md) · [Index](../README.md)
