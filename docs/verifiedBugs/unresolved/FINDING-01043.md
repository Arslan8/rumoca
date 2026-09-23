# FINDING-01043: Not yet established as a bug or a false positive

| Field | Value |
|---|---|
| Verdict | unresolved |
| Scope / group | baseline-blocked |
| Model | Modelica.Electrical.Analog.Examples.ThyristorBehaviourTest |
| Target | thyristor_v4_1.IH |
| Student classification | divisor-reachable-zero |
| Original report | [FINDING-thyristorbehaviourtest-thyristor-v4-1-ih-divzero-2.md](../../v2/bugs/FINDING-thyristorbehaviourtest-thyristor-v4-1-ih-divzero-2.md) — reviewed as `FINDING-01043-thyristorbehaviourtest-thyristor-v4-1-ih.md`, which a later run renamed |
| Original SHA-256 | 9b9df5d90418377bc2e7c2fe0f874544c9fff5bf763a04e66e9b48a73a32953d |

## What remains unresolved

The current Rumoca nominal run is tool-error, before any reported perturbation. This prevents causal attribution to this parameter. Source metadata was recovered, but none of the reviewed source proofs or counterexamples establishes this particular claim. A baseline failure/tool limitation is neither confirmation nor a false positive.

## Source evidence

Compiler/source-resolved declaration: `Electrical/Analog/Semiconductors/Thyristor.mo:9`. Role: `parameter`; binding: `0.006`; effective min: `None`; effective max: `None`. 

[Electrical/Analog/Semiconductors/Thyristor.mo — source snapshot](../evidence/sources/dbc15414032e03ee-Thyristor.mo)

```modelica
7:   parameter SI.Current IDRM=0.1 "Saturation current";
8:   parameter SI.Voltage VTM= 1.7 "Conducting voltage";
9:   parameter SI.Current IH=6e-3 "Holding current";
10:   parameter SI.Current ITM= 25 "Conducting current";
11: 
12:   parameter SI.Voltage VGT= 0.7 "Gate trigger voltage";
```


## Execution evidence

[Rumoca commands, return codes, integrity hashes, bounded output and metadata](../evidence/f2dc7c4a18bb2bd2.json). Baseline: **tool-error**.

No independent runtime override was executed for this target in this audit; this is not a pass.

## Recommended action

Resolve the intended parameter domain and enclosing equations; check inherited bounds, final/protected status, guards and aliases. Construct an otherwise-valid source-level witness, establish a clean baseline in a capable engine, then retranslate at the witness and compare with the runtime override. For equality claims use the actual partner value. Do not apply a blanket min>0 fix yet.

## Scope and limitations

A source-level verdict addresses the reported declaration/claim, not every possible connected system. Tests cover 0–0.5 seconds and are not a proof of long-run stability. Shared instances are not distinct root causes. A missing bound, timeout, compiler error or failed nominal run alone never counts as a verified bug or a false positive. Fixes are proposals; no library/compiler implementation was changed.

[Group and related reports](../groups/baseline-blocked.md) · [Index](../README.md)
