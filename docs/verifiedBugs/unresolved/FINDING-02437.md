# FINDING-02437: Not yet established as a bug or a false positive

| Field | Value |
|---|---|
| Verdict | unresolved |
| Scope / group | baseline-blocked |
| Model | Modelica.Electrical.Machines.Examples.SynchronousMachines.SMPM_NoLoad |
| Target | smpm.Rrq |
| Student classification | physical-domain-unenforced |
| Original report | [FINDING-smpm-noload-smpm-rrq-unbounded.md](../../v2/bugs/FINDING-smpm-noload-smpm-rrq-unbounded.md) — reviewed as `FINDING-02437-smpm-noload-smpm-rrq.md`, which a later run renamed |
| Original SHA-256 | 2b83420a940d525fa0ebaf86c530f52e5975c5fd41cd85ca4570a099f8e249b7 |

## What remains unresolved

The current Rumoca nominal run is tool-error, before any reported perturbation. This prevents causal attribution to this parameter. Source metadata was recovered, but none of the reviewed source proofs or counterexamples establishes this particular claim. A baseline failure/tool limitation is neither confirmation nor a false positive.

## Source evidence

Compiler/source-resolved declaration: `Electrical/Machines/BasicMachines/SynchronousMachines/SM_PermanentMagnet.mo:75`. Role: `parameter`; binding: `smpmData.Rrq`; effective min: `None`; effective max: `None`. 

[Electrical/Machines/BasicMachines/SynchronousMachines/SM_PermanentMagnet.mo — source snapshot](../evidence/sources/a25907bd0a29e9a2-SM_PermanentMagnet.mo)

```modelica
73:       group="Damper cage",
74:       enable=useDamperCage));
75:   parameter SI.Resistance Rrq=Rrd
76:     "Damper resistance in q-axis at TRef" annotation (Dialog(
77:       tab="Nominal resistances and inductances",
78:       group="Damper cage",
```


## Execution evidence

[Rumoca commands, return codes, integrity hashes, bounded output and metadata](../evidence/dd1bf4e5a4d0a401.json). Baseline: **tool-error**.

No independent runtime override was executed for this target in this audit; this is not a pass.

## Recommended action

Resolve the intended parameter domain and enclosing equations; check inherited bounds, final/protected status, guards and aliases. Construct an otherwise-valid source-level witness, establish a clean baseline in a capable engine, then retranslate at the witness and compare with the runtime override. For equality claims use the actual partner value. Do not apply a blanket min>0 fix yet.

## Scope and limitations

A source-level verdict addresses the reported declaration/claim, not every possible connected system. Tests cover 0–0.5 seconds and are not a proof of long-run stability. Shared instances are not distinct root causes. A missing bound, timeout, compiler error or failed nominal run alone never counts as a verified bug or a false positive. Fixes are proposals; no library/compiler implementation was changed.

[Group and related reports](../groups/baseline-blocked.md) · [Index](../README.md)
