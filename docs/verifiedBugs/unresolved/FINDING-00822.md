# FINDING-00822: Not yet established as a bug or a false positive

| Field | Value |
|---|---|
| Verdict | unresolved |
| Scope / group | needs-semantic-proof |
| Model | Modelica.Electrical.Analog.Examples.OpAmps.HighPass |
| Target | derivative.C |
| Student classification | physical-bound-permits-zero |
| Original report | [FINDING-highpass-derivative-c-zerolimit.md](../../v2/bugs/FINDING-highpass-derivative-c-zerolimit.md) — reviewed as `FINDING-00822-highpass-derivative-c.md`, which a later run renamed |
| Original SHA-256 | ef47df8a9e396059f665ea287b16d6607ceb3ac6886e57b9abd6d25cf4f5c726 |

## What remains unresolved

The nominal Rumoca run passes. Available perturbation outcomes are listed below, but no reviewed proof yet connects this exact claim to an unguarded invalid equation or refutes it. A failed post-translation override may change model structure; a passing zero probe alone does not prove the complete parameter domain safe.

## Source evidence

Compiler/source-resolved declaration: `Electrical/Analog/Examples/OpAmps/OpAmpCircuits/Derivative.mo:9`. Role: `parameter`; binding: `(derivative.T / derivative.R1)`; effective min: `0`; effective max: `None`. 

[Electrical/Analog/Examples/OpAmps/OpAmpCircuits/Derivative.mo — source snapshot](../evidence/sources/8eededa2a72767c5-Derivative.mo)

```modelica
7:   parameter SI.Resistance R2=k*R1 "Calculated resistance to reach k";
8:   parameter SI.Time T "Time constant";
9:   parameter SI.Capacitance C=T/R1 "Calculated capacitance to reach T";
10:   SI.Voltage v(start=0)=c.v "Capacitor voltage = state";
11:   Basic.Resistor                            r1(R=R1)
12:     annotation (Placement(transformation(extent={{-50,20},{-30,40}})));
```


## Execution evidence

[Rumoca commands, return codes, integrity hashes, bounded output and metadata](../evidence/c5eb5de89833fa1e.json). Baseline: **clean**.

| Probe | Outcome |
|---|---|
| `derivative.C=0` | reported-failure |

Diagnostic: solve-IR evaluation failed: non-finite derivative evaluation for state 'ground.p.v'

## Recommended action

Resolve the intended parameter domain and enclosing equations; check inherited bounds, final/protected status, guards and aliases. Construct an otherwise-valid source-level witness, establish a clean baseline in a capable engine, then retranslate at the witness and compare with the runtime override. For equality claims use the actual partner value. Do not apply a blanket min>0 fix yet.

## Scope and limitations

A source-level verdict addresses the reported declaration/claim, not every possible connected system. Tests cover 0–0.5 seconds and are not a proof of long-run stability. Shared instances are not distinct root causes. A missing bound, timeout, compiler error or failed nominal run alone never counts as a verified bug or a false positive. Fixes are proposals; no library/compiler implementation was changed.

[Group and related reports](../groups/needs-semantic-proof.md) · [Index](../README.md)
