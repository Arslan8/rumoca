# FINDING-03550: Not yet established as a bug or a false positive

| Field | Value |
|---|---|
| Verdict | unresolved |
| Scope / group | baseline-blocked |
| Model | Modelica.Electrical.PowerConverters.Examples.DCDC.ChopperBuckBoost.ChopperBuckBoost_DutyCycle |
| Target | dcdc.RonTransistor |
| Student classification | physical-domain-unenforced |
| Original report | [FINDING-chopperbuckboost-dutycycle-dcdc-rontransistor-ruleoff.md](../../v2/bugs/FINDING-chopperbuckboost-dutycycle-dcdc-rontransistor-ruleoff.md) — reviewed as `FINDING-03550-chopperbuckboost-dutycycle-dcdc-rontransistor.md`, which a later run renamed |
| Original SHA-256 | 33104ca552dee586c3fa258167b62f7474d850da7257e1bd8b634d9ba9861bc7 |

## What remains unresolved

The current Rumoca nominal run is tool-error, before any reported perturbation. This prevents causal attribution to this parameter. Source metadata was recovered, but none of the reviewed source proofs or counterexamples establishes this particular claim. A baseline failure/tool limitation is neither confirmation nor a false positive.

## Source evidence

Compiler/source-resolved declaration: `Electrical/PowerConverters/DCDC/ChopperBuckBoost.mo:6`. Role: `parameter`; binding: `1e-05`; effective min: `None`; effective max: `None`. 

[Electrical/PowerConverters/DCDC/ChopperBuckBoost.mo — source snapshot](../evidence/sources/8af07a22ec048ec7-ChopperBuckBoost.mo)

```modelica
4:   extends Modelica.Electrical.PowerConverters.Interfaces.DCDC.DCtwoPin2;
5:   extends Modelica.Electrical.Analog.Interfaces.ConditionalHeatPort(final T=293.15);
6:   parameter Modelica.Units.SI.Resistance RonTransistor=1e-05
7:     "Transistor closed resistance";
8:   parameter Modelica.Units.SI.Conductance GoffTransistor=1e-05
9:     "Transistor opened conductance";
```


## Execution evidence

[Rumoca commands, return codes, integrity hashes, bounded output and metadata](../evidence/4c98b27115f983e5.json). Baseline: **tool-error**.

No independent runtime override was executed for this target in this audit; this is not a pass.

## Recommended action

Resolve the intended parameter domain and enclosing equations; check inherited bounds, final/protected status, guards and aliases. Construct an otherwise-valid source-level witness, establish a clean baseline in a capable engine, then retranslate at the witness and compare with the runtime override. For equality claims use the actual partner value. Do not apply a blanket min>0 fix yet.

## Scope and limitations

A source-level verdict addresses the reported declaration/claim, not every possible connected system. Tests cover 0–0.5 seconds and are not a proof of long-run stability. Shared instances are not distinct root causes. A missing bound, timeout, compiler error or failed nominal run alone never counts as a verified bug or a false positive. Fixes are proposals; no library/compiler implementation was changed.

[Group and related reports](../groups/baseline-blocked.md) · [Index](../README.md)
