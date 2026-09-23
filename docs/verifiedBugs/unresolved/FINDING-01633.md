# FINDING-01633: Not yet established as a bug or a false positive

| Field | Value |
|---|---|
| Verdict | unresolved |
| Scope / group | baseline-blocked |
| Model | Modelica.Electrical.Machines.Examples.InductionMachines.IMC_Initialize |
| Target | aimc.Rr |
| Student classification | physical-domain-unenforced |
| Original report | [FINDING-imc-initialize-aimc-rr-unbounded.md](../../v2/bugs/FINDING-imc-initialize-aimc-rr-unbounded.md) — reviewed as `FINDING-01633-imc-initialize-aimc-rr.md`, which a later run renamed |
| Original SHA-256 | 067adf9c8fe904767bdec6988ed9914e4fb6bca3e79c1762e976e77685b7a247 |

## What remains unresolved

The current Rumoca nominal run is tool-error, before any reported perturbation. This prevents causal attribution to this parameter. Source metadata was recovered, but none of the reviewed source proofs or counterexamples establishes this particular claim. A baseline failure/tool limitation is neither confirmation nor a false positive.

## Source evidence

Compiler/source-resolved declaration: `Electrical/Machines/BasicMachines/InductionMachines/IM_SquirrelCage.mo:33`. Role: `parameter`; binding: `aimcData.Rr`; effective min: `None`; effective max: `None`. 

[Electrical/Machines/BasicMachines/InductionMachines/IM_SquirrelCage.mo — source snapshot](../evidence/sources/d35e8ddc6d02c4da-IM_SquirrelCage.mo)

```modelica
31:     "Rotor stray inductance per phase (equivalent three-phase winding)"
32:     annotation (Dialog(tab="Nominal resistances and inductances"));
33:   parameter SI.Resistance Rr(start=0.04*ZsRef)
34:     "Rotor resistance per phase (equivalent three-phase winding) at TRef"
35:     annotation (Dialog(tab="Nominal resistances and inductances"));
36:   parameter SI.Temperature TrRef(start=293.15)
```


## Execution evidence

[Rumoca commands, return codes, integrity hashes, bounded output and metadata](../evidence/6b09ecf975c03970.json). Baseline: **tool-error**.

No independent runtime override was executed for this target in this audit; this is not a pass.

## Recommended action

Resolve the intended parameter domain and enclosing equations; check inherited bounds, final/protected status, guards and aliases. Construct an otherwise-valid source-level witness, establish a clean baseline in a capable engine, then retranslate at the witness and compare with the runtime override. For equality claims use the actual partner value. Do not apply a blanket min>0 fix yet.

## Scope and limitations

A source-level verdict addresses the reported declaration/claim, not every possible connected system. Tests cover 0–0.5 seconds and are not a proof of long-run stability. Shared instances are not distinct root causes. A missing bound, timeout, compiler error or failed nominal run alone never counts as a verified bug or a false positive. Fixes are proposals; no library/compiler implementation was changed.

[Group and related reports](../groups/baseline-blocked.md) · [Index](../README.md)
