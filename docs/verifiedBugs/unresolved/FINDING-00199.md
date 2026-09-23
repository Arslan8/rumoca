# FINDING-00199: Not yet established as a bug or a false positive

| Field | Value |
|---|---|
| Verdict | unresolved |
| Scope / group | baseline-blocked |
| Model | Modelica.Electrical.Analog.Examples.CompareTransformers |
| Target | basicTransformer.L2 |
| Student classification | physical-domain-unenforced |
| Original report | [FINDING-comparetransformers-basictransformer-l2-intent.md](../../v2/bugs/FINDING-comparetransformers-basictransformer-l2-intent.md) — reviewed as `FINDING-00199-comparetransformers-basictransformer-l2.md`, which a later run renamed |
| Original SHA-256 | d1690852b37a5a66a282771613dfb21d0ba6435d8b55ee6958f95fa6f7e24a31 |

## What remains unresolved

The current Rumoca nominal run is tool-error, before any reported perturbation. This prevents causal attribution to this parameter. Source metadata was recovered, but none of the reviewed source proofs or counterexamples establishes this particular claim. A baseline failure/tool limitation is neither confirmation nor a false positive.

## Source evidence

Compiler/source-resolved declaration: `Electrical/Analog/Basic/Transformer.mo:5`. Role: `parameter`; binding: `L2`; effective min: `None`; effective max: `None`. 

[Electrical/Analog/Basic/Transformer.mo — source snapshot](../evidence/sources/952d12a1cba0ce9e-Transformer.mo)

```modelica
3:   extends Interfaces.TwoPort(i1(start=0),i2(start=0));
4:   parameter SI.Inductance L1(start=1) "Primary inductance";
5:   parameter SI.Inductance L2(start=1) "Secondary inductance";
6:   parameter SI.Inductance M(start=1) "Coupling inductance";
7:   Real dv "Difference between voltage drop over primary inductor and voltage drop over secondary inductor";
8: equation
```


## Execution evidence

[Rumoca commands, return codes, integrity hashes, bounded output and metadata](../evidence/ba392aa660731e79.json). Baseline: **tool-error**.

No independent runtime override was executed for this target in this audit; this is not a pass.

## Recommended action

Resolve the intended parameter domain and enclosing equations; check inherited bounds, final/protected status, guards and aliases. Construct an otherwise-valid source-level witness, establish a clean baseline in a capable engine, then retranslate at the witness and compare with the runtime override. For equality claims use the actual partner value. Do not apply a blanket min>0 fix yet.

## Scope and limitations

A source-level verdict addresses the reported declaration/claim, not every possible connected system. Tests cover 0–0.5 seconds and are not a proof of long-run stability. Shared instances are not distinct root causes. A missing bound, timeout, compiler error or failed nominal run alone never counts as a verified bug or a false positive. Fixes are proposals; no library/compiler implementation was changed.

[Group and related reports](../groups/baseline-blocked.md) · [Index](../README.md)
