# FINDING-00361: Not yet established as a bug or a false positive

| Field | Value |
|---|---|
| Verdict | unresolved |
| Scope / group | needs-semantic-proof |
| Model | Modelica.Electrical.Analog.Examples.InvertingAmp |
| Target | R2 |
| Student classification | physical-domain-unenforced |
| Original report | [FINDING-invertingamp-r2-zerolimit.md](../../v2/bugs/FINDING-invertingamp-r2-zerolimit.md) — reviewed as `FINDING-00361-invertingamp-r2.md`, which a later run renamed |
| Original SHA-256 | fd62997b65a1ab0b768736f6a611faaf3fbf0fd4540e602034fc9b4f54a01195 |

## What remains unresolved

The nominal Rumoca run passes. Available perturbation outcomes are listed below, but no reviewed proof yet connects this exact claim to an unguarded invalid equation or refutes it. A failed post-translation override may change model structure; a passing zero probe alone does not prove the complete parameter domain safe.

## Source evidence

Compiler/source-resolved declaration: `Electrical/Analog/Examples/InvertingAmp.mo:10`. Role: `parameter`; binding: `2000`; effective min: `None`; effective max: `None`. 

[Electrical/Analog/Examples/InvertingAmp.mo — source snapshot](../evidence/sources/0a7701dc2c4c8d4f-InvertingAmp.mo)

```modelica
8:   parameter Real k=2 "Desired amplification";
9:   parameter SI.Resistance R1=1000 "Arbitrary resistance";
10:   parameter SI.Resistance R2=k*R1 "Calculated resistance to reach desired amplification k";
11:   Modelica.Electrical.Analog.Ideal.IdealOpAmpLimited opAmp(
12:     out(i(start=0, fixed=false)))
13:     annotation (Placement(transformation(extent={{0,-10},{20,10}})));
```


## Execution evidence

[Rumoca commands, return codes, integrity hashes, bounded output and metadata](../evidence/87d4e09ed047dc9f.json). Baseline: **clean**.

No independent runtime override was executed for this target in this audit; this is not a pass.

## Recommended action

Resolve the intended parameter domain and enclosing equations; check inherited bounds, final/protected status, guards and aliases. Construct an otherwise-valid source-level witness, establish a clean baseline in a capable engine, then retranslate at the witness and compare with the runtime override. For equality claims use the actual partner value. Do not apply a blanket min>0 fix yet.

## Scope and limitations

A source-level verdict addresses the reported declaration/claim, not every possible connected system. Tests cover 0–0.5 seconds and are not a proof of long-run stability. Shared instances are not distinct root causes. A missing bound, timeout, compiler error or failed nominal run alone never counts as a verified bug or a false positive. Fixes are proposals; no library/compiler implementation was changed.

[Group and related reports](../groups/needs-semantic-proof.md) · [Index](../README.md)
