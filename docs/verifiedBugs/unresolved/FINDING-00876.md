# FINDING-00876: Not yet established as a bug or a false positive

| Field | Value |
|---|---|
| Verdict | unresolved |
| Scope / group | needs-semantic-proof |
| Model | Modelica.Electrical.Analog.Examples.OpAmps.NonInvertingAmplifier |
| Target | buffer.R1 |
| Student classification | physical-domain-unenforced |
| Original report | [FINDING-noninvertingamplifier-buffer-r1-zerolimit.md](../../v2/bugs/FINDING-noninvertingamplifier-buffer-r1-zerolimit.md) — reviewed as `FINDING-00876-noninvertingamplifier-buffer-r1.md`, which a later run renamed |
| Original SHA-256 | a61e587a20e2ebdd20df5b58027c7db4c9854a6d490055a477863a0dcc049d2f |

## What remains unresolved

The nominal Rumoca run passes. Available perturbation outcomes are listed below, but no reviewed proof yet connects this exact claim to an unguarded invalid equation or refutes it. A failed post-translation override may change model structure; a passing zero probe alone does not prove the complete parameter domain safe.

## Source evidence

Compiler/source-resolved declaration: `Electrical/Analog/Examples/OpAmps/OpAmpCircuits/Buffer.mo:5`. Role: `parameter`; binding: `1000`; effective min: `None`; effective max: `None`. 

[Electrical/Analog/Examples/OpAmps/OpAmpCircuits/Buffer.mo — source snapshot](../evidence/sources/88331c0e33cc6eb3-Buffer.mo)

```modelica
3:   extends PartialOpAmp;
4:   parameter Real k(final min=0)=1 "Desired amplification";
5:   parameter SI.Resistance R1=1000 "Resistance at negative pin(s)";
6:   parameter SI.Resistance R2=(k - 1)*R1 "Calculated resistance to reach desired amplification k";
7:   Basic.Resistor                            r1(final R=R1)
8:     annotation (Placement(transformation(extent={{-10,-10},{10,10}},
```


## Execution evidence

[Rumoca commands, return codes, integrity hashes, bounded output and metadata](../evidence/368e14d0116ecee5.json). Baseline: **clean**.

No independent runtime override was executed for this target in this audit; this is not a pass.

## Recommended action

Resolve the intended parameter domain and enclosing equations; check inherited bounds, final/protected status, guards and aliases. Construct an otherwise-valid source-level witness, establish a clean baseline in a capable engine, then retranslate at the witness and compare with the runtime override. For equality claims use the actual partner value. Do not apply a blanket min>0 fix yet.

## Scope and limitations

A source-level verdict addresses the reported declaration/claim, not every possible connected system. Tests cover 0–0.5 seconds and are not a proof of long-run stability. Shared instances are not distinct root causes. A missing bound, timeout, compiler error or failed nominal run alone never counts as a verified bug or a false positive. Fixes are proposals; no library/compiler implementation was changed.

[Group and related reports](../groups/needs-semantic-proof.md) · [Index](../README.md)
