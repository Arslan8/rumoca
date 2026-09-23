# FINDING-03567: Not yet established as a bug or a false positive

| Field | Value |
|---|---|
| Verdict | unresolved |
| Scope / group | baseline-blocked |
| Model | Modelica.Electrical.PowerConverters.Examples.DCDC.ChopperStepDown.ChopperStepDown_RL |
| Target | L |
| Student classification | physical-domain-unenforced |
| Original report | [FINDING-chopperstepdown-rl-l-zerolimit.md](../../v2/bugs/FINDING-chopperstepdown-rl-l-zerolimit.md) — reviewed as `FINDING-03567-chopperstepdown-rl-l.md`, which a later run renamed |
| Original SHA-256 | dbfbe7f8807b7b8c5d102b6a26c3af57478c64a8bc75b3fbfe2b78584f0200e6 |

## What remains unresolved

The current Rumoca nominal run is tool-error, before any reported perturbation. This prevents causal attribution to this parameter. Source metadata was recovered, but none of the reviewed source proofs or counterexamples establishes this particular claim. A baseline failure/tool limitation is neither confirmation nor a false positive.

## Source evidence

Compiler/source-resolved declaration: `Electrical/PowerConverters/Examples/DCDC/ExampleTemplates/ChopperStepDown.mo:6`. Role: `parameter`; binding: `0.025`; effective min: `None`; effective max: `None`. 

[Electrical/PowerConverters/Examples/DCDC/ExampleTemplates/ChopperStepDown.mo — source snapshot](../evidence/sources/e37c1187feb5b49d-ChopperStepDown.mo)

```modelica
4:   parameter SI.Frequency f=1000 "Switching frequency";
5:   parameter SI.Voltage Vsource=60 "Source voltage";
6:   parameter SI.Inductance L=25e-3 "Source inductance";
7:   parameter SI.Capacitance C=20e-6 "Smoothing capacitance";
8:   parameter Real dutyCycle=0.20 "Duty cycle";
9:   parameter SI.Current ILoad=1.2 "Load current";
```


## Execution evidence

[Rumoca commands, return codes, integrity hashes, bounded output and metadata](../evidence/93f2abf6f300aa3e.json). Baseline: **tool-error**.

No independent runtime override was executed for this target in this audit; this is not a pass.

## Recommended action

Resolve the intended parameter domain and enclosing equations; check inherited bounds, final/protected status, guards and aliases. Construct an otherwise-valid source-level witness, establish a clean baseline in a capable engine, then retranslate at the witness and compare with the runtime override. For equality claims use the actual partner value. Do not apply a blanket min>0 fix yet.

## Scope and limitations

A source-level verdict addresses the reported declaration/claim, not every possible connected system. Tests cover 0–0.5 seconds and are not a proof of long-run stability. Shared instances are not distinct root causes. A missing bound, timeout, compiler error or failed nominal run alone never counts as a verified bug or a false positive. Fixes are proposals; no library/compiler implementation was changed.

[Group and related reports](../groups/baseline-blocked.md) · [Index](../README.md)
