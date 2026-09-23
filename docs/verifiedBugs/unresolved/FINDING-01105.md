# FINDING-01105: Not yet established as a bug or a false positive

| Field | Value |
|---|---|
| Verdict | unresolved |
| Scope / group | baseline-blocked |
| Model | Modelica.Electrical.Batteries.Examples.SuperCapDischargeCharge |
| Target | superCap.Vnom |
| Student classification | divisor-reachable-zero |
| Original report | [FINDING-supercapdischargecharge-supercap-vnom-divzero.md](../../v2/bugs/FINDING-supercapdischargecharge-supercap-vnom-divzero.md) — reviewed as `FINDING-01105-supercapdischargecharge-supercap-vnom.md`, which a later run renamed |
| Original SHA-256 | fcbf63d0873a79d63e49a2bcabbc1593f49151db20a8a1340d86388fda118a6a |

## What remains unresolved

The current Rumoca nominal run is tool-error, before any reported perturbation. This prevents causal attribution to this parameter. Source metadata was recovered, but none of the reviewed source proofs or counterexamples establishes this particular claim. A baseline failure/tool limitation is neither confirmation nor a false positive.

## Source evidence

Compiler/source-resolved declaration: `Electrical/Batteries/BatteryStacks/SuperCap.mo:5`. Role: `parameter`; binding: `48`; effective min: `None`; effective max: `None`. 

[Electrical/Batteries/BatteryStacks/SuperCap.mo — source snapshot](../evidence/sources/d1694703fa435abc-SuperCap.mo)

```modelica
3:   extends Modelica.Electrical.Analog.Interfaces.TwoPin;
4:   SI.Current i = p.i "Current into the supercap";
5:   parameter SI.Voltage Vnom "Nominal voltage";
6:   parameter SI.Voltage V0=Vnom "Initial voltage";
7:   parameter SI.Capacitance C "Capacitance";
8:   parameter SI.ElectricCharge Qnom=C*Vnom "Nominal charge";
```


## Execution evidence

[Rumoca commands, return codes, integrity hashes, bounded output and metadata](../evidence/19f2dc9fcbf64c3b.json). Baseline: **tool-error**.

No independent runtime override was executed for this target in this audit; this is not a pass.

## Recommended action

Resolve the intended parameter domain and enclosing equations; check inherited bounds, final/protected status, guards and aliases. Construct an otherwise-valid source-level witness, establish a clean baseline in a capable engine, then retranslate at the witness and compare with the runtime override. For equality claims use the actual partner value. Do not apply a blanket min>0 fix yet.

## Scope and limitations

A source-level verdict addresses the reported declaration/claim, not every possible connected system. Tests cover 0–0.5 seconds and are not a proof of long-run stability. Shared instances are not distinct root causes. A missing bound, timeout, compiler error or failed nominal run alone never counts as a verified bug or a false positive. Fixes are proposals; no library/compiler implementation was changed.

[Group and related reports](../groups/baseline-blocked.md) · [Index](../README.md)
