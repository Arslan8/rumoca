# FINDING-00251: Not yet established as a bug or a false positive

| Field | Value |
|---|---|
| Verdict | unresolved |
| Scope / group | baseline-blocked |
| Model | Modelica.Electrical.Analog.Examples.GenerationOfFMUs |
| Target | resistor2.R |
| Student classification | physical-domain-unenforced |
| Original report | [FINDING-generationoffmus-resistor2-r-intent.md](../../v2/bugs/FINDING-generationoffmus-resistor2-r-intent.md) — reviewed as `FINDING-00251-generationoffmus-resistor2-r.md`, which a later run renamed |
| Original SHA-256 | dde80192686609ad894545f855a51795d7910bde3f615a24d37ea585fa64c8e0 |

## What remains unresolved

The current Rumoca nominal run is tool-error, before any reported perturbation. This prevents causal attribution to this parameter. Source metadata was recovered, but none of the reviewed source proofs or counterexamples establishes this particular claim. A baseline failure/tool limitation is neither confirmation nor a false positive.

## Source evidence

Compiler/source-resolved declaration: `Electrical/Analog/Examples/Utilities/Resistor.mo:4`. Role: `parameter`; binding: `10`; effective min: `None`; effective max: `None`. 

[Electrical/Analog/Examples/Utilities/Resistor.mo — source snapshot](../evidence/sources/cf6be82f055f617c-Resistor.mo)

```modelica
2: model Resistor "Input/output block of a resistance model"
3:   extends Modelica.Blocks.Icons.Block;
4:   parameter SI.Resistance R=1 "Resistance";
5:   Modelica.Electrical.Analog.Basic.GeneralVoltageToCurrentAdaptor voltageToCurrent1(
6:       use_pder=false, use_fder=false)
7:     annotation (Placement(transformation(extent={{-30,-10},{-10,10}})));
```


## Execution evidence

[Rumoca commands, return codes, integrity hashes, bounded output and metadata](../evidence/0f4d718c5e58579e.json). Baseline: **tool-error**.

No independent runtime override was executed for this target in this audit; this is not a pass.

## Recommended action

Resolve the intended parameter domain and enclosing equations; check inherited bounds, final/protected status, guards and aliases. Construct an otherwise-valid source-level witness, establish a clean baseline in a capable engine, then retranslate at the witness and compare with the runtime override. For equality claims use the actual partner value. Do not apply a blanket min>0 fix yet.

## Scope and limitations

A source-level verdict addresses the reported declaration/claim, not every possible connected system. Tests cover 0–0.5 seconds and are not a proof of long-run stability. Shared instances are not distinct root causes. A missing bound, timeout, compiler error or failed nominal run alone never counts as a verified bug or a false positive. Fixes are proposals; no library/compiler implementation was changed.

[Group and related reports](../groups/baseline-blocked.md) · [Index](../README.md)
