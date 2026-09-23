# FINDING-00903: Not yet established as a bug or a false positive

| Field | Value |
|---|---|
| Verdict | unresolved |
| Scope / group | baseline-blocked |
| Model | Modelica.Electrical.Analog.Examples.OpAmps.OpAmpCircuits.Gain |
| Target | R2 |
| Student classification | physical-domain-unenforced |
| Original report | [FINDING-gain-r2-zerolimit.md](../../v2/bugs/FINDING-gain-r2-zerolimit.md) — reviewed as `FINDING-00903-gain-r2.md`, which a later run renamed |
| Original SHA-256 | 3e7c26ac1fec879d77a8f536c039d39e20a8c9b7f3c28c0b500f077d2e0f0a24 |

## What remains unresolved

The current Rumoca nominal run is reported-failure, before any reported perturbation. This prevents causal attribution to this parameter. Source metadata was recovered, but none of the reviewed source proofs or counterexamples establishes this particular claim. A baseline failure/tool limitation is neither confirmation nor a false positive.

## Source evidence

Compiler/source-resolved declaration: `Electrical/Analog/Examples/OpAmps/OpAmpCircuits/Gain.mo:6`. Role: `parameter`; binding: `1000`; effective min: `None`; effective max: `None`. 

[Electrical/Analog/Examples/OpAmps/OpAmpCircuits/Gain.mo — source snapshot](../evidence/sources/acd2385377c8da04-Gain.mo)

```modelica
4:   parameter Real k(final min=0)=1 "Desired amplification";
5:   parameter SI.Resistance R1=1000 "Resistance at negative input of OpAmp";
6:   parameter SI.Resistance R2=k*R1 "Calculated resistance to reach desired amplification k";
7:   Basic.Resistor                            r1(final R=R1)
8:     annotation (Placement(transformation(extent={{-50,20},{-30,40}})));
9:   Basic.Resistor                            r2(final R=R2)
```


## Execution evidence

[Rumoca commands, return codes, integrity hashes, bounded output and metadata](../evidence/9689204df4218216.json). Baseline: **reported-failure**.

No independent runtime override was executed for this target in this audit; this is not a pass.

## Recommended action

Resolve the intended parameter domain and enclosing equations; check inherited bounds, final/protected status, guards and aliases. Construct an otherwise-valid source-level witness, establish a clean baseline in a capable engine, then retranslate at the witness and compare with the runtime override. For equality claims use the actual partner value. Do not apply a blanket min>0 fix yet.

## Scope and limitations

A source-level verdict addresses the reported declaration/claim, not every possible connected system. Tests cover 0–0.5 seconds and are not a proof of long-run stability. Shared instances are not distinct root causes. A missing bound, timeout, compiler error or failed nominal run alone never counts as a verified bug or a false positive. Fixes are proposals; no library/compiler implementation was changed.

[Group and related reports](../groups/baseline-blocked.md) · [Index](../README.md)
