# FINDING-01918: Not yet established as a bug or a false positive

| Field | Value |
|---|---|
| Verdict | unresolved |
| Scope / group | baseline-blocked |
| Model | Modelica.Electrical.Machines.Examples.InductionMachines.IMC_YDarc |
| Target | JLoad |
| Student classification | physical-domain-unenforced |
| Original report | [FINDING-imc-ydarc-jload-zerolimit.md](../../v2/bugs/FINDING-imc-ydarc-jload-zerolimit.md) — reviewed as `FINDING-01918-imc-ydarc-jload.md`, which a later run renamed |
| Original SHA-256 | ee0abf08f7c2cd32a60b27d8987974c77474c5e55c22f2c0d9674bcd5fc14222 |

## What remains unresolved

The current Rumoca nominal run is tool-error, before any reported perturbation. This prevents causal attribution to this parameter. Source metadata was recovered, but none of the reviewed source proofs or counterexamples establishes this particular claim. A baseline failure/tool limitation is neither confirmation nor a false positive.

## Source evidence

Compiler/source-resolved declaration: `Electrical/Machines/Examples/InductionMachines/IMC_YDarc.mo:16`. Role: `parameter`; binding: `0.29`; effective min: `None`; effective max: `None`. 

[Electrical/Machines/Examples/InductionMachines/IMC_YDarc.mo — source snapshot](../evidence/sources/cf0b2df7bf01b11b-IMC_YDarc.mo)

```modelica
14:   parameter SI.AngularVelocity wLoad(displayUnit="rev/min")=
15:        1440.45*2*Modelica.Constants.pi/60 "Nominal load speed";
16:   parameter SI.Inertia JLoad=0.29
17:     "Load's moment of inertia";
18:   Machines.BasicMachines.InductionMachines.IM_SquirrelCage aimc(
19:     p=aimcData.p,
```


## Execution evidence

[Rumoca commands, return codes, integrity hashes, bounded output and metadata](../evidence/a03f73e52ba0cfd4.json). Baseline: **tool-error**.

No independent runtime override was executed for this target in this audit; this is not a pass.

## Recommended action

Resolve the intended parameter domain and enclosing equations; check inherited bounds, final/protected status, guards and aliases. Construct an otherwise-valid source-level witness, establish a clean baseline in a capable engine, then retranslate at the witness and compare with the runtime override. For equality claims use the actual partner value. Do not apply a blanket min>0 fix yet.

## Scope and limitations

A source-level verdict addresses the reported declaration/claim, not every possible connected system. Tests cover 0–0.5 seconds and are not a proof of long-run stability. Shared instances are not distinct root causes. A missing bound, timeout, compiler error or failed nominal run alone never counts as a verified bug or a false positive. Fixes are proposals; no library/compiler implementation was changed.

[Group and related reports](../groups/baseline-blocked.md) · [Index](../README.md)
