# FINDING-01215: Not yet established as a bug or a false positive

| Field | Value |
|---|---|
| Verdict | unresolved |
| Scope / group | baseline-blocked |
| Model | Modelica.Electrical.Machines.Examples.DCMachines.DCEE_Start |
| Target | tRamp |
| Student classification | divisor-reachable-zero |
| Original report | `FINDING-01215-dcee-start-tramp.md` — [withdrawn](../../v2/bugs/withdrawn.md); a later run no longer makes this claim |
| Original SHA-256 | 058c906b6e2e260936ddf2c99ad1cf56cbc5b8234b9683dc3489917962dff1da |

## What remains unresolved

The current Rumoca nominal run is tool-error, before any reported perturbation. This prevents causal attribution to this parameter. Source metadata was recovered, but none of the reviewed source proofs or counterexamples establishes this particular claim. A baseline failure/tool limitation is neither confirmation nor a false positive.

## Source evidence

Compiler/source-resolved declaration: `Electrical/Machines/Examples/DCMachines/DCEE_Start.mo:8`. Role: `parameter`; binding: `0.8`; effective min: `None`; effective max: `None`. 

[Electrical/Machines/Examples/DCMachines/DCEE_Start.mo — source snapshot](../evidence/sources/578b93b04921797a-DCEE_Start.mo)

```modelica
6:   parameter SI.Time tStart=0.2
7:     "Start of armature voltage ramp";
8:   parameter SI.Time tRamp=0.8 "Armature voltage ramp";
9:   parameter SI.Voltage Ve=100 "Actual excitation voltage";
10:   parameter SI.Torque TLoad=63.66 "Nominal load torque";
11:   parameter SI.Time tStep=1.5 "Time of load torque step";
```


## Execution evidence

[Rumoca commands, return codes, integrity hashes, bounded output and metadata](../evidence/038fc081f23c709d.json). Baseline: **tool-error**.

No independent runtime override was executed for this target in this audit; this is not a pass.

## Recommended action

Resolve the intended parameter domain and enclosing equations; check inherited bounds, final/protected status, guards and aliases. Construct an otherwise-valid source-level witness, establish a clean baseline in a capable engine, then retranslate at the witness and compare with the runtime override. For equality claims use the actual partner value. Do not apply a blanket min>0 fix yet.

## Scope and limitations

A source-level verdict addresses the reported declaration/claim, not every possible connected system. Tests cover 0–0.5 seconds and are not a proof of long-run stability. Shared instances are not distinct root causes. A missing bound, timeout, compiler error or failed nominal run alone never counts as a verified bug or a false positive. Fixes are proposals; no library/compiler implementation was changed.

[Group and related reports](../groups/baseline-blocked.md) · [Index](../README.md)
