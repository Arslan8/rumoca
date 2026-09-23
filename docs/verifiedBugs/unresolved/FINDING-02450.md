# FINDING-02450: Not yet established as a bug or a false positive

| Field | Value |
|---|---|
| Verdict | unresolved |
| Scope / group | baseline-blocked |
| Model | Modelica.Electrical.Machines.Examples.SynchronousMachines.SMPM_ResistiveBraking |
| Target | smpmData.Lmd |
| Student classification | physical-domain-unenforced |
| Original report | [FINDING-smpm-resistivebraking-smpmdata-lmd-intent.md](../../v2/bugs/FINDING-smpm-resistivebraking-smpmdata-lmd-intent.md) — reviewed as `FINDING-02450-smpm-resistivebraking-smpmdata-lmd.md`, which a later run renamed |
| Original SHA-256 | 7d0ae2c58c862aa1a59c62815a90d6483fb1684e1588d8bdeb3d04cb900552c8 |

## What remains unresolved

The current Rumoca nominal run is tool-error, before any reported perturbation. This prevents causal attribution to this parameter. Source metadata was recovered, but none of the reviewed source proofs or counterexamples establishes this particular claim. A baseline failure/tool limitation is neither confirmation nor a false positive.

## Source evidence

Compiler/source-resolved declaration: `Electrical/Machines/Utilities/ParameterRecords/SM_ReluctanceRotorData.mo:6`. Role: `parameter`; binding: `(0.3 / ((2 * (2 * asin(1.0))) * smpmData.fsNominal))`; effective min: `None`; effective max: `None`. 

[Electrical/Machines/Utilities/ParameterRecords/SM_ReluctanceRotorData.mo — source snapshot](../evidence/sources/1a7d1cf19ec3384d-SM_ReluctanceRotorData.mo)

```modelica
4:   extends InductionMachineData(Lssigma=0.1/(2*pi*fsNominal));
5:   import Modelica.Constants.pi;
6:   parameter SI.Inductance Lmd=2.9/(2*pi*fsNominal)
7:     "Stator main field inductance per phase in d-axis"
8:     annotation (Dialog(tab="Nominal resistances and inductances"));
9:   parameter SI.Inductance Lmq=0.9/(2*pi*fsNominal)
```


## Execution evidence

[Rumoca commands, return codes, integrity hashes, bounded output and metadata](../evidence/e8a73d0f030c129c.json). Baseline: **tool-error**.

No independent runtime override was executed for this target in this audit; this is not a pass.

## Recommended action

Resolve the intended parameter domain and enclosing equations; check inherited bounds, final/protected status, guards and aliases. Construct an otherwise-valid source-level witness, establish a clean baseline in a capable engine, then retranslate at the witness and compare with the runtime override. For equality claims use the actual partner value. Do not apply a blanket min>0 fix yet.

## Scope and limitations

A source-level verdict addresses the reported declaration/claim, not every possible connected system. Tests cover 0–0.5 seconds and are not a proof of long-run stability. Shared instances are not distinct root causes. A missing bound, timeout, compiler error or failed nominal run alone never counts as a verified bug or a false positive. Fixes are proposals; no library/compiler implementation was changed.

[Group and related reports](../groups/baseline-blocked.md) · [Index](../README.md)
