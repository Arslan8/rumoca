# FINDING-03410: Not yet established as a bug or a false positive

| Field | Value |
|---|---|
| Verdict | unresolved |
| Scope / group | baseline-blocked |
| Model | Modelica.Electrical.PowerConverters.Examples.ACDC.RectifierCenterTap2Pulse.DiodeCenterTap2Pulse |
| Target | R |
| Student classification | physical-domain-unenforced |
| Original report | [FINDING-diodecentertap2pulse-r-zerolimit.md](../../v2/bugs/FINDING-diodecentertap2pulse-r-zerolimit.md) — reviewed as `FINDING-03410-diodecentertap2pulse-r.md`, which a later run renamed |
| Original SHA-256 | eebf75d366417a37de35f4e11b8a03bbdd1317843bf3d086b56440321c626c42 |

## What remains unresolved

The current Rumoca nominal run is tool-error, before any reported perturbation. This prevents causal attribution to this parameter. Source metadata was recovered, but none of the reviewed source proofs or counterexamples establishes this particular claim. A baseline failure/tool limitation is neither confirmation nor a false positive.

## Source evidence

Compiler/source-resolved declaration: `Electrical/PowerConverters/Examples/ACDC/RectifierCenterTap2Pulse/DiodeCenterTap2Pulse.mo:8`. Role: `parameter`; binding: `20`; effective min: `None`; effective max: `None`. 

[Electrical/PowerConverters/Examples/ACDC/RectifierCenterTap2Pulse/DiodeCenterTap2Pulse.mo — source snapshot](../evidence/sources/528b9e7692ba42ef-DiodeCenterTap2Pulse.mo)

```modelica
6:   parameter SI.Voltage Vrms=110 "RMS supply voltage";
7:   parameter SI.Frequency f=50 "Frequency";
8:   parameter SI.Resistance R=20 "Load resistance";
9: 
10:   Modelica.Electrical.Analog.Basic.Ground ground annotation (Placement(
11:         transformation(
```


## Execution evidence

[Rumoca commands, return codes, integrity hashes, bounded output and metadata](../evidence/5328f657991b3474.json). Baseline: **tool-error**.

No independent runtime override was executed for this target in this audit; this is not a pass.

## Recommended action

Resolve the intended parameter domain and enclosing equations; check inherited bounds, final/protected status, guards and aliases. Construct an otherwise-valid source-level witness, establish a clean baseline in a capable engine, then retranslate at the witness and compare with the runtime override. For equality claims use the actual partner value. Do not apply a blanket min>0 fix yet.

## Scope and limitations

A source-level verdict addresses the reported declaration/claim, not every possible connected system. Tests cover 0–0.5 seconds and are not a proof of long-run stability. Shared instances are not distinct root causes. A missing bound, timeout, compiler error or failed nominal run alone never counts as a verified bug or a false positive. Fixes are proposals; no library/compiler implementation was changed.

[Group and related reports](../groups/baseline-blocked.md) · [Index](../README.md)
