# FINDING-00779: Not yet established as a bug or a false positive

| Field | Value |
|---|---|
| Verdict | unresolved |
| Scope / group | needs-semantic-proof |
| Model | Modelica.Electrical.Analog.Examples.OpAmps.Comparator |
| Target | potentiometer.R |
| Student classification | physical-domain-unenforced |
| Original report | [FINDING-comparator-potentiometer-r-zerolimit.md](../../v2/bugs/FINDING-comparator-potentiometer-r-zerolimit.md) — reviewed as `FINDING-00779-comparator-potentiometer-r.md`, which a later run renamed |
| Original SHA-256 | ee730fcced32faec7109ab50a1569714bed4531f3b28ffb1f6044054e99aebd2 |

## What remains unresolved

The nominal Rumoca run passes. Available perturbation outcomes are listed below, but no reviewed proof yet connects this exact claim to an unguarded invalid equation or refutes it. A failed post-translation override may change model structure; a passing zero probe alone does not prove the complete parameter domain safe.

## Source evidence

Compiler/source-resolved declaration: `Electrical/Analog/Basic/Potentiometer.mo:3`. Role: `parameter`; binding: `R`; effective min: `None`; effective max: `None`. 

[Electrical/Analog/Basic/Potentiometer.mo — source snapshot](../evidence/sources/13cbf2fa671930be-Potentiometer.mo)

```modelica
1: within Modelica.Electrical.Analog.Basic;
2: model Potentiometer "Adjustable resistor"
3:   parameter SI.Resistance R(start=1)
4:     "Resistance at temperature T_ref";
5:   parameter SI.Temperature T_ref=293.15 "Reference temperature";
6:   parameter SI.LinearTemperatureCoefficient alpha=0
```


## Execution evidence

[Rumoca commands, return codes, integrity hashes, bounded output and metadata](../evidence/7def794e383a0da2.json). Baseline: **clean**.

No independent runtime override was executed for this target in this audit; this is not a pass.

## Recommended action

Resolve the intended parameter domain and enclosing equations; check inherited bounds, final/protected status, guards and aliases. Construct an otherwise-valid source-level witness, establish a clean baseline in a capable engine, then retranslate at the witness and compare with the runtime override. For equality claims use the actual partner value. Do not apply a blanket min>0 fix yet.

## Scope and limitations

A source-level verdict addresses the reported declaration/claim, not every possible connected system. Tests cover 0–0.5 seconds and are not a proof of long-run stability. Shared instances are not distinct root causes. A missing bound, timeout, compiler error or failed nominal run alone never counts as a verified bug or a false positive. Fixes are proposals; no library/compiler implementation was changed.

[Group and related reports](../groups/needs-semantic-proof.md) · [Index](../README.md)
