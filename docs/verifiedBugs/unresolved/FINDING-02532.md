# FINDING-02532: Not yet established as a bug or a false positive

| Field | Value |
|---|---|
| Verdict | unresolved |
| Scope / group | baseline-blocked |
| Model | Modelica.Electrical.Machines.Examples.SynchronousMachines.SMPM_VoltageSource |
| Target | dqCurrentController.Ld |
| Student classification | physical-domain-unenforced |
| Original report | [FINDING-smpm-voltagesource-dqcurrentcontroller-ld-intent.md](../../v2/bugs/FINDING-smpm-voltagesource-dqcurrentcontroller-ld-intent.md) — reviewed as `FINDING-02532-smpm-voltagesource-dqcurrentcontroller-ld.md`, which a later run renamed |
| Original SHA-256 | 4ae20096e55fbad34d03396a9696059f0f31ab2ac547471f05b8375a3aa0710f |

## What remains unresolved

The current Rumoca nominal run is tool-error, before any reported perturbation. This prevents causal attribution to this parameter. Source metadata was recovered, but none of the reviewed source proofs or counterexamples establishes this particular claim. A baseline failure/tool limitation is neither confirmation nor a false positive.

## Source evidence

Compiler/source-resolved declaration: `Electrical/Machines/Utilities/DQCurrentController.mo:12`. Role: `parameter`; binding: `(smpm.Lssigma + smpm.Lmd)`; effective min: `None`; effective max: `None`. 

[Electrical/Machines/Utilities/DQCurrentController.mo — source snapshot](../evidence/sources/3dac81a76c618fc6-DQCurrentController.mo)

```modelica
10:     "Open circuit RMS voltage per phase @ fsNominal";
11:   parameter SI.Resistance Rs "Stator resistance per phase";
12:   parameter SI.Inductance Ld "Inductance in d-axis";
13:   parameter SI.Inductance Lq "Inductance in q-axis";
14:   //Decoupling
15:   parameter Boolean decoupling=false "Use decoupling network";
```


## Execution evidence

[Rumoca commands, return codes, integrity hashes, bounded output and metadata](../evidence/d529fc5d98897b6a.json). Baseline: **tool-error**.

No independent runtime override was executed for this target in this audit; this is not a pass.

## Recommended action

Resolve the intended parameter domain and enclosing equations; check inherited bounds, final/protected status, guards and aliases. Construct an otherwise-valid source-level witness, establish a clean baseline in a capable engine, then retranslate at the witness and compare with the runtime override. For equality claims use the actual partner value. Do not apply a blanket min>0 fix yet.

## Scope and limitations

A source-level verdict addresses the reported declaration/claim, not every possible connected system. Tests cover 0–0.5 seconds and are not a proof of long-run stability. Shared instances are not distinct root causes. A missing bound, timeout, compiler error or failed nominal run alone never counts as a verified bug or a false positive. Fixes are proposals; no library/compiler implementation was changed.

[Group and related reports](../groups/baseline-blocked.md) · [Index](../README.md)
