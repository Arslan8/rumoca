# FINDING-04843: Not yet established as a bug or a false positive

| Field | Value |
|---|---|
| Verdict | unresolved |
| Scope / group | baseline-blocked |
| Model | ModelicaTest.Blocks.UnitDeduction |
| Target | k |
| Student classification | divisor-reachable-zero |
| Original report | `FINDING-04843-unitdeduction-k.md` — [withdrawn](../../v2/bugs/withdrawn.md); a later run no longer makes this claim |
| Original SHA-256 | f2865672bc19ea5cb14fc6962faf7e21aaf18d1fb18523bfd7142d0cccf8d55c |

## What remains unresolved

The current Rumoca nominal run is tool-error, before any reported perturbation. This prevents causal attribution to this parameter. Source metadata was recovered, but none of the reviewed source proofs or counterexamples establishes this particular claim. A baseline failure/tool limitation is neither confirmation nor a false positive.

## Source evidence

Compiler/source-resolved declaration: `/data/mrumoca/rumoca/target/corpus/ModelicaStandardLibrary-4.1.0/ModelicaTest/Blocks.mo:783`. Role: `parameter`; binding: `1`; effective min: `None`; effective max: `None`. 

[/data/mrumoca/rumoca/target/corpus/ModelicaStandardLibrary-4.1.0/ModelicaTest/Blocks.mo — source snapshot](../evidence/sources/544eeae6ef829e9e-Blocks.mo)

```modelica
781:   model UnitDeduction "Test unit deduction"
782:     extends Modelica.Icons.Example;
783:     parameter Real k(unit="1")=1 "Propagated to relevant blocks";
784:     Modelica.Blocks.Continuous.Integrator integrator
785:       annotation (Placement(transformation(extent={{0,30},{20,50}})));
786:     Modelica.Mechanics.Rotational.Components.Inertia inertia(
```


## Execution evidence

[Rumoca commands, return codes, integrity hashes, bounded output and metadata](../evidence/434be1b21277e1f1.json). Baseline: **tool-error**.

No independent runtime override was executed for this target in this audit; this is not a pass.

## Recommended action

Resolve the intended parameter domain and enclosing equations; check inherited bounds, final/protected status, guards and aliases. Construct an otherwise-valid source-level witness, establish a clean baseline in a capable engine, then retranslate at the witness and compare with the runtime override. For equality claims use the actual partner value. Do not apply a blanket min>0 fix yet.

## Scope and limitations

A source-level verdict addresses the reported declaration/claim, not every possible connected system. Tests cover 0–0.5 seconds and are not a proof of long-run stability. Shared instances are not distinct root causes. A missing bound, timeout, compiler error or failed nominal run alone never counts as a verified bug or a false positive. Fixes are proposals; no library/compiler implementation was changed.

[Group and related reports](../groups/baseline-blocked.md) · [Index](../README.md)
