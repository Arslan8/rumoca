# FINDING-00195: Not yet established as a bug or a false positive

| Field | Value |
|---|---|
| Verdict | unresolved |
| Scope / group | baseline-blocked |
| Model | Modelica.Electrical.Analog.Examples.CompareTransformers |
| Target | M |
| Student classification | physical-domain-unenforced |
| Original report | [FINDING-comparetransformers-m-zerolimit.md](../../v2/bugs/FINDING-comparetransformers-m-zerolimit.md) — reviewed as `FINDING-00195-comparetransformers-m.md`, which a later run renamed |
| Original SHA-256 | b1777b39790f4ea1f82b43cf6ea16f96b0ab0430e52271bc0c41a0fec222209d |

## What remains unresolved

The current Rumoca nominal run is tool-error, before any reported perturbation. This prevents causal attribution to this parameter. Source metadata was recovered, but none of the reviewed source proofs or counterexamples establishes this particular claim. A baseline failure/tool limitation is neither confirmation nor a false positive.

## Source evidence

Compiler/source-resolved declaration: `Electrical/Analog/Examples/CompareTransformers.mo:26`. Role: `parameter`; binding: `(Lm1 / n)`; effective min: `None`; effective max: `None`. 

[Electrical/Analog/Examples/CompareTransformers.mo — source snapshot](../evidence/sources/d966c9a4658ed8b4-CompareTransformers.mo)

```modelica
24:   final parameter SI.Inductance L2=L2sigma + M/n
25:     "Secondary no-load inductance";
26:   final parameter SI.Inductance M=Lm1/n "Mutual inductance";
27:   output SI.Voltage v1B = resistor11.n.v
28:     "Primary voltage, basic transformer";
29:   output SI.Current i1B = resistor11.i
```


## Execution evidence

[Rumoca commands, return codes, integrity hashes, bounded output and metadata](../evidence/ba392aa660731e79.json). Baseline: **tool-error**.

No independent runtime override was executed for this target in this audit; this is not a pass.

## Recommended action

Resolve the intended parameter domain and enclosing equations; check inherited bounds, final/protected status, guards and aliases. Construct an otherwise-valid source-level witness, establish a clean baseline in a capable engine, then retranslate at the witness and compare with the runtime override. For equality claims use the actual partner value. Do not apply a blanket min>0 fix yet.

## Scope and limitations

A source-level verdict addresses the reported declaration/claim, not every possible connected system. Tests cover 0–0.5 seconds and are not a proof of long-run stability. Shared instances are not distinct root causes. A missing bound, timeout, compiler error or failed nominal run alone never counts as a verified bug or a false positive. Fixes are proposals; no library/compiler implementation was changed.

[Group and related reports](../groups/baseline-blocked.md) · [Index](../README.md)
