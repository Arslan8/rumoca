# FINDING-01004: Not yet established as a bug or a false positive

| Field | Value |
|---|---|
| Verdict | unresolved |
| Scope / group | baseline-blocked |
| Model | Modelica.Electrical.Analog.Examples.SimpleTriacCircuit |
| Target | simpleTriac.thyristor.Roff |
| Student classification | physical-domain-unenforced |
| Original report | [FINDING-simpletriaccircuit-simpletriac-thyristor-roff-unbounded.md](../../v2/bugs/FINDING-simpletriaccircuit-simpletriac-thyristor-roff-unbounded.md) — reviewed as `FINDING-01004-simpletriaccircuit-simpletriac-thyristor-roff.md`, which a later run renamed |
| Original SHA-256 | e1aac3b4c7fc6aef5f344d904075755c6bacce60c26aaccb2433a687fca5fd64 |

## What remains unresolved

The current Rumoca nominal run is tool-error, before any reported perturbation. This prevents causal attribution to this parameter. Source metadata was recovered, but none of the reviewed source proofs or counterexamples establishes this particular claim. A baseline failure/tool limitation is neither confirmation nor a false positive.

## Source evidence

Compiler/source-resolved declaration: `Electrical/Analog/Semiconductors/Thyristor.mo:40`. Role: `parameter`; binding: `(((simpleTriac.thyristor.VDRM ^ 2) / simpleTriac.thyristor.VTM) / simpleTriac.thyristor.IH)`; effective min: `None`; effective max: `None`. 

[Electrical/Analog/Semiconductors/Thyristor.mo — source snapshot](../evidence/sources/dbc15414032e03ee-Thyristor.mo)

```modelica
38:   parameter SI.Resistance Ron=(VTM-0.7)/ITM
39:     "Forward conducting mode resistance";
40:   parameter SI.Resistance Roff=(VDRM^2)/VTM/IH
41:     "Blocking mode resistance";
42: 
43: equation
```


## Execution evidence

[Rumoca commands, return codes, integrity hashes, bounded output and metadata](../evidence/8cc61e5c60b87812.json). Baseline: **tool-error**.

No independent runtime override was executed for this target in this audit; this is not a pass.

## Recommended action

Resolve the intended parameter domain and enclosing equations; check inherited bounds, final/protected status, guards and aliases. Construct an otherwise-valid source-level witness, establish a clean baseline in a capable engine, then retranslate at the witness and compare with the runtime override. For equality claims use the actual partner value. Do not apply a blanket min>0 fix yet.

## Scope and limitations

A source-level verdict addresses the reported declaration/claim, not every possible connected system. Tests cover 0–0.5 seconds and are not a proof of long-run stability. Shared instances are not distinct root causes. A missing bound, timeout, compiler error or failed nominal run alone never counts as a verified bug or a false positive. Fixes are proposals; no library/compiler implementation was changed.

[Group and related reports](../groups/baseline-blocked.md) · [Index](../README.md)
