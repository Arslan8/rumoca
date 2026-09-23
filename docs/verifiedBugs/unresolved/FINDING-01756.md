# FINDING-01756: Not yet established as a bug or a false positive

| Field | Value |
|---|---|
| Verdict | unresolved |
| Scope / group | baseline-blocked |
| Model | Modelica.Electrical.Machines.Examples.InductionMachines.IMC_Inverter |
| Target | JLoad |
| Student classification | physical-domain-unenforced |
| Original report | [FINDING-imc-inverter-jload-zerolimit.md](../../v2/bugs/FINDING-imc-inverter-jload-zerolimit.md) — reviewed as `FINDING-01756-imc-inverter-jload.md`, which a later run renamed |
| Original SHA-256 | 4b33dbd1964d8be96932aa64a0dacc5dbce4227e078140078b79452a0a78178c |

## What remains unresolved

The current Rumoca nominal run is tool-error, before any reported perturbation. This prevents causal attribution to this parameter. Source metadata was recovered, but none of the reviewed source proofs or counterexamples establishes this particular claim. A baseline failure/tool limitation is neither confirmation nor a false positive.

## Source evidence

Compiler/source-resolved declaration: `Electrical/Machines/Examples/InductionMachines/IMC_Inverter.mo:13`. Role: `parameter`; binding: `0.29`; effective min: `None`; effective max: `None`. 

[Electrical/Machines/Examples/InductionMachines/IMC_Inverter.mo — source snapshot](../evidence/sources/2a51068c12e8e031-IMC_Inverter.mo)

```modelica
11:   parameter SI.Torque TLoad=161.4 "Nominal load torque";
12:   parameter SI.Time tStep=1.2 "Time of load torque step";
13:   parameter SI.Inertia JLoad=0.29
14:     "Load's moment of inertia";
15:   Machines.BasicMachines.InductionMachines.IM_SquirrelCage aimc(
16:     p=aimcData.p,
```


## Execution evidence

[Rumoca commands, return codes, integrity hashes, bounded output and metadata](../evidence/8e3358d86efa2aa5.json). Baseline: **tool-error**.

No independent runtime override was executed for this target in this audit; this is not a pass.

## Recommended action

Resolve the intended parameter domain and enclosing equations; check inherited bounds, final/protected status, guards and aliases. Construct an otherwise-valid source-level witness, establish a clean baseline in a capable engine, then retranslate at the witness and compare with the runtime override. For equality claims use the actual partner value. Do not apply a blanket min>0 fix yet.

## Scope and limitations

A source-level verdict addresses the reported declaration/claim, not every possible connected system. Tests cover 0–0.5 seconds and are not a proof of long-run stability. Shared instances are not distinct root causes. A missing bound, timeout, compiler error or failed nominal run alone never counts as a verified bug or a false positive. Fixes are proposals; no library/compiler implementation was changed.

[Group and related reports](../groups/baseline-blocked.md) · [Index](../README.md)
