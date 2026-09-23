# FINDING-01100: Not yet established as a bug or a false positive

| Field | Value |
|---|---|
| Verdict | unresolved |
| Scope / group | baseline-blocked |
| Model | Modelica.Electrical.Batteries.Examples.SuperCapDischargeCharge |
| Target | superCap.Qnom |
| Student classification | physical-domain-unenforced |
| Original report | [FINDING-supercapdischargecharge-supercap-qnom-intent.md](../../v2/bugs/FINDING-supercapdischargecharge-supercap-qnom-intent.md) — reviewed as `FINDING-01100-supercapdischargecharge-supercap-qnom.md`, which a later run renamed |
| Original SHA-256 | c4454567bfde597923246ba6f95b92b98e468c6955d93fc69d0ff78532d2c916 |

## What remains unresolved

The current Rumoca nominal run is tool-error, before any reported perturbation. This prevents causal attribution to this parameter. Source metadata was recovered, but none of the reviewed source proofs or counterexamples establishes this particular claim. A baseline failure/tool limitation is neither confirmation nor a false positive.

## Source evidence

Compiler/source-resolved declaration: `Electrical/Batteries/BatteryStacks/SuperCap.mo:8`. Role: `parameter`; binding: `24000`; effective min: `None`; effective max: `None`. 

[Electrical/Batteries/BatteryStacks/SuperCap.mo — source snapshot](../evidence/sources/d1694703fa435abc-SuperCap.mo)

```modelica
6:   parameter SI.Voltage V0=Vnom "Initial voltage";
7:   parameter SI.Capacitance C "Capacitance";
8:   parameter SI.ElectricCharge Qnom=C*Vnom "Nominal charge";
9:   parameter SI.Resistance Rs "Series resistance";
10:   parameter SI.Temperature T_ref=293.15 "Reference temperature";
11:   parameter SI.LinearTemperatureCoefficient alpha=0 "Temperature coefficient of resistance at T_ref";
```


## Execution evidence

[Rumoca commands, return codes, integrity hashes, bounded output and metadata](../evidence/19f2dc9fcbf64c3b.json). Baseline: **tool-error**.

No independent runtime override was executed for this target in this audit; this is not a pass.

## Recommended action

Resolve the intended parameter domain and enclosing equations; check inherited bounds, final/protected status, guards and aliases. Construct an otherwise-valid source-level witness, establish a clean baseline in a capable engine, then retranslate at the witness and compare with the runtime override. For equality claims use the actual partner value. Do not apply a blanket min>0 fix yet.

## Scope and limitations

A source-level verdict addresses the reported declaration/claim, not every possible connected system. Tests cover 0–0.5 seconds and are not a proof of long-run stability. Shared instances are not distinct root causes. A missing bound, timeout, compiler error or failed nominal run alone never counts as a verified bug or a false positive. Fixes are proposals; no library/compiler implementation was changed.

[Group and related reports](../groups/baseline-blocked.md) · [Index](../README.md)
