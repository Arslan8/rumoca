# FINDING-03682: Not yet established as a bug or a false positive

| Field | Value |
|---|---|
| Verdict | unresolved |
| Scope / group | baseline-blocked |
| Model | Modelica.Electrical.PowerConverters.Examples.DCDC.HBridge.HBridge_TrianglePWM_RL |
| Target | hbridge.RonDiode |
| Student classification | physical-domain-unenforced |
| Original report | [FINDING-hbridge-trianglepwm-rl-hbridge-rondiode-intent.md](../../v2/bugs/FINDING-hbridge-trianglepwm-rl-hbridge-rondiode-intent.md) — reviewed as `FINDING-03682-hbridge-trianglepwm-rl-hbridge-rondiode.md`, which a later run renamed |
| Original SHA-256 | b233e4d3ce82cf891746514ac57b7c844bae97adbae5153bd066b359e9bcff63 |

## What remains unresolved

The current Rumoca nominal run is tool-error, before any reported perturbation. This prevents causal attribution to this parameter. Source metadata was recovered, but none of the reviewed source proofs or counterexamples establishes this particular claim. A baseline failure/tool limitation is neither confirmation nor a false positive.

## Source evidence

Compiler/source-resolved declaration: `Electrical/PowerConverters/DCDC/HBridge.mo:14`. Role: `parameter`; binding: `1e-05`; effective min: `None`; effective max: `None`. 

[Electrical/PowerConverters/DCDC/HBridge.mo — source snapshot](../evidence/sources/c29a16811f4c814b-HBridge.mo)

```modelica
12:   parameter SI.Voltage VkneeTransistor=0
13:     "Transistor threshold voltage";
14:   parameter SI.Resistance RonDiode=1e-05
15:     "Diode closed resistance";
16:   parameter SI.Conductance GoffDiode=1e-05
17:     "Diode opened conductance";
```


## Execution evidence

[Rumoca commands, return codes, integrity hashes, bounded output and metadata](../evidence/a7d46efa22385e7e.json). Baseline: **tool-error**.

No independent runtime override was executed for this target in this audit; this is not a pass.

## Recommended action

Resolve the intended parameter domain and enclosing equations; check inherited bounds, final/protected status, guards and aliases. Construct an otherwise-valid source-level witness, establish a clean baseline in a capable engine, then retranslate at the witness and compare with the runtime override. For equality claims use the actual partner value. Do not apply a blanket min>0 fix yet.

## Scope and limitations

A source-level verdict addresses the reported declaration/claim, not every possible connected system. Tests cover 0–0.5 seconds and are not a proof of long-run stability. Shared instances are not distinct root causes. A missing bound, timeout, compiler error or failed nominal run alone never counts as a verified bug or a false positive. Fixes are proposals; no library/compiler implementation was changed.

[Group and related reports](../groups/baseline-blocked.md) · [Index](../README.md)
