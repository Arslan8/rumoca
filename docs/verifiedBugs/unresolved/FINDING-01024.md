# FINDING-01024: Not yet established as a bug or a false positive

| Field | Value |
|---|---|
| Verdict | unresolved |
| Scope / group | baseline-blocked |
| Model | Modelica.Electrical.Analog.Examples.SimpleTriacCircuit |
| Target | simpleTriac.thyristor1.Von |
| Student classification | divisor-reachable-zero |
| Original report | [FINDING-simpletriaccircuit-simpletriac-thyristor1-von-divunreach-2.md](../../v2/bugs/FINDING-simpletriaccircuit-simpletriac-thyristor1-von-divunreach-2.md) — reviewed as `FINDING-01024-simpletriaccircuit-simpletriac-thyristor1-von.md`, which a later run renamed |
| Original SHA-256 | de2f0146024222c1aa8b4dafe2caa81563f8f38da250b6281a4bc684ad03c1c1 |

## What remains unresolved

The current Rumoca nominal run is tool-error, before any reported perturbation. This prevents causal attribution to this parameter. Source metadata was recovered, but none of the reviewed source proofs or counterexamples establishes this particular claim. A baseline failure/tool limitation is neither confirmation nor a false positive.

## Source evidence

Compiler/source-resolved declaration: `Electrical/Analog/Semiconductors/Thyristor.mo:36`. Role: `parameter`; binding: `5`; effective min: `None`; effective max: `None`. 

[Electrical/Analog/Semiconductors/Thyristor.mo — source snapshot](../evidence/sources/dbc15414032e03ee-Thyristor.mo)

```modelica
34: 
35: protected
36:   parameter SI.Voltage Von=5;
37:   parameter SI.Voltage Voff= 1.5;
38:   parameter SI.Resistance Ron=(VTM-0.7)/ITM
39:     "Forward conducting mode resistance";
```


## Execution evidence

[Rumoca commands, return codes, integrity hashes, bounded output and metadata](../evidence/8cc61e5c60b87812.json). Baseline: **tool-error**.

No independent runtime override was executed for this target in this audit; this is not a pass.

## Recommended action

Resolve the intended parameter domain and enclosing equations; check inherited bounds, final/protected status, guards and aliases. Construct an otherwise-valid source-level witness, establish a clean baseline in a capable engine, then retranslate at the witness and compare with the runtime override. For equality claims use the actual partner value. Do not apply a blanket min>0 fix yet.

## Scope and limitations

A source-level verdict addresses the reported declaration/claim, not every possible connected system. Tests cover 0–0.5 seconds and are not a proof of long-run stability. Shared instances are not distinct root causes. A missing bound, timeout, compiler error or failed nominal run alone never counts as a verified bug or a false positive. Fixes are proposals; no library/compiler implementation was changed.

[Group and related reports](../groups/baseline-blocked.md) · [Index](../README.md)
