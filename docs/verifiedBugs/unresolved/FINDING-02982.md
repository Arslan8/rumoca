# FINDING-02982: Not yet established as a bug or a false positive

| Field | Value |
|---|---|
| Verdict | unresolved |
| Scope / group | baseline-blocked |
| Model | Modelica.Electrical.Polyphase.Examples.TransformerYY |
| Target | LT |
| Student classification | physical-domain-unenforced |
| Original report | [FINDING-transformeryy-lt-zerolimit.md](../../v2/bugs/FINDING-transformeryy-lt-zerolimit.md) — reviewed as `FINDING-02982-transformeryy-lt.md`, which a later run renamed |
| Original SHA-256 | 08d5301840a718e541292cd2ecfb2002945bb0f95a86428227e647802a43d271 |

## What remains unresolved

The current Rumoca nominal run is tool-error, before any reported perturbation. This prevents causal attribution to this parameter. Source metadata was recovered, but none of the reviewed source proofs or counterexamples establishes this particular claim. A baseline failure/tool limitation is neither confirmation nor a false positive.

## Source evidence

Compiler/source-resolved declaration: `Electrical/Polyphase/Examples/TransformerYY.mo:8`. Role: `parameter`; binding: `0.003`; effective min: `None`; effective max: `None`. 

[Electrical/Polyphase/Examples/TransformerYY.mo — source snapshot](../evidence/sources/9f59ff1cc167961b-TransformerYY.mo)

```modelica
6:   parameter SI.Frequency f=5 "Frequency";
7:   parameter SI.Inductance Lm=1 "Transformer main inductance";
8:   parameter SI.Inductance LT=0.003
9:     "Transformer stray inductance";
10:   parameter SI.Resistance RT=0.05 "Transformer resistance";
11:   parameter SI.Resistance RL=1 "Load Resistance";
```


## Execution evidence

[Rumoca commands, return codes, integrity hashes, bounded output and metadata](../evidence/6c48332d26bb37af.json). Baseline: **tool-error**.

No independent runtime override was executed for this target in this audit; this is not a pass.

## Recommended action

Resolve the intended parameter domain and enclosing equations; check inherited bounds, final/protected status, guards and aliases. Construct an otherwise-valid source-level witness, establish a clean baseline in a capable engine, then retranslate at the witness and compare with the runtime override. For equality claims use the actual partner value. Do not apply a blanket min>0 fix yet.

## Scope and limitations

A source-level verdict addresses the reported declaration/claim, not every possible connected system. Tests cover 0–0.5 seconds and are not a proof of long-run stability. Shared instances are not distinct root causes. A missing bound, timeout, compiler error or failed nominal run alone never counts as a verified bug or a false positive. Fixes are proposals; no library/compiler implementation was changed.

[Group and related reports](../groups/baseline-blocked.md) · [Index](../README.md)
