# FINDING-00860: Not yet established as a bug or a false positive

| Field | Value |
|---|---|
| Verdict | unresolved |
| Scope / group | needs-semantic-proof |
| Model | Modelica.Electrical.Analog.Examples.OpAmps.LowPass |
| Target | firstOrder.C |
| Student classification | physical-bound-permits-zero |
| Original report | [FINDING-lowpass-firstorder-c-zerolimit.md](../../v2/bugs/FINDING-lowpass-firstorder-c-zerolimit.md) — reviewed as `FINDING-00860-lowpass-firstorder-c.md`, which a later run renamed |
| Original SHA-256 | 55c4fc241c78c7c3caf6c100db612d7d5ab62707fbe6334785f972663433a754 |

## What remains unresolved

The nominal Rumoca run passes. Available perturbation outcomes are listed below, but no reviewed proof yet connects this exact claim to an unguarded invalid equation or refutes it. A failed post-translation override may change model structure; a passing zero probe alone does not prove the complete parameter domain safe.

## Source evidence

Compiler/source-resolved declaration: `Electrical/Analog/Examples/OpAmps/OpAmpCircuits/FirstOrder.mo:9`. Role: `parameter`; binding: `(firstOrder.T / firstOrder.R2)`; effective min: `0`; effective max: `None`. 

[Electrical/Analog/Examples/OpAmps/OpAmpCircuits/FirstOrder.mo — source snapshot](../evidence/sources/fe466a33db669be9-FirstOrder.mo)

```modelica
7:   parameter SI.Resistance R2=k*R1 "Calculated resistance to reach k";
8:   parameter SI.Time T "Time constant";
9:   parameter SI.Capacitance C=T/R2 "Calculated capacitance to reach T";
10:   SI.Voltage v(start=0)=c.v "Capacitor voltage = state";
11:   Basic.Resistor                            r1(R=R1)
12:     annotation (Placement(transformation(extent={{-50,20},{-30,40}})));
```


## Execution evidence

[Rumoca commands, return codes, integrity hashes, bounded output and metadata](../evidence/0328afa01e2550ef.json). Baseline: **clean**.

| Probe | Outcome |
|---|---|
| `firstOrder.C=0` | reported-failure |

Diagnostic: solve-IR evaluation failed: non-finite derivative evaluation for state 'ground.p.v'

## Recommended action

Resolve the intended parameter domain and enclosing equations; check inherited bounds, final/protected status, guards and aliases. Construct an otherwise-valid source-level witness, establish a clean baseline in a capable engine, then retranslate at the witness and compare with the runtime override. For equality claims use the actual partner value. Do not apply a blanket min>0 fix yet.

## Scope and limitations

A source-level verdict addresses the reported declaration/claim, not every possible connected system. Tests cover 0–0.5 seconds and are not a proof of long-run stability. Shared instances are not distinct root causes. A missing bound, timeout, compiler error or failed nominal run alone never counts as a verified bug or a false positive. Fixes are proposals; no library/compiler implementation was changed.

[Group and related reports](../groups/needs-semantic-proof.md) · [Index](../README.md)
