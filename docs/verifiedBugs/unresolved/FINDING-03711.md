# FINDING-03711: Not yet established as a bug or a false positive

| Field | Value |
|---|---|
| Verdict | unresolved |
| Scope / group | baseline-blocked |
| Model | Modelica.Electrical.PowerConverters.Examples.DCDC.HBridge.HBridge_TrianglePWM_RL |
| Target | f |
| Student classification | divisor-reachable-zero |
| Original report | [FINDING-hbridge-trianglepwm-rl-f-divzero-2.md](../../v2/bugs/FINDING-hbridge-trianglepwm-rl-f-divzero-2.md) — reviewed as `FINDING-03711-hbridge-trianglepwm-rl-f.md`, which a later run renamed |
| Original SHA-256 | e74f75ac5d5386a8740b1544d0d089b7b6d40ee212cf30686e596767bfaadec8 |

## What remains unresolved

The current Rumoca nominal run is tool-error, before any reported perturbation. This prevents causal attribution to this parameter. Source metadata was recovered, but none of the reviewed source proofs or counterexamples establishes this particular claim. A baseline failure/tool limitation is neither confirmation nor a false positive.

## Source evidence

Compiler/source-resolved declaration: `Electrical/PowerConverters/Examples/DCDC/ExampleTemplates/HBridge.mo:4`. Role: `parameter`; binding: `1000`; effective min: `None`; effective max: `None`. 

[Electrical/PowerConverters/Examples/DCDC/ExampleTemplates/HBridge.mo — source snapshot](../evidence/sources/788574ec918aee05-HBridge.mo)

```modelica
2: partial model HBridge "H bridge DC/DC converter"
3:   extends Icons.ExampleTemplate;
4:   parameter SI.Frequency f=1000 "Switching frequency";
5:   PowerConverters.DCDC.HBridge hbridge(useHeatPort=false)
6:     annotation (Placement(transformation(extent={{-60,-10},{-40,10}})));
7:   Modelica.Electrical.Analog.Sources.ConstantVoltage constantVoltage(V=
```


## Execution evidence

[Rumoca commands, return codes, integrity hashes, bounded output and metadata](../evidence/a7d46efa22385e7e.json). Baseline: **tool-error**.

No independent runtime override was executed for this target in this audit; this is not a pass.

## Recommended action

Resolve the intended parameter domain and enclosing equations; check inherited bounds, final/protected status, guards and aliases. Construct an otherwise-valid source-level witness, establish a clean baseline in a capable engine, then retranslate at the witness and compare with the runtime override. For equality claims use the actual partner value. Do not apply a blanket min>0 fix yet.

## Scope and limitations

A source-level verdict addresses the reported declaration/claim, not every possible connected system. Tests cover 0–0.5 seconds and are not a proof of long-run stability. Shared instances are not distinct root causes. A missing bound, timeout, compiler error or failed nominal run alone never counts as a verified bug or a false positive. Fixes are proposals; no library/compiler implementation was changed.

[Group and related reports](../groups/baseline-blocked.md) · [Index](../README.md)
