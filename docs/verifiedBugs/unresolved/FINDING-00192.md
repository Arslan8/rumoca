# FINDING-00192: Not yet established as a bug or a false positive

| Field | Value |
|---|---|
| Verdict | unresolved |
| Scope / group | baseline-blocked |
| Model | Modelica.Electrical.Analog.Examples.CompareTransformers |
| Target | RL |
| Student classification | physical-domain-unenforced |
| Original report | [FINDING-comparetransformers-rl-zerolimit.md](../../v2/bugs/FINDING-comparetransformers-rl-zerolimit.md) — reviewed as `FINDING-00192-comparetransformers-rl.md`, which a later run renamed |
| Original SHA-256 | 8a97f64e07efb6780a5d53a33192b71a17afa6f8e5f943efae71b32ec812534a |

## What remains unresolved

The current Rumoca nominal run is tool-error, before any reported perturbation. This prevents causal attribution to this parameter. Source metadata was recovered, but none of the reviewed source proofs or counterexamples establishes this particular claim. A baseline failure/tool limitation is neither confirmation nor a false positive.

## Source evidence

Compiler/source-resolved declaration: `Electrical/Analog/Examples/CompareTransformers.mo:21`. Role: `parameter`; binding: `(1 / (n ^ 2))`; effective min: `None`; effective max: `None`. 

[Electrical/Analog/Examples/CompareTransformers.mo — source snapshot](../evidence/sources/d966c9a4658ed8b4-CompareTransformers.mo)

```modelica
19:   parameter SI.Resistance R2=0.01/n^2
20:     "Secondary resistance w.r.t. secondary side";
21:   parameter SI.Resistance RL=1/n^2 "Load resistance";
22:   final parameter SI.Inductance L1=L1sigma + M*n
23:     "Primary no-load inductance";
24:   final parameter SI.Inductance L2=L2sigma + M/n
```


## Execution evidence

[Rumoca commands, return codes, integrity hashes, bounded output and metadata](../evidence/ba392aa660731e79.json). Baseline: **tool-error**.

No independent runtime override was executed for this target in this audit; this is not a pass.

## Recommended action

Resolve the intended parameter domain and enclosing equations; check inherited bounds, final/protected status, guards and aliases. Construct an otherwise-valid source-level witness, establish a clean baseline in a capable engine, then retranslate at the witness and compare with the runtime override. For equality claims use the actual partner value. Do not apply a blanket min>0 fix yet.

## Scope and limitations

A source-level verdict addresses the reported declaration/claim, not every possible connected system. Tests cover 0–0.5 seconds and are not a proof of long-run stability. Shared instances are not distinct root causes. A missing bound, timeout, compiler error or failed nominal run alone never counts as a verified bug or a false positive. Fixes are proposals; no library/compiler implementation was changed.

[Group and related reports](../groups/baseline-blocked.md) · [Index](../README.md)
