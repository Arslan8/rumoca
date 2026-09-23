# FINDING-03025: Not yet established as a bug or a false positive

| Field | Value |
|---|---|
| Verdict | unresolved |
| Scope / group | baseline-blocked |
| Model | Modelica.Electrical.PowerConverters.Examples.ACDC.RectifierBridge2mPulse.HalfControlledBridge2mPulse |
| Target | R |
| Student classification | physical-domain-unenforced |
| Original report | [FINDING-halfcontrolledbridge2mpulse-r-zerolimit.md](../../v2/bugs/FINDING-halfcontrolledbridge2mpulse-r-zerolimit.md) — reviewed as `FINDING-03025-halfcontrolledbridge2mpulse-r.md`, which a later run renamed |
| Original SHA-256 | 454a6b4c52189a2d6262599f3b3ce80b188eb9488e611cc2a93f80c0032ea5a7 |

## What remains unresolved

The current Rumoca nominal run is tool-error, before any reported perturbation. This prevents causal attribution to this parameter. Source metadata was recovered, but none of the reviewed source proofs or counterexamples establishes this particular claim. A baseline failure/tool limitation is neither confirmation nor a false positive.

## Source evidence

Compiler/source-resolved declaration: `Electrical/PowerConverters/Examples/ACDC/RectifierBridge2mPulse/HalfControlledBridge2mPulse.mo:11`. Role: `parameter`; binding: `20`; effective min: `None`; effective max: `None`. 

[Electrical/PowerConverters/Examples/ACDC/RectifierBridge2mPulse/HalfControlledBridge2mPulse.mo — source snapshot](../evidence/sources/cf43e40c882005bb-HalfControlledBridge2mPulse.mo)

```modelica
9:   parameter SI.Angle constantFiringAngle=30*pi/180
10:     "Firing angle";
11:   parameter SI.Resistance R=20 "Load resistance";
12: 
13:   Modelica.Electrical.Polyphase.Sources.SineVoltage sineVoltage(
14:     final m=m,
```


## Execution evidence

[Rumoca commands, return codes, integrity hashes, bounded output and metadata](../evidence/a54fb2c8ac8f1d80.json). Baseline: **tool-error**.

No independent runtime override was executed for this target in this audit; this is not a pass.

## Recommended action

Resolve the intended parameter domain and enclosing equations; check inherited bounds, final/protected status, guards and aliases. Construct an otherwise-valid source-level witness, establish a clean baseline in a capable engine, then retranslate at the witness and compare with the runtime override. For equality claims use the actual partner value. Do not apply a blanket min>0 fix yet.

## Scope and limitations

A source-level verdict addresses the reported declaration/claim, not every possible connected system. Tests cover 0–0.5 seconds and are not a proof of long-run stability. Shared instances are not distinct root causes. A missing bound, timeout, compiler error or failed nominal run alone never counts as a verified bug or a false positive. Fixes are proposals; no library/compiler implementation was changed.

[Group and related reports](../groups/baseline-blocked.md) · [Index](../README.md)
