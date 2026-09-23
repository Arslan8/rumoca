# FINDING-02549: Not yet established as a bug or a false positive

| Field | Value |
|---|---|
| Verdict | unresolved |
| Scope / group | baseline-blocked |
| Model | Modelica.Electrical.Machines.Examples.SynchronousMachines.SMPM_VoltageSource |
| Target | smpmData.TsRef |
| Student classification | divisor-reachable-zero |
| Original report | `FINDING-02549-smpm-voltagesource-smpmdata-tsref.md` — [withdrawn](../../v2/bugs/withdrawn.md); a later run no longer makes this claim |
| Original SHA-256 | 930557e5a1b8e2f932df102744f5f8aef715f1cc66d2784022e606d7b4b6b394 |

## What remains unresolved

The current Rumoca nominal run is tool-error, before any reported perturbation. This prevents causal attribution to this parameter. Source metadata was recovered, but none of the reviewed source proofs or counterexamples establishes this particular claim. A baseline failure/tool limitation is neither confirmation nor a false positive.

## Source evidence

Compiler/source-resolved declaration: `Electrical/Machines/Utilities/ParameterRecords/InductionMachineData.mo:13`. Role: `parameter`; binding: `293.15`; effective min: `0.0`; effective max: `None`. 

[Electrical/Machines/Utilities/ParameterRecords/InductionMachineData.mo — source snapshot](../evidence/sources/8d312108fd6330eb-InductionMachineData.mo)

```modelica
11:     "Stator resistance per phase at TRef"
12:     annotation (Dialog(tab="Nominal resistances and inductances"));
13:   parameter SI.Temperature TsRef=293.15
14:     "Reference temperature of stator resistance"
15:     annotation (Dialog(tab="Nominal resistances and inductances"));
16:   parameter Machines.Thermal.LinearTemperatureCoefficient20 alpha20s=0
```


## Execution evidence

[Rumoca commands, return codes, integrity hashes, bounded output and metadata](../evidence/d529fc5d98897b6a.json). Baseline: **tool-error**.

No independent runtime override was executed for this target in this audit; this is not a pass.

## Recommended action

Resolve the intended parameter domain and enclosing equations; check inherited bounds, final/protected status, guards and aliases. Construct an otherwise-valid source-level witness, establish a clean baseline in a capable engine, then retranslate at the witness and compare with the runtime override. For equality claims use the actual partner value. Do not apply a blanket min>0 fix yet.

## Scope and limitations

A source-level verdict addresses the reported declaration/claim, not every possible connected system. Tests cover 0–0.5 seconds and are not a proof of long-run stability. Shared instances are not distinct root causes. A missing bound, timeout, compiler error or failed nominal run alone never counts as a verified bug or a false positive. Fixes are proposals; no library/compiler implementation was changed.

[Group and related reports](../groups/baseline-blocked.md) · [Index](../README.md)
