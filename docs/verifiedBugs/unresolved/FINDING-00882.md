# FINDING-00882: Not yet established as a bug or a false positive

| Field | Value |
|---|---|
| Verdict | unresolved |
| Scope / group | baseline-blocked |
| Model | Modelica.Electrical.Analog.Examples.OpAmps.OpAmpCircuits.Add |
| Target | R2 |
| Student classification | physical-domain-unenforced |
| Original report | [FINDING-add-r2-zerolimit.md](../../v2/bugs/FINDING-add-r2-zerolimit.md) — reviewed as `FINDING-00882-add-r2.md`, which a later run renamed |
| Original SHA-256 | 4acec519fea6ece317a2a69612deb24c2816f3b3b7ed25c1ad9becd6a30c0093 |

## What remains unresolved

The current Rumoca nominal run is reported-failure, before any reported perturbation. This prevents causal attribution to this parameter. Source metadata was recovered, but none of the reviewed source proofs or counterexamples establishes this particular claim. A baseline failure/tool limitation is neither confirmation nor a false positive.

## Source evidence

Compiler/source-resolved declaration: `Electrical/Analog/Examples/OpAmps/OpAmpCircuits/Add.mo:10`. Role: `parameter`; binding: `1000`; effective min: `None`; effective max: `None`. 

[Electrical/Analog/Examples/OpAmps/OpAmpCircuits/Add.mo — source snapshot](../evidence/sources/3108643ab0a7222b-Add.mo)

```modelica
8:   parameter SI.Resistance R=1000 "Resistance at output of OpAmp";
9:   parameter SI.Resistance R1=R/k1 "Calculated resistance to reach desired weight 1";
10:   parameter SI.Resistance R2=R/k2 "Calculated resistance to reach desired weight 2";
11:   Basic.Resistor  r1(final R=R1)
12:     annotation (Placement(transformation(extent={{-10,-10},{10,10}},
13:         origin={-40,70})));
```


## Execution evidence

[Rumoca commands, return codes, integrity hashes, bounded output and metadata](../evidence/6ed8186d7e25baf8.json). Baseline: **reported-failure**.

No independent runtime override was executed for this target in this audit; this is not a pass.

## Recommended action

Resolve the intended parameter domain and enclosing equations; check inherited bounds, final/protected status, guards and aliases. Construct an otherwise-valid source-level witness, establish a clean baseline in a capable engine, then retranslate at the witness and compare with the runtime override. For equality claims use the actual partner value. Do not apply a blanket min>0 fix yet.

## Scope and limitations

A source-level verdict addresses the reported declaration/claim, not every possible connected system. Tests cover 0–0.5 seconds and are not a proof of long-run stability. Shared instances are not distinct root causes. A missing bound, timeout, compiler error or failed nominal run alone never counts as a verified bug or a false positive. Fixes are proposals; no library/compiler implementation was changed.

[Group and related reports](../groups/baseline-blocked.md) · [Index](../README.md)
