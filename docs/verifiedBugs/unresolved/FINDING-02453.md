# FINDING-02453: Not yet established as a bug or a false positive

| Field | Value |
|---|---|
| Verdict | unresolved |
| Scope / group | baseline-blocked |
| Model | Modelica.Electrical.Machines.Examples.SynchronousMachines.SMPM_ResistiveBraking |
| Target | smpmData.Lrsigmaq |
| Student classification | physical-domain-unenforced |
| Original report | [FINDING-smpm-resistivebraking-smpmdata-lrsigmaq-intent.md](../../v2/bugs/FINDING-smpm-resistivebraking-smpmdata-lrsigmaq-intent.md) — reviewed as `FINDING-02453-smpm-resistivebraking-smpmdata-lrsigmaq.md`, which a later run renamed |
| Original SHA-256 | 169f33e9f2c46ab8399e312032fce89e51fb13c8837f842e41fe3d83a14afc98 |

## What remains unresolved

The current Rumoca nominal run is tool-error, before any reported perturbation. This prevents causal attribution to this parameter. Source metadata was recovered, but none of the reviewed source proofs or counterexamples establishes this particular claim. A baseline failure/tool limitation is neither confirmation nor a false positive.

## Source evidence

Compiler/source-resolved declaration: `Electrical/Machines/Utilities/ParameterRecords/SM_ReluctanceRotorData.mo:20`. Role: `parameter`; binding: `smpmData.Lrsigmad`; effective min: `None`; effective max: `None`. 

[Electrical/Machines/Utilities/ParameterRecords/SM_ReluctanceRotorData.mo — source snapshot](../evidence/sources/1a7d1cf19ec3384d-SM_ReluctanceRotorData.mo)

```modelica
18:       group="Damper cage",
19:       enable=useDamperCage));
20:   parameter SI.Inductance Lrsigmaq=Lrsigmad
21:     "Damper stray inductance in q-axis" annotation (Dialog(
22:       tab="Nominal resistances and inductances",
23:       group="Damper cage",
```


## Execution evidence

[Rumoca commands, return codes, integrity hashes, bounded output and metadata](../evidence/e8a73d0f030c129c.json). Baseline: **tool-error**.

No independent runtime override was executed for this target in this audit; this is not a pass.

## Recommended action

Resolve the intended parameter domain and enclosing equations; check inherited bounds, final/protected status, guards and aliases. Construct an otherwise-valid source-level witness, establish a clean baseline in a capable engine, then retranslate at the witness and compare with the runtime override. For equality claims use the actual partner value. Do not apply a blanket min>0 fix yet.

## Scope and limitations

A source-level verdict addresses the reported declaration/claim, not every possible connected system. Tests cover 0–0.5 seconds and are not a proof of long-run stability. Shared instances are not distinct root causes. A missing bound, timeout, compiler error or failed nominal run alone never counts as a verified bug or a false positive. Fixes are proposals; no library/compiler implementation was changed.

[Group and related reports](../groups/baseline-blocked.md) · [Index](../README.md)
