# FINDING-03680: Not yet established as a bug or a false positive

| Field | Value |
|---|---|
| Verdict | unresolved |
| Scope / group | baseline-blocked |
| Model | Modelica.Electrical.PowerConverters.Examples.DCDC.HBridge.HBridge_TrianglePWM_RL |
| Target | hbridge.RonTransistor |
| Student classification | physical-domain-unenforced |
| Original report | [FINDING-hbridge-trianglepwm-rl-hbridge-rontransistor-intent.md](../../v2/bugs/FINDING-hbridge-trianglepwm-rl-hbridge-rontransistor-intent.md) — reviewed as `FINDING-03680-hbridge-trianglepwm-rl-hbridge-rontransistor.md`, which a later run renamed |
| Original SHA-256 | 172ebc3e929ccd6ef950ce963b2bc87c5d2184f7e5b8244cc22b3c61fd4ec39f |

## What remains unresolved

The current Rumoca nominal run is tool-error, before any reported perturbation. This prevents causal attribution to this parameter. Source metadata was recovered, but none of the reviewed source proofs or counterexamples establishes this particular claim. A baseline failure/tool limitation is neither confirmation nor a false positive.

## Source evidence

Compiler/source-resolved declaration: `Electrical/PowerConverters/DCDC/HBridge.mo:8`. Role: `parameter`; binding: `1e-05`; effective min: `None`; effective max: `None`. 

[Electrical/PowerConverters/DCDC/HBridge.mo — source snapshot](../evidence/sources/c29a16811f4c814b-HBridge.mo)

```modelica
6:   extends Modelica.Electrical.Analog.Interfaces.ConditionalHeatPort(final T=
7:        293.15);
8:   parameter SI.Resistance RonTransistor=1e-05
9:     "Transistor closed resistance";
10:   parameter SI.Conductance GoffTransistor=1e-05
11:     "Transistor opened conductance";
```


## Execution evidence

[Rumoca commands, return codes, integrity hashes, bounded output and metadata](../evidence/a7d46efa22385e7e.json). Baseline: **tool-error**.

No independent runtime override was executed for this target in this audit; this is not a pass.

## Recommended action

Resolve the intended parameter domain and enclosing equations; check inherited bounds, final/protected status, guards and aliases. Construct an otherwise-valid source-level witness, establish a clean baseline in a capable engine, then retranslate at the witness and compare with the runtime override. For equality claims use the actual partner value. Do not apply a blanket min>0 fix yet.

## Scope and limitations

A source-level verdict addresses the reported declaration/claim, not every possible connected system. Tests cover 0–0.5 seconds and are not a proof of long-run stability. Shared instances are not distinct root causes. A missing bound, timeout, compiler error or failed nominal run alone never counts as a verified bug or a false positive. Fixes are proposals; no library/compiler implementation was changed.

[Group and related reports](../groups/baseline-blocked.md) · [Index](../README.md)
