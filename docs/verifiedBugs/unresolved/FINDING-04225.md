# FINDING-04225: Not yet established as a bug or a false positive

| Field | Value |
|---|---|
| Verdict | unresolved |
| Scope / group | baseline-blocked |
| Model | Modelica.Mechanics.MultiBody.Examples.Loops.Utilities.GasForce2 |
| Target | k |
| Student classification | physical-domain-unenforced |
| Original report | [FINDING-gasforce2-k-zerolimit.md](../../v2/bugs/FINDING-gasforce2-k-zerolimit.md) — reviewed as `FINDING-04225-gasforce2-k.md`, which a later run renamed |
| Original SHA-256 | 81afe5403a836f7551dc15cce27dacfd8b0ba31e17ffee924fc118ae35a6e2e3 |

## What remains unresolved

The current Rumoca nominal run is tool-error, before any reported perturbation. This prevents causal attribution to this parameter. Source metadata was recovered, but none of the reviewed source proofs or counterexamples establishes this particular claim. A baseline failure/tool limitation is neither confirmation nor a false positive.

## Source evidence

Compiler/source-resolved declaration: `Mechanics/MultiBody/Examples/Loops/Utilities/GasForce2.mo:12`. Role: `parameter`; binding: `1`; effective min: `None`; effective max: `None`. 

[Mechanics/MultiBody/Examples/Loops/Utilities/GasForce2.mo — source snapshot](../evidence/sources/9608bc74964b28fd-GasForce2.mo)

```modelica
10:   parameter SI.Volume k1=1
11:     "Volume V = k0 + k1*(1-x), with x = 1 - s_rel/L";
12:   parameter SI.HeatCapacity k=1 "Gas constant (p*V = k*T)";
13: 
14: /*
15:   parameter Real k0=0.01;
```


## Execution evidence

[Rumoca commands, return codes, integrity hashes, bounded output and metadata](../evidence/30a4dbfee9aed5a7.json). Baseline: **tool-error**.

No independent runtime override was executed for this target in this audit; this is not a pass.

## Recommended action

Resolve the intended parameter domain and enclosing equations; check inherited bounds, final/protected status, guards and aliases. Construct an otherwise-valid source-level witness, establish a clean baseline in a capable engine, then retranslate at the witness and compare with the runtime override. For equality claims use the actual partner value. Do not apply a blanket min>0 fix yet.

## Scope and limitations

A source-level verdict addresses the reported declaration/claim, not every possible connected system. Tests cover 0–0.5 seconds and are not a proof of long-run stability. Shared instances are not distinct root causes. A missing bound, timeout, compiler error or failed nominal run alone never counts as a verified bug or a false positive. Fixes are proposals; no library/compiler implementation was changed.

[Group and related reports](../groups/baseline-blocked.md) · [Index](../README.md)
