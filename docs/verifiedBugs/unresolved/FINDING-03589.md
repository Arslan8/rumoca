# FINDING-03589: Not yet established as a bug or a false positive

| Field | Value |
|---|---|
| Verdict | unresolved |
| Scope / group | baseline-blocked |
| Model | Modelica.Electrical.PowerConverters.Examples.DCDC.ChopperStepDown.ChopperStepDown_R |
| Target | chopperStepDown.GoffTransistor |
| Student classification | physical-domain-unenforced |
| Original report | [FINDING-chopperstepdown-r-chopperstepdown-gofftransistor-zerolimit.md](../../v2/bugs/FINDING-chopperstepdown-r-chopperstepdown-gofftransistor-zerolimit.md) — reviewed as `FINDING-03589-chopperstepdown-r-chopperstepdown-gofftransistor.md`, which a later run renamed |
| Original SHA-256 | d3cc4a805a5cad2bef2fde4b68bf14c4b8934b832022e9df6e467bd205b80f4c |

## What remains unresolved

The current Rumoca nominal run is tool-error, before any reported perturbation. This prevents causal attribution to this parameter. Source metadata was recovered, but none of the reviewed source proofs or counterexamples establishes this particular claim. A baseline failure/tool limitation is neither confirmation nor a false positive.

## Source evidence

Compiler/source-resolved declaration: `Electrical/PowerConverters/DCDC/ChopperStepDown.mo:7`. Role: `parameter`; binding: `1e-05`; effective min: `None`; effective max: `None`. 

[Electrical/PowerConverters/DCDC/ChopperStepDown.mo — source snapshot](../evidence/sources/22f96ecb9781d221-ChopperStepDown.mo)

```modelica
5:   parameter SI.Resistance RonTransistor=1e-05
6:     "Transistor closed resistance";
7:   parameter SI.Conductance GoffTransistor=1e-05
8:     "Transistor opened conductance";
9:   parameter SI.Voltage VkneeTransistor=0
10:     "Transistor threshold voltage";
```


## Execution evidence

[Rumoca commands, return codes, integrity hashes, bounded output and metadata](../evidence/229a7168b91e7a47.json). Baseline: **tool-error**.

No independent runtime override was executed for this target in this audit; this is not a pass.

## Recommended action

Resolve the intended parameter domain and enclosing equations; check inherited bounds, final/protected status, guards and aliases. Construct an otherwise-valid source-level witness, establish a clean baseline in a capable engine, then retranslate at the witness and compare with the runtime override. For equality claims use the actual partner value. Do not apply a blanket min>0 fix yet.

## Scope and limitations

A source-level verdict addresses the reported declaration/claim, not every possible connected system. Tests cover 0–0.5 seconds and are not a proof of long-run stability. Shared instances are not distinct root causes. A missing bound, timeout, compiler error or failed nominal run alone never counts as a verified bug or a false positive. Fixes are proposals; no library/compiler implementation was changed.

[Group and related reports](../groups/baseline-blocked.md) · [Index](../README.md)
