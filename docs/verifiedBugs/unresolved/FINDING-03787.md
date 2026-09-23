# FINDING-03787: Not yet established as a bug or a false positive

| Field | Value |
|---|---|
| Verdict | unresolved |
| Scope / group | baseline-blocked |
| Model | Modelica.Magnetic.FluxTubes.Examples.MovingCoilActuator.ArmatureStroke |
| Target | pmActuator.l_PM |
| Student classification | divisor-reachable-zero |
| Original report | `FINDING-03787-armaturestroke-pmactuator-l-pm.md` — [withdrawn](../../v2/bugs/withdrawn.md); a later run no longer makes this claim |
| Original SHA-256 | 046ea0558f657972a643362125e1c1e45d7a83c9b830a67140d583d47deed259 |

## What remains unresolved

The current Rumoca nominal run is tool-error, before any reported perturbation. This prevents causal attribution to this parameter. Source metadata was recovered, but none of the reviewed source proofs or counterexamples establishes this particular claim. A baseline failure/tool limitation is neither confirmation nor a false positive.

## Source evidence

Compiler/source-resolved declaration: `Magnetic/FluxTubes/Examples/MovingCoilActuator/Components/PermeanceActuator.mo:13`. Role: `parameter`; binding: `0.0035`; effective min: `None`; effective max: `None`. 

[Magnetic/FluxTubes/Examples/MovingCoilActuator/Components/PermeanceActuator.mo — source snapshot](../evidence/sources/1142230a24c5b94d-PermeanceActuator.mo)

```modelica
11:     "Radius of ferromagnetic stator core";
12: 
13:   parameter SI.Length l_PM=3.5e-3
14:     "Radial thickness of permanent magnet ring";
15:   parameter SI.Length t=0.02
16:     "Axial length of permanent magnet ring and air gap respectively";
```


## Execution evidence

[Rumoca commands, return codes, integrity hashes, bounded output and metadata](../evidence/086c556da894438a.json). Baseline: **tool-error**.

No independent runtime override was executed for this target in this audit; this is not a pass.

## Recommended action

Resolve the intended parameter domain and enclosing equations; check inherited bounds, final/protected status, guards and aliases. Construct an otherwise-valid source-level witness, establish a clean baseline in a capable engine, then retranslate at the witness and compare with the runtime override. For equality claims use the actual partner value. Do not apply a blanket min>0 fix yet.

## Scope and limitations

A source-level verdict addresses the reported declaration/claim, not every possible connected system. Tests cover 0–0.5 seconds and are not a proof of long-run stability. Shared instances are not distinct root causes. A missing bound, timeout, compiler error or failed nominal run alone never counts as a verified bug or a false positive. Fixes are proposals; no library/compiler implementation was changed.

[Group and related reports](../groups/baseline-blocked.md) · [Index](../README.md)
