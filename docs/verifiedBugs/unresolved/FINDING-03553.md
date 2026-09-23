# FINDING-03553: Not yet established as a bug or a false positive

| Field | Value |
|---|---|
| Verdict | unresolved |
| Scope / group | baseline-blocked |
| Model | Modelica.Electrical.PowerConverters.Examples.DCDC.ChopperBuckBoost.ChopperBuckBoost_DutyCycle |
| Target | dcdc.GoffDiode |
| Student classification | physical-domain-unenforced |
| Original report | [FINDING-chopperbuckboost-dutycycle-dcdc-goffdiode-zerolimit.md](../../v2/bugs/FINDING-chopperbuckboost-dutycycle-dcdc-goffdiode-zerolimit.md) — reviewed as `FINDING-03553-chopperbuckboost-dutycycle-dcdc-goffdiode.md`, which a later run renamed |
| Original SHA-256 | 618a5a3c06c51a4a98d7c91fa09fb8988b834ec7f3be7494b470afceb6aeca93 |

## What remains unresolved

The current Rumoca nominal run is tool-error, before any reported perturbation. This prevents causal attribution to this parameter. Source metadata was recovered, but none of the reviewed source proofs or counterexamples establishes this particular claim. A baseline failure/tool limitation is neither confirmation nor a false positive.

## Source evidence

Compiler/source-resolved declaration: `Electrical/PowerConverters/DCDC/ChopperBuckBoost.mo:14`. Role: `parameter`; binding: `1e-05`; effective min: `None`; effective max: `None`. 

[Electrical/PowerConverters/DCDC/ChopperBuckBoost.mo — source snapshot](../evidence/sources/8af07a22ec048ec7-ChopperBuckBoost.mo)

```modelica
12:   parameter Modelica.Units.SI.Resistance RonDiode=1e-05
13:     "Diode closed resistance";
14:   parameter Modelica.Units.SI.Conductance GoffDiode=1e-05
15:     "Diode opened conductance";
16:   parameter Modelica.Units.SI.Voltage VkneeDiode=0
17:     "Diode threshold voltage";
```


## Execution evidence

[Rumoca commands, return codes, integrity hashes, bounded output and metadata](../evidence/4c98b27115f983e5.json). Baseline: **tool-error**.

No independent runtime override was executed for this target in this audit; this is not a pass.

## Recommended action

Resolve the intended parameter domain and enclosing equations; check inherited bounds, final/protected status, guards and aliases. Construct an otherwise-valid source-level witness, establish a clean baseline in a capable engine, then retranslate at the witness and compare with the runtime override. For equality claims use the actual partner value. Do not apply a blanket min>0 fix yet.

## Scope and limitations

A source-level verdict addresses the reported declaration/claim, not every possible connected system. Tests cover 0–0.5 seconds and are not a proof of long-run stability. Shared instances are not distinct root causes. A missing bound, timeout, compiler error or failed nominal run alone never counts as a verified bug or a false positive. Fixes are proposals; no library/compiler implementation was changed.

[Group and related reports](../groups/baseline-blocked.md) · [Index](../README.md)
