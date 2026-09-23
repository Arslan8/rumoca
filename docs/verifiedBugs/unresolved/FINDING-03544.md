# FINDING-03544: Not yet established as a bug or a false positive

| Field | Value |
|---|---|
| Verdict | unresolved |
| Scope / group | baseline-blocked |
| Model | Modelica.Electrical.PowerConverters.Examples.DCDC.ChopperBuckBoost.ChopperBuckBoost_DutyCycle |
| Target | RiLV |
| Student classification | physical-domain-unenforced |
| Original report | [FINDING-chopperbuckboost-dutycycle-rilv-zerolimit.md](../../v2/bugs/FINDING-chopperbuckboost-dutycycle-rilv-zerolimit.md) — reviewed as `FINDING-03544-chopperbuckboost-dutycycle-rilv.md`, which a later run renamed |
| Original SHA-256 | 9021e80282d5948052aa5ed71d857b701ab05ab07dfc6a8c532685045460cedb |

## What remains unresolved

The current Rumoca nominal run is tool-error, before any reported perturbation. This prevents causal attribution to this parameter. Source metadata was recovered, but none of the reviewed source proofs or counterexamples establishes this particular claim. A baseline failure/tool limitation is neither confirmation nor a false positive.

## Source evidence

Compiler/source-resolved declaration: `Electrical/PowerConverters/Examples/DCDC/ExampleTemplates/ChopperBuckBoost.mo:5`. Role: `parameter`; binding: `0.01`; effective min: `None`; effective max: `None`. 

[Electrical/PowerConverters/Examples/DCDC/ExampleTemplates/ChopperBuckBoost.mo — source snapshot](../evidence/sources/19afeb24726d89ac-ChopperBuckBoost.mo)

```modelica
3:   extends Modelica.Electrical.PowerConverters.Icons.ExampleTemplate;
4:   parameter Modelica.Units.SI.Voltage VLV=12 "LV voltage";
5:   parameter Modelica.Units.SI.Resistance RiLV=0.01 "LV inner resistance";
6:   parameter Modelica.Units.SI.Voltage VHV=24 "HV voltage";
7:   parameter Modelica.Units.SI.Resistance RiHV=0.01 "HV inner resistance";
8:   parameter Modelica.Units.SI.Capacitance CLV=500e-6 "Low voltage capacitance";
```


## Execution evidence

[Rumoca commands, return codes, integrity hashes, bounded output and metadata](../evidence/4c98b27115f983e5.json). Baseline: **tool-error**.

No independent runtime override was executed for this target in this audit; this is not a pass.

## Recommended action

Resolve the intended parameter domain and enclosing equations; check inherited bounds, final/protected status, guards and aliases. Construct an otherwise-valid source-level witness, establish a clean baseline in a capable engine, then retranslate at the witness and compare with the runtime override. For equality claims use the actual partner value. Do not apply a blanket min>0 fix yet.

## Scope and limitations

A source-level verdict addresses the reported declaration/claim, not every possible connected system. Tests cover 0–0.5 seconds and are not a proof of long-run stability. Shared instances are not distinct root causes. A missing bound, timeout, compiler error or failed nominal run alone never counts as a verified bug or a false positive. Fixes are proposals; no library/compiler implementation was changed.

[Group and related reports](../groups/baseline-blocked.md) · [Index](../README.md)
