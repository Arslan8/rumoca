# FINDING-03051: Not yet established as a bug or a false positive

| Field | Value |
|---|---|
| Verdict | unresolved |
| Scope / group | baseline-blocked |
| Model | Modelica.Electrical.PowerConverters.Examples.ACDC.RectifierBridge2mPulse.ThyristorBridge2mPulse_DC_Drive |
| Target | ZMains |
| Student classification | physical-domain-unenforced |
| Original report | [FINDING-thyristorbridge2mpulse-dc-drive-zmains-zerolimit.md](../../v2/bugs/FINDING-thyristorbridge2mpulse-dc-drive-zmains-zerolimit.md) — reviewed as `FINDING-03051-thyristorbridge2mpulse-dc-drive-zmains.md`, which a later run renamed |
| Original SHA-256 | 7f243b6d37b256ebb2fb8adaf9e8f6ff4d2bae66566a6044eca52ef82b8590e0 |

## What remains unresolved

The current Rumoca nominal run is tool-error, before any reported perturbation. This prevents causal attribution to this parameter. Source metadata was recovered, but none of the reviewed source proofs or counterexamples establishes this particular claim. A baseline failure/tool limitation is neither confirmation nor a false positive.

## Source evidence

Compiler/source-resolved declaration: `Electrical/PowerConverters/Examples/ACDC/RectifierBridge2mPulse/ThyristorBridge2mPulse_DC_Drive.mo:14`. Role: `parameter`; binding: `(((Vrms ^ 2) / SMains) * m)`; effective min: `None`; effective max: `None`. 

[Electrical/PowerConverters/Examples/ACDC/RectifierBridge2mPulse/ThyristorBridge2mPulse_DC_Drive.mo — source snapshot](../evidence/sources/d6dfee8541471ef8-ThyristorBridge2mPulse_DC_Drive.mo)

```modelica
12:     "Mains short circuit apparent power";
13:   parameter Real lamdaMains=0.1 "Mains short circuit power factor";
14:   final parameter SI.Impedance ZMains=Vrms^2/SMains*m
15:     "Mains short circuit impedance";
16:   final parameter SI.Resistance RMains=ZMains*lamdaMains
17:     "Mains resistance" annotation (Evaluate=true);
```


## Execution evidence

[Rumoca commands, return codes, integrity hashes, bounded output and metadata](../evidence/d8e62ee37d41ac80.json). Baseline: **tool-error**.

No independent runtime override was executed for this target in this audit; this is not a pass.

## Recommended action

Resolve the intended parameter domain and enclosing equations; check inherited bounds, final/protected status, guards and aliases. Construct an otherwise-valid source-level witness, establish a clean baseline in a capable engine, then retranslate at the witness and compare with the runtime override. For equality claims use the actual partner value. Do not apply a blanket min>0 fix yet.

## Scope and limitations

A source-level verdict addresses the reported declaration/claim, not every possible connected system. Tests cover 0–0.5 seconds and are not a proof of long-run stability. Shared instances are not distinct root causes. A missing bound, timeout, compiler error or failed nominal run alone never counts as a verified bug or a false positive. Fixes are proposals; no library/compiler implementation was changed.

[Group and related reports](../groups/baseline-blocked.md) · [Index](../README.md)
