# FINDING-01969: Not yet established as a bug or a false positive

| Field | Value |
|---|---|
| Verdict | unresolved |
| Scope / group | baseline-blocked |
| Model | Modelica.Electrical.Machines.Examples.InductionMachines.IMC_YDarc |
| Target | aimcData.Lm |
| Student classification | physical-domain-unenforced |
| Original report | [FINDING-imc-ydarc-aimcdata-lm-intent.md](../../v2/bugs/FINDING-imc-ydarc-aimcdata-lm-intent.md) — reviewed as `FINDING-01969-imc-ydarc-aimcdata-lm.md`, which a later run renamed |
| Original SHA-256 | 9b1ca3c5f3b6b690a369a24a0532dc37243a4649efda378906bd2e14b13c3503 |

## What remains unresolved

The current Rumoca nominal run is tool-error, before any reported perturbation. This prevents causal attribution to this parameter. Source metadata was recovered, but none of the reviewed source proofs or counterexamples establishes this particular claim. A baseline failure/tool limitation is neither confirmation nor a false positive.

## Source evidence

Compiler/source-resolved declaration: `Electrical/Machines/Utilities/ParameterRecords/IM_SquirrelCageData.mo:6`. Role: `parameter`; binding: `((3 * sqrt((1 - 0.0667))) / ((2 * (2 * asin(1.0))) * aimcData.fsNominal))`; effective min: `None`; effective max: `None`. 

[Electrical/Machines/Utilities/ParameterRecords/IM_SquirrelCageData.mo — source snapshot](../evidence/sources/70af5b683b0d8bad-IM_SquirrelCageData.mo)

```modelica
4:   extends InductionMachineData;
5:   import Modelica.Constants.pi;
6:   parameter SI.Inductance Lm=3*sqrt(1 - 0.0667)/(2*pi*
7:       fsNominal) "Stator main field inductance per phase"
8:     annotation (Dialog(tab="Nominal resistances and inductances"));
9:   parameter SI.Inductance Lrsigma=3*(1 - sqrt(1 - 0.0667))/
```


## Execution evidence

[Rumoca commands, return codes, integrity hashes, bounded output and metadata](../evidence/a03f73e52ba0cfd4.json). Baseline: **tool-error**.

No independent runtime override was executed for this target in this audit; this is not a pass.

## Recommended action

Resolve the intended parameter domain and enclosing equations; check inherited bounds, final/protected status, guards and aliases. Construct an otherwise-valid source-level witness, establish a clean baseline in a capable engine, then retranslate at the witness and compare with the runtime override. For equality claims use the actual partner value. Do not apply a blanket min>0 fix yet.

## Scope and limitations

A source-level verdict addresses the reported declaration/claim, not every possible connected system. Tests cover 0–0.5 seconds and are not a proof of long-run stability. Shared instances are not distinct root causes. A missing bound, timeout, compiler error or failed nominal run alone never counts as a verified bug or a false positive. Fixes are proposals; no library/compiler implementation was changed.

[Group and related reports](../groups/baseline-blocked.md) · [Index](../README.md)
