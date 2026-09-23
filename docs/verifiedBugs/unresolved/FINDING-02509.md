# FINDING-02509: Not yet established as a bug or a false positive

| Field | Value |
|---|---|
| Verdict | unresolved |
| Scope / group | baseline-blocked |
| Model | Modelica.Electrical.Machines.Examples.SynchronousMachines.SMPM_VoltageSource |
| Target | JLoad |
| Student classification | physical-domain-unenforced |
| Original report | [FINDING-smpm-voltagesource-jload-zerolimit.md](../../v2/bugs/FINDING-smpm-voltagesource-jload-zerolimit.md) — reviewed as `FINDING-02509-smpm-voltagesource-jload.md`, which a later run renamed |
| Original SHA-256 | d2c225e283739c7067a5b856342b796b4bbfe1cadd63bede5dd704d326ad7002 |

## What remains unresolved

The current Rumoca nominal run is tool-error, before any reported perturbation. This prevents causal attribution to this parameter. Source metadata was recovered, but none of the reviewed source proofs or counterexamples establishes this particular claim. A baseline failure/tool limitation is neither confirmation nor a false positive.

## Source evidence

Compiler/source-resolved declaration: `Electrical/Machines/Examples/SynchronousMachines/SMPM_VoltageSource.mo:12`. Role: `parameter`; binding: `0.29`; effective min: `None`; effective max: `None`. 

[Electrical/Machines/Examples/SynchronousMachines/SMPM_VoltageSource.mo — source snapshot](../evidence/sources/29342da380ccf385-SMPM_VoltageSource.mo)

```modelica
10:     "Nominal speed";
11:   parameter SI.Torque TLoad=181.4 "Nominal load torque";
12:   parameter SI.Inertia JLoad=0.29
13:     "Load's moment of inertia";
14:   Machines.BasicMachines.SynchronousMachines.SM_PermanentMagnet smpm(
15:     phiMechanical(start=0, fixed=true),
```


## Execution evidence

[Rumoca commands, return codes, integrity hashes, bounded output and metadata](../evidence/d529fc5d98897b6a.json). Baseline: **tool-error**.

No independent runtime override was executed for this target in this audit; this is not a pass.

## Recommended action

Resolve the intended parameter domain and enclosing equations; check inherited bounds, final/protected status, guards and aliases. Construct an otherwise-valid source-level witness, establish a clean baseline in a capable engine, then retranslate at the witness and compare with the runtime override. For equality claims use the actual partner value. Do not apply a blanket min>0 fix yet.

## Scope and limitations

A source-level verdict addresses the reported declaration/claim, not every possible connected system. Tests cover 0–0.5 seconds and are not a proof of long-run stability. Shared instances are not distinct root causes. A missing bound, timeout, compiler error or failed nominal run alone never counts as a verified bug or a false positive. Fixes are proposals; no library/compiler implementation was changed.

[Group and related reports](../groups/baseline-blocked.md) · [Index](../README.md)
