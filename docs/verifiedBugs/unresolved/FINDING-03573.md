# FINDING-03573: Not yet established as a bug or a false positive

| Field | Value |
|---|---|
| Verdict | unresolved |
| Scope / group | baseline-blocked |
| Model | Modelica.Electrical.PowerConverters.Examples.DCDC.ChopperStepDown.ChopperStepDown_RL |
| Target | chopperStepDown.GoffDiode |
| Student classification | physical-bound-permits-zero |
| Original report | [FINDING-chopperstepdown-rl-chopperstepdown-goffdiode-zerolimit.md](../../v2/bugs/FINDING-chopperstepdown-rl-chopperstepdown-goffdiode-zerolimit.md) — reviewed as `FINDING-03573-chopperstepdown-rl-chopperstepdown-goffdiode.md`, which a later run renamed |
| Original SHA-256 | 402b1f6f2eb32bfe11441ab68a70ff7e0f8a7737e61f66198e420b5a7d83edab |

## What remains unresolved

The current Rumoca nominal run is tool-error, before any reported perturbation. This prevents causal attribution to this parameter. Source metadata was recovered, but none of the reviewed source proofs or counterexamples establishes this particular claim. A baseline failure/tool limitation is neither confirmation nor a false positive.

## Source evidence

Compiler/source-resolved declaration: `Electrical/PowerConverters/DCDC/ChopperStepDown.mo:13`. Role: `parameter`; binding: `1e-05`; effective min: `0`; effective max: `None`. 

[Electrical/PowerConverters/DCDC/ChopperStepDown.mo — source snapshot](../evidence/sources/22f96ecb9781d221-ChopperStepDown.mo)

```modelica
11:   parameter SI.Resistance RonDiode(final min=0) = 1e-05
12:     "Closed diode resistance";
13:   parameter SI.Conductance GoffDiode(final min=0) = 1e-05
14:     "Opened diode conductance";
15:   parameter SI.Voltage VkneeDiode(final min=0) = 0
16:     "Diode forward threshold voltage";
```


## Execution evidence

[Rumoca commands, return codes, integrity hashes, bounded output and metadata](../evidence/93f2abf6f300aa3e.json). Baseline: **tool-error**.

No independent runtime override was executed for this target in this audit; this is not a pass.

## Recommended action

Resolve the intended parameter domain and enclosing equations; check inherited bounds, final/protected status, guards and aliases. Construct an otherwise-valid source-level witness, establish a clean baseline in a capable engine, then retranslate at the witness and compare with the runtime override. For equality claims use the actual partner value. Do not apply a blanket min>0 fix yet.

## Scope and limitations

A source-level verdict addresses the reported declaration/claim, not every possible connected system. Tests cover 0–0.5 seconds and are not a proof of long-run stability. Shared instances are not distinct root causes. A missing bound, timeout, compiler error or failed nominal run alone never counts as a verified bug or a false positive. Fixes are proposals; no library/compiler implementation was changed.

[Group and related reports](../groups/baseline-blocked.md) · [Index](../README.md)
