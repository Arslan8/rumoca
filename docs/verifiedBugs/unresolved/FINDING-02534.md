# FINDING-02534: Not yet established as a bug or a false positive

| Field | Value |
|---|---|
| Verdict | unresolved |
| Scope / group | baseline-blocked |
| Model | Modelica.Electrical.Machines.Examples.SynchronousMachines.SMPM_VoltageSource |
| Target | dqCurrentController.unitResistance |
| Student classification | physical-domain-unenforced |
| Original report | [FINDING-smpm-voltagesource-dqcurrentcontroller-unitresistance-zerolimit.md](../../v2/bugs/FINDING-smpm-voltagesource-dqcurrentcontroller-unitresistance-zerolimit.md) — reviewed as `FINDING-02534-smpm-voltagesource-dqcurrentcontroller-unitresistance.md`, which a later run renamed |
| Original SHA-256 | 843f6aeaa03170da10853bc70f38fe044aa54fee8b910e771fd7c6ae7096c0d9 |

## What remains unresolved

The current Rumoca nominal run is tool-error, before any reported perturbation. This prevents causal attribution to this parameter. Source metadata was recovered, but none of the reviewed source proofs or counterexamples establishes this particular claim. A baseline failure/tool limitation is neither confirmation nor a false positive.

## Source evidence

Compiler/source-resolved declaration: `Electrical/Machines/Utilities/DQCurrentController.mo:75`. Role: `constant`; binding: `1`; effective min: `None`; effective max: `None`. 

[Electrical/Machines/Utilities/DQCurrentController.mo — source snapshot](../evidence/sources/3dac81a76c618fc6-DQCurrentController.mo)

```modelica
73:     annotation (Placement(transformation(extent={{-10,-40},{10,-20}})));
74: protected
75:   constant SI.Resistance unitResistance=1
76:     annotation (HideResult=true);
77: equation
78:   connect(fromDQ.y, y) annotation (Line(
```


## Execution evidence

[Rumoca commands, return codes, integrity hashes, bounded output and metadata](../evidence/d529fc5d98897b6a.json). Baseline: **tool-error**.

No independent runtime override was executed for this target in this audit; this is not a pass.

## Recommended action

Resolve the intended parameter domain and enclosing equations; check inherited bounds, final/protected status, guards and aliases. Construct an otherwise-valid source-level witness, establish a clean baseline in a capable engine, then retranslate at the witness and compare with the runtime override. For equality claims use the actual partner value. Do not apply a blanket min>0 fix yet.

## Scope and limitations

A source-level verdict addresses the reported declaration/claim, not every possible connected system. Tests cover 0–0.5 seconds and are not a proof of long-run stability. Shared instances are not distinct root causes. A missing bound, timeout, compiler error or failed nominal run alone never counts as a verified bug or a false positive. Fixes are proposals; no library/compiler implementation was changed.

[Group and related reports](../groups/baseline-blocked.md) · [Index](../README.md)
