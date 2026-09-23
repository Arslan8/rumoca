# FINDING-03453: Not yet established as a bug or a false positive

| Field | Value |
|---|---|
| Verdict | unresolved |
| Scope / group | baseline-blocked |
| Model | Modelica.Electrical.PowerConverters.Examples.ACDC.RectifierCenterTapmPulse.DiodeCenterTapmPulse |
| Target | rectifier.RonDiode |
| Student classification | physical-bound-permits-zero |
| Original report | [FINDING-diodecentertapmpulse-rectifier-rondiode-ruleoff.md](../../v2/bugs/FINDING-diodecentertapmpulse-rectifier-rondiode-ruleoff.md) — reviewed as `FINDING-03453-diodecentertapmpulse-rectifier-rondiode.md`, which a later run renamed |
| Original SHA-256 | ca565165b2985f78a5249d1b731769e56b84f5fa55f8b9433c6673988b22a3b7 |

## What remains unresolved

The current Rumoca nominal run is tool-error, before any reported perturbation. This prevents causal attribution to this parameter. Source metadata was recovered, but none of the reviewed source proofs or counterexamples establishes this particular claim. A baseline failure/tool limitation is neither confirmation nor a false positive.

## Source evidence

Compiler/source-resolved declaration: `Electrical/PowerConverters/ACDC/DiodeCenterTapmPulse.mo:6`. Role: `parameter`; binding: `1e-05`; effective min: `0`; effective max: `None`. 

[Electrical/PowerConverters/ACDC/DiodeCenterTapmPulse.mo — source snapshot](../evidence/sources/33058f25d3f088a7-DiodeCenterTapmPulse.mo)

```modelica
4:   extends Icons.Converter;
5:   parameter Integer m(final min=3) = 3 "Number of phases" annotation(Evaluate=true);
6:   parameter SI.Resistance RonDiode(final min=0) = 1e-05
7:     "Closed diode resistance";
8:   parameter SI.Conductance GoffDiode(final min=0) = 1e-05
9:     "Opened diode conductance";
```


## Execution evidence

[Rumoca commands, return codes, integrity hashes, bounded output and metadata](../evidence/9b175e838d577425.json). Baseline: **tool-error**.

No independent runtime override was executed for this target in this audit; this is not a pass.

## Recommended action

Resolve the intended parameter domain and enclosing equations; check inherited bounds, final/protected status, guards and aliases. Construct an otherwise-valid source-level witness, establish a clean baseline in a capable engine, then retranslate at the witness and compare with the runtime override. For equality claims use the actual partner value. Do not apply a blanket min>0 fix yet.

## Scope and limitations

A source-level verdict addresses the reported declaration/claim, not every possible connected system. Tests cover 0–0.5 seconds and are not a proof of long-run stability. Shared instances are not distinct root causes. A missing bound, timeout, compiler error or failed nominal run alone never counts as a verified bug or a false positive. Fixes are proposals; no library/compiler implementation was changed.

[Group and related reports](../groups/baseline-blocked.md) · [Index](../README.md)
