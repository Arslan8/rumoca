# FINDING-01018: Not yet established as a bug or a false positive

| Field | Value |
|---|---|
| Verdict | unresolved |
| Scope / group | baseline-blocked |
| Model | Modelica.Electrical.Analog.Examples.SimpleTriacCircuit |
| Target | simpleTriac.Nbv |
| Student classification | divisor-reachable-zero |
| Original report | `FINDING-01018-simpletriaccircuit-simpletriac-nbv.md` — [withdrawn](../../v2/bugs/withdrawn.md); a later run no longer makes this claim |
| Original SHA-256 | d822d3e7c0ece7476130be5033fe04ab78c204e4c9d4ce5532d10476baa4ac2d |

## What remains unresolved

The current Rumoca nominal run is tool-error, before any reported perturbation. This prevents causal attribution to this parameter. Source metadata was recovered, but none of the reviewed source proofs or counterexamples establishes this particular claim. A baseline failure/tool limitation is neither confirmation nor a false positive.

## Source evidence

Compiler/source-resolved declaration: `Electrical/Analog/Semiconductors/SimpleTriac.mo:19`. Role: `parameter`; binding: `0.74`; effective min: `None`; effective max: `None`. 

[Electrical/Analog/Semiconductors/SimpleTriac.mo — source snapshot](../evidence/sources/cc33e8068808135c-SimpleTriac.mo)

```modelica
17:   parameter SI.Voltage Vt=0.04
18:     "Voltage equivalent of temperature (kT/qn)";
19:   parameter Real Nbv=0.74 "Reverse Breakthrough emission coefficient";
20: 
21:   Modelica.Electrical.Analog.Interfaces.NegativePin n "Cathode"
22:     annotation (Placement(transformation(extent={{-110,-10},{-90,10}})));
```


## Execution evidence

[Rumoca commands, return codes, integrity hashes, bounded output and metadata](../evidence/8cc61e5c60b87812.json). Baseline: **tool-error**.

No independent runtime override was executed for this target in this audit; this is not a pass.

## Recommended action

Resolve the intended parameter domain and enclosing equations; check inherited bounds, final/protected status, guards and aliases. Construct an otherwise-valid source-level witness, establish a clean baseline in a capable engine, then retranslate at the witness and compare with the runtime override. For equality claims use the actual partner value. Do not apply a blanket min>0 fix yet.

## Scope and limitations

A source-level verdict addresses the reported declaration/claim, not every possible connected system. Tests cover 0–0.5 seconds and are not a proof of long-run stability. Shared instances are not distinct root causes. A missing bound, timeout, compiler error or failed nominal run alone never counts as a verified bug or a false positive. Fixes are proposals; no library/compiler implementation was changed.

[Group and related reports](../groups/baseline-blocked.md) · [Index](../README.md)
