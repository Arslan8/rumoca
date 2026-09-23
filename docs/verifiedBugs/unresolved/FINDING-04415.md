# FINDING-04415: Not yet established as a bug or a false positive

| Field | Value |
|---|---|
| Verdict | unresolved |
| Scope / group | baseline-blocked |
| Model | Modelica.Mechanics.Rotational.Examples.Utilities.Spring |
| Target | c |
| Student classification | physical-domain-unenforced |
| Original report | [FINDING-spring-c-zerolimit.md](../../v2/bugs/FINDING-spring-c-zerolimit.md) — reviewed as `FINDING-04415-spring-c.md`, which a later run renamed |
| Original SHA-256 | fe378491fda818e78506e305691fe64f866922177768b033d219e15c99a1a59e |

## What remains unresolved

The current Rumoca nominal run is reported-failure, before any reported perturbation. This prevents causal attribution to this parameter. Source metadata was recovered, but none of the reviewed source proofs or counterexamples establishes this particular claim. A baseline failure/tool limitation is neither confirmation nor a false positive.

## Source evidence

Compiler/source-resolved declaration: `Mechanics/Rotational/Examples/Utilities/Spring.mo:4`. Role: `parameter`; binding: `10000.0`; effective min: `None`; effective max: `None`. 

[Mechanics/Rotational/Examples/Utilities/Spring.mo — source snapshot](../evidence/sources/d58b719abab92a29-Spring.mo)

```modelica
2: model Spring "Input/output block of a spring model"
3:   extends Modelica.Blocks.Icons.Block;
4:   parameter SI.RotationalSpringConstant c=1e4
5:     "Spring constant";
6:   parameter SI.Angle phi_rel0=0
7:     "Unstretched spring angle";
```


## Execution evidence

[Rumoca commands, return codes, integrity hashes, bounded output and metadata](../evidence/2bc3532846c9224e.json). Baseline: **reported-failure**.

No independent runtime override was executed for this target in this audit; this is not a pass.

## Recommended action

Resolve the intended parameter domain and enclosing equations; check inherited bounds, final/protected status, guards and aliases. Construct an otherwise-valid source-level witness, establish a clean baseline in a capable engine, then retranslate at the witness and compare with the runtime override. For equality claims use the actual partner value. Do not apply a blanket min>0 fix yet.

## Scope and limitations

A source-level verdict addresses the reported declaration/claim, not every possible connected system. Tests cover 0–0.5 seconds and are not a proof of long-run stability. Shared instances are not distinct root causes. A missing bound, timeout, compiler error or failed nominal run alone never counts as a verified bug or a false positive. Fixes are proposals; no library/compiler implementation was changed.

[Group and related reports](../groups/baseline-blocked.md) · [Index](../README.md)
