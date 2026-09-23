# FINDING-05043: Not yet established as a bug or a false positive

| Field | Value |
|---|---|
| Verdict | unresolved |
| Scope / group | baseline-blocked |
| Model | ModelicaTest.Translational.TestBraking |
| Target | eddyCurrentForce.alpha20 |
| Student classification | divisor-reachable-zero |
| Original report | `FINDING-05043-testbraking-eddycurrentforce-alpha20.md` — [withdrawn](../../v2/bugs/withdrawn.md); a later run no longer makes this claim |
| Original SHA-256 | 177e78286e793e18bf75a4e915ed6ec9420a03417c7a379767a92d2f1390c7bd |

## What remains unresolved

The current Rumoca nominal run is tool-error, before any reported perturbation. This prevents causal attribution to this parameter. Source metadata was recovered, but none of the reviewed source proofs or counterexamples establishes this particular claim. A baseline failure/tool limitation is neither confirmation nor a false positive.

## Source evidence

Compiler/source-resolved declaration: `Mechanics/Translational/Sources/EddyCurrentForce.mo:12`. Role: `parameter`; binding: `0.00392`; effective min: `None`; effective max: `None`. 

[Mechanics/Translational/Sources/EddyCurrentForce.mo — source snapshot](../evidence/sources/002a973c5a08daf5-EddyCurrentForce.mo)

```modelica
10:   parameter SI.Temperature TRef(start=293.15)
11:     "Reference temperature";
12:   parameter Modelica.Electrical.Machines.Thermal.LinearTemperatureCoefficient20
13:     alpha20(start=0) "Temperature coefficient of material";
14:   extends Modelica.Mechanics.Translational.Interfaces.PartialForce;
15:   extends Modelica.Thermal.HeatTransfer.Interfaces.PartialElementaryConditionalHeatPort;
```


## Execution evidence

[Rumoca commands, return codes, integrity hashes, bounded output and metadata](../evidence/3891acfdf63d91b5.json). Baseline: **tool-error**.

No independent runtime override was executed for this target in this audit; this is not a pass.

## Recommended action

Resolve the intended parameter domain and enclosing equations; check inherited bounds, final/protected status, guards and aliases. Construct an otherwise-valid source-level witness, establish a clean baseline in a capable engine, then retranslate at the witness and compare with the runtime override. For equality claims use the actual partner value. Do not apply a blanket min>0 fix yet.

## Scope and limitations

A source-level verdict addresses the reported declaration/claim, not every possible connected system. Tests cover 0–0.5 seconds and are not a proof of long-run stability. Shared instances are not distinct root causes. A missing bound, timeout, compiler error or failed nominal run alone never counts as a verified bug or a false positive. Fixes are proposals; no library/compiler implementation was changed.

[Group and related reports](../groups/baseline-blocked.md) · [Index](../README.md)
