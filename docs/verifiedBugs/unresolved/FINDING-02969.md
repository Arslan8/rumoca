# FINDING-02969: Not yet established as a bug or a false positive

| Field | Value |
|---|---|
| Verdict | unresolved |
| Scope / group | baseline-blocked |
| Model | Modelica.Electrical.Polyphase.Examples.TransformerYD |
| Target | idealTransformer.Lm1 |
| Student classification | physical-domain-unenforced |
| Original report | [FINDING-transformeryd-idealtransformer-lm1-intent.md](../../v2/bugs/FINDING-transformeryd-idealtransformer-lm1-intent.md) — reviewed as `FINDING-02969-transformeryd-idealtransformer-lm1.md`, which a later run renamed |
| Original SHA-256 | 4f4875331cc13e37b7e91cf954bb1a415560bfea19539c7c7e264e1c333e09de |

## What remains unresolved

The current Rumoca nominal run is tool-error, before any reported perturbation. This prevents causal attribution to this parameter. Source metadata was recovered, but none of the reviewed source proofs or counterexamples establishes this particular claim. A baseline failure/tool limitation is neither confirmation nor a false positive.

## Source evidence

Compiler/source-resolved declaration: `Electrical/Polyphase/Ideal/IdealTransformer.mo:7`. Role: `parameter`; binding: `fill(Lm, m)`; effective min: `None`; effective max: `None`. 

[Electrical/Polyphase/Ideal/IdealTransformer.mo — source snapshot](../evidence/sources/4cb00668938c5c75-IdealTransformer.mo)

```modelica
5:   parameter Boolean considerMagnetization=false
6:     "Choice of considering magnetization";
7:   parameter SI.Inductance Lm1[m](start=fill(1, m))
8:     "Magnetization inductances w.r.t. primary side";
9:   Modelica.Electrical.Analog.Ideal.IdealTransformer idealTransformer[m](
10:     final n=n,
```


## Execution evidence

[Rumoca commands, return codes, integrity hashes, bounded output and metadata](../evidence/cd732620e9124b88.json). Baseline: **tool-error**.

No independent runtime override was executed for this target in this audit; this is not a pass.

## Recommended action

Resolve the intended parameter domain and enclosing equations; check inherited bounds, final/protected status, guards and aliases. Construct an otherwise-valid source-level witness, establish a clean baseline in a capable engine, then retranslate at the witness and compare with the runtime override. For equality claims use the actual partner value. Do not apply a blanket min>0 fix yet.

## Scope and limitations

A source-level verdict addresses the reported declaration/claim, not every possible connected system. Tests cover 0–0.5 seconds and are not a proof of long-run stability. Shared instances are not distinct root causes. A missing bound, timeout, compiler error or failed nominal run alone never counts as a verified bug or a false positive. Fixes are proposals; no library/compiler implementation was changed.

[Group and related reports](../groups/baseline-blocked.md) · [Index](../README.md)
