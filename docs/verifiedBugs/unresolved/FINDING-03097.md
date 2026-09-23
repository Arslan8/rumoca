# FINDING-03097: Not yet established as a bug or a false positive

| Field | Value |
|---|---|
| Verdict | unresolved |
| Scope / group | baseline-blocked |
| Model | Modelica.Electrical.PowerConverters.Examples.ACDC.RectifierBridge2mPulse.ThyristorBridge2mPulse_DC_Drive |
| Target | SMains |
| Student classification | divisor-reachable-zero |
| Original report | [FINDING-thyristorbridge2mpulse-dc-drive-smains-divzero-2.md](../../v2/bugs/FINDING-thyristorbridge2mpulse-dc-drive-smains-divzero-2.md) — reviewed as `FINDING-03097-thyristorbridge2mpulse-dc-drive-smains.md`, which a later run renamed |
| Original SHA-256 | f87635edefb78c55cc2e1a5ab94c5099b97a054fb85d7edfbf22f6c2fa77df7c |

## What remains unresolved

The current Rumoca nominal run is tool-error, before any reported perturbation. This prevents causal attribution to this parameter. Source metadata was recovered, but none of the reviewed source proofs or counterexamples establishes this particular claim. A baseline failure/tool limitation is neither confirmation nor a false positive.

## Source evidence

Compiler/source-resolved declaration: `Electrical/PowerConverters/Examples/ACDC/RectifierBridge2mPulse/ThyristorBridge2mPulse_DC_Drive.mo:11`. Role: `parameter`; binding: `250000.0`; effective min: `None`; effective max: `None`. 

[Electrical/PowerConverters/Examples/ACDC/RectifierBridge2mPulse/ThyristorBridge2mPulse_DC_Drive.mo — source snapshot](../evidence/sources/d6dfee8541471ef8-ThyristorBridge2mPulse_DC_Drive.mo)

```modelica
9:     "RMS supply voltage";
10:   parameter SI.Frequency f=50 "Frequency";
11:   parameter SI.ApparentPower SMains=250E3
12:     "Mains short circuit apparent power";
13:   parameter Real lamdaMains=0.1 "Mains short circuit power factor";
14:   final parameter SI.Impedance ZMains=Vrms^2/SMains*m
```


## Execution evidence

[Rumoca commands, return codes, integrity hashes, bounded output and metadata](../evidence/d8e62ee37d41ac80.json). Baseline: **tool-error**.

No independent runtime override was executed for this target in this audit; this is not a pass.

## Recommended action

Resolve the intended parameter domain and enclosing equations; check inherited bounds, final/protected status, guards and aliases. Construct an otherwise-valid source-level witness, establish a clean baseline in a capable engine, then retranslate at the witness and compare with the runtime override. For equality claims use the actual partner value. Do not apply a blanket min>0 fix yet.

## Scope and limitations

A source-level verdict addresses the reported declaration/claim, not every possible connected system. Tests cover 0–0.5 seconds and are not a proof of long-run stability. Shared instances are not distinct root causes. A missing bound, timeout, compiler error or failed nominal run alone never counts as a verified bug or a false positive. Fixes are proposals; no library/compiler implementation was changed.

[Group and related reports](../groups/baseline-blocked.md) · [Index](../README.md)
