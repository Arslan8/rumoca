# FINDING-01902: Not yet established as a bug or a false positive

| Field | Value |
|---|---|
| Verdict | unresolved |
| Scope / group | baseline-blocked |
| Model | Modelica.Electrical.Machines.Examples.InductionMachines.IMC_Transformer |
| Target | aimcData.Rr |
| Student classification | physical-domain-unenforced |
| Original report | [FINDING-imc-transformer-aimcdata-rr-unbounded.md](../../v2/bugs/FINDING-imc-transformer-aimcdata-rr-unbounded.md) — reviewed as `FINDING-01902-imc-transformer-aimcdata-rr.md`, which a later run renamed |
| Original SHA-256 | 2fc8d4b514b66b52fc5eae9da5c97575eaf76da7f5a9aa8802eb518b6370f851 |

## What remains unresolved

The current Rumoca nominal run is tool-error, before any reported perturbation. This prevents causal attribution to this parameter. Source metadata was recovered, but none of the reviewed source proofs or counterexamples establishes this particular claim. A baseline failure/tool limitation is neither confirmation nor a false positive.

## Source evidence

Compiler/source-resolved declaration: `Electrical/Machines/Utilities/ParameterRecords/IM_SquirrelCageData.mo:13`. Role: `parameter`; binding: `0.04`; effective min: `None`; effective max: `None`. 

[Electrical/Machines/Utilities/ParameterRecords/IM_SquirrelCageData.mo — source snapshot](../evidence/sources/70af5b683b0d8bad-IM_SquirrelCageData.mo)

```modelica
11:     "Rotor stray inductance per phase (equivalent three-phase winding)"
12:     annotation (Dialog(tab="Nominal resistances and inductances"));
13:   parameter SI.Resistance Rr=0.04
14:     "Rotor resistance per phase (equivalent three-phase winding) at TRef"
15:     annotation (Dialog(tab="Nominal resistances and inductances"));
16:   parameter SI.Temperature TrRef=293.15
```


## Execution evidence

[Rumoca commands, return codes, integrity hashes, bounded output and metadata](../evidence/ea078e37b0773dc4.json). Baseline: **tool-error**.

No independent runtime override was executed for this target in this audit; this is not a pass.

## Recommended action

Resolve the intended parameter domain and enclosing equations; check inherited bounds, final/protected status, guards and aliases. Construct an otherwise-valid source-level witness, establish a clean baseline in a capable engine, then retranslate at the witness and compare with the runtime override. For equality claims use the actual partner value. Do not apply a blanket min>0 fix yet.

## Scope and limitations

A source-level verdict addresses the reported declaration/claim, not every possible connected system. Tests cover 0–0.5 seconds and are not a proof of long-run stability. Shared instances are not distinct root causes. A missing bound, timeout, compiler error or failed nominal run alone never counts as a verified bug or a false positive. Fixes are proposals; no library/compiler implementation was changed.

[Group and related reports](../groups/baseline-blocked.md) · [Index](../README.md)
