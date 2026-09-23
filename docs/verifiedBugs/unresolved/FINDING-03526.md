# FINDING-03526: Not yet established as a bug or a false positive

| Field | Value |
|---|---|
| Verdict | unresolved |
| Scope / group | baseline-blocked |
| Model | Modelica.Electrical.PowerConverters.Examples.DCAC.SinglePhaseTwoLevel.SinglePhaseTwoLevel_RL |
| Target | R |
| Student classification | physical-domain-unenforced |
| Original report | [FINDING-singlephasetwolevel-rl-r-zerolimit.md](../../v2/bugs/FINDING-singlephasetwolevel-rl-r-zerolimit.md) — reviewed as `FINDING-03526-singlephasetwolevel-rl-r.md`, which a later run renamed |
| Original SHA-256 | bfa58a3bdbdf0aaf9b0c3199c2721b195f70fea5fd864112d6038e2767e6b0fd |

## What remains unresolved

The current Rumoca nominal run is tool-error, before any reported perturbation. This prevents causal attribution to this parameter. Source metadata was recovered, but none of the reviewed source proofs or counterexamples establishes this particular claim. A baseline failure/tool limitation is neither confirmation nor a false positive.

## Source evidence

Compiler/source-resolved declaration: `Electrical/PowerConverters/Examples/DCAC/SinglePhaseTwoLevel/SinglePhaseTwoLevel_RL.mo:9`. Role: `parameter`; binding: `100`; effective min: `None`; effective max: `None`. 

[Electrical/PowerConverters/Examples/DCAC/SinglePhaseTwoLevel/SinglePhaseTwoLevel_RL.mo — source snapshot](../evidence/sources/bbcba57719bc5cc4-SinglePhaseTwoLevel_RL.mo)

```modelica
7:       f=f1));
8:   extends Modelica.Icons.Example;
9:   parameter SI.Resistance R=100 "Resistance";
10:   parameter SI.Inductance L=1 "Inductance";
11:   parameter SI.Frequency f1=50 "AC frequency";
12:   Modelica.Electrical.Analog.Basic.Resistor resistor(R=R) annotation (
```


## Execution evidence

[Rumoca commands, return codes, integrity hashes, bounded output and metadata](../evidence/7d284fdabd6d0933.json). Baseline: **tool-error**.

No independent runtime override was executed for this target in this audit; this is not a pass.

## Recommended action

Resolve the intended parameter domain and enclosing equations; check inherited bounds, final/protected status, guards and aliases. Construct an otherwise-valid source-level witness, establish a clean baseline in a capable engine, then retranslate at the witness and compare with the runtime override. For equality claims use the actual partner value. Do not apply a blanket min>0 fix yet.

## Scope and limitations

A source-level verdict addresses the reported declaration/claim, not every possible connected system. Tests cover 0–0.5 seconds and are not a proof of long-run stability. Shared instances are not distinct root causes. A missing bound, timeout, compiler error or failed nominal run alone never counts as a verified bug or a false positive. Fixes are proposals; no library/compiler implementation was changed.

[Group and related reports](../groups/baseline-blocked.md) · [Index](../README.md)
