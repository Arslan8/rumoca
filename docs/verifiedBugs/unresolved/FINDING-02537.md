# FINDING-02537: Not yet established as a bug or a false positive

| Field | Value |
|---|---|
| Verdict | unresolved |
| Scope / group | baseline-blocked |
| Model | Modelica.Electrical.Machines.Examples.SynchronousMachines.SMPM_VoltageSource |
| Target | smpmData.Lrsigmad |
| Student classification | physical-domain-unenforced |
| Original report | [FINDING-smpm-voltagesource-smpmdata-lrsigmad-intent.md](../../v2/bugs/FINDING-smpm-voltagesource-smpmdata-lrsigmad-intent.md) — reviewed as `FINDING-02537-smpm-voltagesource-smpmdata-lrsigmad.md`, which a later run renamed |
| Original SHA-256 | 6185eda00c02eaae6b7468fc6f0d8d340bbeb0097db19c365a5b130812275661 |

## What remains unresolved

The current Rumoca nominal run is tool-error, before any reported perturbation. This prevents causal attribution to this parameter. Source metadata was recovered, but none of the reviewed source proofs or counterexamples establishes this particular claim. A baseline failure/tool limitation is neither confirmation nor a false positive.

## Source evidence

Compiler/source-resolved declaration: `Electrical/Machines/Utilities/ParameterRecords/SM_ReluctanceRotorData.mo:15`. Role: `parameter`; binding: `(0.05 / ((2 * (2 * asin(1.0))) * smpmData.fsNominal))`; effective min: `None`; effective max: `None`. 

[Electrical/Machines/Utilities/ParameterRecords/SM_ReluctanceRotorData.mo — source snapshot](../evidence/sources/1a7d1cf19ec3384d-SM_ReluctanceRotorData.mo)

```modelica
13:     annotation (Evaluate=true,Dialog(tab=
14:           "Nominal resistances and inductances", group="Damper cage"));
15:   parameter SI.Inductance Lrsigmad=0.05/(2*pi*fsNominal)
16:     "Damper stray inductance in d-axis" annotation (Dialog(
17:       tab="Nominal resistances and inductances",
18:       group="Damper cage",
```


## Execution evidence

[Rumoca commands, return codes, integrity hashes, bounded output and metadata](../evidence/d529fc5d98897b6a.json). Baseline: **tool-error**.

No independent runtime override was executed for this target in this audit; this is not a pass.

## Recommended action

Resolve the intended parameter domain and enclosing equations; check inherited bounds, final/protected status, guards and aliases. Construct an otherwise-valid source-level witness, establish a clean baseline in a capable engine, then retranslate at the witness and compare with the runtime override. For equality claims use the actual partner value. Do not apply a blanket min>0 fix yet.

## Scope and limitations

A source-level verdict addresses the reported declaration/claim, not every possible connected system. Tests cover 0–0.5 seconds and are not a proof of long-run stability. Shared instances are not distinct root causes. A missing bound, timeout, compiler error or failed nominal run alone never counts as a verified bug or a false positive. Fixes are proposals; no library/compiler implementation was changed.

[Group and related reports](../groups/baseline-blocked.md) · [Index](../README.md)
