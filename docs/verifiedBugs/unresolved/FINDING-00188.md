# FINDING-00188: Not yet established as a bug or a false positive

| Field | Value |
|---|---|
| Verdict | unresolved |
| Scope / group | baseline-blocked |
| Model | Modelica.Electrical.Analog.Examples.CompareTransformers |
| Target | L1sigma |
| Student classification | physical-domain-unenforced |
| Original report | [FINDING-comparetransformers-l1sigma-intent.md](../../v2/bugs/FINDING-comparetransformers-l1sigma-intent.md) — reviewed as `FINDING-00188-comparetransformers-l1sigma.md`, which a later run renamed |
| Original SHA-256 | 4140d7a3c012d212a3a9439df7f21db578d47061afcbadc670fe5e58a7797b7c |

## What remains unresolved

The current Rumoca nominal run is tool-error, before any reported perturbation. This prevents causal attribution to this parameter. Source metadata was recovered, but none of the reviewed source proofs or counterexamples establishes this particular claim. A baseline failure/tool limitation is neither confirmation nor a false positive.

## Source evidence

Compiler/source-resolved declaration: `Electrical/Analog/Examples/CompareTransformers.mo:13`. Role: `parameter`; binding: `(0.05 / ((2 * (2 * asin(1.0))) * f))`; effective min: `None`; effective max: `None`. 

[Electrical/Analog/Examples/CompareTransformers.mo — source snapshot](../evidence/sources/d966c9a4658ed8b4-CompareTransformers.mo)

```modelica
11:   parameter SI.Resistance R1=0.01
12:     "Primary resistance w.r.t. primary side";
13:   parameter SI.Inductance L1sigma=0.05/(2*pi*f)
14:     "Primary leakage inductance w.r.t. primary side";
15:   parameter SI.Inductance Lm1= 10./(2*pi*f)
16:     "Magnetizing inductance w.r.t. primary side";
```


## Execution evidence

[Rumoca commands, return codes, integrity hashes, bounded output and metadata](../evidence/ba392aa660731e79.json). Baseline: **tool-error**.

No independent runtime override was executed for this target in this audit; this is not a pass.

## Recommended action

Resolve the intended parameter domain and enclosing equations; check inherited bounds, final/protected status, guards and aliases. Construct an otherwise-valid source-level witness, establish a clean baseline in a capable engine, then retranslate at the witness and compare with the runtime override. For equality claims use the actual partner value. Do not apply a blanket min>0 fix yet.

## Scope and limitations

A source-level verdict addresses the reported declaration/claim, not every possible connected system. Tests cover 0–0.5 seconds and are not a proof of long-run stability. Shared instances are not distinct root causes. A missing bound, timeout, compiler error or failed nominal run alone never counts as a verified bug or a false positive. Fixes are proposals; no library/compiler implementation was changed.

[Group and related reports](../groups/baseline-blocked.md) · [Index](../README.md)
