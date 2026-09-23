# FINDING-04407: Not yet established as a bug or a false positive

| Field | Value |
|---|---|
| Verdict | unresolved |
| Scope / group | baseline-blocked |
| Model | Modelica.Mechanics.Rotational.Examples.Utilities.DirectInertia |
| Target | J |
| Student classification | physical-bound-permits-zero |
| Original report | [FINDING-directinertia-j-zerolimit.md](../../v2/bugs/FINDING-directinertia-j-zerolimit.md) — reviewed as `FINDING-04407-directinertia-j.md`, which a later run renamed |
| Original SHA-256 | 416dfae77fc45439105a3fa4d86ab378f9a8c4f1fbe936e6fe2fa0246455540f |

## What remains unresolved

The current Rumoca nominal run is reported-failure, before any reported perturbation. This prevents causal attribution to this parameter. Source metadata was recovered, but none of the reviewed source proofs or counterexamples establishes this particular claim. A baseline failure/tool limitation is neither confirmation nor a false positive.

## Source evidence

Compiler/source-resolved declaration: `Mechanics/Rotational/Examples/Utilities/DirectInertia.mo:4`. Role: `parameter`; binding: `1`; effective min: `0`; effective max: `None`. 

[Mechanics/Rotational/Examples/Utilities/DirectInertia.mo — source snapshot](../evidence/sources/35b852774e7ea9ab-DirectInertia.mo)

```modelica
2: model DirectInertia "Input/output block of a direct inertia model"
3:   extends Modelica.Blocks.Icons.Block;
4:   parameter SI.Inertia J(min=0)=1 "Inertia";
5:   Modelica.Mechanics.Rotational.Components.Inertia inertia(
6:     J=J,
7:     phi(start=0, fixed=true),
```


## Execution evidence

[Rumoca commands, return codes, integrity hashes, bounded output and metadata](../evidence/db41281980f8cb9b.json). Baseline: **reported-failure**.

No independent runtime override was executed for this target in this audit; this is not a pass.

## Recommended action

Resolve the intended parameter domain and enclosing equations; check inherited bounds, final/protected status, guards and aliases. Construct an otherwise-valid source-level witness, establish a clean baseline in a capable engine, then retranslate at the witness and compare with the runtime override. For equality claims use the actual partner value. Do not apply a blanket min>0 fix yet.

## Scope and limitations

A source-level verdict addresses the reported declaration/claim, not every possible connected system. Tests cover 0–0.5 seconds and are not a proof of long-run stability. Shared instances are not distinct root causes. A missing bound, timeout, compiler error or failed nominal run alone never counts as a verified bug or a false positive. Fixes are proposals; no library/compiler implementation was changed.

[Group and related reports](../groups/baseline-blocked.md) · [Index](../README.md)
