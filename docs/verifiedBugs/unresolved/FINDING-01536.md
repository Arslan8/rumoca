# FINDING-01536: Not yet established as a bug or a false positive

| Field | Value |
|---|---|
| Verdict | unresolved |
| Scope / group | baseline-blocked |
| Model | Modelica.Electrical.Machines.Examples.InductionMachines.IMC_DCBraking |
| Target | JLoad |
| Student classification | physical-domain-unenforced |
| Original report | [FINDING-imc-dcbraking-jload-zerolimit.md](../../v2/bugs/FINDING-imc-dcbraking-jload-zerolimit.md) — reviewed as `FINDING-01536-imc-dcbraking-jload.md`, which a later run renamed |
| Original SHA-256 | f0de21bfdd8488ad2b2d1bbd0be9d51da4830f4df573a5129cef3ec64d3777c7 |

## What remains unresolved

The current Rumoca nominal run is tool-error, before any reported perturbation. This prevents causal attribution to this parameter. Source metadata was recovered, but none of the reviewed source proofs or counterexamples establishes this particular claim. A baseline failure/tool limitation is neither confirmation nor a false positive.

## Source evidence

Compiler/source-resolved declaration: `Electrical/Machines/Examples/InductionMachines/IMC_DCBraking.mo:8`. Role: `parameter`; binding: `(4 * imcData.Jr)`; effective min: `None`; effective max: `None`. 

[Electrical/Machines/Examples/InductionMachines/IMC_DCBraking.mo — source snapshot](../evidence/sources/97f383f6819dcce7-IMC_DCBraking.mo)

```modelica
6:   parameter SI.AngularVelocity w0(displayUnit="rev/min")=
7:     2*pi*imcData.fsNominal/imcData.p "Initial mechanical speed";
8:   parameter SI.Inertia JLoad=4*imcData.Jr
9:     "Load's moment of inertia";
10:   SI.Torque tauElectrical=imc.tauElectrical "Electrical torque";
11:   SI.Torque tauShaft=imc.tauShaft "Shaft torque";
```


## Execution evidence

[Rumoca commands, return codes, integrity hashes, bounded output and metadata](../evidence/489fdf592354cb9a.json). Baseline: **tool-error**.

No independent runtime override was executed for this target in this audit; this is not a pass.

## Recommended action

Resolve the intended parameter domain and enclosing equations; check inherited bounds, final/protected status, guards and aliases. Construct an otherwise-valid source-level witness, establish a clean baseline in a capable engine, then retranslate at the witness and compare with the runtime override. For equality claims use the actual partner value. Do not apply a blanket min>0 fix yet.

## Scope and limitations

A source-level verdict addresses the reported declaration/claim, not every possible connected system. Tests cover 0–0.5 seconds and are not a proof of long-run stability. Shared instances are not distinct root causes. A missing bound, timeout, compiler error or failed nominal run alone never counts as a verified bug or a false positive. Fixes are proposals; no library/compiler implementation was changed.

[Group and related reports](../groups/baseline-blocked.md) · [Index](../README.md)
