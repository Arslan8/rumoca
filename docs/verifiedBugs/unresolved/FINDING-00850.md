# FINDING-00850: Not yet established as a bug or a false positive

| Field | Value |
|---|---|
| Verdict | unresolved |
| Scope / group | needs-semantic-proof |
| Model | Modelica.Electrical.Analog.Examples.OpAmps.LCOscillator |
| Target | R2 |
| Student classification | physical-domain-unenforced |
| Original report | [FINDING-lcoscillator-r2-zerolimit.md](../../v2/bugs/FINDING-lcoscillator-r2-zerolimit.md) — reviewed as `FINDING-00850-lcoscillator-r2.md`, which a later run renamed |
| Original SHA-256 | 38413b54da31110d40ecf8c839e259a21787d2fa1ede7fd3e5319d0ebbf86635 |

## What remains unresolved

The nominal Rumoca run passes. Available perturbation outcomes are listed below, but no reviewed proof yet connects this exact claim to an unguarded invalid equation or refutes it. A failed post-translation override may change model structure; a passing zero probe alone does not prove the complete parameter domain safe.

## Source evidence

Compiler/source-resolved declaration: `Electrical/Analog/Examples/OpAmps/LCOscillator.mo:12`. Role: `parameter`; binding: `((A - 1) * R1)`; effective min: `None`; effective max: `None`. 

[Electrical/Analog/Examples/OpAmps/LCOscillator.mo — source snapshot](../evidence/sources/3c553b6c97a587b8-LCOscillator.mo)

```modelica
10:   parameter SI.Resistance R=10000.0 "Damping resistance";
11:   parameter SI.Resistance R1=10000.0 "Arbitrary high resistance";
12:   parameter SI.Resistance R2=(A - 1)*R1 "Calculated resistance to reach amplification A";
13:   parameter Real gamma=(1 - A)/(2*R*C) "Calculated characteristical parameter";
14:   Modelica.Electrical.Analog.Basic.Ground ground annotation (Placement(
15:         transformation(
```


## Execution evidence

[Rumoca commands, return codes, integrity hashes, bounded output and metadata](../evidence/8425a760f9ce6583.json). Baseline: **clean**.

No independent runtime override was executed for this target in this audit; this is not a pass.

## Recommended action

Resolve the intended parameter domain and enclosing equations; check inherited bounds, final/protected status, guards and aliases. Construct an otherwise-valid source-level witness, establish a clean baseline in a capable engine, then retranslate at the witness and compare with the runtime override. For equality claims use the actual partner value. Do not apply a blanket min>0 fix yet.

## Scope and limitations

A source-level verdict addresses the reported declaration/claim, not every possible connected system. Tests cover 0–0.5 seconds and are not a proof of long-run stability. Shared instances are not distinct root causes. A missing bound, timeout, compiler error or failed nominal run alone never counts as a verified bug or a false positive. Fixes are proposals; no library/compiler implementation was changed.

[Group and related reports](../groups/needs-semantic-proof.md) · [Index](../README.md)
