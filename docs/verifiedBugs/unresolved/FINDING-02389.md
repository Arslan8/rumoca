# FINDING-02389: Not yet established as a bug or a false positive

| Field | Value |
|---|---|
| Verdict | unresolved |
| Scope / group | baseline-blocked |
| Model | Modelica.Electrical.Machines.Examples.SynchronousMachines.SMPM_Inverter |
| Target | smpmData.Rrd |
| Student classification | physical-domain-unenforced |
| Original report | [FINDING-smpm-inverter-smpmdata-rrd-unbounded.md](../../v2/bugs/FINDING-smpm-inverter-smpmdata-rrd-unbounded.md) — reviewed as `FINDING-02389-smpm-inverter-smpmdata-rrd.md`, which a later run renamed |
| Original SHA-256 | 4aadc65c5f412182c58b6923dd78395771d973a2501f01c8933350406c0ba00b |

## What remains unresolved

The current Rumoca nominal run is tool-error, before any reported perturbation. This prevents causal attribution to this parameter. Source metadata was recovered, but none of the reviewed source proofs or counterexamples establishes this particular claim. A baseline failure/tool limitation is neither confirmation nor a false positive.

## Source evidence

Compiler/source-resolved declaration: `Electrical/Machines/Utilities/ParameterRecords/SM_ReluctanceRotorData.mo:25`. Role: `parameter`; binding: `0.04`; effective min: `None`; effective max: `None`. 

[Electrical/Machines/Utilities/ParameterRecords/SM_ReluctanceRotorData.mo — source snapshot](../evidence/sources/1a7d1cf19ec3384d-SM_ReluctanceRotorData.mo)

```modelica
23:       group="Damper cage",
24:       enable=useDamperCage));
25:   parameter SI.Resistance Rrd=0.04
26:     "Damper resistance in d-axis at TRef" annotation (Dialog(
27:       tab="Nominal resistances and inductances",
28:       group="Damper cage",
```


## Execution evidence

[Rumoca commands, return codes, integrity hashes, bounded output and metadata](../evidence/08f6cfe3d6ca76d9.json). Baseline: **tool-error**.

No independent runtime override was executed for this target in this audit; this is not a pass.

## Recommended action

Resolve the intended parameter domain and enclosing equations; check inherited bounds, final/protected status, guards and aliases. Construct an otherwise-valid source-level witness, establish a clean baseline in a capable engine, then retranslate at the witness and compare with the runtime override. For equality claims use the actual partner value. Do not apply a blanket min>0 fix yet.

## Scope and limitations

A source-level verdict addresses the reported declaration/claim, not every possible connected system. Tests cover 0–0.5 seconds and are not a proof of long-run stability. Shared instances are not distinct root causes. A missing bound, timeout, compiler error or failed nominal run alone never counts as a verified bug or a false positive. Fixes are proposals; no library/compiler implementation was changed.

[Group and related reports](../groups/baseline-blocked.md) · [Index](../README.md)
