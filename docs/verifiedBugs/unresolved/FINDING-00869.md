# FINDING-00869: Not yet established as a bug or a false positive

| Field | Value |
|---|---|
| Verdict | unresolved |
| Scope / group | needs-semantic-proof |
| Model | Modelica.Electrical.Analog.Examples.OpAmps.Multivibrator |
| Target | C |
| Student classification | physical-bound-permits-zero |
| Original report | [FINDING-multivibrator-c-zerolimit.md](../../v2/bugs/FINDING-multivibrator-c-zerolimit.md) — reviewed as `FINDING-00869-multivibrator-c.md`, which a later run renamed |
| Original SHA-256 | 4fe0625c81155f47dac85a21c810f2397372a0d604a671d6b793fdb33acfed4c |

## What remains unresolved

The nominal Rumoca run passes. Available perturbation outcomes are listed below, but no reviewed proof yet connects this exact claim to an unguarded invalid equation or refutes it. A failed post-translation override may change model structure; a passing zero probe alone does not prove the complete parameter domain safe.

## Source evidence

Compiler/source-resolved declaration: `Electrical/Analog/Examples/OpAmps/Multivibrator.mo:10`. Role: `parameter`; binding: `((1 / f) / ((2 * R) * log((1 + ((2 * R1) / R2)))))`; effective min: `0`; effective max: `None`. 

[Electrical/Analog/Examples/OpAmps/Multivibrator.mo — source snapshot](../evidence/sources/9b4c9c1643c6e629-Multivibrator.mo)

```modelica
8:   parameter SI.Resistance R2=1000 "Resistance 2 for adjusting the Schmitt trigger voltage level";
9:   parameter SI.Resistance R=1000 "Arbitrary resistance";
10:   parameter SI.Capacitance C=1/f/(2*R*log(1 + 2*R1/R2)) "Calculated capacitance to reach the desired frequency f";
11:   Modelica.Electrical.Analog.Ideal.IdealizedOpAmpLimited opAmp(
12:     Vps=Vps,
13:     Vns=Vns,
```


## Execution evidence

[Rumoca commands, return codes, integrity hashes, bounded output and metadata](../evidence/03f0a994c6cd5a22.json). Baseline: **clean**.

| Probe | Outcome |
|---|---|
| `C=0` | reported-failure |

Diagnostic: solve-IR evaluation failed: non-finite derivative evaluation for state 'opAmp.vps'

## Recommended action

Resolve the intended parameter domain and enclosing equations; check inherited bounds, final/protected status, guards and aliases. Construct an otherwise-valid source-level witness, establish a clean baseline in a capable engine, then retranslate at the witness and compare with the runtime override. For equality claims use the actual partner value. Do not apply a blanket min>0 fix yet.

## Scope and limitations

A source-level verdict addresses the reported declaration/claim, not every possible connected system. Tests cover 0–0.5 seconds and are not a proof of long-run stability. Shared instances are not distinct root causes. A missing bound, timeout, compiler error or failed nominal run alone never counts as a verified bug or a false positive. Fixes are proposals; no library/compiler implementation was changed.

[Group and related reports](../groups/needs-semantic-proof.md) · [Index](../README.md)
