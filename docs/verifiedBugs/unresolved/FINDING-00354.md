# FINDING-00354: Not yet established as a bug or a false positive

| Field | Value |
|---|---|
| Verdict | unresolved |
| Scope / group | baseline-blocked |
| Model | Modelica.Electrical.Analog.Examples.IdealTriacCircuit |
| Target | idealTriac.Cdis |
| Student classification | physical-bound-permits-zero |
| Original report | [FINDING-idealtriaccircuit-idealtriac-cdis-zerolimit.md](../../v2/bugs/FINDING-idealtriaccircuit-idealtriac-cdis-zerolimit.md) — reviewed as `FINDING-00354-idealtriaccircuit-idealtriac-cdis.md`, which a later run renamed |
| Original SHA-256 | e106f262e7b7290a302f4d0f10c687cc45c2524d5ea03f7e71d8788a9c1a97af |

## What remains unresolved

The current Rumoca nominal run is tool-error, before any reported perturbation. This prevents causal attribution to this parameter. Source metadata was recovered, but none of the reviewed source proofs or counterexamples establishes this particular claim. A baseline failure/tool limitation is neither confirmation nor a false positive.

## Source evidence

Compiler/source-resolved declaration: `Electrical/Analog/Ideal/IdealTriac.mo:12`. Role: `parameter`; binding: `0.005`; effective min: `0`; effective max: `None`. 

[Electrical/Analog/Ideal/IdealTriac.mo — source snapshot](../evidence/sources/6407b2b0e648b82a-IdealTriac.mo)

```modelica
10: 
11:   parameter SI.Resistance Rdis=100 "Resistance of disturbance elimination";
12:   parameter SI.Capacitance Cdis=0.005 "Capacity of disturbance elimination";
13: 
14:   Modelica.Electrical.Analog.Ideal.IdealThyristor idealThyristor(
15:     Ron=Ron,
```


## Execution evidence

[Rumoca commands, return codes, integrity hashes, bounded output and metadata](../evidence/549c8b40d7c2a5ed.json). Baseline: **tool-error**.

No independent runtime override was executed for this target in this audit; this is not a pass.

## Recommended action

Resolve the intended parameter domain and enclosing equations; check inherited bounds, final/protected status, guards and aliases. Construct an otherwise-valid source-level witness, establish a clean baseline in a capable engine, then retranslate at the witness and compare with the runtime override. For equality claims use the actual partner value. Do not apply a blanket min>0 fix yet.

## Scope and limitations

A source-level verdict addresses the reported declaration/claim, not every possible connected system. Tests cover 0–0.5 seconds and are not a proof of long-run stability. Shared instances are not distinct root causes. A missing bound, timeout, compiler error or failed nominal run alone never counts as a verified bug or a false positive. Fixes are proposals; no library/compiler implementation was changed.

[Group and related reports](../groups/baseline-blocked.md) · [Index](../README.md)
