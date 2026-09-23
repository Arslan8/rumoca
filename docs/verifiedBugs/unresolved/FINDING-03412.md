# FINDING-03412: Not yet established as a bug or a false positive

| Field | Value |
|---|---|
| Verdict | unresolved |
| Scope / group | baseline-blocked |
| Model | Modelica.Electrical.PowerConverters.Examples.ACDC.RectifierCenterTap2Pulse.DiodeCenterTap2Pulse |
| Target | rectifier.GoffDiode |
| Student classification | physical-bound-permits-zero |
| Original report | [FINDING-diodecentertap2pulse-rectifier-goffdiode-zerolimit.md](../../v2/bugs/FINDING-diodecentertap2pulse-rectifier-goffdiode-zerolimit.md) — reviewed as `FINDING-03412-diodecentertap2pulse-rectifier-goffdiode.md`, which a later run renamed |
| Original SHA-256 | 737a6dfb836f9590a8bea37588d7a8023bcd78267c0e234df76ca3ab2a705580 |

## What remains unresolved

The current Rumoca nominal run is tool-error, before any reported perturbation. This prevents causal attribution to this parameter. Source metadata was recovered, but none of the reviewed source proofs or counterexamples establishes this particular claim. A baseline failure/tool limitation is neither confirmation nor a false positive.

## Source evidence

Compiler/source-resolved declaration: `Electrical/PowerConverters/ACDC/DiodeCenterTap2Pulse.mo:7`. Role: `parameter`; binding: `1e-05`; effective min: `0`; effective max: `None`. 

[Electrical/PowerConverters/ACDC/DiodeCenterTap2Pulse.mo — source snapshot](../evidence/sources/8622ed3d5ba1ae94-DiodeCenterTap2Pulse.mo)

```modelica
5:   parameter SI.Resistance RonDiode(final min=0) = 1e-05
6:     "Closed diode resistance";
7:   parameter SI.Conductance GoffDiode(final min=0) = 1e-05
8:     "Opened diode conductance";
9:   parameter SI.Voltage VkneeDiode(final min=0) = 0
10:     "Diode forward threshold voltage";
```


## Execution evidence

[Rumoca commands, return codes, integrity hashes, bounded output and metadata](../evidence/5328f657991b3474.json). Baseline: **tool-error**.

No independent runtime override was executed for this target in this audit; this is not a pass.

## Recommended action

Resolve the intended parameter domain and enclosing equations; check inherited bounds, final/protected status, guards and aliases. Construct an otherwise-valid source-level witness, establish a clean baseline in a capable engine, then retranslate at the witness and compare with the runtime override. For equality claims use the actual partner value. Do not apply a blanket min>0 fix yet.

## Scope and limitations

A source-level verdict addresses the reported declaration/claim, not every possible connected system. Tests cover 0–0.5 seconds and are not a proof of long-run stability. Shared instances are not distinct root causes. A missing bound, timeout, compiler error or failed nominal run alone never counts as a verified bug or a false positive. Fixes are proposals; no library/compiler implementation was changed.

[Group and related reports](../groups/baseline-blocked.md) · [Index](../README.md)
