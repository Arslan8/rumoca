# FINDING-00934: Not yet established as a bug or a false positive

| Field | Value |
|---|---|
| Verdict | unresolved |
| Scope / group | needs-semantic-proof |
| Model | Modelica.Electrical.Analog.Examples.OpAmps.VoltageFollower |
| Target | Ri |
| Student classification | physical-domain-unenforced |
| Original report | [FINDING-voltagefollower-ri-zerolimit.md](../../v2/bugs/FINDING-voltagefollower-ri-zerolimit.md) — reviewed as `FINDING-00934-voltagefollower-ri.md`, which a later run renamed |
| Original SHA-256 | 629f2ab8f797537c66c9bd96aa38e1cea2ac299af0cd5ca305d64fe7d904c64b |

## What remains unresolved

The nominal Rumoca run passes. Available perturbation outcomes are listed below, but no reviewed proof yet connects this exact claim to an unguarded invalid equation or refutes it. A failed post-translation override may change model structure; a passing zero probe alone does not prove the complete parameter domain safe.

## Source evidence

Compiler/source-resolved declaration: `Electrical/Analog/Examples/OpAmps/VoltageFollower.mo:8`. Role: `parameter`; binding: `1`; effective min: `None`; effective max: `None`. 

[Electrical/Analog/Examples/OpAmps/VoltageFollower.mo — source snapshot](../evidence/sources/9a2ef7ccb82a00cb-VoltageFollower.mo)

```modelica
6:   parameter SI.Voltage Vin=5 "Amplitude of input voltage";
7:   parameter SI.Frequency f=10 "Frequency of input voltage";
8:   parameter SI.Resistance Ri=1
9:     "Inner resistance of input voltage source";
10:   parameter SI.Resistance Rl=1 "Load resistance";
11:   Modelica.Electrical.Analog.Ideal.IdealizedOpAmpLimited opAmp(
```


## Execution evidence

[Rumoca commands, return codes, integrity hashes, bounded output and metadata](../evidence/e51ccafaf08188b5.json). Baseline: **clean**.

No independent runtime override was executed for this target in this audit; this is not a pass.

## Recommended action

Resolve the intended parameter domain and enclosing equations; check inherited bounds, final/protected status, guards and aliases. Construct an otherwise-valid source-level witness, establish a clean baseline in a capable engine, then retranslate at the witness and compare with the runtime override. For equality claims use the actual partner value. Do not apply a blanket min>0 fix yet.

## Scope and limitations

A source-level verdict addresses the reported declaration/claim, not every possible connected system. Tests cover 0–0.5 seconds and are not a proof of long-run stability. Shared instances are not distinct root causes. A missing bound, timeout, compiler error or failed nominal run alone never counts as a verified bug or a false positive. Fixes are proposals; no library/compiler implementation was changed.

[Group and related reports](../groups/needs-semantic-proof.md) · [Index](../README.md)
