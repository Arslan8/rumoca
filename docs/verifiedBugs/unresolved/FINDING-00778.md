# FINDING-00778: Not yet established as a bug or a false positive

| Field | Value |
|---|---|
| Verdict | unresolved |
| Scope / group | needs-semantic-proof |
| Model | Modelica.Electrical.Analog.Examples.OpAmps.Comparator |
| Target | R |
| Student classification | physical-domain-unenforced |
| Original report | [FINDING-comparator-r-zerolimit.md](../../v2/bugs/FINDING-comparator-r-zerolimit.md) — reviewed as `FINDING-00778-comparator-r.md`, which a later run renamed |
| Original SHA-256 | 3a4971e1ad9b1127fe8b55a7b9fd74f5112d5f24a254f912b11460dcad5b26c5 |

## What remains unresolved

The nominal Rumoca run passes. Available perturbation outcomes are listed below, but no reviewed proof yet connects this exact claim to an unguarded invalid equation or refutes it. A failed post-translation override may change model structure; a passing zero probe alone does not prove the complete parameter domain safe.

## Source evidence

Compiler/source-resolved declaration: `Electrical/Analog/Examples/OpAmps/Comparator.mo:10`. Role: `parameter`; binding: `1000`; effective min: `None`; effective max: `None`. 

[Electrical/Analog/Examples/OpAmps/Comparator.mo — source snapshot](../evidence/sources/c3b4a9d44d7708f1-Comparator.mo)

```modelica
8:   parameter SI.Voltage Vref=0 "Reference voltage";
9:   parameter Real k=(Vref - Vns)/(Vps - Vns) "Calculated potentiometer ratio to reach Vref";
10:   parameter SI.Resistance R=1000 "Resistance of potentiometer";
11:   Modelica.Electrical.Analog.Ideal.IdealizedOpAmpLimited opAmp(Vps=Vps, Vns=
12:         Vns) annotation (Placement(transformation(extent={{0,10},{20,-10}})));
13:   Modelica.Electrical.Analog.Basic.Ground ground
```


## Execution evidence

[Rumoca commands, return codes, integrity hashes, bounded output and metadata](../evidence/7def794e383a0da2.json). Baseline: **clean**.

No independent runtime override was executed for this target in this audit; this is not a pass.

## Recommended action

Resolve the intended parameter domain and enclosing equations; check inherited bounds, final/protected status, guards and aliases. Construct an otherwise-valid source-level witness, establish a clean baseline in a capable engine, then retranslate at the witness and compare with the runtime override. For equality claims use the actual partner value. Do not apply a blanket min>0 fix yet.

## Scope and limitations

A source-level verdict addresses the reported declaration/claim, not every possible connected system. Tests cover 0–0.5 seconds and are not a proof of long-run stability. Shared instances are not distinct root causes. A missing bound, timeout, compiler error or failed nominal run alone never counts as a verified bug or a false positive. Fixes are proposals; no library/compiler implementation was changed.

[Group and related reports](../groups/needs-semantic-proof.md) · [Index](../README.md)
