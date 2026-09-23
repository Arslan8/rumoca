# FINDING-01182: Not yet established as a bug or a false positive

| Field | Value |
|---|---|
| Verdict | unresolved |
| Scope / group | baseline-blocked |
| Model | Modelica.Electrical.Machines.Examples.DCMachines.DC_CompareCharacteristics |
| Target | tRamp |
| Student classification | divisor-reachable-zero |
| Original report | `FINDING-01182-dc-comparecharacteristics-tramp.md` — [withdrawn](../../v2/bugs/withdrawn.md); a later run no longer makes this claim |
| Original SHA-256 | 735f131938aac06ea99c1f0031b132ae3ac90641d8872aba802262137a77cb6f |

## What remains unresolved

The current Rumoca nominal run is tool-error, before any reported perturbation. This prevents causal attribution to this parameter. Source metadata was recovered, but none of the reviewed source proofs or counterexamples establishes this particular claim. A baseline failure/tool limitation is neither confirmation nor a false positive.

## Source evidence

Compiler/source-resolved declaration: `Electrical/Machines/Examples/DCMachines/DC_CompareCharacteristics.mo:9`. Role: `parameter`; binding: `5.0`; effective min: `None`; effective max: `None`. 

[Electrical/Machines/Examples/DCMachines/DC_CompareCharacteristics.mo — source snapshot](../evidence/sources/66b2e4a4123edad2-DC_CompareCharacteristics.mo)

```modelica
7:   parameter SI.Torque TLoad=63.66 "Nominal load torque";
8:   parameter SI.Time tStart=0.5 "Start of load torque ramp";
9:   parameter SI.Time tRamp=5.0 "Load torque ramp";
10:   parameter SI.Inertia JLoad=0.15 "Load's moment of inertia";
11:   Modelica.Electrical.Analog.Sources.ConstantVoltage armatureVoltage(V=Va)
12:     annotation (Placement(transformation(extent={{10,-10},{-10,10}},
```


## Execution evidence

[Rumoca commands, return codes, integrity hashes, bounded output and metadata](../evidence/f15341d4427cc3e0.json). Baseline: **tool-error**.

No independent runtime override was executed for this target in this audit; this is not a pass.

## Recommended action

Resolve the intended parameter domain and enclosing equations; check inherited bounds, final/protected status, guards and aliases. Construct an otherwise-valid source-level witness, establish a clean baseline in a capable engine, then retranslate at the witness and compare with the runtime override. For equality claims use the actual partner value. Do not apply a blanket min>0 fix yet.

## Scope and limitations

A source-level verdict addresses the reported declaration/claim, not every possible connected system. Tests cover 0–0.5 seconds and are not a proof of long-run stability. Shared instances are not distinct root causes. A missing bound, timeout, compiler error or failed nominal run alone never counts as a verified bug or a false positive. Fixes are proposals; no library/compiler implementation was changed.

[Group and related reports](../groups/baseline-blocked.md) · [Index](../README.md)
