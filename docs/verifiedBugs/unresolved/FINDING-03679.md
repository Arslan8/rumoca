# FINDING-03679: Not yet established as a bug or a false positive

| Field | Value |
|---|---|
| Verdict | unresolved |
| Scope / group | baseline-blocked |
| Model | Modelica.Electrical.PowerConverters.Examples.DCDC.HBridge.HBridge_R |
| Target | f |
| Student classification | divisor-reachable-zero |
| Original report | `FINDING-03679-hbridge-r-f.md` — [withdrawn](../../v2/bugs/withdrawn.md); a later run no longer makes this claim |
| Original SHA-256 | 2d55a8be39ffead084a80806ba28202540b96c235998c64127cec57857dba3ca |

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

[Rumoca commands, return codes, integrity hashes, bounded output and metadata](../evidence/9ec1246440080430.json). Baseline: **tool-error**.

No independent runtime override was executed for this target in this audit; this is not a pass.

## Recommended action

Resolve the intended parameter domain and enclosing equations; check inherited bounds, final/protected status, guards and aliases. Construct an otherwise-valid source-level witness, establish a clean baseline in a capable engine, then retranslate at the witness and compare with the runtime override. For equality claims use the actual partner value. Do not apply a blanket min>0 fix yet.

## Scope and limitations

A source-level verdict addresses the reported declaration/claim, not every possible connected system. Tests cover 0–0.5 seconds and are not a proof of long-run stability. Shared instances are not distinct root causes. A missing bound, timeout, compiler error or failed nominal run alone never counts as a verified bug or a false positive. Fixes are proposals; no library/compiler implementation was changed.

[Group and related reports](../groups/baseline-blocked.md) · [Index](../README.md)
