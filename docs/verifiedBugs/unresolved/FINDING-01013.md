# FINDING-01013: Not yet established as a bug or a false positive

| Field | Value |
|---|---|
| Verdict | unresolved |
| Scope / group | baseline-blocked |
| Model | Modelica.Electrical.Analog.Examples.SimpleTriacCircuit |
| Target | simpleTriac.TON |
| Student classification | divisor-reachable-zero |
| Original report | `FINDING-01013-simpletriaccircuit-simpletriac-ton.md` — [withdrawn](../../v2/bugs/withdrawn.md); a later run no longer makes this claim |
| Original SHA-256 | a7bbef3ce960dfd42c91b2e32f5b32ae198a097d47267a7890ba9170def27aca |

## What remains unresolved

The current Rumoca nominal run is tool-error, before any reported perturbation. This prevents causal attribution to this parameter. Source metadata was recovered, but none of the reviewed source proofs or counterexamples establishes this particular claim. A baseline failure/tool limitation is neither confirmation nor a false positive.

## Source evidence

Compiler/source-resolved declaration: `Electrical/Analog/Semiconductors/SimpleTriac.mo:15`. Role: `parameter`; binding: `1e-06`; effective min: `None`; effective max: `None`. 

[Electrical/Analog/Semiconductors/SimpleTriac.mo — source snapshot](../evidence/sources/cc33e8068808135c-SimpleTriac.mo)

```modelica
13:   parameter SI.Current IGT= 5e-3 "Gate trigger current";
14: 
15:   parameter SI.Time TON = 1e-6 "Switch on time";
16:   parameter SI.Time TOFF = 15e-6 "Switch off time";
17:   parameter SI.Voltage Vt=0.04
18:     "Voltage equivalent of temperature (kT/qn)";
```


## Execution evidence

[Rumoca commands, return codes, integrity hashes, bounded output and metadata](../evidence/8cc61e5c60b87812.json). Baseline: **tool-error**.

No independent runtime override was executed for this target in this audit; this is not a pass.

## Recommended action

Resolve the intended parameter domain and enclosing equations; check inherited bounds, final/protected status, guards and aliases. Construct an otherwise-valid source-level witness, establish a clean baseline in a capable engine, then retranslate at the witness and compare with the runtime override. For equality claims use the actual partner value. Do not apply a blanket min>0 fix yet.

## Scope and limitations

A source-level verdict addresses the reported declaration/claim, not every possible connected system. Tests cover 0–0.5 seconds and are not a proof of long-run stability. Shared instances are not distinct root causes. A missing bound, timeout, compiler error or failed nominal run alone never counts as a verified bug or a false positive. Fixes are proposals; no library/compiler implementation was changed.

[Group and related reports](../groups/baseline-blocked.md) · [Index](../README.md)
