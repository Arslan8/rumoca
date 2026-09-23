# FINDING-02115: Not yet established as a bug or a false positive

| Field | Value |
|---|---|
| Verdict | unresolved |
| Scope / group | baseline-blocked |
| Model | Modelica.Electrical.Machines.Examples.InductionMachines.IMS_Start |
| Target | aimsData.Rs |
| Student classification | divisor-reachable-zero |
| Original report | [FINDING-ims-start-aimsdata-rs-unbounded.md](../../v2/bugs/FINDING-ims-start-aimsdata-rs-unbounded.md) — reviewed as `FINDING-02115-ims-start-aimsdata-rs.md`, which a later run renamed |
| Original SHA-256 | 0ea27af1704db2efa8464fb40fc45f5ae792d6894177c35aa3c9f6976a616f88 |

## What remains unresolved

The current Rumoca nominal run is tool-error, before any reported perturbation. This prevents causal attribution to this parameter. Source metadata was recovered, but none of the reviewed source proofs or counterexamples establishes this particular claim. A baseline failure/tool limitation is neither confirmation nor a false positive.

## Source evidence

Compiler/source-resolved declaration: `Electrical/Machines/Utilities/ParameterRecords/InductionMachineData.mo:10`. Role: `parameter`; binding: `0.03`; effective min: `None`; effective max: `None`. 

[Electrical/Machines/Utilities/ParameterRecords/InductionMachineData.mo — source snapshot](../evidence/sources/8d312108fd6330eb-InductionMachineData.mo)

```modelica
8:   parameter Integer p(min=1) = 2 "Number of pole pairs (Integer)";
9:   parameter SI.Frequency fsNominal=50 "Nominal frequency";
10:   parameter SI.Resistance Rs=0.03
11:     "Stator resistance per phase at TRef"
12:     annotation (Dialog(tab="Nominal resistances and inductances"));
13:   parameter SI.Temperature TsRef=293.15
```


## Execution evidence

[Rumoca commands, return codes, integrity hashes, bounded output and metadata](../evidence/2804e4f64ad6a33e.json). Baseline: **tool-error**.

No independent runtime override was executed for this target in this audit; this is not a pass.

## Recommended action

Resolve the intended parameter domain and enclosing equations; check inherited bounds, final/protected status, guards and aliases. Construct an otherwise-valid source-level witness, establish a clean baseline in a capable engine, then retranslate at the witness and compare with the runtime override. For equality claims use the actual partner value. Do not apply a blanket min>0 fix yet.

## Scope and limitations

A source-level verdict addresses the reported declaration/claim, not every possible connected system. Tests cover 0–0.5 seconds and are not a proof of long-run stability. Shared instances are not distinct root causes. A missing bound, timeout, compiler error or failed nominal run alone never counts as a verified bug or a false positive. Fixes are proposals; no library/compiler implementation was changed.

[Group and related reports](../groups/baseline-blocked.md) · [Index](../README.md)
