# FINDING-01016: Not yet established as a bug or a false positive

| Field | Value |
|---|---|
| Verdict | unresolved |
| Scope / group | baseline-blocked |
| Model | Modelica.Electrical.Analog.Examples.SimpleTriacCircuit |
| Target | simpleTriac.VTM |
| Student classification | divisor-reachable-zero |
| Original report | `FINDING-01016-simpletriaccircuit-simpletriac-vtm.md` — [withdrawn](../../v2/bugs/withdrawn.md); a later run no longer makes this claim |
| Original SHA-256 | f1fba768d7f5d5b3d88849da9d136473ae8a46f94fa4ba0b57e724ff290eaeb0 |

## What remains unresolved

The current Rumoca nominal run is tool-error, before any reported perturbation. This prevents causal attribution to this parameter. Source metadata was recovered, but none of the reviewed source proofs or counterexamples establishes this particular claim. A baseline failure/tool limitation is neither confirmation nor a false positive.

## Source evidence

Compiler/source-resolved declaration: `Electrical/Analog/Semiconductors/SimpleTriac.mo:8`. Role: `parameter`; binding: `1.7`; effective min: `None`; effective max: `None`. 

[Electrical/Analog/Semiconductors/SimpleTriac.mo — source snapshot](../evidence/sources/cc33e8068808135c-SimpleTriac.mo)

```modelica
6:     "Reverse breakthrough voltage";
7:   parameter SI.Current IDRM=0.1 "Saturation current";
8:   parameter SI.Voltage VTM= 1.7 "Conducting voltage";
9:   parameter SI.Current IH=6e-3 "Holding current";
10:   parameter SI.Current ITM= 25 "Conducting current";
11: 
```


## Execution evidence

[Rumoca commands, return codes, integrity hashes, bounded output and metadata](../evidence/8cc61e5c60b87812.json). Baseline: **tool-error**.

No independent runtime override was executed for this target in this audit; this is not a pass.

## Recommended action

Resolve the intended parameter domain and enclosing equations; check inherited bounds, final/protected status, guards and aliases. Construct an otherwise-valid source-level witness, establish a clean baseline in a capable engine, then retranslate at the witness and compare with the runtime override. For equality claims use the actual partner value. Do not apply a blanket min>0 fix yet.

## Scope and limitations

A source-level verdict addresses the reported declaration/claim, not every possible connected system. Tests cover 0–0.5 seconds and are not a proof of long-run stability. Shared instances are not distinct root causes. A missing bound, timeout, compiler error or failed nominal run alone never counts as a verified bug or a false positive. Fixes are proposals; no library/compiler implementation was changed.

[Group and related reports](../groups/baseline-blocked.md) · [Index](../README.md)
