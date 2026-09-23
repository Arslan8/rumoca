# FINDING-03580: Not yet established as a bug or a false positive

| Field | Value |
|---|---|
| Verdict | unresolved |
| Scope / group | baseline-blocked |
| Model | Modelica.Electrical.PowerConverters.Examples.DCDC.ChopperStepDown.ChopperStepDown_RL |
| Target | LLoad |
| Student classification | physical-domain-unenforced |
| Original report | [FINDING-chopperstepdown-rl-lload-zerolimit.md](../../v2/bugs/FINDING-chopperstepdown-rl-lload-zerolimit.md) — reviewed as `FINDING-03580-chopperstepdown-rl-lload.md`, which a later run renamed |
| Original SHA-256 | 37bfb5b88f3ffeade25239633bba069c97b0ea661da4e0d6e74c6655b664caf7 |

## What remains unresolved

The current Rumoca nominal run is tool-error, before any reported perturbation. This prevents causal attribution to this parameter. Source metadata was recovered, but none of the reviewed source proofs or counterexamples establishes this particular claim. A baseline failure/tool limitation is neither confirmation nor a false positive.

## Source evidence

Compiler/source-resolved declaration: `Electrical/PowerConverters/Examples/DCDC/ChopperStepDown/ChopperStepDown_RL.mo:5`. Role: `parameter`; binding: `0.025`; effective min: `None`; effective max: `None`. 

[Electrical/PowerConverters/Examples/DCDC/ChopperStepDown/ChopperStepDown_RL.mo — source snapshot](../evidence/sources/45379c69776f9fe1-ChopperStepDown_RL.mo)

```modelica
3:   extends ExampleTemplates.ChopperStepDown(signalPWM(useConstantDutyCycle=false));
4:   extends Modelica.Icons.Example;
5:   parameter SI.Inductance LLoad=0.025 "Load inductance";
6:   Modelica.Electrical.Analog.Basic.Resistor loadResistor(R=RLoad)
7:     annotation (
8:       Placement(transformation(
```


## Execution evidence

[Rumoca commands, return codes, integrity hashes, bounded output and metadata](../evidence/93f2abf6f300aa3e.json). Baseline: **tool-error**.

No independent runtime override was executed for this target in this audit; this is not a pass.

## Recommended action

Resolve the intended parameter domain and enclosing equations; check inherited bounds, final/protected status, guards and aliases. Construct an otherwise-valid source-level witness, establish a clean baseline in a capable engine, then retranslate at the witness and compare with the runtime override. For equality claims use the actual partner value. Do not apply a blanket min>0 fix yet.

## Scope and limitations

A source-level verdict addresses the reported declaration/claim, not every possible connected system. Tests cover 0–0.5 seconds and are not a proof of long-run stability. Shared instances are not distinct root causes. A missing bound, timeout, compiler error or failed nominal run alone never counts as a verified bug or a false positive. Fixes are proposals; no library/compiler implementation was changed.

[Group and related reports](../groups/baseline-blocked.md) · [Index](../README.md)
