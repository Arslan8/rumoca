# FINDING-04697: Not yet established as a bug or a false positive

| Field | Value |
|---|---|
| Verdict | unresolved |
| Scope / group | baseline-blocked |
| Model | Modelica.Thermal.FluidHeatFlow.Examples.TwoTanks |
| Target | openTank1.ATank |
| Student classification | physical-domain-unenforced |
| Original report | [FINDING-twotanks-opentank1-atank-unbounded.md](../../v2/bugs/FINDING-twotanks-opentank1-atank-unbounded.md) — reviewed as `FINDING-04697-twotanks-opentank1-atank.md`, which a later run renamed |
| Original SHA-256 | cd5a7856a51589978c2445940b89b7a939c3227ad21df97bac07adfd2c6073f9 |

## What remains unresolved

The current Rumoca nominal run is reported-failure, before any reported perturbation. This prevents causal attribution to this parameter. Source metadata was recovered, but none of the reviewed source proofs or counterexamples establishes this particular claim. A baseline failure/tool limitation is neither confirmation nor a false positive.

## Source evidence

Compiler/source-resolved declaration: `Thermal/FluidHeatFlow/Components/OpenTank.mo:5`. Role: `parameter`; binding: `1`; effective min: `None`; effective max: `None`. 

[Thermal/FluidHeatFlow/Components/OpenTank.mo — source snapshot](../evidence/sources/4432b03925a57aa2-OpenTank.mo)

```modelica
3:   extends FluidHeatFlow.BaseClasses.SinglePortBottom(final Exchange=true);
4: 
5:   parameter SI.Area ATank(start=1) "Cross section of tank";
6:   parameter SI.Length hTank(start=1) "Height of tank";
7:   parameter SI.Pressure pAmbient(start=0) "Ambient pressure";
8:   parameter SI.Acceleration g(final min=0)=Modelica.Constants.g_n "Gravitation";
```


## Execution evidence

[Rumoca commands, return codes, integrity hashes, bounded output and metadata](../evidence/5866a31e0c70d3ca.json). Baseline: **reported-failure**.

No independent runtime override was executed for this target in this audit; this is not a pass.

## Recommended action

Resolve the intended parameter domain and enclosing equations; check inherited bounds, final/protected status, guards and aliases. Construct an otherwise-valid source-level witness, establish a clean baseline in a capable engine, then retranslate at the witness and compare with the runtime override. For equality claims use the actual partner value. Do not apply a blanket min>0 fix yet.

## Scope and limitations

A source-level verdict addresses the reported declaration/claim, not every possible connected system. Tests cover 0–0.5 seconds and are not a proof of long-run stability. Shared instances are not distinct root causes. A missing bound, timeout, compiler error or failed nominal run alone never counts as a verified bug or a false positive. Fixes are proposals; no library/compiler implementation was changed.

[Group and related reports](../groups/baseline-blocked.md) · [Index](../README.md)
