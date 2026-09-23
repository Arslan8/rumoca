# FINDING-03433: Not yet established as a bug or a false positive

| Field | Value |
|---|---|
| Verdict | unresolved |
| Scope / group | baseline-blocked |
| Model | Modelica.Electrical.PowerConverters.Examples.ACDC.RectifierCenterTap2Pulse.ThyristorCenterTap2Pulse_RLV_Characteristic |
| Target | L |
| Student classification | physical-domain-unenforced |
| Original report | [FINDING-thyristorcentertap2pulse-rlv-characteristic-l-zerolimit.md](../../v2/bugs/FINDING-thyristorcentertap2pulse-rlv-characteristic-l-zerolimit.md) — reviewed as `FINDING-03433-thyristorcentertap2pulse-rlv-characteristic-l.md`, which a later run renamed |
| Original SHA-256 | b9464cf02a282511f1635d1baf964c5eb4b58acdfade49a067410dcc6aa98048 |

## What remains unresolved

The current Rumoca nominal run is tool-error, before any reported perturbation. This prevents causal attribution to this parameter. Source metadata was recovered, but none of the reviewed source proofs or counterexamples establishes this particular claim. A baseline failure/tool limitation is neither confirmation nor a false positive.

## Source evidence

Compiler/source-resolved declaration: `Electrical/PowerConverters/Examples/ACDC/RectifierCenterTap2Pulse/ThyristorCenterTap2Pulse_RLV_Characteristic.mo:9`. Role: `parameter`; binding: `1`; effective min: `None`; effective max: `None`. 

[Electrical/PowerConverters/Examples/ACDC/RectifierCenterTap2Pulse/ThyristorCenterTap2Pulse_RLV_Characteristic.mo — source snapshot](../evidence/sources/4dadfbe0a2907d6d-ThyristorCenterTap2Pulse_RLV_Characteristic.mo)

```modelica
7:   import Modelica.Constants.pi;
8:   parameter SI.Resistance R=20 "Load resistance";
9:   parameter SI.Inductance L=1 "Load resistance"
10:     annotation (Evaluate=true);
11:   parameter SI.Voltage VDC=-120 "DC load offset voltage";
12:   Modelica.Electrical.Analog.Basic.Resistor resistor(R=R) annotation (
```


## Execution evidence

[Rumoca commands, return codes, integrity hashes, bounded output and metadata](../evidence/bda11651497ff36c.json). Baseline: **tool-error**.

No independent runtime override was executed for this target in this audit; this is not a pass.

## Recommended action

Resolve the intended parameter domain and enclosing equations; check inherited bounds, final/protected status, guards and aliases. Construct an otherwise-valid source-level witness, establish a clean baseline in a capable engine, then retranslate at the witness and compare with the runtime override. For equality claims use the actual partner value. Do not apply a blanket min>0 fix yet.

## Scope and limitations

A source-level verdict addresses the reported declaration/claim, not every possible connected system. Tests cover 0–0.5 seconds and are not a proof of long-run stability. Shared instances are not distinct root causes. A missing bound, timeout, compiler error or failed nominal run alone never counts as a verified bug or a false positive. Fixes are proposals; no library/compiler implementation was changed.

[Group and related reports](../groups/baseline-blocked.md) · [Index](../README.md)
