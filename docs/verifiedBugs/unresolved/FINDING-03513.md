# FINDING-03513: Not yet established as a bug or a false positive

| Field | Value |
|---|---|
| Verdict | unresolved |
| Scope / group | baseline-blocked |
| Model | Modelica.Electrical.PowerConverters.Examples.ACDC.RectifierCenterTapmPulse.ThyristorCenterTapmPulse_R |
| Target | R |
| Student classification | physical-domain-unenforced |
| Original report | [FINDING-thyristorcentertapmpulse-r-r-zerolimit.md](../../v2/bugs/FINDING-thyristorcentertapmpulse-r-r-zerolimit.md) — reviewed as `FINDING-03513-thyristorcentertapmpulse-r-r.md`, which a later run renamed |
| Original SHA-256 | 38c7e0d561b7f79a1754fed312d992ee9c1446fd67510399ccdfbc35307f30e6 |

## What remains unresolved

The current Rumoca nominal run is tool-error, before any reported perturbation. This prevents causal attribution to this parameter. Source metadata was recovered, but none of the reviewed source proofs or counterexamples establishes this particular claim. A baseline failure/tool limitation is neither confirmation nor a false positive.

## Source evidence

Compiler/source-resolved declaration: `Electrical/PowerConverters/Examples/ACDC/RectifierCenterTapmPulse/ThyristorCenterTapmPulse_R.mo:10`. Role: `parameter`; binding: `20`; effective min: `None`; effective max: `None`. 

[Electrical/PowerConverters/Examples/ACDC/RectifierCenterTapmPulse/ThyristorCenterTapmPulse_R.mo — source snapshot](../evidence/sources/65e0bbc4a31cb164-ThyristorCenterTapmPulse_R.mo)

```modelica
8:   parameter SI.Angle constantFiringAngle=30*pi/180
9:     "Firing angle";
10:   parameter SI.Resistance R=20 "Load resistance";
11:   Modelica.Electrical.Analog.Basic.Resistor resistor(R=R) annotation (
12:       Placement(transformation(
13:         origin={30,30},
```


## Execution evidence

[Rumoca commands, return codes, integrity hashes, bounded output and metadata](../evidence/4465555654ddfa32.json). Baseline: **tool-error**.

No independent runtime override was executed for this target in this audit; this is not a pass.

## Recommended action

Resolve the intended parameter domain and enclosing equations; check inherited bounds, final/protected status, guards and aliases. Construct an otherwise-valid source-level witness, establish a clean baseline in a capable engine, then retranslate at the witness and compare with the runtime override. For equality claims use the actual partner value. Do not apply a blanket min>0 fix yet.

## Scope and limitations

A source-level verdict addresses the reported declaration/claim, not every possible connected system. Tests cover 0–0.5 seconds and are not a proof of long-run stability. Shared instances are not distinct root causes. A missing bound, timeout, compiler error or failed nominal run alone never counts as a verified bug or a false positive. Fixes are proposals; no library/compiler implementation was changed.

[Group and related reports](../groups/baseline-blocked.md) · [Index](../README.md)
