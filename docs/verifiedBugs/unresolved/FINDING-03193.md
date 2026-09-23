# FINDING-03193: Not yet established as a bug or a false positive

| Field | Value |
|---|---|
| Verdict | unresolved |
| Scope / group | baseline-blocked |
| Model | Modelica.Electrical.PowerConverters.Examples.ACDC.RectifierBridge2Pulse.DiodeBridge2Pulse |
| Target | R |
| Student classification | physical-domain-unenforced |
| Original report | [FINDING-diodebridge2pulse-r-zerolimit.md](../../v2/bugs/FINDING-diodebridge2pulse-r-zerolimit.md) — reviewed as `FINDING-03193-diodebridge2pulse-r.md`, which a later run renamed |
| Original SHA-256 | 59731081ea2622ac2bc480b72ba36df87597d2f95a660a4f3da805934277feb9 |

## What remains unresolved

The current Rumoca nominal run is tool-error, before any reported perturbation. This prevents causal attribution to this parameter. Source metadata was recovered, but none of the reviewed source proofs or counterexamples establishes this particular claim. A baseline failure/tool limitation is neither confirmation nor a false positive.

## Source evidence

Compiler/source-resolved declaration: `Electrical/PowerConverters/Examples/ACDC/RectifierBridge2Pulse/DiodeBridge2Pulse.mo:8`. Role: `parameter`; binding: `20`; effective min: `None`; effective max: `None`. 

[Electrical/PowerConverters/Examples/ACDC/RectifierBridge2Pulse/DiodeBridge2Pulse.mo — source snapshot](../evidence/sources/35d93e7b453ee922-DiodeBridge2Pulse.mo)

```modelica
6:   parameter SI.Voltage Vrms=110 "RMS supply voltage";
7:   parameter SI.Frequency f=50 "Frequency";
8:   parameter SI.Resistance R=20 "Load resistance";
9:   // parameter SI.Inductance L = 1 "Load resistance" annotation(Evaluate=true);
10:   // parameter SI.Voltage VDC=-120 "DC load offset voltage";
11:   Modelica.Electrical.Analog.Basic.Ground ground annotation (Placement(
```


## Execution evidence

[Rumoca commands, return codes, integrity hashes, bounded output and metadata](../evidence/38b6ae365110419a.json). Baseline: **tool-error**.

No independent runtime override was executed for this target in this audit; this is not a pass.

## Recommended action

Resolve the intended parameter domain and enclosing equations; check inherited bounds, final/protected status, guards and aliases. Construct an otherwise-valid source-level witness, establish a clean baseline in a capable engine, then retranslate at the witness and compare with the runtime override. For equality claims use the actual partner value. Do not apply a blanket min>0 fix yet.

## Scope and limitations

A source-level verdict addresses the reported declaration/claim, not every possible connected system. Tests cover 0–0.5 seconds and are not a proof of long-run stability. Shared instances are not distinct root causes. A missing bound, timeout, compiler error or failed nominal run alone never counts as a verified bug or a false positive. Fixes are proposals; no library/compiler implementation was changed.

[Group and related reports](../groups/baseline-blocked.md) · [Index](../README.md)
