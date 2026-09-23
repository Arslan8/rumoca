# FINDING-00829: Not yet established as a bug or a false positive

| Field | Value |
|---|---|
| Verdict | unresolved |
| Scope / group | needs-semantic-proof |
| Model | Modelica.Electrical.Analog.Examples.OpAmps.Integrator |
| Target | integrator.C |
| Student classification | physical-bound-permits-zero |
| Original report | [FINDING-integrator-integrator-c-zerolimit.md](../../v2/bugs/FINDING-integrator-integrator-c-zerolimit.md) — reviewed as `FINDING-00829-integrator-integrator-c.md`, which a later run renamed |
| Original SHA-256 | 7a14577061ae272c4cffd755211ba35a528a640bddac00f007f357f20e038b69 |

## What remains unresolved

The nominal Rumoca run passes. Available perturbation outcomes are listed below, but no reviewed proof yet connects this exact claim to an unguarded invalid equation or refutes it. A failed post-translation override may change model structure; a passing zero probe alone does not prove the complete parameter domain safe.

## Source evidence

Compiler/source-resolved declaration: `Electrical/Analog/Examples/OpAmps/OpAmpCircuits/Integrator.mo:8`. Role: `parameter`; binding: `((1 / integrator.k) / (((2 * (2 * asin(1.0))) * integrator.f) * integrator.R))`; effective min: `0`; effective max: `None`. 

[Electrical/Analog/Examples/OpAmps/OpAmpCircuits/Integrator.mo — source snapshot](../evidence/sources/ea69c7eb54c29e22-Integrator.mo)

```modelica
6:   parameter SI.Frequency f "Frequency";
7:   parameter SI.Resistance R=1000 "Resistance at negative input of OpAmp";
8:   parameter SI.Capacitance C=1/k/(2*pi*f*R) "Calculated capacitance to reach desired amplification k";
9:   SI.Voltage v(start=0)=c.v "Capacitor voltage = state";
10:   Basic.Capacitor  c(final C=C)
11:     annotation (Placement(transformation(extent={{30,20},{10,40}})));
```


## Execution evidence

[Rumoca commands, return codes, integrity hashes, bounded output and metadata](../evidence/1e4f5d7bf77ea670.json). Baseline: **clean**.

| Probe | Outcome |
|---|---|
| `integrator.C=0` | reported-failure |

Diagnostic: solve-IR evaluation failed: non-finite derivative evaluation for state 'ground.p.v'

## Recommended action

Resolve the intended parameter domain and enclosing equations; check inherited bounds, final/protected status, guards and aliases. Construct an otherwise-valid source-level witness, establish a clean baseline in a capable engine, then retranslate at the witness and compare with the runtime override. For equality claims use the actual partner value. Do not apply a blanket min>0 fix yet.

## Scope and limitations

A source-level verdict addresses the reported declaration/claim, not every possible connected system. Tests cover 0–0.5 seconds and are not a proof of long-run stability. Shared instances are not distinct root causes. A missing bound, timeout, compiler error or failed nominal run alone never counts as a verified bug or a false positive. Fixes are proposals; no library/compiler implementation was changed.

[Group and related reports](../groups/needs-semantic-proof.md) · [Index](../README.md)
