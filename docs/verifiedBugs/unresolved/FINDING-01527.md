# FINDING-01527: Not yet established as a bug or a false positive

| Field | Value |
|---|---|
| Verdict | unresolved |
| Scope / group | baseline-blocked |
| Model | Modelica.Electrical.Machines.Examples.DCMachines.DCSE_Start |
| Target | tRamp |
| Student classification | divisor-reachable-zero |
| Original report | `FINDING-01527-dcse-start-tramp.md` — [withdrawn](../../v2/bugs/withdrawn.md); a later run no longer makes this claim |
| Original SHA-256 | 7e377262fd07dd16337188114df8267cfc509c1d8f3fb05ff3bbcaf244afdc38 |

## What remains unresolved

The current Rumoca nominal run is tool-error, before any reported perturbation. This prevents causal attribution to this parameter. Source metadata was recovered, but none of the reviewed source proofs or counterexamples establishes this particular claim. A baseline failure/tool limitation is neither confirmation nor a false positive.

## Source evidence

Compiler/source-resolved declaration: `Electrical/Machines/Examples/DCMachines/DCSE_Start.mo:7`. Role: `parameter`; binding: `0.9`; effective min: `None`; effective max: `None`. 

[Electrical/Machines/Examples/DCMachines/DCSE_Start.mo — source snapshot](../evidence/sources/fb93406f366db131-DCSE_Start.mo)

```modelica
5:   parameter SI.Voltage Va=100 "Actual armature voltage";
6:   parameter SI.Time tStart=0.1 "Start of resistance ramp";
7:   parameter SI.Time tRamp=0.9 "Resistance ramp";
8:   parameter SI.Torque TLoad=63.66 "Nominal load torque";
9:   parameter SI.AngularVelocity wLoad(displayUnit="rev/min")=
10:        1410*2*Modelica.Constants.pi/60 "Nominal load speed";
```


## Execution evidence

[Rumoca commands, return codes, integrity hashes, bounded output and metadata](../evidence/40df0fa91f83b25d.json). Baseline: **tool-error**.

No independent runtime override was executed for this target in this audit; this is not a pass.

## Recommended action

Resolve the intended parameter domain and enclosing equations; check inherited bounds, final/protected status, guards and aliases. Construct an otherwise-valid source-level witness, establish a clean baseline in a capable engine, then retranslate at the witness and compare with the runtime override. For equality claims use the actual partner value. Do not apply a blanket min>0 fix yet.

## Scope and limitations

A source-level verdict addresses the reported declaration/claim, not every possible connected system. Tests cover 0–0.5 seconds and are not a proof of long-run stability. Shared instances are not distinct root causes. A missing bound, timeout, compiler error or failed nominal run alone never counts as a verified bug or a false positive. Fixes are proposals; no library/compiler implementation was changed.

[Group and related reports](../groups/baseline-blocked.md) · [Index](../README.md)
