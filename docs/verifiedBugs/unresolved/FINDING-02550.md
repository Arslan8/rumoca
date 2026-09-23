# FINDING-02550: Not yet established as a bug or a false positive

| Field | Value |
|---|---|
| Verdict | unresolved |
| Scope / group | baseline-blocked |
| Model | Modelica.Electrical.Machines.Examples.SynchronousMachines.SMPM_VoltageSource |
| Target | smpmData.alpha20s |
| Student classification | divisor-reachable-zero |
| Original report | `FINDING-02550-smpm-voltagesource-smpmdata-alpha20s.md` — [withdrawn](../../v2/bugs/withdrawn.md); a later run no longer makes this claim |
| Original SHA-256 | 06e136aa1681844e47f738c172b1c51811a7a1971b93e0324e1b2ec5052fb725 |

## What remains unresolved

The current Rumoca nominal run is tool-error, before any reported perturbation. This prevents causal attribution to this parameter. Source metadata was recovered, but none of the reviewed source proofs or counterexamples establishes this particular claim. A baseline failure/tool limitation is neither confirmation nor a false positive.

## Source evidence

Compiler/source-resolved declaration: `Electrical/Machines/Utilities/ParameterRecords/InductionMachineData.mo:16`. Role: `parameter`; binding: `0`; effective min: `None`; effective max: `None`. 

[Electrical/Machines/Utilities/ParameterRecords/InductionMachineData.mo — source snapshot](../evidence/sources/8d312108fd6330eb-InductionMachineData.mo)

```modelica
14:     "Reference temperature of stator resistance"
15:     annotation (Dialog(tab="Nominal resistances and inductances"));
16:   parameter Machines.Thermal.LinearTemperatureCoefficient20 alpha20s=0
17:     "Temperature coefficient of stator resistance at 20 degC"
18:     annotation (Dialog(tab="Nominal resistances and inductances"));
19:   parameter Real effectiveStatorTurns=1 "Effective number of stator turns";
```


## Execution evidence

[Rumoca commands, return codes, integrity hashes, bounded output and metadata](../evidence/d529fc5d98897b6a.json). Baseline: **tool-error**.

No independent runtime override was executed for this target in this audit; this is not a pass.

## Recommended action

Resolve the intended parameter domain and enclosing equations; check inherited bounds, final/protected status, guards and aliases. Construct an otherwise-valid source-level witness, establish a clean baseline in a capable engine, then retranslate at the witness and compare with the runtime override. For equality claims use the actual partner value. Do not apply a blanket min>0 fix yet.

## Scope and limitations

A source-level verdict addresses the reported declaration/claim, not every possible connected system. Tests cover 0–0.5 seconds and are not a proof of long-run stability. Shared instances are not distinct root causes. A missing bound, timeout, compiler error or failed nominal run alone never counts as a verified bug or a false positive. Fixes are proposals; no library/compiler implementation was changed.

[Group and related reports](../groups/baseline-blocked.md) · [Index](../README.md)
