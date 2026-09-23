# FINDING-03568: Not yet established as a bug or a false positive

| Field | Value |
|---|---|
| Verdict | unresolved |
| Scope / group | baseline-blocked |
| Model | Modelica.Electrical.PowerConverters.Examples.DCDC.ChopperStepDown.ChopperStepDown_RL |
| Target | C |
| Student classification | physical-bound-permits-zero |
| Original report | [FINDING-chopperstepdown-rl-c-zerolimit.md](../../v2/bugs/FINDING-chopperstepdown-rl-c-zerolimit.md) — reviewed as `FINDING-03568-chopperstepdown-rl-c.md`, which a later run renamed |
| Original SHA-256 | a080a241b459e529f0c2fc7060878908a4c4b7e9e16547e695778fe225168ab4 |

## What remains unresolved

The current Rumoca nominal run is tool-error, before any reported perturbation. This prevents causal attribution to this parameter. Source metadata was recovered, but none of the reviewed source proofs or counterexamples establishes this particular claim. A baseline failure/tool limitation is neither confirmation nor a false positive.

## Source evidence

Compiler/source-resolved declaration: `Electrical/PowerConverters/Examples/DCDC/ExampleTemplates/ChopperStepDown.mo:7`. Role: `parameter`; binding: `2e-05`; effective min: `0`; effective max: `None`. 

[Electrical/PowerConverters/Examples/DCDC/ExampleTemplates/ChopperStepDown.mo — source snapshot](../evidence/sources/e37c1187feb5b49d-ChopperStepDown.mo)

```modelica
5:   parameter SI.Voltage Vsource=60 "Source voltage";
6:   parameter SI.Inductance L=25e-3 "Source inductance";
7:   parameter SI.Capacitance C=20e-6 "Smoothing capacitance";
8:   parameter Real dutyCycle=0.20 "Duty cycle";
9:   parameter SI.Current ILoad=1.2 "Load current";
10:   parameter SI.Resistance RLoad=V0/ILoad "Load resistance";
```


## Execution evidence

[Rumoca commands, return codes, integrity hashes, bounded output and metadata](../evidence/93f2abf6f300aa3e.json). Baseline: **tool-error**.

No independent runtime override was executed for this target in this audit; this is not a pass.

## Recommended action

Resolve the intended parameter domain and enclosing equations; check inherited bounds, final/protected status, guards and aliases. Construct an otherwise-valid source-level witness, establish a clean baseline in a capable engine, then retranslate at the witness and compare with the runtime override. For equality claims use the actual partner value. Do not apply a blanket min>0 fix yet.

## Scope and limitations

A source-level verdict addresses the reported declaration/claim, not every possible connected system. Tests cover 0–0.5 seconds and are not a proof of long-run stability. Shared instances are not distinct root causes. A missing bound, timeout, compiler error or failed nominal run alone never counts as a verified bug or a false positive. Fixes are proposals; no library/compiler implementation was changed.

[Group and related reports](../groups/baseline-blocked.md) · [Index](../README.md)
