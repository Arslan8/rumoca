# FINDING-02449: Not yet established as a bug or a false positive

| Field | Value |
|---|---|
| Verdict | unresolved |
| Scope / group | baseline-blocked |
| Model | Modelica.Electrical.Machines.Examples.SynchronousMachines.SMPM_ResistiveBraking |
| Target | JLoad |
| Student classification | physical-domain-unenforced |
| Original report | [FINDING-smpm-resistivebraking-jload-zerolimit.md](../../v2/bugs/FINDING-smpm-resistivebraking-jload-zerolimit.md) — reviewed as `FINDING-02449-smpm-resistivebraking-jload.md`, which a later run renamed |
| Original SHA-256 | 5a61858e55229c781d7ad3e32b9fcc9f27c4586d00ee353917d725b820a82018 |

## What remains unresolved

The current Rumoca nominal run is tool-error, before any reported perturbation. This prevents causal attribution to this parameter. Source metadata was recovered, but none of the reviewed source proofs or counterexamples establishes this particular claim. A baseline failure/tool limitation is neither confirmation nor a false positive.

## Source evidence

Compiler/source-resolved declaration: `Electrical/Machines/Examples/SynchronousMachines/SMPM_ResistiveBraking.mo:7`. Role: `parameter`; binding: `(4 * smpmData.Jr)`; effective min: `None`; effective max: `None`. 

[Electrical/Machines/Examples/SynchronousMachines/SMPM_ResistiveBraking.mo — source snapshot](../evidence/sources/9fd2da3a57240a36-SMPM_ResistiveBraking.mo)

```modelica
5:   import Modelica.Constants.pi;
6:   constant Integer m=3 "Number of phases";
7:   parameter SI.Inertia JLoad=4*smpmData.Jr "Load's moment of inertia";
8:   parameter SI.AngularVelocity w0(displayUnit="rev/min")=
9:     2*pi*smpmData.fsNominal/smpmData.p "Initial speed";
10:   parameter Real k[3]={1,3,5} "Braking resistance stages w.r.t. Rs";
```


## Execution evidence

[Rumoca commands, return codes, integrity hashes, bounded output and metadata](../evidence/e8a73d0f030c129c.json). Baseline: **tool-error**.

No independent runtime override was executed for this target in this audit; this is not a pass.

## Recommended action

Resolve the intended parameter domain and enclosing equations; check inherited bounds, final/protected status, guards and aliases. Construct an otherwise-valid source-level witness, establish a clean baseline in a capable engine, then retranslate at the witness and compare with the runtime override. For equality claims use the actual partner value. Do not apply a blanket min>0 fix yet.

## Scope and limitations

A source-level verdict addresses the reported declaration/claim, not every possible connected system. Tests cover 0–0.5 seconds and are not a proof of long-run stability. Shared instances are not distinct root causes. A missing bound, timeout, compiler error or failed nominal run alone never counts as a verified bug or a false positive. Fixes are proposals; no library/compiler implementation was changed.

[Group and related reports](../groups/baseline-blocked.md) · [Index](../README.md)
