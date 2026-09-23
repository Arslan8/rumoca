# FINDING-00353: Not yet established as a bug or a false positive

| Field | Value |
|---|---|
| Verdict | unresolved |
| Scope / group | baseline-blocked |
| Model | Modelica.Electrical.Analog.Examples.IdealTriacCircuit |
| Target | idealTriac.Rdis |
| Student classification | physical-domain-unenforced |
| Original report | [FINDING-idealtriaccircuit-idealtriac-rdis-zerolimit.md](../../v2/bugs/FINDING-idealtriaccircuit-idealtriac-rdis-zerolimit.md) — reviewed as `FINDING-00353-idealtriaccircuit-idealtriac-rdis.md`, which a later run renamed |
| Original SHA-256 | 34471b10198987ce81260ed420052f5f86390b8b56a1b409f33cd84d15659fa0 |

## What remains unresolved

The current Rumoca nominal run is tool-error, before any reported perturbation. This prevents causal attribution to this parameter. Source metadata was recovered, but none of the reviewed source proofs or counterexamples establishes this particular claim. A baseline failure/tool limitation is neither confirmation nor a false positive.

## Source evidence

Compiler/source-resolved declaration: `Electrical/Analog/Ideal/IdealTriac.mo:11`. Role: `parameter`; binding: `100`; effective min: `None`; effective max: `None`. 

[Electrical/Analog/Ideal/IdealTriac.mo — source snapshot](../evidence/sources/6407b2b0e648b82a-IdealTriac.mo)

```modelica
9:     start=0) = 0.8 "Threshold voltage for positive and negative phase";
10: 
11:   parameter SI.Resistance Rdis=100 "Resistance of disturbance elimination";
12:   parameter SI.Capacitance Cdis=0.005 "Capacity of disturbance elimination";
13: 
14:   Modelica.Electrical.Analog.Ideal.IdealThyristor idealThyristor(
```


## Execution evidence

[Rumoca commands, return codes, integrity hashes, bounded output and metadata](../evidence/549c8b40d7c2a5ed.json). Baseline: **tool-error**.

No independent runtime override was executed for this target in this audit; this is not a pass.

## Recommended action

Resolve the intended parameter domain and enclosing equations; check inherited bounds, final/protected status, guards and aliases. Construct an otherwise-valid source-level witness, establish a clean baseline in a capable engine, then retranslate at the witness and compare with the runtime override. For equality claims use the actual partner value. Do not apply a blanket min>0 fix yet.

## Scope and limitations

A source-level verdict addresses the reported declaration/claim, not every possible connected system. Tests cover 0–0.5 seconds and are not a proof of long-run stability. Shared instances are not distinct root causes. A missing bound, timeout, compiler error or failed nominal run alone never counts as a verified bug or a false positive. Fixes are proposals; no library/compiler implementation was changed.

[Group and related reports](../groups/baseline-blocked.md) · [Index](../README.md)
