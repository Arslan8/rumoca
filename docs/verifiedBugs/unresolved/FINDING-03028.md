# FINDING-03028: Not yet established as a bug or a false positive

| Field | Value |
|---|---|
| Verdict | unresolved |
| Scope / group | baseline-blocked |
| Model | Modelica.Electrical.PowerConverters.Examples.ACDC.RectifierBridge2mPulse.HalfControlledBridge2mPulse |
| Target | rectifier.RonThyristor |
| Student classification | physical-bound-permits-zero |
| Original report | [FINDING-halfcontrolledbridge2mpulse-rectifier-ronthyristor-ruleoff.md](../../v2/bugs/FINDING-halfcontrolledbridge2mpulse-rectifier-ronthyristor-ruleoff.md) — reviewed as `FINDING-03028-halfcontrolledbridge2mpulse-rectifier-ronthyristor.md`, which a later run renamed |
| Original SHA-256 | 06b66a25bcc824e239796c26644547ee7af11d5aa74fae296eed48771c8be433 |

## What remains unresolved

The current Rumoca nominal run is tool-error, before any reported perturbation. This prevents causal attribution to this parameter. Source metadata was recovered, but none of the reviewed source proofs or counterexamples establishes this particular claim. A baseline failure/tool limitation is neither confirmation nor a false positive.

## Source evidence

Compiler/source-resolved declaration: `Electrical/PowerConverters/ACDC/HalfControlledBridge2mPulse.mo:13`. Role: `parameter`; binding: `1e-05`; effective min: `0`; effective max: `None`. 

[Electrical/PowerConverters/ACDC/HalfControlledBridge2mPulse.mo — source snapshot](../evidence/sources/3a5118c17e7bc544-HalfControlledBridge2mPulse.mo)

```modelica
11:   parameter SI.Voltage VkneeDiode(final min=0) = 0
12:     "Diode forward threshold voltage";
13:   parameter SI.Resistance RonThyristor(final min=0) = 1e-05
14:     "Closed thyristor resistance";
15:   parameter SI.Conductance GoffThyristor(final min=0) = 1e-05
16:     "Opened thyristor conductance";
```


## Execution evidence

[Rumoca commands, return codes, integrity hashes, bounded output and metadata](../evidence/a54fb2c8ac8f1d80.json). Baseline: **tool-error**.

No independent runtime override was executed for this target in this audit; this is not a pass.

## Recommended action

Resolve the intended parameter domain and enclosing equations; check inherited bounds, final/protected status, guards and aliases. Construct an otherwise-valid source-level witness, establish a clean baseline in a capable engine, then retranslate at the witness and compare with the runtime override. For equality claims use the actual partner value. Do not apply a blanket min>0 fix yet.

## Scope and limitations

A source-level verdict addresses the reported declaration/claim, not every possible connected system. Tests cover 0–0.5 seconds and are not a proof of long-run stability. Shared instances are not distinct root causes. A missing bound, timeout, compiler error or failed nominal run alone never counts as a verified bug or a false positive. Fixes are proposals; no library/compiler implementation was changed.

[Group and related reports](../groups/baseline-blocked.md) · [Index](../README.md)
