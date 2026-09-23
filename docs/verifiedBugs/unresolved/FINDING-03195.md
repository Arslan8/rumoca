# FINDING-03195: Not yet established as a bug or a false positive

| Field | Value |
|---|---|
| Verdict | unresolved |
| Scope / group | baseline-blocked |
| Model | Modelica.Electrical.PowerConverters.Examples.ACDC.RectifierBridge2Pulse.DiodeBridge2Pulse |
| Target | rectifier.GoffDiode |
| Student classification | physical-bound-permits-zero |
| Original report | [FINDING-diodebridge2pulse-rectifier-goffdiode-zerolimit.md](../../v2/bugs/FINDING-diodebridge2pulse-rectifier-goffdiode-zerolimit.md) — reviewed as `FINDING-03195-diodebridge2pulse-rectifier-goffdiode.md`, which a later run renamed |
| Original SHA-256 | 9caeeaa848627bb30c8c5ce9327eec06c409ff2439c9b53b06a159455dee7548 |

## What remains unresolved

The current Rumoca nominal run is tool-error, before any reported perturbation. This prevents causal attribution to this parameter. Source metadata was recovered, but none of the reviewed source proofs or counterexamples establishes this particular claim. A baseline failure/tool limitation is neither confirmation nor a false positive.

## Source evidence

Compiler/source-resolved declaration: `Electrical/PowerConverters/ACDC/DiodeBridge2Pulse.mo:7`. Role: `parameter`; binding: `1e-05`; effective min: `0`; effective max: `None`. 

[Electrical/PowerConverters/ACDC/DiodeBridge2Pulse.mo — source snapshot](../evidence/sources/e7616dd51e09dc86-DiodeBridge2Pulse.mo)

```modelica
5:   parameter SI.Resistance RonDiode(final min=0) = 1e-05
6:     "Closed diode resistance";
7:   parameter SI.Conductance GoffDiode(final min=0) = 1e-05
8:     "Opened diode conductance";
9:   parameter SI.Voltage VkneeDiode(final min=0) = 0
10:     "Diode forward threshold voltage";
```


## Execution evidence

[Rumoca commands, return codes, integrity hashes, bounded output and metadata](../evidence/38b6ae365110419a.json). Baseline: **tool-error**.

No independent runtime override was executed for this target in this audit; this is not a pass.

## Recommended action

Resolve the intended parameter domain and enclosing equations; check inherited bounds, final/protected status, guards and aliases. Construct an otherwise-valid source-level witness, establish a clean baseline in a capable engine, then retranslate at the witness and compare with the runtime override. For equality claims use the actual partner value. Do not apply a blanket min>0 fix yet.

## Scope and limitations

A source-level verdict addresses the reported declaration/claim, not every possible connected system. Tests cover 0–0.5 seconds and are not a proof of long-run stability. Shared instances are not distinct root causes. A missing bound, timeout, compiler error or failed nominal run alone never counts as a verified bug or a false positive. Fixes are proposals; no library/compiler implementation was changed.

[Group and related reports](../groups/baseline-blocked.md) · [Index](../README.md)
