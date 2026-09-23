# FINDING-02591: Not yet established as a bug or a false positive

| Field | Value |
|---|---|
| Verdict | unresolved |
| Scope / group | baseline-blocked |
| Model | Modelica.Electrical.Machines.Examples.SynchronousMachines.SMR_DOL |
| Target | smrData.Lmd |
| Student classification | physical-domain-unenforced |
| Original report | [FINDING-smr-dol-smrdata-lmd-intent.md](../../v2/bugs/FINDING-smr-dol-smrdata-lmd-intent.md) — reviewed as `FINDING-02591-smr-dol-smrdata-lmd.md`, which a later run renamed |
| Original SHA-256 | 69b36e9355df86c1badb669e6f29de322a4eeddf34868446fe5c8e6eae044c8b |

## What remains unresolved

The current Rumoca nominal run is tool-error, before any reported perturbation. This prevents causal attribution to this parameter. Source metadata was recovered, but none of the reviewed source proofs or counterexamples establishes this particular claim. A baseline failure/tool limitation is neither confirmation nor a false positive.

## Source evidence

Compiler/source-resolved declaration: `Electrical/Machines/Utilities/ParameterRecords/SM_ReluctanceRotorData.mo:6`. Role: `parameter`; binding: `(2.9 / ((2 * (2 * asin(1.0))) * smrData.fsNominal))`; effective min: `None`; effective max: `None`. 

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

[Rumoca commands, return codes, integrity hashes, bounded output and metadata](../evidence/c3f17a08fd4d3c9d.json). Baseline: **tool-error**.

No independent runtime override was executed for this target in this audit; this is not a pass.

## Recommended action

Resolve the intended parameter domain and enclosing equations; check inherited bounds, final/protected status, guards and aliases. Construct an otherwise-valid source-level witness, establish a clean baseline in a capable engine, then retranslate at the witness and compare with the runtime override. For equality claims use the actual partner value. Do not apply a blanket min>0 fix yet.

## Scope and limitations

A source-level verdict addresses the reported declaration/claim, not every possible connected system. Tests cover 0–0.5 seconds and are not a proof of long-run stability. Shared instances are not distinct root causes. A missing bound, timeout, compiler error or failed nominal run alone never counts as a verified bug or a false positive. Fixes are proposals; no library/compiler implementation was changed.

[Group and related reports](../groups/baseline-blocked.md) · [Index](../README.md)
