# FINDING-02359: Not yet established as a bug or a false positive

| Field | Value |
|---|---|
| Verdict | unresolved |
| Scope / group | baseline-blocked |
| Model | Modelica.Electrical.Machines.Examples.SynchronousMachines.SMPM_Inverter |
| Target | JLoad |
| Student classification | physical-domain-unenforced |
| Original report | [FINDING-smpm-inverter-jload-zerolimit.md](../../v2/bugs/FINDING-smpm-inverter-jload-zerolimit.md) — reviewed as `FINDING-02359-smpm-inverter-jload.md`, which a later run renamed |
| Original SHA-256 | 6ffb33e159a46329ec13999da1e32fb9912c7803773afcabe70fbbb8c03c58ad |

## What remains unresolved

The current Rumoca nominal run is tool-error, before any reported perturbation. This prevents causal attribution to this parameter. Source metadata was recovered, but none of the reviewed source proofs or counterexamples establishes this particular claim. A baseline failure/tool limitation is neither confirmation nor a false positive.

## Source evidence

Compiler/source-resolved declaration: `Electrical/Machines/Examples/SynchronousMachines/SMPM_Inverter.mo:13`. Role: `parameter`; binding: `0.29`; effective min: `None`; effective max: `None`. 

[Electrical/Machines/Examples/SynchronousMachines/SMPM_Inverter.mo — source snapshot](../evidence/sources/de83e26b3376ebdc-SMPM_Inverter.mo)

```modelica
11:   parameter SI.Torque TLoad=181.4 "Nominal load torque";
12:   parameter SI.Time tStep=1.2 "Time of load torque step";
13:   parameter SI.Inertia JLoad=0.29
14:     "Load's moment of inertia";
15:   Machines.BasicMachines.SynchronousMachines.SM_PermanentMagnet smpm(
16:     p=smpmData.p,
```


## Execution evidence

[Rumoca commands, return codes, integrity hashes, bounded output and metadata](../evidence/08f6cfe3d6ca76d9.json). Baseline: **tool-error**.

No independent runtime override was executed for this target in this audit; this is not a pass.

## Recommended action

Resolve the intended parameter domain and enclosing equations; check inherited bounds, final/protected status, guards and aliases. Construct an otherwise-valid source-level witness, establish a clean baseline in a capable engine, then retranslate at the witness and compare with the runtime override. For equality claims use the actual partner value. Do not apply a blanket min>0 fix yet.

## Scope and limitations

A source-level verdict addresses the reported declaration/claim, not every possible connected system. Tests cover 0–0.5 seconds and are not a proof of long-run stability. Shared instances are not distinct root causes. A missing bound, timeout, compiler error or failed nominal run alone never counts as a verified bug or a false positive. Fixes are proposals; no library/compiler implementation was changed.

[Group and related reports](../groups/baseline-blocked.md) · [Index](../README.md)
