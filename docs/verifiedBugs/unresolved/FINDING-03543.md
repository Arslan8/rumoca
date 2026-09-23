# FINDING-03543: Not yet established as a bug or a false positive

| Field | Value |
|---|---|
| Verdict | unresolved |
| Scope / group | baseline-blocked |
| Model | Modelica.Electrical.PowerConverters.Examples.DCAC.SinglePhaseTwoLevel.SinglePhaseTwoLevel_R |
| Target | f |
| Student classification | divisor-reachable-zero |
| Original report | `FINDING-03543-singlephasetwolevel-r-f.md` — [withdrawn](../../v2/bugs/withdrawn.md); a later run no longer makes this claim |
| Original SHA-256 | 8c960f5f843215b28c864511da374805e58a68b1c5a314f4691fa3ae40e706e1 |

## What remains unresolved

The current Rumoca nominal run is tool-error, before any reported perturbation. This prevents causal attribution to this parameter. Source metadata was recovered, but none of the reviewed source proofs or counterexamples establishes this particular claim. A baseline failure/tool limitation is neither confirmation nor a false positive.

## Source evidence

Compiler/source-resolved declaration: `Electrical/PowerConverters/Examples/DCAC/ExampleTemplates/SinglePhaseTwoLevel.mo:5`. Role: `parameter`; binding: `1000`; effective min: `None`; effective max: `None`. 

[Electrical/PowerConverters/Examples/DCAC/ExampleTemplates/SinglePhaseTwoLevel.mo — source snapshot](../evidence/sources/ee3135b4fdd3c377-SinglePhaseTwoLevel.mo)

```modelica
3:   "Single-phase two level inverter including control"
4:   extends Icons.ExampleTemplate;
5:   parameter SI.Frequency f=1000 "Switching frequency";
6:   Modelica.Electrical.Analog.Sources.ConstantVoltage constantVoltage_n(
7:       V=50) annotation (Placement(transformation(
8:         extent={{-10,-10},{10,10}},
```


## Execution evidence

[Rumoca commands, return codes, integrity hashes, bounded output and metadata](../evidence/4ad8e8cc710430a9.json). Baseline: **tool-error**.

No independent runtime override was executed for this target in this audit; this is not a pass.

## Recommended action

Resolve the intended parameter domain and enclosing equations; check inherited bounds, final/protected status, guards and aliases. Construct an otherwise-valid source-level witness, establish a clean baseline in a capable engine, then retranslate at the witness and compare with the runtime override. For equality claims use the actual partner value. Do not apply a blanket min>0 fix yet.

## Scope and limitations

A source-level verdict addresses the reported declaration/claim, not every possible connected system. Tests cover 0–0.5 seconds and are not a proof of long-run stability. Shared instances are not distinct root causes. A missing bound, timeout, compiler error or failed nominal run alone never counts as a verified bug or a false positive. Fixes are proposals; no library/compiler implementation was changed.

[Group and related reports](../groups/baseline-blocked.md) · [Index](../README.md)
