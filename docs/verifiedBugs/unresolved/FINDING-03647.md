# FINDING-03647: Not yet established as a bug or a false positive

| Field | Value |
|---|---|
| Verdict | unresolved |
| Scope / group | baseline-blocked |
| Model | Modelica.Electrical.PowerConverters.Examples.DCDC.HBridge.HBridge_RL |
| Target | L |
| Student classification | physical-domain-unenforced |
| Original report | [FINDING-hbridge-rl-l-zerolimit.md](../../v2/bugs/FINDING-hbridge-rl-l-zerolimit.md) — reviewed as `FINDING-03647-hbridge-rl-l.md`, which a later run renamed |
| Original SHA-256 | 6ee9c1b9f3cd9dc335085f88f81a0b1fedb5f1e6b9e0a5a760513c8e8ada1929 |

## What remains unresolved

The current Rumoca nominal run is tool-error, before any reported perturbation. This prevents causal attribution to this parameter. Source metadata was recovered, but none of the reviewed source proofs or counterexamples establishes this particular claim. A baseline failure/tool limitation is neither confirmation nor a false positive.

## Source evidence

Compiler/source-resolved declaration: `Electrical/PowerConverters/Examples/DCDC/HBridge/HBridge_RL.mo:6`. Role: `parameter`; binding: `1`; effective min: `None`; effective max: `None`. 

[Electrical/PowerConverters/Examples/DCDC/HBridge/HBridge_RL.mo — source snapshot](../evidence/sources/d6115cd4b0494335-HBridge_RL.mo)

```modelica
4:   extends Modelica.Icons.Example;
5:   parameter SI.Resistance R=100 "Resistance";
6:   parameter SI.Inductance L=1 "Inductance";
7:   Modelica.Electrical.Analog.Basic.Resistor resistor(R=R) annotation (
8:       Placement(transformation(
9:         extent={{-10,-10},{10,10}},
```


## Execution evidence

[Rumoca commands, return codes, integrity hashes, bounded output and metadata](../evidence/ab2cc6b174d1b7a8.json). Baseline: **tool-error**.

No independent runtime override was executed for this target in this audit; this is not a pass.

## Recommended action

Resolve the intended parameter domain and enclosing equations; check inherited bounds, final/protected status, guards and aliases. Construct an otherwise-valid source-level witness, establish a clean baseline in a capable engine, then retranslate at the witness and compare with the runtime override. For equality claims use the actual partner value. Do not apply a blanket min>0 fix yet.

## Scope and limitations

A source-level verdict addresses the reported declaration/claim, not every possible connected system. Tests cover 0–0.5 seconds and are not a proof of long-run stability. Shared instances are not distinct root causes. A missing bound, timeout, compiler error or failed nominal run alone never counts as a verified bug or a false positive. Fixes are proposals; no library/compiler implementation was changed.

[Group and related reports](../groups/baseline-blocked.md) · [Index](../README.md)
