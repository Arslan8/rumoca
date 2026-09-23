# FINDING-02965: Not yet established as a bug or a false positive

| Field | Value |
|---|---|
| Verdict | unresolved |
| Scope / group | baseline-blocked |
| Model | Modelica.Electrical.Polyphase.Examples.TransformerYD |
| Target | Lm |
| Student classification | physical-domain-unenforced |
| Original report | [FINDING-transformeryd-lm-intent.md](../../v2/bugs/FINDING-transformeryd-lm-intent.md) — reviewed as `FINDING-02965-transformeryd-lm.md`, which a later run renamed |
| Original SHA-256 | 42b81af8c47f8891ab0c411eeb9ceb51e98e2f52f0abc474545b1b51e4403ecc |

## What remains unresolved

The current Rumoca nominal run is tool-error, before any reported perturbation. This prevents causal attribution to this parameter. Source metadata was recovered, but none of the reviewed source proofs or counterexamples establishes this particular claim. A baseline failure/tool limitation is neither confirmation nor a false positive.

## Source evidence

Compiler/source-resolved declaration: `Electrical/Polyphase/Examples/TransformerYD.mo:7`. Role: `parameter`; binding: `1`; effective min: `None`; effective max: `None`. 

[Electrical/Polyphase/Examples/TransformerYD.mo — source snapshot](../evidence/sources/53d01f69abffa983-TransformerYD.mo)

```modelica
5:   parameter SI.Voltage V=1 "Amplitude of Star-Voltage";
6:   parameter SI.Frequency f=5 "Frequency";
7:   parameter SI.Inductance Lm=1 "Transformer main inductance";
8:   parameter SI.Inductance LT=0.003
9:     "Transformer stray inductance";
10:   parameter SI.Resistance RT=0.05 "Transformer resistance";
```


## Execution evidence

[Rumoca commands, return codes, integrity hashes, bounded output and metadata](../evidence/cd732620e9124b88.json). Baseline: **tool-error**.

No independent runtime override was executed for this target in this audit; this is not a pass.

## Recommended action

Resolve the intended parameter domain and enclosing equations; check inherited bounds, final/protected status, guards and aliases. Construct an otherwise-valid source-level witness, establish a clean baseline in a capable engine, then retranslate at the witness and compare with the runtime override. For equality claims use the actual partner value. Do not apply a blanket min>0 fix yet.

## Scope and limitations

A source-level verdict addresses the reported declaration/claim, not every possible connected system. Tests cover 0–0.5 seconds and are not a proof of long-run stability. Shared instances are not distinct root causes. A missing bound, timeout, compiler error or failed nominal run alone never counts as a verified bug or a false positive. Fixes are proposals; no library/compiler implementation was changed.

[Group and related reports](../groups/baseline-blocked.md) · [Index](../README.md)
