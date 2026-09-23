# FINDING-02257: Not yet established as a bug or a false positive

| Field | Value |
|---|---|
| Verdict | unresolved |
| Scope / group | baseline-blocked |
| Model | Modelica.Electrical.Machines.Examples.SynchronousMachines.SMPM_Braking |
| Target | JLoad |
| Student classification | physical-domain-unenforced |
| Original report | [FINDING-smpm-braking-jload-zerolimit.md](../../v2/bugs/FINDING-smpm-braking-jload-zerolimit.md) — reviewed as `FINDING-02257-smpm-braking-jload.md`, which a later run renamed |
| Original SHA-256 | d7fd10e46beb7769a760a1947ac1727aabeaed3a34b38c931061d08ffda16617 |

## What remains unresolved

The current Rumoca nominal run is tool-error, before any reported perturbation. This prevents causal attribution to this parameter. Source metadata was recovered, but none of the reviewed source proofs or counterexamples establishes this particular claim. A baseline failure/tool limitation is neither confirmation nor a false positive.

## Source evidence

Compiler/source-resolved declaration: `Electrical/Machines/Examples/SynchronousMachines/SMPM_Braking.mo:11`. Role: `parameter`; binding: `0.29`; effective min: `None`; effective max: `None`. 

[Electrical/Machines/Examples/SynchronousMachines/SMPM_Braking.mo — source snapshot](../evidence/sources/e7038e99bb1477be-SMPM_Braking.mo)

```modelica
9:   parameter SI.AngularVelocity wNominal=2*pi*smpmData.fsNominal/smpmData.p
10:     "Nominal speed";
11:   parameter SI.Inertia JLoad=0.29
12:     "Load's moment of inertia";
13:   Machines.BasicMachines.SynchronousMachines.SM_PermanentMagnet smpm(
14:     phiMechanical(start=0, fixed=true),
```


## Execution evidence

[Rumoca commands, return codes, integrity hashes, bounded output and metadata](../evidence/aa20b722e1669c45.json). Baseline: **tool-error**.

No independent runtime override was executed for this target in this audit; this is not a pass.

## Recommended action

Resolve the intended parameter domain and enclosing equations; check inherited bounds, final/protected status, guards and aliases. Construct an otherwise-valid source-level witness, establish a clean baseline in a capable engine, then retranslate at the witness and compare with the runtime override. For equality claims use the actual partner value. Do not apply a blanket min>0 fix yet.

## Scope and limitations

A source-level verdict addresses the reported declaration/claim, not every possible connected system. Tests cover 0–0.5 seconds and are not a proof of long-run stability. Shared instances are not distinct root causes. A missing bound, timeout, compiler error or failed nominal run alone never counts as a verified bug or a false positive. Fixes are proposals; no library/compiler implementation was changed.

[Group and related reports](../groups/baseline-blocked.md) · [Index](../README.md)
