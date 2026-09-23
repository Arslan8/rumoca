# FINDING-03004: Not yet established as a bug or a false positive

| Field | Value |
|---|---|
| Verdict | unresolved |
| Scope / group | baseline-blocked |
| Model | Modelica.Electrical.PowerConverters.Examples.ACDC.RectifierBridge2mPulse.DiodeBridge2mPulse |
| Target | R |
| Student classification | physical-domain-unenforced |
| Original report | [FINDING-diodebridge2mpulse-r-zerolimit.md](../../v2/bugs/FINDING-diodebridge2mpulse-r-zerolimit.md) — reviewed as `FINDING-03004-diodebridge2mpulse-r.md`, which a later run renamed |
| Original SHA-256 | c7ab214eee58eb82f36a0e92f8e7fd7151ac6ac364c7b345f06f6753d2f7815e |

## What remains unresolved

The current Rumoca nominal run is tool-error, before any reported perturbation. This prevents causal attribution to this parameter. Source metadata was recovered, but none of the reviewed source proofs or counterexamples establishes this particular claim. A baseline failure/tool limitation is neither confirmation nor a false positive.

## Source evidence

Compiler/source-resolved declaration: `Electrical/PowerConverters/Examples/ACDC/RectifierBridge2mPulse/DiodeBridge2mPulse.mo:9`. Role: `parameter`; binding: `20`; effective min: `None`; effective max: `None`. 

[Electrical/PowerConverters/Examples/ACDC/RectifierBridge2mPulse/DiodeBridge2mPulse.mo — source snapshot](../evidence/sources/84a111bb1bbd0a90-DiodeBridge2mPulse.mo)

```modelica
7:   parameter SI.Voltage Vrms=110 "RMS supply voltage";
8:   parameter SI.Frequency f=50 "Frequency";
9:   parameter SI.Resistance R=20 "Load resistance";
10: 
11:   Modelica.Electrical.Polyphase.Sources.SineVoltage sineVoltage(
12:     final m=m,
```


## Execution evidence

[Rumoca commands, return codes, integrity hashes, bounded output and metadata](../evidence/bd25d8120598eda3.json). Baseline: **tool-error**.

No independent runtime override was executed for this target in this audit; this is not a pass.

## Recommended action

Resolve the intended parameter domain and enclosing equations; check inherited bounds, final/protected status, guards and aliases. Construct an otherwise-valid source-level witness, establish a clean baseline in a capable engine, then retranslate at the witness and compare with the runtime override. For equality claims use the actual partner value. Do not apply a blanket min>0 fix yet.

## Scope and limitations

A source-level verdict addresses the reported declaration/claim, not every possible connected system. Tests cover 0–0.5 seconds and are not a proof of long-run stability. Shared instances are not distinct root causes. A missing bound, timeout, compiler error or failed nominal run alone never counts as a verified bug or a false positive. Fixes are proposals; no library/compiler implementation was changed.

[Group and related reports](../groups/baseline-blocked.md) · [Index](../README.md)
