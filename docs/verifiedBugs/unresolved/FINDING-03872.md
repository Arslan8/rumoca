# FINDING-03872: Not yet established as a bug or a false positive

| Field | Value |
|---|---|
| Verdict | unresolved |
| Scope / group | baseline-blocked |
| Model | Modelica.Magnetic.FluxTubes.Examples.SolenoidActuator.Components.SimpleSolenoid |
| Target | t_yokeBot |
| Student classification | divisor-reachable-zero |
| Original report | `FINDING-03872-simplesolenoid-t-yokebot.md` — [withdrawn](../../v2/bugs/withdrawn.md); a later run no longer makes this claim |
| Original SHA-256 | f6a61422dd3e24f1ed65a93c3d4ce798c0ac1595a141253678481614c5da066d |

## What remains unresolved

The current Rumoca nominal run is tool-error, before any reported perturbation. This prevents causal attribution to this parameter. Source metadata was recovered, but none of the reviewed source proofs or counterexamples establishes this particular claim. A baseline failure/tool limitation is neither confirmation nor a false positive.

## Source evidence

Compiler/source-resolved declaration: `Magnetic/FluxTubes/Examples/SolenoidActuator/Components/SimpleSolenoid.mo:14`. Role: `parameter`; binding: `0.0035`; effective min: `None`; effective max: `None`. 

[Magnetic/FluxTubes/Examples/SolenoidActuator/Components/SimpleSolenoid.mo — source snapshot](../evidence/sources/781a69dd73dfb074-SimpleSolenoid.mo)

```modelica
12:   parameter SI.Radius r_yokeIn=13.5e-3 "Inner yoke radius";
13:   parameter SI.Length l_yoke=35e-3 "Axial yoke length";
14:   parameter SI.Length t_yokeBot=3.5e-3 "Axial thickness of yoke bottom";
15: 
16:   //pole
17:   parameter SI.Length l_pole=6.5e-3 "Axial length of pole";
```


## Execution evidence

[Rumoca commands, return codes, integrity hashes, bounded output and metadata](../evidence/58e9d70f53839800.json). Baseline: **tool-error**.

No independent runtime override was executed for this target in this audit; this is not a pass.

## Recommended action

Resolve the intended parameter domain and enclosing equations; check inherited bounds, final/protected status, guards and aliases. Construct an otherwise-valid source-level witness, establish a clean baseline in a capable engine, then retranslate at the witness and compare with the runtime override. For equality claims use the actual partner value. Do not apply a blanket min>0 fix yet.

## Scope and limitations

A source-level verdict addresses the reported declaration/claim, not every possible connected system. Tests cover 0–0.5 seconds and are not a proof of long-run stability. Shared instances are not distinct root causes. A missing bound, timeout, compiler error or failed nominal run alone never counts as a verified bug or a false positive. Fixes are proposals; no library/compiler implementation was changed.

[Group and related reports](../groups/baseline-blocked.md) · [Index](../README.md)
