# FINDING-00918: Not yet established as a bug or a false positive

| Field | Value |
|---|---|
| Verdict | unresolved |
| Scope / group | baseline-blocked |
| Model | Modelica.Electrical.Analog.Examples.OpAmps.SchmittTrigger |
| Target | f |
| Student classification | divisor-reachable-zero |
| Original report | [FINDING-schmitttrigger-f-divzero-2.md](../../v2/bugs/FINDING-schmitttrigger-f-divzero-2.md) — reviewed as `FINDING-00918-schmitttrigger-f.md`, which a later run renamed |
| Original SHA-256 | c6e103d516642b8c7d1afc8aa02cf527f4101c1ca7a0147281e06f4f5586d2bc |

## What remains unresolved

The current Rumoca nominal run is reported-failure, before any reported perturbation. This prevents causal attribution to this parameter. Source metadata was recovered, but none of the reviewed source proofs or counterexamples establishes this particular claim. A baseline failure/tool limitation is neither confirmation nor a false positive.

## Source evidence

Compiler/source-resolved declaration: `Electrical/Analog/Examples/OpAmps/SchmittTrigger.mo:7`. Role: `parameter`; binding: `10`; effective min: `None`; effective max: `None`. 

[Electrical/Analog/Examples/OpAmps/SchmittTrigger.mo — source snapshot](../evidence/sources/1146643cdb8f90b2-SchmittTrigger.mo)

```modelica
5:   parameter SI.Voltage Vns=-15 "Negative supply";
6:   parameter SI.Voltage Vin=5 "Amplitude of input voltage";
7:   parameter SI.Frequency f=10 "Frequency of input voltage";
8:   parameter SI.Voltage vHys=1 "(Positive) hysteresis voltage";
9:   parameter Real k=vHys/Vps "Auxiliary calculated parameter to be used in R2 calculation";
10:   parameter SI.Resistance R1=1000 "Arbitrary resistance";
```


## Execution evidence

[Rumoca commands, return codes, integrity hashes, bounded output and metadata](../evidence/18175c686731491f.json). Baseline: **reported-failure**.

No independent runtime override was executed for this target in this audit; this is not a pass.

## Recommended action

Resolve the intended parameter domain and enclosing equations; check inherited bounds, final/protected status, guards and aliases. Construct an otherwise-valid source-level witness, establish a clean baseline in a capable engine, then retranslate at the witness and compare with the runtime override. For equality claims use the actual partner value. Do not apply a blanket min>0 fix yet.

## Scope and limitations

A source-level verdict addresses the reported declaration/claim, not every possible connected system. Tests cover 0–0.5 seconds and are not a proof of long-run stability. Shared instances are not distinct root causes. A missing bound, timeout, compiler error or failed nominal run alone never counts as a verified bug or a false positive. Fixes are proposals; no library/compiler implementation was changed.

[Group and related reports](../groups/baseline-blocked.md) · [Index](../README.md)
