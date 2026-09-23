# FINDING-01508: Not yet established as a bug or a false positive

| Field | Value |
|---|---|
| Verdict | unresolved |
| Scope / group | baseline-blocked |
| Model | Modelica.Electrical.Machines.Examples.DCMachines.DCSE_Start |
| Target | JLoad |
| Student classification | physical-domain-unenforced |
| Original report | [FINDING-dcse-start-jload-zerolimit.md](../../v2/bugs/FINDING-dcse-start-jload-zerolimit.md) — reviewed as `FINDING-01508-dcse-start-jload.md`, which a later run renamed |
| Original SHA-256 | ff1e1fdb603172648d467be18e2975a395f4b721ca3c5665ad7fc0ed1d659060 |

## What remains unresolved

The current Rumoca nominal run is tool-error, before any reported perturbation. This prevents causal attribution to this parameter. Source metadata was recovered, but none of the reviewed source proofs or counterexamples establishes this particular claim. A baseline failure/tool limitation is neither confirmation nor a false positive.

## Source evidence

Compiler/source-resolved declaration: `Electrical/Machines/Examples/DCMachines/DCSE_Start.mo:11`. Role: `parameter`; binding: `0.15`; effective min: `None`; effective max: `None`. 

[Electrical/Machines/Examples/DCMachines/DCSE_Start.mo — source snapshot](../evidence/sources/fb93406f366db131-DCSE_Start.mo)

```modelica
9:   parameter SI.AngularVelocity wLoad(displayUnit="rev/min")=
10:        1410*2*Modelica.Constants.pi/60 "Nominal load speed";
11:   parameter SI.Inertia JLoad=0.15
12:     "Load's moment of inertia";
13:   Machines.BasicMachines.DCMachines.DC_SeriesExcited dcse(
14:     VaNominal=dcseData.VaNominal,
```


## Execution evidence

[Rumoca commands, return codes, integrity hashes, bounded output and metadata](../evidence/40df0fa91f83b25d.json). Baseline: **tool-error**.

No independent runtime override was executed for this target in this audit; this is not a pass.

## Recommended action

Resolve the intended parameter domain and enclosing equations; check inherited bounds, final/protected status, guards and aliases. Construct an otherwise-valid source-level witness, establish a clean baseline in a capable engine, then retranslate at the witness and compare with the runtime override. For equality claims use the actual partner value. Do not apply a blanket min>0 fix yet.

## Scope and limitations

A source-level verdict addresses the reported declaration/claim, not every possible connected system. Tests cover 0–0.5 seconds and are not a proof of long-run stability. Shared instances are not distinct root causes. A missing bound, timeout, compiler error or failed nominal run alone never counts as a verified bug or a false positive. Fixes are proposals; no library/compiler implementation was changed.

[Group and related reports](../groups/baseline-blocked.md) · [Index](../README.md)
