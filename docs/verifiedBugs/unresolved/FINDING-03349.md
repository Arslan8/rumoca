# FINDING-03349: Not yet established as a bug or a false positive

| Field | Value |
|---|---|
| Verdict | unresolved |
| Scope / group | baseline-blocked |
| Model | Modelica.Electrical.PowerConverters.Examples.ACDC.RectifierCenterTap2mPulse.ThyristorCenterTap2mPulse_RLV_Characteristic |
| Target | rectifier.GoffThyristor |
| Student classification | physical-bound-permits-zero |
| Original report | [FINDING-thyristorcentertap2mpulse-rlv-characteristic-rectifier-goffthyristor-r.md](../../v2/bugs/FINDING-thyristorcentertap2mpulse-rlv-characteristic-rectifier-goffthyristor-r.md) — reviewed as `FINDING-03349-thyristorcentertap2mpulse-rlv-characteristic-rectifier-goffthyristor.md`, which a later run renamed |
| Original SHA-256 | fe19f5a484dafb5aa2d55b06f78528c9dd812912f81713f4b350e7224b15b917 |

## What remains unresolved

The current Rumoca nominal run is tool-error, before any reported perturbation. This prevents causal attribution to this parameter. Source metadata was recovered, but none of the reviewed source proofs or counterexamples establishes this particular claim. A baseline failure/tool limitation is neither confirmation nor a false positive.

## Source evidence

Compiler/source-resolved declaration: `Electrical/PowerConverters/ACDC/ThyristorCenterTap2mPulse.mo:9`. Role: `parameter`; binding: `1e-05`; effective min: `0`; effective max: `None`. 

[Electrical/PowerConverters/ACDC/ThyristorCenterTap2mPulse.mo — source snapshot](../evidence/sources/28d232291cd240b9-ThyristorCenterTap2mPulse.mo)

```modelica
7:   parameter SI.Resistance RonThyristor(final min=0) = 1e-05
8:     "Closed thyristor resistance";
9:   parameter SI.Conductance GoffThyristor(final min=0) = 1e-05
10:     "Opened thyristor conductance";
11:   parameter SI.Voltage VkneeThyristor(final min=0) = 0
12:     "Thyristor forward threshold voltage";
```


## Execution evidence

[Rumoca commands, return codes, integrity hashes, bounded output and metadata](../evidence/a43926ff56fe6156.json). Baseline: **tool-error**.

No independent runtime override was executed for this target in this audit; this is not a pass.

## Recommended action

Resolve the intended parameter domain and enclosing equations; check inherited bounds, final/protected status, guards and aliases. Construct an otherwise-valid source-level witness, establish a clean baseline in a capable engine, then retranslate at the witness and compare with the runtime override. For equality claims use the actual partner value. Do not apply a blanket min>0 fix yet.

## Scope and limitations

A source-level verdict addresses the reported declaration/claim, not every possible connected system. Tests cover 0–0.5 seconds and are not a proof of long-run stability. Shared instances are not distinct root causes. A missing bound, timeout, compiler error or failed nominal run alone never counts as a verified bug or a false positive. Fixes are proposals; no library/compiler implementation was changed.

[Group and related reports](../groups/baseline-blocked.md) · [Index](../README.md)
