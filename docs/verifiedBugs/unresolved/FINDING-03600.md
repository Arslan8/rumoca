# FINDING-03600: Not yet established as a bug or a false positive

| Field | Value |
|---|---|
| Verdict | unresolved |
| Scope / group | baseline-blocked |
| Model | Modelica.Electrical.PowerConverters.Examples.DCDC.ChopperStepDown.ChopperStepDown_R |
| Target | ILoad |
| Student classification | divisor-reachable-zero |
| Original report | [FINDING-chopperstepdown-r-iload-divzero-2.md](../../v2/bugs/FINDING-chopperstepdown-r-iload-divzero-2.md) — reviewed as `FINDING-03600-chopperstepdown-r-iload.md`, which a later run renamed |
| Original SHA-256 | 40d9da6c8fab04642b9339a50946e43c1f11ed164796026888bc04da1d1ba831 |

## What remains unresolved

The current Rumoca nominal run is tool-error, before any reported perturbation. This prevents causal attribution to this parameter. Source metadata was recovered, but none of the reviewed source proofs or counterexamples establishes this particular claim. A baseline failure/tool limitation is neither confirmation nor a false positive.

## Source evidence

Compiler/source-resolved declaration: `Electrical/PowerConverters/Examples/DCDC/ExampleTemplates/ChopperStepDown.mo:9`. Role: `parameter`; binding: `1.2`; effective min: `None`; effective max: `None`. 

[Electrical/PowerConverters/Examples/DCDC/ExampleTemplates/ChopperStepDown.mo — source snapshot](../evidence/sources/e37c1187feb5b49d-ChopperStepDown.mo)

```modelica
7:   parameter SI.Capacitance C=20e-6 "Smoothing capacitance";
8:   parameter Real dutyCycle=0.20 "Duty cycle";
9:   parameter SI.Current ILoad=1.2 "Load current";
10:   parameter SI.Resistance RLoad=V0/ILoad "Load resistance";
11:   parameter SI.Voltage V0=Vsource*dutyCycle "No-load output voltage";
12:   Modelica.Electrical.Analog.Sources.ConstantVoltage constantVoltage(final V=Vsource)
```


## Execution evidence

[Rumoca commands, return codes, integrity hashes, bounded output and metadata](../evidence/229a7168b91e7a47.json). Baseline: **tool-error**.

No independent runtime override was executed for this target in this audit; this is not a pass.

## Recommended action

Resolve the intended parameter domain and enclosing equations; check inherited bounds, final/protected status, guards and aliases. Construct an otherwise-valid source-level witness, establish a clean baseline in a capable engine, then retranslate at the witness and compare with the runtime override. For equality claims use the actual partner value. Do not apply a blanket min>0 fix yet.

## Scope and limitations

A source-level verdict addresses the reported declaration/claim, not every possible connected system. Tests cover 0–0.5 seconds and are not a proof of long-run stability. Shared instances are not distinct root causes. A missing bound, timeout, compiler error or failed nominal run alone never counts as a verified bug or a false positive. Fixes are proposals; no library/compiler implementation was changed.

[Group and related reports](../groups/baseline-blocked.md) · [Index](../README.md)
