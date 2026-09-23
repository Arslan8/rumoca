# FINDING-00783: Not yet established as a bug or a false positive

| Field | Value |
|---|---|
| Verdict | unresolved |
| Scope / group | needs-semantic-proof |
| Model | Modelica.Electrical.Analog.Examples.OpAmps.ControlCircuit |
| Target | feedbackA.R1 |
| Student classification | physical-domain-unenforced |
| Original report | [FINDING-controlcircuit-feedbacka-r1-zerolimit.md](../../v2/bugs/FINDING-controlcircuit-feedbacka-r1-zerolimit.md) — reviewed as `FINDING-00783-controlcircuit-feedbacka-r1.md`, which a later run renamed |
| Original SHA-256 | 13836a441c24dfaceeebc79aed8ced6019d82440f62d80f6d64243538aae2630 |

## What remains unresolved

The nominal Rumoca run passes. Available perturbation outcomes are listed below, but no reviewed proof yet connects this exact claim to an unguarded invalid equation or refutes it. A failed post-translation override may change model structure; a passing zero probe alone does not prove the complete parameter domain safe.

## Source evidence

Compiler/source-resolved declaration: `Electrical/Analog/Examples/OpAmps/OpAmpCircuits/Feedback.mo:7`. Role: `parameter`; binding: `1000`; effective min: `None`; effective max: `None`. 

[Electrical/Analog/Examples/OpAmps/OpAmpCircuits/Feedback.mo — source snapshot](../evidence/sources/8767f5f11d8a92ba-Feedback.mo)

```modelica
5:   SI.Current i1_2=p1_2.i "Current flowing from pos. to neg. pin of port 1_2";
6:   parameter Real k(final min=0)=1 "Desired amplification";
7:   parameter SI.Resistance R1=1000 "Resistance at inputs of OpAmp";
8:   parameter SI.Resistance R3=R1/k "Calculated resistance to reach desired amplification k";
9:   Basic.Resistor                            r1(final R=R1)
10:     annotation (Placement(transformation(extent={{-10,-10},{10,10}},
```


## Execution evidence

[Rumoca commands, return codes, integrity hashes, bounded output and metadata](../evidence/38386543da2fe8c7.json). Baseline: **clean**.

No independent runtime override was executed for this target in this audit; this is not a pass.

## Recommended action

Resolve the intended parameter domain and enclosing equations; check inherited bounds, final/protected status, guards and aliases. Construct an otherwise-valid source-level witness, establish a clean baseline in a capable engine, then retranslate at the witness and compare with the runtime override. For equality claims use the actual partner value. Do not apply a blanket min>0 fix yet.

## Scope and limitations

A source-level verdict addresses the reported declaration/claim, not every possible connected system. Tests cover 0–0.5 seconds and are not a proof of long-run stability. Shared instances are not distinct root causes. A missing bound, timeout, compiler error or failed nominal run alone never counts as a verified bug or a false positive. Fixes are proposals; no library/compiler implementation was changed.

[Group and related reports](../groups/needs-semantic-proof.md) · [Index](../README.md)
