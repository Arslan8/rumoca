# FINDING-00815: Not yet established as a bug or a false positive

| Field | Value |
|---|---|
| Verdict | unresolved |
| Scope / group | needs-semantic-proof |
| Model | Modelica.Electrical.Analog.Examples.OpAmps.Differentiator |
| Target | der_.C |
| Student classification | physical-bound-permits-zero |
| Original report | [FINDING-differentiator-der-c-zerolimit.md](../../v2/bugs/FINDING-differentiator-der-c-zerolimit.md) — reviewed as `FINDING-00815-differentiator-der-c.md`, which a later run renamed |
| Original SHA-256 | 47db690309bebf74e40fc9d1b2cc6221941372779eb2512bfdd653dda04bf048 |

## What remains unresolved

The nominal Rumoca run passes. Available perturbation outcomes are listed below, but no reviewed proof yet connects this exact claim to an unguarded invalid equation or refutes it. A failed post-translation override may change model structure; a passing zero probe alone does not prove the complete parameter domain safe.

## Source evidence

Compiler/source-resolved declaration: `Electrical/Analog/Examples/OpAmps/OpAmpCircuits/Der.mo:8`. Role: `parameter`; binding: `(der_.k / (((2 * (2 * asin(1.0))) * der_.f) * der_.R))`; effective min: `0`; effective max: `None`. 

[Electrical/Analog/Examples/OpAmps/OpAmpCircuits/Der.mo — source snapshot](../evidence/sources/0db365a039713113-Der.mo)

```modelica
6:   parameter SI.Frequency f "Frequency";
7:   parameter SI.Resistance R=1000 "Resistance at output of OpAmp";
8:   parameter SI.Capacitance C=k/(2*pi*f*R) "Calculated capacitance to reach desired amplification k";
9:   SI.Voltage v(start=0)=c.v "Capacitor voltage = state";
10:   Basic.Capacitor                            c(final C=C)
11:     annotation (Placement(transformation(extent={{-50,20},{-30,40}})));
```


## Execution evidence

[Rumoca commands, return codes, integrity hashes, bounded output and metadata](../evidence/9fb3c0f95a3c9b11.json). Baseline: **clean**.

| Probe | Outcome |
|---|---|
| `der_.C=0` | reported-failure |

Diagnostic: solve-IR evaluation failed: non-finite derivative evaluation for state 'ground.p.v'

## Recommended action

Resolve the intended parameter domain and enclosing equations; check inherited bounds, final/protected status, guards and aliases. Construct an otherwise-valid source-level witness, establish a clean baseline in a capable engine, then retranslate at the witness and compare with the runtime override. For equality claims use the actual partner value. Do not apply a blanket min>0 fix yet.

## Scope and limitations

A source-level verdict addresses the reported declaration/claim, not every possible connected system. Tests cover 0–0.5 seconds and are not a proof of long-run stability. Shared instances are not distinct root causes. A missing bound, timeout, compiler error or failed nominal run alone never counts as a verified bug or a false positive. Fixes are proposals; no library/compiler implementation was changed.

[Group and related reports](../groups/needs-semantic-proof.md) · [Index](../README.md)
