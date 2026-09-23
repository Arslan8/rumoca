# FINDING-03267: Not yet established as a bug or a false positive

| Field | Value |
|---|---|
| Verdict | unresolved |
| Scope / group | baseline-blocked |
| Model | Modelica.Electrical.PowerConverters.Examples.ACDC.RectifierBridge2Pulse.ThyristorBridge2Pulse_RL |
| Target | R |
| Student classification | physical-domain-unenforced |
| Original report | [FINDING-thyristorbridge2pulse-rl-r-zerolimit.md](../../v2/bugs/FINDING-thyristorbridge2pulse-rl-r-zerolimit.md) — reviewed as `FINDING-03267-thyristorbridge2pulse-rl-r.md`, which a later run renamed |
| Original SHA-256 | d460b0a705555db4accb0f12b35700c9f7a2542876ca011a0043525ee3badcf9 |

## What remains unresolved

The current Rumoca nominal run is tool-error, before any reported perturbation. This prevents causal attribution to this parameter. Source metadata was recovered, but none of the reviewed source proofs or counterexamples establishes this particular claim. A baseline failure/tool limitation is neither confirmation nor a false positive.

## Source evidence

Compiler/source-resolved declaration: `Electrical/PowerConverters/Examples/ACDC/RectifierBridge2Pulse/ThyristorBridge2Pulse_RL.mo:10`. Role: `parameter`; binding: `20`; effective min: `None`; effective max: `None`. 

[Electrical/PowerConverters/Examples/ACDC/RectifierBridge2Pulse/ThyristorBridge2Pulse_RL.mo — source snapshot](../evidence/sources/c8f0f20dac2d1fde-ThyristorBridge2Pulse_RL.mo)

```modelica
8:   parameter SI.Angle constantFiringAngle=30*pi/180
9:     "Firing angle";
10:   parameter SI.Resistance R=20 "Load resistance";
11:   parameter SI.Inductance L=1 "Load resistance"
12:     annotation (Evaluate=true);
13:   Modelica.Electrical.Analog.Basic.Resistor resistor(R=R) annotation (
```


## Execution evidence

[Rumoca commands, return codes, integrity hashes, bounded output and metadata](../evidence/e47715a239123b3f.json). Baseline: **tool-error**.

No independent runtime override was executed for this target in this audit; this is not a pass.

## Recommended action

Resolve the intended parameter domain and enclosing equations; check inherited bounds, final/protected status, guards and aliases. Construct an otherwise-valid source-level witness, establish a clean baseline in a capable engine, then retranslate at the witness and compare with the runtime override. For equality claims use the actual partner value. Do not apply a blanket min>0 fix yet.

## Scope and limitations

A source-level verdict addresses the reported declaration/claim, not every possible connected system. Tests cover 0–0.5 seconds and are not a proof of long-run stability. Shared instances are not distinct root causes. A missing bound, timeout, compiler error or failed nominal run alone never counts as a verified bug or a false positive. Fixes are proposals; no library/compiler implementation was changed.

[Group and related reports](../groups/baseline-blocked.md) · [Index](../README.md)
