# FINDING-03789: Not yet established as a bug or a false positive

| Field | Value |
|---|---|
| Verdict | unresolved |
| Scope / group | baseline-blocked |
| Model | Modelica.Magnetic.FluxTubes.Examples.MovingCoilActuator.ArmatureStroke |
| Target | pmActuator.material.T_ref |
| Student classification | divisor-reachable-zero |
| Original report | `FINDING-03789-armaturestroke-pmactuator-material-t-ref.md` — [withdrawn](../../v2/bugs/withdrawn.md); a later run no longer makes this claim |
| Original SHA-256 | f98c27b649b161dcc518c4b0a1435ded52c5a4027e2e5269df44c2da9f5cf142 |

## What remains unresolved

The current Rumoca nominal run is tool-error, before any reported perturbation. This prevents causal attribution to this parameter. Source metadata was recovered, but none of the reviewed source proofs or counterexamples establishes this particular claim. A baseline failure/tool limitation is neither confirmation nor a false positive.

## Source evidence

Compiler/source-resolved declaration: `Magnetic/FluxTubes/Material/HardMagnetic/BaseData.mo:9`. Role: `parameter`; binding: `(20 + 273.15)`; effective min: `0.0`; effective max: `None`. 

[Magnetic/FluxTubes/Material/HardMagnetic/BaseData.mo — source snapshot](../evidence/sources/72a5ba9004272a6d-BaseData.mo)

```modelica
7:   parameter SI.MagneticFluxDensity B_rRef=1
8:     "Remanence at reference temperature";
9:   parameter SI.Temperature T_ref=293.15 "Reference temperature";
10:   parameter SI.LinearTemperatureCoefficient alpha_Br=0
11:     "Temperature coefficient of remanence at reference temperature";
12: 
```


## Execution evidence

[Rumoca commands, return codes, integrity hashes, bounded output and metadata](../evidence/086c556da894438a.json). Baseline: **tool-error**.

No independent runtime override was executed for this target in this audit; this is not a pass.

## Recommended action

Resolve the intended parameter domain and enclosing equations; check inherited bounds, final/protected status, guards and aliases. Construct an otherwise-valid source-level witness, establish a clean baseline in a capable engine, then retranslate at the witness and compare with the runtime override. For equality claims use the actual partner value. Do not apply a blanket min>0 fix yet.

## Scope and limitations

A source-level verdict addresses the reported declaration/claim, not every possible connected system. Tests cover 0–0.5 seconds and are not a proof of long-run stability. Shared instances are not distinct root causes. A missing bound, timeout, compiler error or failed nominal run alone never counts as a verified bug or a false positive. Fixes are proposals; no library/compiler implementation was changed.

[Group and related reports](../groups/baseline-blocked.md) · [Index](../README.md)
