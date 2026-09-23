# FINDING-01012: Not yet established as a bug or a false positive

| Field | Value |
|---|---|
| Verdict | unresolved |
| Scope / group | baseline-blocked |
| Model | Modelica.Electrical.Analog.Examples.SimpleTriacCircuit |
| Target | simpleTriac.VGT |
| Student classification | divisor-reachable-zero |
| Original report | `FINDING-01012-simpletriaccircuit-simpletriac-vgt.md` — [withdrawn](../../v2/bugs/withdrawn.md); a later run no longer makes this claim |
| Original SHA-256 | 0e999fb33e815c8fc8eee96c610644baf2198a8f895d36f8e7fe5f755af5b2fb |

## What remains unresolved

The current Rumoca nominal run is tool-error, before any reported perturbation. This prevents causal attribution to this parameter. Source metadata was recovered, but none of the reviewed source proofs or counterexamples establishes this particular claim. A baseline failure/tool limitation is neither confirmation nor a false positive.

## Source evidence

Compiler/source-resolved declaration: `Electrical/Analog/Semiconductors/SimpleTriac.mo:12`. Role: `parameter`; binding: `0.7`; effective min: `None`; effective max: `None`. 

[Electrical/Analog/Semiconductors/SimpleTriac.mo — source snapshot](../evidence/sources/cc33e8068808135c-SimpleTriac.mo)

```modelica
10:   parameter SI.Current ITM= 25 "Conducting current";
11: 
12:   parameter SI.Voltage VGT= 0.7 "Gate trigger voltage";
13:   parameter SI.Current IGT= 5e-3 "Gate trigger current";
14: 
15:   parameter SI.Time TON = 1e-6 "Switch on time";
```


## Execution evidence

[Rumoca commands, return codes, integrity hashes, bounded output and metadata](../evidence/8cc61e5c60b87812.json). Baseline: **tool-error**.

No independent runtime override was executed for this target in this audit; this is not a pass.

## Recommended action

Resolve the intended parameter domain and enclosing equations; check inherited bounds, final/protected status, guards and aliases. Construct an otherwise-valid source-level witness, establish a clean baseline in a capable engine, then retranslate at the witness and compare with the runtime override. For equality claims use the actual partner value. Do not apply a blanket min>0 fix yet.

## Scope and limitations

A source-level verdict addresses the reported declaration/claim, not every possible connected system. Tests cover 0–0.5 seconds and are not a proof of long-run stability. Shared instances are not distinct root causes. A missing bound, timeout, compiler error or failed nominal run alone never counts as a verified bug or a false positive. Fixes are proposals; no library/compiler implementation was changed.

[Group and related reports](../groups/baseline-blocked.md) · [Index](../README.md)
