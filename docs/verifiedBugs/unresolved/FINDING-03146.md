# FINDING-03146: Not yet established as a bug or a false positive

| Field | Value |
|---|---|
| Verdict | unresolved |
| Scope / group | baseline-blocked |
| Model | Modelica.Electrical.PowerConverters.Examples.ACDC.RectifierBridge2mPulse.ThyristorBridge2mPulse_RLV_Characteristic |
| Target | L |
| Student classification | physical-domain-unenforced |
| Original report | [FINDING-thyristorbridge2mpulse-rlv-characteristic-l-zerolimit.md](../../v2/bugs/FINDING-thyristorbridge2mpulse-rlv-characteristic-l-zerolimit.md) — reviewed as `FINDING-03146-thyristorbridge2mpulse-rlv-characteristic-l.md`, which a later run renamed |
| Original SHA-256 | 80011587421d72bd10567d2d227bb4c4706b90c1934a4fc78ca3427c2afffd74 |

## What remains unresolved

The current Rumoca nominal run is tool-error, before any reported perturbation. This prevents causal attribution to this parameter. Source metadata was recovered, but none of the reviewed source proofs or counterexamples establishes this particular claim. A baseline failure/tool limitation is neither confirmation nor a false positive.

## Source evidence

Compiler/source-resolved declaration: `Electrical/PowerConverters/Examples/ACDC/RectifierBridge2mPulse/ThyristorBridge2mPulse_RLV_Characteristic.mo:12`. Role: `parameter`; binding: `1`; effective min: `None`; effective max: `None`. 

[Electrical/PowerConverters/Examples/ACDC/RectifierBridge2mPulse/ThyristorBridge2mPulse_RLV_Characteristic.mo — source snapshot](../evidence/sources/3ebe2b5a97e55da9-ThyristorBridge2mPulse_RLV_Characteristic.mo)

```modelica
10:     "Ideal max. DC voltage";
11:   parameter SI.Resistance R=20 "Load resistance";
12:   parameter SI.Inductance L=1 "Load resistance"
13:     annotation (Evaluate=true);
14:   parameter SI.Voltage VDC=-260 "DC load offset voltage";
15:   Modelica.Electrical.Analog.Basic.Resistor resistor(R=R) annotation (
```


## Execution evidence

[Rumoca commands, return codes, integrity hashes, bounded output and metadata](../evidence/af0a11dcd533810e.json). Baseline: **tool-error**.

No independent runtime override was executed for this target in this audit; this is not a pass.

## Recommended action

Resolve the intended parameter domain and enclosing equations; check inherited bounds, final/protected status, guards and aliases. Construct an otherwise-valid source-level witness, establish a clean baseline in a capable engine, then retranslate at the witness and compare with the runtime override. For equality claims use the actual partner value. Do not apply a blanket min>0 fix yet.

## Scope and limitations

A source-level verdict addresses the reported declaration/claim, not every possible connected system. Tests cover 0–0.5 seconds and are not a proof of long-run stability. Shared instances are not distinct root causes. A missing bound, timeout, compiler error or failed nominal run alone never counts as a verified bug or a false positive. Fixes are proposals; no library/compiler implementation was changed.

[Group and related reports](../groups/baseline-blocked.md) · [Index](../README.md)
