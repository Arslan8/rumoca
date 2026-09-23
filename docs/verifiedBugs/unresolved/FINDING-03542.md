# FINDING-03542: Not yet established as a bug or a false positive

| Field | Value |
|---|---|
| Verdict | unresolved |
| Scope / group | baseline-blocked |
| Model | Modelica.Electrical.PowerConverters.Examples.DCAC.SinglePhaseTwoLevel.SinglePhaseTwoLevel_R |
| Target | R |
| Student classification | physical-domain-unenforced |
| Original report | [FINDING-singlephasetwolevel-r-r-zerolimit.md](../../v2/bugs/FINDING-singlephasetwolevel-r-r-zerolimit.md) — reviewed as `FINDING-03542-singlephasetwolevel-r-r.md`, which a later run renamed |
| Original SHA-256 | 193fad08a095f577a1bf499a01fee508e8c2398121a3439bd53f12aad5733806 |

## What remains unresolved

The current Rumoca nominal run is tool-error, before any reported perturbation. This prevents causal attribution to this parameter. Source metadata was recovered, but none of the reviewed source proofs or counterexamples establishes this particular claim. A baseline failure/tool limitation is neither confirmation nor a false positive.

## Source evidence

Compiler/source-resolved declaration: `Electrical/PowerConverters/Examples/DCAC/SinglePhaseTwoLevel/SinglePhaseTwoLevel_R.mo:9`. Role: `parameter`; binding: `100`; effective min: `None`; effective max: `None`. 

[Electrical/PowerConverters/Examples/DCAC/SinglePhaseTwoLevel/SinglePhaseTwoLevel_R.mo — source snapshot](../evidence/sources/002b7183c49d9f13-SinglePhaseTwoLevel_R.mo)

```modelica
7:       f=f1));
8:   extends Modelica.Icons.Example;
9:   parameter SI.Resistance R=100 "Resistance";
10:   parameter SI.Frequency f1=50 "AC frequency";
11:   Modelica.Electrical.Analog.Basic.Resistor resistor(R=R) annotation (
12:       Placement(transformation(
```


## Execution evidence

[Rumoca commands, return codes, integrity hashes, bounded output and metadata](../evidence/4ad8e8cc710430a9.json). Baseline: **tool-error**.

No independent runtime override was executed for this target in this audit; this is not a pass.

## Recommended action

Resolve the intended parameter domain and enclosing equations; check inherited bounds, final/protected status, guards and aliases. Construct an otherwise-valid source-level witness, establish a clean baseline in a capable engine, then retranslate at the witness and compare with the runtime override. For equality claims use the actual partner value. Do not apply a blanket min>0 fix yet.

## Scope and limitations

A source-level verdict addresses the reported declaration/claim, not every possible connected system. Tests cover 0–0.5 seconds and are not a proof of long-run stability. Shared instances are not distinct root causes. A missing bound, timeout, compiler error or failed nominal run alone never counts as a verified bug or a false positive. Fixes are proposals; no library/compiler implementation was changed.

[Group and related reports](../groups/baseline-blocked.md) · [Index](../README.md)
