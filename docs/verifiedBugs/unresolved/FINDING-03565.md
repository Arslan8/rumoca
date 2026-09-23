# FINDING-03565: Not yet established as a bug or a false positive

| Field | Value |
|---|---|
| Verdict | unresolved |
| Scope / group | baseline-blocked |
| Model | Modelica.Electrical.PowerConverters.Examples.DCDC.ChopperBuckBoost.ChopperBuckBoost_DutyCycle |
| Target | fS |
| Student classification | divisor-reachable-zero |
| Original report | `FINDING-03565-chopperbuckboost-dutycycle-fs.md` — [withdrawn](../../v2/bugs/withdrawn.md); a later run no longer makes this claim |
| Original SHA-256 | 78e7f5a94bc98607a0f589282f9417b1e6500d3e65f5cc24b21e6f945e26a748 |

## What remains unresolved

The current Rumoca nominal run is tool-error, before any reported perturbation. This prevents causal attribution to this parameter. Source metadata was recovered, but none of the reviewed source proofs or counterexamples establishes this particular claim. A baseline failure/tool limitation is neither confirmation nor a false positive.

## Source evidence

Compiler/source-resolved declaration: `Electrical/PowerConverters/Examples/DCDC/ExampleTemplates/ChopperBuckBoost.mo:12`. Role: `parameter`; binding: `40000.0`; effective min: `None`; effective max: `None`. 

[Electrical/PowerConverters/Examples/DCDC/ExampleTemplates/ChopperBuckBoost.mo — source snapshot](../evidence/sources/19afeb24726d89ac-ChopperBuckBoost.mo)

```modelica
10:   parameter Modelica.Units.SI.Inductance L=10e-6 "Inductance";
11:   parameter Modelica.Units.SI.Resistance R=1e-3 "Resistance of inductor";
12:   parameter Modelica.Units.SI.Frequency fS=40e3 "Switching frequency";
13:   parameter Real idleDutyCycle=1 - VLV/VHV "Duty cycle for idle operation";
14:   Modelica.Electrical.PowerConverters.DCDC.ChopperBuckBoost dcdc
15:     annotation (Placement(transformation(extent={{10,-8},{30,12}})));
```


## Execution evidence

[Rumoca commands, return codes, integrity hashes, bounded output and metadata](../evidence/4c98b27115f983e5.json). Baseline: **tool-error**.

No independent runtime override was executed for this target in this audit; this is not a pass.

## Recommended action

Resolve the intended parameter domain and enclosing equations; check inherited bounds, final/protected status, guards and aliases. Construct an otherwise-valid source-level witness, establish a clean baseline in a capable engine, then retranslate at the witness and compare with the runtime override. For equality claims use the actual partner value. Do not apply a blanket min>0 fix yet.

## Scope and limitations

A source-level verdict addresses the reported declaration/claim, not every possible connected system. Tests cover 0–0.5 seconds and are not a proof of long-run stability. Shared instances are not distinct root causes. A missing bound, timeout, compiler error or failed nominal run alone never counts as a verified bug or a false positive. Fixes are proposals; no library/compiler implementation was changed.

[Group and related reports](../groups/baseline-blocked.md) · [Index](../README.md)
