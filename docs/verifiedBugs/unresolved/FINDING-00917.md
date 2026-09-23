# FINDING-00917: Not yet established as a bug or a false positive

| Field | Value |
|---|---|
| Verdict | unresolved |
| Scope / group | baseline-blocked |
| Model | Modelica.Electrical.Analog.Examples.OpAmps.SchmittTrigger |
| Target | R2 |
| Student classification | physical-domain-unenforced |
| Original report | [FINDING-schmitttrigger-r2-zerolimit.md](../../v2/bugs/FINDING-schmitttrigger-r2-zerolimit.md) — reviewed as `FINDING-00917-schmitttrigger-r2.md`, which a later run renamed |
| Original SHA-256 | 9776a5daca20834eabf948cfba9e58dd44f9b519aa9959e4e67a586845761319 |

## What remains unresolved

The current Rumoca nominal run is reported-failure, before any reported perturbation. This prevents causal attribution to this parameter. Source metadata was recovered, but none of the reviewed source proofs or counterexamples establishes this particular claim. A baseline failure/tool limitation is neither confirmation nor a false positive.

## Source evidence

Compiler/source-resolved declaration: `Electrical/Analog/Examples/OpAmps/SchmittTrigger.mo:11`. Role: `parameter`; binding: `(R1 / k)`; effective min: `None`; effective max: `None`. 

[Electrical/Analog/Examples/OpAmps/SchmittTrigger.mo — source snapshot](../evidence/sources/1146643cdb8f90b2-SchmittTrigger.mo)

```modelica
9:   parameter Real k=vHys/Vps "Auxiliary calculated parameter to be used in R2 calculation";
10:   parameter SI.Resistance R1=1000 "Arbitrary resistance";
11:   parameter SI.Resistance R2=R1/k "Calculated resistance to reach hysteresis voltage";
12:   Modelica.Electrical.Analog.Ideal.IdealizedOpAmpLimited opAmp(
13:     Vps=Vps,
14:     Vns=Vns,
```


## Execution evidence

[Rumoca commands, return codes, integrity hashes, bounded output and metadata](../evidence/18175c686731491f.json). Baseline: **reported-failure**.

No independent runtime override was executed for this target in this audit; this is not a pass.

## Recommended action

Resolve the intended parameter domain and enclosing equations; check inherited bounds, final/protected status, guards and aliases. Construct an otherwise-valid source-level witness, establish a clean baseline in a capable engine, then retranslate at the witness and compare with the runtime override. For equality claims use the actual partner value. Do not apply a blanket min>0 fix yet.

## Scope and limitations

A source-level verdict addresses the reported declaration/claim, not every possible connected system. Tests cover 0–0.5 seconds and are not a proof of long-run stability. Shared instances are not distinct root causes. A missing bound, timeout, compiler error or failed nominal run alone never counts as a verified bug or a false positive. Fixes are proposals; no library/compiler implementation was changed.

[Group and related reports](../groups/baseline-blocked.md) · [Index](../README.md)
