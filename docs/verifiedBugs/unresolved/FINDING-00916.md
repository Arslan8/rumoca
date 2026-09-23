# FINDING-00916: Not yet established as a bug or a false positive

| Field | Value |
|---|---|
| Verdict | unresolved |
| Scope / group | baseline-blocked |
| Model | Modelica.Electrical.Analog.Examples.OpAmps.SchmittTrigger |
| Target | R1 |
| Student classification | physical-domain-unenforced |
| Original report | [FINDING-schmitttrigger-r1-intent.md](../../v2/bugs/FINDING-schmitttrigger-r1-intent.md) — reviewed as `FINDING-00916-schmitttrigger-r1.md`, which a later run renamed |
| Original SHA-256 | fd6ad9b19043cfc91ca702c8af453cf5fa712927c68a28aaef910344e3e76e61 |

## What remains unresolved

The current Rumoca nominal run is reported-failure, before any reported perturbation. This prevents causal attribution to this parameter. Source metadata was recovered, but none of the reviewed source proofs or counterexamples establishes this particular claim. A baseline failure/tool limitation is neither confirmation nor a false positive.

## Source evidence

Compiler/source-resolved declaration: `Electrical/Analog/Examples/OpAmps/SchmittTrigger.mo:10`. Role: `parameter`; binding: `1000`; effective min: `None`; effective max: `None`. 

[Electrical/Analog/Examples/OpAmps/SchmittTrigger.mo — source snapshot](../evidence/sources/1146643cdb8f90b2-SchmittTrigger.mo)

```modelica
8:   parameter SI.Voltage vHys=1 "(Positive) hysteresis voltage";
9:   parameter Real k=vHys/Vps "Auxiliary calculated parameter to be used in R2 calculation";
10:   parameter SI.Resistance R1=1000 "Arbitrary resistance";
11:   parameter SI.Resistance R2=R1/k "Calculated resistance to reach hysteresis voltage";
12:   Modelica.Electrical.Analog.Ideal.IdealizedOpAmpLimited opAmp(
13:     Vps=Vps,
```


## Execution evidence

[Rumoca commands, return codes, integrity hashes, bounded output and metadata](../evidence/18175c686731491f.json). Baseline: **reported-failure**.

No independent runtime override was executed for this target in this audit; this is not a pass.

## Recommended action

Resolve the intended parameter domain and enclosing equations; check inherited bounds, final/protected status, guards and aliases. Construct an otherwise-valid source-level witness, establish a clean baseline in a capable engine, then retranslate at the witness and compare with the runtime override. For equality claims use the actual partner value. Do not apply a blanket min>0 fix yet.

## Scope and limitations

A source-level verdict addresses the reported declaration/claim, not every possible connected system. Tests cover 0–0.5 seconds and are not a proof of long-run stability. Shared instances are not distinct root causes. A missing bound, timeout, compiler error or failed nominal run alone never counts as a verified bug or a false positive. Fixes are proposals; no library/compiler implementation was changed.

[Group and related reports](../groups/baseline-blocked.md) · [Index](../README.md)
