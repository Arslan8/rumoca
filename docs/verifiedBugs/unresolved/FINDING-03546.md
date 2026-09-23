# FINDING-03546: Not yet established as a bug or a false positive

| Field | Value |
|---|---|
| Verdict | unresolved |
| Scope / group | baseline-blocked |
| Model | Modelica.Electrical.PowerConverters.Examples.DCDC.ChopperBuckBoost.ChopperBuckBoost_DutyCycle |
| Target | CLV |
| Student classification | physical-bound-permits-zero |
| Original report | [FINDING-chopperbuckboost-dutycycle-clv-zerolimit.md](../../v2/bugs/FINDING-chopperbuckboost-dutycycle-clv-zerolimit.md) — reviewed as `FINDING-03546-chopperbuckboost-dutycycle-clv.md`, which a later run renamed |
| Original SHA-256 | 917cd4e232930f85a73ccee9395e64b0de095c55cefff021f3c206f1f616dd30 |

## What remains unresolved

The current Rumoca nominal run is tool-error, before any reported perturbation. This prevents causal attribution to this parameter. Source metadata was recovered, but none of the reviewed source proofs or counterexamples establishes this particular claim. A baseline failure/tool limitation is neither confirmation nor a false positive.

## Source evidence

Compiler/source-resolved declaration: `Electrical/PowerConverters/Examples/DCDC/ExampleTemplates/ChopperBuckBoost.mo:8`. Role: `parameter`; binding: `0.0005`; effective min: `0`; effective max: `None`. 

[Electrical/PowerConverters/Examples/DCDC/ExampleTemplates/ChopperBuckBoost.mo — source snapshot](../evidence/sources/19afeb24726d89ac-ChopperBuckBoost.mo)

```modelica
6:   parameter Modelica.Units.SI.Voltage VHV=24 "HV voltage";
7:   parameter Modelica.Units.SI.Resistance RiHV=0.01 "HV inner resistance";
8:   parameter Modelica.Units.SI.Capacitance CLV=500e-6 "Low voltage capacitance";
9:   parameter Modelica.Units.SI.Capacitance CHV=250e-6 "High voltage capacitance";
10:   parameter Modelica.Units.SI.Inductance L=10e-6 "Inductance";
11:   parameter Modelica.Units.SI.Resistance R=1e-3 "Resistance of inductor";
```


## Execution evidence

[Rumoca commands, return codes, integrity hashes, bounded output and metadata](../evidence/4c98b27115f983e5.json). Baseline: **tool-error**.

No independent runtime override was executed for this target in this audit; this is not a pass.

## Recommended action

Resolve the intended parameter domain and enclosing equations; check inherited bounds, final/protected status, guards and aliases. Construct an otherwise-valid source-level witness, establish a clean baseline in a capable engine, then retranslate at the witness and compare with the runtime override. For equality claims use the actual partner value. Do not apply a blanket min>0 fix yet.

## Scope and limitations

A source-level verdict addresses the reported declaration/claim, not every possible connected system. Tests cover 0–0.5 seconds and are not a proof of long-run stability. Shared instances are not distinct root causes. A missing bound, timeout, compiler error or failed nominal run alone never counts as a verified bug or a false positive. Fixes are proposals; no library/compiler implementation was changed.

[Group and related reports](../groups/baseline-blocked.md) · [Index](../README.md)
