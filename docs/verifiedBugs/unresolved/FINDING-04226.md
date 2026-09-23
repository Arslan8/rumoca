# FINDING-04226: Not yet established as a bug or a false positive

| Field | Value |
|---|---|
| Verdict | unresolved |
| Scope / group | baseline-blocked |
| Model | Modelica.Mechanics.MultiBody.Examples.Loops.Utilities.GasForce2 |
| Target | L |
| Student classification | divisor-reachable-zero |
| Original report | [FINDING-gasforce2-l-divzero.md](../../v2/bugs/FINDING-gasforce2-l-divzero.md) — reviewed as `FINDING-04226-gasforce2-l.md`, which a later run renamed |
| Original SHA-256 | 68d550f00956a8cf8d3e34aafb0cbf9a73d464861c66a998d9317530d995c461 |

## What remains unresolved

The current Rumoca nominal run is tool-error, before any reported perturbation. This prevents causal attribution to this parameter. Source metadata was recovered, but none of the reviewed source proofs or counterexamples establishes this particular claim. A baseline failure/tool limitation is neither confirmation nor a false positive.

## Source evidence

Compiler/source-resolved declaration: `Mechanics/MultiBody/Examples/Loops/Utilities/GasForce2.mo:6`. Role: `parameter`; binding: `None`; effective min: `None`; effective max: `None`. 

[Mechanics/MultiBody/Examples/Loops/Utilities/GasForce2.mo — source snapshot](../evidence/sources/9608bc74964b28fd-GasForce2.mo)

```modelica
4: 
5:   extends Modelica.Mechanics.Translational.Interfaces.PartialCompliant;
6:   parameter SI.Length L "Length of cylinder";
7:   parameter SI.Length d "Diameter of cylinder";
8:   parameter SI.Volume k0=0.01
9:     "Volume V = k0 + k1*(1-x), with x = 1 - s_rel/L";
```


## Execution evidence

[Rumoca commands, return codes, integrity hashes, bounded output and metadata](../evidence/30a4dbfee9aed5a7.json). Baseline: **tool-error**.

No independent runtime override was executed for this target in this audit; this is not a pass.

## Recommended action

Resolve the intended parameter domain and enclosing equations; check inherited bounds, final/protected status, guards and aliases. Construct an otherwise-valid source-level witness, establish a clean baseline in a capable engine, then retranslate at the witness and compare with the runtime override. For equality claims use the actual partner value. Do not apply a blanket min>0 fix yet.

## Scope and limitations

A source-level verdict addresses the reported declaration/claim, not every possible connected system. Tests cover 0–0.5 seconds and are not a proof of long-run stability. Shared instances are not distinct root causes. A missing bound, timeout, compiler error or failed nominal run alone never counts as a verified bug or a false positive. Fixes are proposals; no library/compiler implementation was changed.

[Group and related reports](../groups/baseline-blocked.md) · [Index](../README.md)
