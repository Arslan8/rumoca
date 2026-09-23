# FINDING-00259: Not yet established as a bug or a false positive

| Field | Value |
|---|---|
| Verdict | unresolved |
| Scope / group | baseline-blocked |
| Model | Modelica.Electrical.Analog.Examples.GenerationOfFMUs |
| Target | conductor4.G |
| Student classification | physical-domain-unenforced |
| Original report | [FINDING-generationoffmus-conductor4-g-intent.md](../../v2/bugs/FINDING-generationoffmus-conductor4-g-intent.md) — reviewed as `FINDING-00259-generationoffmus-conductor4-g.md`, which a later run renamed |
| Original SHA-256 | 2000102e7477370bd363183b2bb0c09a250d7f97d99a84878b3a0976a9b10e5e |

## What remains unresolved

The current Rumoca nominal run is tool-error, before any reported perturbation. This prevents causal attribution to this parameter. Source metadata was recovered, but none of the reviewed source proofs or counterexamples establishes this particular claim. A baseline failure/tool limitation is neither confirmation nor a false positive.

## Source evidence

Compiler/source-resolved declaration: `Electrical/Analog/Examples/Utilities/Conductor.mo:4`. Role: `parameter`; binding: `10`; effective min: `None`; effective max: `None`. 

[Electrical/Analog/Examples/Utilities/Conductor.mo — source snapshot](../evidence/sources/11b842f4cf59f85f-Conductor.mo)

```modelica
2: model Conductor "Input/output block of a conductance model"
3:   extends Modelica.Blocks.Icons.Block;
4:   parameter SI.Conductance G=1 "Conductance";
5:   Modelica.Electrical.Analog.Basic.GeneralCurrentToVoltageAdaptor currentToVoltage1(
6:       use_pder=false, use_fder=false)
7:     annotation (Placement(transformation(extent={{-10,-10},{-30,10}})));
```


## Execution evidence

[Rumoca commands, return codes, integrity hashes, bounded output and metadata](../evidence/0f4d718c5e58579e.json). Baseline: **tool-error**.

No independent runtime override was executed for this target in this audit; this is not a pass.

## Recommended action

Resolve the intended parameter domain and enclosing equations; check inherited bounds, final/protected status, guards and aliases. Construct an otherwise-valid source-level witness, establish a clean baseline in a capable engine, then retranslate at the witness and compare with the runtime override. For equality claims use the actual partner value. Do not apply a blanket min>0 fix yet.

## Scope and limitations

A source-level verdict addresses the reported declaration/claim, not every possible connected system. Tests cover 0–0.5 seconds and are not a proof of long-run stability. Shared instances are not distinct root causes. A missing bound, timeout, compiler error or failed nominal run alone never counts as a verified bug or a false positive. Fixes are proposals; no library/compiler implementation was changed.

[Group and related reports](../groups/baseline-blocked.md) · [Index](../README.md)
