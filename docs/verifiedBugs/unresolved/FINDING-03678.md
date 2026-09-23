# FINDING-03678: Not yet established as a bug or a false positive

| Field | Value |
|---|---|
| Verdict | unresolved |
| Scope / group | baseline-blocked |
| Model | Modelica.Electrical.PowerConverters.Examples.DCDC.HBridge.HBridge_R |
| Target | R |
| Student classification | physical-domain-unenforced |
| Original report | [FINDING-hbridge-r-r-zerolimit.md](../../v2/bugs/FINDING-hbridge-r-r-zerolimit.md) — reviewed as `FINDING-03678-hbridge-r-r.md`, which a later run renamed |
| Original SHA-256 | f9d48246e732d5e092f5de2f55fe710752b44214ba9028ffc03a1b250daa756c |

## What remains unresolved

The current Rumoca nominal run is tool-error, before any reported perturbation. This prevents causal attribution to this parameter. Source metadata was recovered, but none of the reviewed source proofs or counterexamples establishes this particular claim. A baseline failure/tool limitation is neither confirmation nor a false positive.

## Source evidence

Compiler/source-resolved declaration: `Electrical/PowerConverters/Examples/DCDC/HBridge/HBridge_R.mo:5`. Role: `parameter`; binding: `100`; effective min: `None`; effective max: `None`. 

[Electrical/PowerConverters/Examples/DCDC/HBridge/HBridge_R.mo — source snapshot](../evidence/sources/c10dad4aa5cd41e0-HBridge_R.mo)

```modelica
3:   extends ExampleTemplates.HBridge;
4:   extends Modelica.Icons.Example;
5:   parameter SI.Resistance R=100 "Resistance";
6:   Modelica.Electrical.Analog.Basic.Resistor resistor(R=R) annotation (
7:       Placement(transformation(
8:         extent={{-10,-10},{10,10}},
```


## Execution evidence

[Rumoca commands, return codes, integrity hashes, bounded output and metadata](../evidence/9ec1246440080430.json). Baseline: **tool-error**.

No independent runtime override was executed for this target in this audit; this is not a pass.

## Recommended action

Resolve the intended parameter domain and enclosing equations; check inherited bounds, final/protected status, guards and aliases. Construct an otherwise-valid source-level witness, establish a clean baseline in a capable engine, then retranslate at the witness and compare with the runtime override. For equality claims use the actual partner value. Do not apply a blanket min>0 fix yet.

## Scope and limitations

A source-level verdict addresses the reported declaration/claim, not every possible connected system. Tests cover 0–0.5 seconds and are not a proof of long-run stability. Shared instances are not distinct root causes. A missing bound, timeout, compiler error or failed nominal run alone never counts as a verified bug or a false positive. Fixes are proposals; no library/compiler implementation was changed.

[Group and related reports](../groups/baseline-blocked.md) · [Index](../README.md)
