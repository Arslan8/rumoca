# FINDING-03792: Not yet established as a bug or a false positive

| Field | Value |
|---|---|
| Verdict | unresolved |
| Scope / group | baseline-blocked |
| Model | Modelica.Magnetic.FluxTubes.Examples.MovingCoilActuator.ArmatureStroke |
| Target | pmActuator.material.H_cBRef |
| Student classification | divisor-reachable-zero |
| Original report | `FINDING-03792-armaturestroke-pmactuator-material-h-cbref.md` — [withdrawn](../../v2/bugs/withdrawn.md); a later run no longer makes this claim |
| Original SHA-256 | ceade4ef56d28af2dd95326b7afdd716aaaee07c4952621986c8901ba1b802bf |

## What remains unresolved

The current Rumoca nominal run is tool-error, before any reported perturbation. This prevents causal attribution to this parameter. Source metadata was recovered, but none of the reviewed source proofs or counterexamples establishes this particular claim. A baseline failure/tool limitation is neither confirmation nor a false positive.

## Source evidence

Compiler/source-resolved declaration: `Magnetic/FluxTubes/Material/HardMagnetic/BaseData.mo:5`. Role: `parameter`; binding: `400000`; effective min: `None`; effective max: `None`. 

[Magnetic/FluxTubes/Material/HardMagnetic/BaseData.mo — source snapshot](../evidence/sources/72a5ba9004272a6d-BaseData.mo)

```modelica
3:   extends Modelica.Icons.Record;
4: 
5:   parameter SI.MagneticFieldStrength H_cBRef=1
6:     "Coercivity at reference temperature";
7:   parameter SI.MagneticFluxDensity B_rRef=1
8:     "Remanence at reference temperature";
```


## Execution evidence

[Rumoca commands, return codes, integrity hashes, bounded output and metadata](../evidence/086c556da894438a.json). Baseline: **tool-error**.

No independent runtime override was executed for this target in this audit; this is not a pass.

## Recommended action

Resolve the intended parameter domain and enclosing equations; check inherited bounds, final/protected status, guards and aliases. Construct an otherwise-valid source-level witness, establish a clean baseline in a capable engine, then retranslate at the witness and compare with the runtime override. For equality claims use the actual partner value. Do not apply a blanket min>0 fix yet.

## Scope and limitations

A source-level verdict addresses the reported declaration/claim, not every possible connected system. Tests cover 0–0.5 seconds and are not a proof of long-run stability. Shared instances are not distinct root causes. A missing bound, timeout, compiler error or failed nominal run alone never counts as a verified bug or a false positive. Fixes are proposals; no library/compiler implementation was changed.

[Group and related reports](../groups/baseline-blocked.md) · [Index](../README.md)
