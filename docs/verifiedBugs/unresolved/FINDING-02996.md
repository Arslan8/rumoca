# FINDING-02996: Not yet established as a bug or a false positive

| Field | Value |
|---|---|
| Verdict | unresolved |
| Scope / group | baseline-blocked |
| Model | Modelica.Electrical.Polyphase.Examples.TransformerYY |
| Target | nT |
| Student classification | divisor-reachable-zero |
| Original report | `FINDING-02996-transformeryy-nt.md` — [withdrawn](../../v2/bugs/withdrawn.md); a later run no longer makes this claim |
| Original SHA-256 | 232013c17b9a94c44170a6fa3d4bfe44969bf7890d275b45846c0d3a9e0fa6a0 |

## What remains unresolved

The current Rumoca nominal run is tool-error, before any reported perturbation. This prevents causal attribution to this parameter. Source metadata was recovered, but none of the reviewed source proofs or counterexamples establishes this particular claim. A baseline failure/tool limitation is neither confirmation nor a false positive.

## Source evidence

Compiler/source-resolved declaration: `Electrical/Polyphase/Examples/TransformerYY.mo:12`. Role: `parameter`; binding: `1`; effective min: `None`; effective max: `None`. 

[Electrical/Polyphase/Examples/TransformerYY.mo — source snapshot](../evidence/sources/9f59ff1cc167961b-TransformerYY.mo)

```modelica
10:   parameter SI.Resistance RT=0.05 "Transformer resistance";
11:   parameter SI.Resistance RL=1 "Load Resistance";
12:   parameter Real nT=1 "Transformer ratio";
13:   Sources.SineVoltage sineVoltage(
14:     V=fill(V, m),
15:     f=fill(f, m),
```


## Execution evidence

[Rumoca commands, return codes, integrity hashes, bounded output and metadata](../evidence/6c48332d26bb37af.json). Baseline: **tool-error**.

No independent runtime override was executed for this target in this audit; this is not a pass.

## Recommended action

Resolve the intended parameter domain and enclosing equations; check inherited bounds, final/protected status, guards and aliases. Construct an otherwise-valid source-level witness, establish a clean baseline in a capable engine, then retranslate at the witness and compare with the runtime override. For equality claims use the actual partner value. Do not apply a blanket min>0 fix yet.

## Scope and limitations

A source-level verdict addresses the reported declaration/claim, not every possible connected system. Tests cover 0–0.5 seconds and are not a proof of long-run stability. Shared instances are not distinct root causes. A missing bound, timeout, compiler error or failed nominal run alone never counts as a verified bug or a false positive. Fixes are proposals; no library/compiler implementation was changed.

[Group and related reports](../groups/baseline-blocked.md) · [Index](../README.md)
