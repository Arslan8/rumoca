# FINDING-00201: Not yet established as a bug or a false positive

| Field | Value |
|---|---|
| Verdict | unresolved |
| Scope / group | baseline-blocked |
| Model | Modelica.Electrical.Analog.Examples.CompareTransformers |
| Target | idealTransformer.Lm1 |
| Student classification | physical-domain-unenforced |
| Original report | [FINDING-comparetransformers-idealtransformer-lm1-intent.md](../../v2/bugs/FINDING-comparetransformers-idealtransformer-lm1-intent.md) — reviewed as `FINDING-00201-comparetransformers-idealtransformer-lm1.md`, which a later run renamed |
| Original SHA-256 | 754c7b5db100732ec799edc6ff6bdcfe21fe3be7fa15470cc2dd724fb231658e |

## What remains unresolved

The current Rumoca nominal run is tool-error, before any reported perturbation. This prevents causal attribution to this parameter. Source metadata was recovered, but none of the reviewed source proofs or counterexamples establishes this particular claim. A baseline failure/tool limitation is neither confirmation nor a false positive.

## Source evidence

Compiler/source-resolved declaration: `Electrical/Analog/Ideal/IdealTransformer.mo:7`. Role: `parameter`; binding: `Lm1`; effective min: `None`; effective max: `None`. 

[Electrical/Analog/Ideal/IdealTransformer.mo — source snapshot](../evidence/sources/a5bbe8e9c0cad68c-IdealTransformer.mo)

```modelica
5:   parameter Boolean considerMagnetization=false
6:     "Choice of considering magnetization" annotation(Evaluate = true);
7:   parameter SI.Inductance Lm1(start=1)
8:     "Magnetization inductance w.r.t. primary side"
9:     annotation (Dialog(enable=considerMagnetization));
10: protected
```


## Execution evidence

[Rumoca commands, return codes, integrity hashes, bounded output and metadata](../evidence/ba392aa660731e79.json). Baseline: **tool-error**.

No independent runtime override was executed for this target in this audit; this is not a pass.

## Recommended action

Resolve the intended parameter domain and enclosing equations; check inherited bounds, final/protected status, guards and aliases. Construct an otherwise-valid source-level witness, establish a clean baseline in a capable engine, then retranslate at the witness and compare with the runtime override. For equality claims use the actual partner value. Do not apply a blanket min>0 fix yet.

## Scope and limitations

A source-level verdict addresses the reported declaration/claim, not every possible connected system. Tests cover 0–0.5 seconds and are not a proof of long-run stability. Shared instances are not distinct root causes. A missing bound, timeout, compiler error or failed nominal run alone never counts as a verified bug or a false positive. Fixes are proposals; no library/compiler implementation was changed.

[Group and related reports](../groups/baseline-blocked.md) · [Index](../README.md)
