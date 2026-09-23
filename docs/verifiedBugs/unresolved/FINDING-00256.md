# FINDING-00256: Not yet established as a bug or a false positive

| Field | Value |
|---|---|
| Verdict | unresolved |
| Scope / group | baseline-blocked |
| Model | Modelica.Electrical.Analog.Examples.GenerationOfFMUs |
| Target | inverseInductor3.L |
| Student classification | physical-bound-permits-zero |
| Original report | [FINDING-generationoffmus-inverseinductor3-l-intent.md](../../v2/bugs/FINDING-generationoffmus-inverseinductor3-l-intent.md) — reviewed as `FINDING-00256-generationoffmus-inverseinductor3-l.md`, which a later run renamed |
| Original SHA-256 | 19b3eb528c2a16f6ed833b7a1e4f2f031d48df53f16cd3cb0528a340f8dee40a |

## What remains unresolved

The current Rumoca nominal run is tool-error, before any reported perturbation. This prevents causal attribution to this parameter. Source metadata was recovered, but none of the reviewed source proofs or counterexamples establishes this particular claim. A baseline failure/tool limitation is neither confirmation nor a false positive.

## Source evidence

Compiler/source-resolved declaration: `Electrical/Analog/Examples/Utilities/InverseInductor.mo:4`. Role: `parameter`; binding: `0.002`; effective min: `0`; effective max: `None`. 

[Electrical/Analog/Examples/Utilities/InverseInductor.mo — source snapshot](../evidence/sources/9406323d45d3ccbd-InverseInductor.mo)

```modelica
2: model InverseInductor "Input/output block of an inverse inductor model"
3:   extends Modelica.Blocks.Icons.Block;
4:   parameter SI.Inductance L(min=0)=1 "Inductance";
5:   Modelica.Electrical.Analog.Basic.Inductor inductor(i(fixed=true, start=0), L=
6:         L) annotation (Placement(transformation(
7:         extent={{-10,-10},{10,10}},
```


## Execution evidence

[Rumoca commands, return codes, integrity hashes, bounded output and metadata](../evidence/0f4d718c5e58579e.json). Baseline: **tool-error**.

No independent runtime override was executed for this target in this audit; this is not a pass.

## Recommended action

Resolve the intended parameter domain and enclosing equations; check inherited bounds, final/protected status, guards and aliases. Construct an otherwise-valid source-level witness, establish a clean baseline in a capable engine, then retranslate at the witness and compare with the runtime override. For equality claims use the actual partner value. Do not apply a blanket min>0 fix yet.

## Scope and limitations

A source-level verdict addresses the reported declaration/claim, not every possible connected system. Tests cover 0–0.5 seconds and are not a proof of long-run stability. Shared instances are not distinct root causes. A missing bound, timeout, compiler error or failed nominal run alone never counts as a verified bug or a false positive. Fixes are proposals; no library/compiler implementation was changed.

[Group and related reports](../groups/baseline-blocked.md) · [Index](../README.md)
