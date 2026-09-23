# FINDING-02531: Not yet established as a bug or a false positive

| Field | Value |
|---|---|
| Verdict | unresolved |
| Scope / group | baseline-blocked |
| Model | Modelica.Electrical.Machines.Examples.SynchronousMachines.SMPM_VoltageSource |
| Target | dqCurrentController.Rs |
| Student classification | physical-domain-unenforced |
| Original report | [FINDING-smpm-voltagesource-dqcurrentcontroller-rs-unbounded.md](../../v2/bugs/FINDING-smpm-voltagesource-dqcurrentcontroller-rs-unbounded.md) — reviewed as `FINDING-02531-smpm-voltagesource-dqcurrentcontroller-rs.md`, which a later run renamed |
| Original SHA-256 | b084708b4048423e003fa7e4054b987c5197b3abc621672d4cb1e535e611feab |

## What remains unresolved

The current Rumoca nominal run is tool-error, before any reported perturbation. This prevents causal attribution to this parameter. Source metadata was recovered, but none of the reviewed source proofs or counterexamples establishes this particular claim. A baseline failure/tool limitation is neither confirmation nor a false positive.

## Source evidence

Compiler/source-resolved declaration: `Electrical/Machines/Utilities/DQCurrentController.mo:11`. Role: `parameter`; binding: `Modelica.Electrical.Machines.Thermal.convertResistance(smpm.Rs, smpm.TsRef, smpm.alpha20s, smpm.TsOperational)`; effective min: `None`; effective max: `None`. 

[Electrical/Machines/Utilities/DQCurrentController.mo — source snapshot](../evidence/sources/3dac81a76c618fc6-DQCurrentController.mo)

```modelica
9:   parameter SI.Voltage VsOpenCircuit
10:     "Open circuit RMS voltage per phase @ fsNominal";
11:   parameter SI.Resistance Rs "Stator resistance per phase";
12:   parameter SI.Inductance Ld "Inductance in d-axis";
13:   parameter SI.Inductance Lq "Inductance in q-axis";
14:   //Decoupling
```


## Execution evidence

[Rumoca commands, return codes, integrity hashes, bounded output and metadata](../evidence/d529fc5d98897b6a.json). Baseline: **tool-error**.

No independent runtime override was executed for this target in this audit; this is not a pass.

## Recommended action

Resolve the intended parameter domain and enclosing equations; check inherited bounds, final/protected status, guards and aliases. Construct an otherwise-valid source-level witness, establish a clean baseline in a capable engine, then retranslate at the witness and compare with the runtime override. For equality claims use the actual partner value. Do not apply a blanket min>0 fix yet.

## Scope and limitations

A source-level verdict addresses the reported declaration/claim, not every possible connected system. Tests cover 0–0.5 seconds and are not a proof of long-run stability. Shared instances are not distinct root causes. A missing bound, timeout, compiler error or failed nominal run alone never counts as a verified bug or a false positive. Fixes are proposals; no library/compiler implementation was changed.

[Group and related reports](../groups/baseline-blocked.md) · [Index](../README.md)
