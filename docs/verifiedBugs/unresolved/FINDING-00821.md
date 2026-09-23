# FINDING-00821: Not yet established as a bug or a false positive

| Field | Value |
|---|---|
| Verdict | unresolved |
| Scope / group | needs-semantic-proof |
| Model | Modelica.Electrical.Analog.Examples.OpAmps.HighPass |
| Target | derivative.R2 |
| Student classification | physical-domain-unenforced |
| Original report | [FINDING-highpass-derivative-r2-zerolimit.md](../../v2/bugs/FINDING-highpass-derivative-r2-zerolimit.md) — reviewed as `FINDING-00821-highpass-derivative-r2.md`, which a later run renamed |
| Original SHA-256 | e291e5a2927f1fda9bb595b92fec3561149856522e6133864bb57a62cf4651aa |

## What remains unresolved

The nominal Rumoca run passes. Available perturbation outcomes are listed below, but no reviewed proof yet connects this exact claim to an unguarded invalid equation or refutes it. A failed post-translation override may change model structure; a passing zero probe alone does not prove the complete parameter domain safe.

## Source evidence

Compiler/source-resolved declaration: `Electrical/Analog/Examples/OpAmps/OpAmpCircuits/Derivative.mo:7`. Role: `parameter`; binding: `1000`; effective min: `None`; effective max: `None`. 

[Electrical/Analog/Examples/OpAmps/OpAmpCircuits/Derivative.mo — source snapshot](../evidence/sources/8eededa2a72767c5-Derivative.mo)

```modelica
5:   parameter Real k(final min=0)=1 "Desired amplification";
6:   parameter SI.Resistance R1=1000 "Resistance at negative input of OpAmp";
7:   parameter SI.Resistance R2=k*R1 "Calculated resistance to reach k";
8:   parameter SI.Time T "Time constant";
9:   parameter SI.Capacitance C=T/R1 "Calculated capacitance to reach T";
10:   SI.Voltage v(start=0)=c.v "Capacitor voltage = state";
```


## Execution evidence

[Rumoca commands, return codes, integrity hashes, bounded output and metadata](../evidence/c5eb5de89833fa1e.json). Baseline: **clean**.

No independent runtime override was executed for this target in this audit; this is not a pass.

## Recommended action

Resolve the intended parameter domain and enclosing equations; check inherited bounds, final/protected status, guards and aliases. Construct an otherwise-valid source-level witness, establish a clean baseline in a capable engine, then retranslate at the witness and compare with the runtime override. For equality claims use the actual partner value. Do not apply a blanket min>0 fix yet.

## Scope and limitations

A source-level verdict addresses the reported declaration/claim, not every possible connected system. Tests cover 0–0.5 seconds and are not a proof of long-run stability. Shared instances are not distinct root causes. A missing bound, timeout, compiler error or failed nominal run alone never counts as a verified bug or a false positive. Fixes are proposals; no library/compiler implementation was changed.

[Group and related reports](../groups/needs-semantic-proof.md) · [Index](../README.md)
