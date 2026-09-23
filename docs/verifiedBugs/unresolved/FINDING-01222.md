# FINDING-01222: Not yet established as a bug or a false positive

| Field | Value |
|---|---|
| Verdict | unresolved |
| Scope / group | baseline-blocked |
| Model | Modelica.Electrical.Machines.Examples.DCMachines.DCPM_Cooling |
| Target | Ca |
| Student classification | physical-domain-unenforced |
| Original report | [FINDING-dcpm-cooling-ca-zerolimit.md](../../v2/bugs/FINDING-dcpm-cooling-ca-zerolimit.md) — reviewed as `FINDING-01222-dcpm-cooling-ca.md`, which a later run renamed |
| Original SHA-256 | a4d2a60cd0fcd3777c3075dc0c338fd896b25b58269806c7f94f6fdeb1ddf53b |

## What remains unresolved

The current Rumoca nominal run is tool-error, before any reported perturbation. This prevents causal attribution to this parameter. Source metadata was recovered, but none of the reviewed source proofs or counterexamples establishes this particular claim. A baseline failure/tool limitation is neither confirmation nor a false positive.

## Source evidence

Compiler/source-resolved declaration: `Electrical/Machines/Examples/DCMachines/DCPM_Cooling.mo:13`. Role: `parameter`; binding: `20`; effective min: `None`; effective max: `None`. 

[Electrical/Machines/Examples/DCMachines/DCPM_Cooling.mo — source snapshot](../evidence/sources/f148851cfdfd9dcf-DCPM_Cooling.mo)

```modelica
11:   parameter SI.Temperature TAmbient=293.15
12:     "Ambient temperature";
13:   parameter SI.HeatCapacity Ca=20
14:     "Armature's heat capacity";
15:   parameter SI.HeatCapacity Cc=50 "Core's heat capacity";
16:   final parameter SI.Power Losses=dcpm.Ra*dcpm.IaNominal^2
```


## Execution evidence

[Rumoca commands, return codes, integrity hashes, bounded output and metadata](../evidence/2651adcda9432b0e.json). Baseline: **tool-error**.

No independent runtime override was executed for this target in this audit; this is not a pass.

## Recommended action

Resolve the intended parameter domain and enclosing equations; check inherited bounds, final/protected status, guards and aliases. Construct an otherwise-valid source-level witness, establish a clean baseline in a capable engine, then retranslate at the witness and compare with the runtime override. For equality claims use the actual partner value. Do not apply a blanket min>0 fix yet.

## Scope and limitations

A source-level verdict addresses the reported declaration/claim, not every possible connected system. Tests cover 0–0.5 seconds and are not a proof of long-run stability. Shared instances are not distinct root causes. A missing bound, timeout, compiler error or failed nominal run alone never counts as a verified bug or a false positive. Fixes are proposals; no library/compiler implementation was changed.

[Group and related reports](../groups/baseline-blocked.md) · [Index](../README.md)
