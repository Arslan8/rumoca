# FINDING-01037: Not yet established as a bug or a false positive

| Field | Value |
|---|---|
| Verdict | unresolved |
| Scope / group | baseline-blocked |
| Model | Modelica.Electrical.Analog.Examples.ThyristorBehaviourTest |
| Target | thyristor_v4_1.IGT |
| Student classification | divisor-reachable-zero |
| Original report | [FINDING-thyristorbehaviourtest-thyristor-v4-1-igt-divunresolved-2.md](../../v2/bugs/FINDING-thyristorbehaviourtest-thyristor-v4-1-igt-divunresolved-2.md) — reviewed as `FINDING-01037-thyristorbehaviourtest-thyristor-v4-1-igt.md`, which a later run renamed |
| Original SHA-256 | d59c05d7fe0301396832c36a830bd5528b914970b12dd939199145432b68ba82 |

## What remains unresolved

The current Rumoca nominal run is tool-error, before any reported perturbation. This prevents causal attribution to this parameter. Source metadata was recovered, but none of the reviewed source proofs or counterexamples establishes this particular claim. A baseline failure/tool limitation is neither confirmation nor a false positive.

## Source evidence

Compiler/source-resolved declaration: `Electrical/Analog/Semiconductors/Thyristor.mo:13`. Role: `parameter`; binding: `0.005`; effective min: `None`; effective max: `None`. 

[Electrical/Analog/Semiconductors/Thyristor.mo — source snapshot](../evidence/sources/dbc15414032e03ee-Thyristor.mo)

```modelica
11: 
12:   parameter SI.Voltage VGT= 0.7 "Gate trigger voltage";
13:   parameter SI.Current IGT= 5e-3 "Gate trigger current";
14: 
15:   parameter SI.Time TON = 1e-6 "Switch on time";
16:   parameter SI.Time TOFF = 15e-6 "Switch off time";
```


## Execution evidence

[Rumoca commands, return codes, integrity hashes, bounded output and metadata](../evidence/f2dc7c4a18bb2bd2.json). Baseline: **tool-error**.

No independent runtime override was executed for this target in this audit; this is not a pass.

## Recommended action

Resolve the intended parameter domain and enclosing equations; check inherited bounds, final/protected status, guards and aliases. Construct an otherwise-valid source-level witness, establish a clean baseline in a capable engine, then retranslate at the witness and compare with the runtime override. For equality claims use the actual partner value. Do not apply a blanket min>0 fix yet.

## Scope and limitations

A source-level verdict addresses the reported declaration/claim, not every possible connected system. Tests cover 0–0.5 seconds and are not a proof of long-run stability. Shared instances are not distinct root causes. A missing bound, timeout, compiler error or failed nominal run alone never counts as a verified bug or a false positive. Fixes are proposals; no library/compiler implementation was changed.

[Group and related reports](../groups/baseline-blocked.md) · [Index](../README.md)
