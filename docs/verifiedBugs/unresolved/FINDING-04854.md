# FINDING-04854: Not yet established as a bug or a false positive

| Field | Value |
|---|---|
| Verdict | unresolved |
| Scope / group | baseline-blocked |
| Model | ModelicaTest.Electrical.Machines.SMPM_VoltageSourceWithLosses |
| Target | JLoad |
| Student classification | physical-domain-unenforced |
| Original report | [FINDING-smpm-voltagesourcewithlosses-jload-zerolimit.md](../../v2/bugs/FINDING-smpm-voltagesourcewithlosses-jload-zerolimit.md) — reviewed as `FINDING-04854-smpm-voltagesourcewithlosses-jload.md`, which a later run renamed |
| Original SHA-256 | 998cd790765e8197bb1558c5a8b2ec683cdb89a7ad2a2349fe4744a1cc89453e |

## What remains unresolved

The current Rumoca nominal run is tool-error, before any reported perturbation. This prevents causal attribution to this parameter. Source metadata was recovered, but none of the reviewed source proofs or counterexamples establishes this particular claim. A baseline failure/tool limitation is neither confirmation nor a false positive.

## Source evidence

Compiler/source-resolved declaration: `/data/mrumoca/rumoca/target/corpus/ModelicaStandardLibrary-4.1.0/ModelicaTest/Electrical/Machines.mo:14`. Role: `parameter`; binding: `0.29`; effective min: `None`; effective max: `None`. 

[/data/mrumoca/rumoca/target/corpus/ModelicaStandardLibrary-4.1.0/ModelicaTest/Electrical/Machines.mo — source snapshot](../evidence/sources/6428706528f3156e-Machines.mo)

```modelica
12:       "Nominal speed";
13:     parameter SI.Torque TLoad=181.4 "Nominal load torque";
14:     parameter SI.Inertia JLoad=0.29
15:       "Load's moment of inertia";
16:     Modelica.Electrical.Machines.BasicMachines.SynchronousMachines.SM_PermanentMagnet
17:       smpm(
```


## Execution evidence

[Rumoca commands, return codes, integrity hashes, bounded output and metadata](../evidence/f5cf46ada0ef7a80.json). Baseline: **tool-error**.

No independent runtime override was executed for this target in this audit; this is not a pass.

## Recommended action

Resolve the intended parameter domain and enclosing equations; check inherited bounds, final/protected status, guards and aliases. Construct an otherwise-valid source-level witness, establish a clean baseline in a capable engine, then retranslate at the witness and compare with the runtime override. For equality claims use the actual partner value. Do not apply a blanket min>0 fix yet.

## Scope and limitations

A source-level verdict addresses the reported declaration/claim, not every possible connected system. Tests cover 0–0.5 seconds and are not a proof of long-run stability. Shared instances are not distinct root causes. A missing bound, timeout, compiler error or failed nominal run alone never counts as a verified bug or a false positive. Fixes are proposals; no library/compiler implementation was changed.

[Group and related reports](../groups/baseline-blocked.md) · [Index](../README.md)
