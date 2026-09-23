# FINDING-03123: Not yet established as a bug or a false positive

| Field | Value |
|---|---|
| Verdict | unresolved |
| Scope / group | baseline-blocked |
| Model | Modelica.Electrical.PowerConverters.Examples.ACDC.RectifierBridge2mPulse.ThyristorBridge2mPulse_RL |
| Target | L |
| Student classification | physical-domain-unenforced |
| Original report | [FINDING-thyristorbridge2mpulse-rl-l-zerolimit.md](../../v2/bugs/FINDING-thyristorbridge2mpulse-rl-l-zerolimit.md) — reviewed as `FINDING-03123-thyristorbridge2mpulse-rl-l.md`, which a later run renamed |
| Original SHA-256 | 08fc3c8e5f3f5525a26d4dcbfef376e78b135259a5ba97893928c9e1b9085705 |

## What remains unresolved

The current Rumoca nominal run is tool-error, before any reported perturbation. This prevents causal attribution to this parameter. Source metadata was recovered, but none of the reviewed source proofs or counterexamples establishes this particular claim. A baseline failure/tool limitation is neither confirmation nor a false positive.

## Source evidence

Compiler/source-resolved declaration: `Electrical/PowerConverters/Examples/ACDC/RectifierBridge2mPulse/ThyristorBridge2mPulse_RL.mo:12`. Role: `parameter`; binding: `1`; effective min: `None`; effective max: `None`. 

[Electrical/PowerConverters/Examples/ACDC/RectifierBridge2mPulse/ThyristorBridge2mPulse_RL.mo — source snapshot](../evidence/sources/c192bbb36534cc2e-ThyristorBridge2mPulse_RL.mo)

```modelica
10:     "Firing angle";
11:   parameter SI.Resistance R=20 "Load resistance";
12:   parameter SI.Inductance L=1 "Load resistance"
13:     annotation (Evaluate=true);
14:   Modelica.Electrical.Analog.Basic.Resistor resistor(R=R) annotation (
15:       Placement(transformation(
```


## Execution evidence

[Rumoca commands, return codes, integrity hashes, bounded output and metadata](../evidence/4d19590d8eeb4e15.json). Baseline: **tool-error**.

No independent runtime override was executed for this target in this audit; this is not a pass.

## Recommended action

Resolve the intended parameter domain and enclosing equations; check inherited bounds, final/protected status, guards and aliases. Construct an otherwise-valid source-level witness, establish a clean baseline in a capable engine, then retranslate at the witness and compare with the runtime override. For equality claims use the actual partner value. Do not apply a blanket min>0 fix yet.

## Scope and limitations

A source-level verdict addresses the reported declaration/claim, not every possible connected system. Tests cover 0–0.5 seconds and are not a proof of long-run stability. Shared instances are not distinct root causes. A missing bound, timeout, compiler error or failed nominal run alone never counts as a verified bug or a false positive. Fixes are proposals; no library/compiler implementation was changed.

[Group and related reports](../groups/baseline-blocked.md) · [Index](../README.md)
