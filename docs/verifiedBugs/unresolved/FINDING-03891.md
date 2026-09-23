# FINDING-03891: Not yet established as a bug or a false positive

| Field | Value |
|---|---|
| Verdict | unresolved |
| Scope / group | baseline-blocked |
| Model | Modelica.Magnetic.QuasiStatic.FundamentalWave.Examples.ExampleUtilities.FieldWeakeningController |
| Target | Ti |
| Student classification | divisor-reachable-zero |
| Original report | `FINDING-03891-fieldweakeningcontroller-ti.md` — [withdrawn](../../v2/bugs/withdrawn.md); a later run no longer makes this claim |
| Original SHA-256 | 51cdd834bd51f5b52ede72992d786324b068da1f8c03a15fbde157df87e6c4ae |

## What remains unresolved

The current Rumoca nominal run is tool-error, before any reported perturbation. This prevents causal attribution to this parameter. Source metadata was recovered, but none of the reviewed source proofs or counterexamples establishes this particular claim. A baseline failure/tool limitation is neither confirmation nor a false positive.

## Source evidence

Compiler/source-resolved declaration: `Magnetic/QuasiStatic/FundamentalWave/Examples/ExampleUtilities/FieldWeakeningController.mo:7`. Role: `parameter`; binding: `1e-06`; effective min: `None`; effective max: `None`. 

[Magnetic/QuasiStatic/FundamentalWave/Examples/ExampleUtilities/FieldWeakeningController.mo — source snapshot](../evidence/sources/4d61e3a7866cff9f-FieldWeakeningController.mo)

```modelica
5:   parameter Modelica.Units.SI.Current IMax "Maximum rms current per phase";
6:   parameter Real kp=1 "Proportional gain of field weakening controller";
7:   parameter Modelica.Units.SI.Time Ti=1e-6 "Integral time constant of field weakening controller";
8:   Blocks.Interfaces.RealInput iqRef
9:     annotation (Placement(transformation(extent={{-140,-20},{-100,20}})));
10:   Blocks.Interfaces.RealInput vs "Stator voltage magnitude" annotation (Placement(transformation(
```


## Execution evidence

[Rumoca commands, return codes, integrity hashes, bounded output and metadata](../evidence/8d20a687b0312239.json). Baseline: **tool-error**.

No independent runtime override was executed for this target in this audit; this is not a pass.

## Recommended action

Resolve the intended parameter domain and enclosing equations; check inherited bounds, final/protected status, guards and aliases. Construct an otherwise-valid source-level witness, establish a clean baseline in a capable engine, then retranslate at the witness and compare with the runtime override. For equality claims use the actual partner value. Do not apply a blanket min>0 fix yet.

## Scope and limitations

A source-level verdict addresses the reported declaration/claim, not every possible connected system. Tests cover 0–0.5 seconds and are not a proof of long-run stability. Shared instances are not distinct root causes. A missing bound, timeout, compiler error or failed nominal run alone never counts as a verified bug or a false positive. Fixes are proposals; no library/compiler implementation was changed.

[Group and related reports](../groups/baseline-blocked.md) · [Index](../README.md)
