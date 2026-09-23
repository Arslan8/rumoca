# FINDING-01173: Not yet established as a bug or a false positive

| Field | Value |
|---|---|
| Verdict | unresolved |
| Scope / group | baseline-blocked |
| Model | Modelica.Electrical.Machines.Examples.DCMachines.DC_CompareCharacteristics |
| Target | dcse.Lme |
| Student classification | physical-domain-unenforced |
| Original report | [FINDING-dc-comparecharacteristics-dcse-lme-zerolimit.md](../../v2/bugs/FINDING-dc-comparecharacteristics-dcse-lme-zerolimit.md) — reviewed as `FINDING-01173-dc-comparecharacteristics-dcse-lme.md`, which a later run renamed |
| Original SHA-256 | 5670617c9789bfb1f5c90a61b9802002431b05eb775f3d8755a8e35242d868ab |

## What remains unresolved

The current Rumoca nominal run is tool-error, before any reported perturbation. This prevents causal attribution to this parameter. Source metadata was recovered, but none of the reviewed source proofs or counterexamples establishes this particular claim. A baseline failure/tool limitation is neither confirmation nor a false positive.

## Source evidence

Compiler/source-resolved declaration: `Electrical/Machines/BasicMachines/DCMachines/DC_SeriesExcited.mo:84`. Role: `parameter`; binding: `(dcse.Le * (1 - dcse.sigmae))`; effective min: `None`; effective max: `None`. 

[Electrical/Machines/BasicMachines/DCMachines/DC_SeriesExcited.mo — source snapshot](../evidence/sources/d5e46cdc01821f26-DC_SeriesExcited.mo)

```modelica
82:           extent={{-90,-50},{-110,-70}})));
83: protected
84:   final parameter SI.Inductance Lme=Le*(1 - sigmae)
85:     "Main part of excitation inductance";
86:   final parameter SI.Inductance Lesigma=Le*sigmae
87:     "Stray part of excitation inductance" annotation (Evaluate=true);
```


## Execution evidence

[Rumoca commands, return codes, integrity hashes, bounded output and metadata](../evidence/f15341d4427cc3e0.json). Baseline: **tool-error**.

No independent runtime override was executed for this target in this audit; this is not a pass.

## Recommended action

Resolve the intended parameter domain and enclosing equations; check inherited bounds, final/protected status, guards and aliases. Construct an otherwise-valid source-level witness, establish a clean baseline in a capable engine, then retranslate at the witness and compare with the runtime override. For equality claims use the actual partner value. Do not apply a blanket min>0 fix yet.

## Scope and limitations

A source-level verdict addresses the reported declaration/claim, not every possible connected system. Tests cover 0–0.5 seconds and are not a proof of long-run stability. Shared instances are not distinct root causes. A missing bound, timeout, compiler error or failed nominal run alone never counts as a verified bug or a false positive. Fixes are proposals; no library/compiler implementation was changed.

[Group and related reports](../groups/baseline-blocked.md) · [Index](../README.md)
