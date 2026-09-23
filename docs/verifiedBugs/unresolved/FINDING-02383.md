# FINDING-02383: Not yet established as a bug or a false positive

| Field | Value |
|---|---|
| Verdict | unresolved |
| Scope / group | baseline-blocked |
| Model | Modelica.Electrical.Machines.Examples.SynchronousMachines.SMPM_Inverter |
| Target | smpm.damperCage.Rrq |
| Student classification | physical-domain-unenforced |
| Original report | [FINDING-smpm-inverter-smpm-dampercage-rrq-zerolimit.md](../../v2/bugs/FINDING-smpm-inverter-smpm-dampercage-rrq-zerolimit.md) — reviewed as `FINDING-02383-smpm-inverter-smpm-dampercage-rrq.md`, which a later run renamed |
| Original SHA-256 | a138a870418af8127c9abb0b5ec2f9af2d04155187571f15d42c729974dd47ed |

## What remains unresolved

The current Rumoca nominal run is tool-error, before any reported perturbation. This prevents causal attribution to this parameter. Source metadata was recovered, but none of the reviewed source proofs or counterexamples establishes this particular claim. A baseline failure/tool limitation is neither confirmation nor a false positive.

## Source evidence

Compiler/source-resolved declaration: `Electrical/Machines/BasicMachines/Components/DamperCage.mo:9`. Role: `parameter`; binding: `smpmData.Rrq`; effective min: `None`; effective max: `None`. 

[Electrical/Machines/BasicMachines/Components/DamperCage.mo — source snapshot](../evidence/sources/a430d3c774d76eaf-DamperCage.mo)

```modelica
7:   parameter SI.Resistance Rrd
8:     "Resistance in d-axis per phase translated to stator at T_ref";
9:   parameter SI.Resistance Rrq
10:     "Resistance in q-axis per phase translated to stator at T_ref";
11:   parameter SI.Temperature T_ref=293.15
12:     "Reference temperature of both resistances in d- and q-axis";
```


## Execution evidence

[Rumoca commands, return codes, integrity hashes, bounded output and metadata](../evidence/08f6cfe3d6ca76d9.json). Baseline: **tool-error**.

No independent runtime override was executed for this target in this audit; this is not a pass.

## Recommended action

Resolve the intended parameter domain and enclosing equations; check inherited bounds, final/protected status, guards and aliases. Construct an otherwise-valid source-level witness, establish a clean baseline in a capable engine, then retranslate at the witness and compare with the runtime override. For equality claims use the actual partner value. Do not apply a blanket min>0 fix yet.

## Scope and limitations

A source-level verdict addresses the reported declaration/claim, not every possible connected system. Tests cover 0–0.5 seconds and are not a proof of long-run stability. Shared instances are not distinct root causes. A missing bound, timeout, compiler error or failed nominal run alone never counts as a verified bug or a false positive. Fixes are proposals; no library/compiler implementation was changed.

[Group and related reports](../groups/baseline-blocked.md) · [Index](../README.md)
