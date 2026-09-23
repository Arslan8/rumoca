# FINDING-03054: Not yet established as a bug or a false positive

| Field | Value |
|---|---|
| Verdict | unresolved |
| Scope / group | baseline-blocked |
| Model | Modelica.Electrical.PowerConverters.Examples.ACDC.RectifierBridge2mPulse.ThyristorBridge2mPulse_DC_Drive |
| Target | Ld |
| Student classification | physical-domain-unenforced |
| Original report | [FINDING-thyristorbridge2mpulse-dc-drive-ld-zerolimit.md](../../v2/bugs/FINDING-thyristorbridge2mpulse-dc-drive-ld-zerolimit.md) — reviewed as `FINDING-03054-thyristorbridge2mpulse-dc-drive-ld.md`, which a later run renamed |
| Original SHA-256 | 3612aac4818c5b943c8f2be09b45ea26376c5519fcb437e24f15dcf11ea2f4e3 |

## What remains unresolved

The current Rumoca nominal run is tool-error, before any reported perturbation. This prevents causal attribution to this parameter. Source metadata was recovered, but none of the reviewed source proofs or counterexamples establishes this particular claim. A baseline failure/tool limitation is neither confirmation nor a false positive.

## Source evidence

Compiler/source-resolved declaration: `Electrical/PowerConverters/Examples/ACDC/RectifierBridge2mPulse/ThyristorBridge2mPulse_DC_Drive.mo:21`. Role: `parameter`; binding: `(3 * dcpmData.La)`; effective min: `None`; effective max: `None`. 

[Electrical/PowerConverters/Examples/ACDC/RectifierBridge2mPulse/ThyristorBridge2mPulse_DC_Drive.mo — source snapshot](../evidence/sources/d6dfee8541471ef8-ThyristorBridge2mPulse_DC_Drive.mo)

```modelica
19:       lamdaMains^2)/(2*pi*f) "Mains inductance"
20:     annotation (Evaluate=true);
21:   parameter SI.Inductance Ld=3*dcpmData.La
22:     "Smoothing inductance" annotation (Evaluate=true);
23:   final parameter SI.Torque tauNominal=dcpmData.ViNominal
24:       *dcpmData.IaNominal/dcpmData.wNominal "Nominal torque";
```


## Execution evidence

[Rumoca commands, return codes, integrity hashes, bounded output and metadata](../evidence/d8e62ee37d41ac80.json). Baseline: **tool-error**.

No independent runtime override was executed for this target in this audit; this is not a pass.

## Recommended action

Resolve the intended parameter domain and enclosing equations; check inherited bounds, final/protected status, guards and aliases. Construct an otherwise-valid source-level witness, establish a clean baseline in a capable engine, then retranslate at the witness and compare with the runtime override. For equality claims use the actual partner value. Do not apply a blanket min>0 fix yet.

## Scope and limitations

A source-level verdict addresses the reported declaration/claim, not every possible connected system. Tests cover 0–0.5 seconds and are not a proof of long-run stability. Shared instances are not distinct root causes. A missing bound, timeout, compiler error or failed nominal run alone never counts as a verified bug or a false positive. Fixes are proposals; no library/compiler implementation was changed.

[Group and related reports](../groups/baseline-blocked.md) · [Index](../README.md)
