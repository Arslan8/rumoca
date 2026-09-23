# FINDING-00508: Not yet established as a bug or a false positive

| Field | Value |
|---|---|
| Verdict | unresolved |
| Scope / group | baseline-blocked |
| Model | Modelica.Electrical.Analog.Examples.Lines.SmoothStep |
| Target | z0 |
| Student classification | physical-domain-unenforced |
| Original report | [FINDING-smoothstep-z0-intent.md](../../v2/bugs/FINDING-smoothstep-z0-intent.md) — reviewed as `FINDING-00508-smoothstep-z0.md`, which a later run renamed |
| Original SHA-256 | 4e0724c95d3788106d4a803d1328636e29caf086d016a9c11bfc3e08c4aa2f3f |

## What remains unresolved

The current Rumoca nominal run is tool-error, before any reported perturbation. This prevents causal attribution to this parameter. Source metadata was recovered, but none of the reviewed source proofs or counterexamples establishes this particular claim. A baseline failure/tool limitation is neither confirmation nor a false positive.

## Source evidence

Compiler/source-resolved declaration: `Electrical/Analog/Examples/Lines/SmoothStep.mo:17`. Role: `parameter`; binding: `sqrt((l1 / c1))`; effective min: `None`; effective max: `None`. 

[Electrical/Analog/Examples/Lines/SmoothStep.mo — source snapshot](../evidence/sources/5f3b41af825e9949-SmoothStep.mo)

```modelica
15:   parameter SI.Velocity c=1/sqrt(l1*c1) "Speed of EM wave";
16:   parameter SI.Time  td=len/c "Transmission delay";
17:   parameter SI.Impedance z0=sqrt(l1/c1) "Characteristic impedance for very high frequency";
18:   Modelica.Blocks.Sources.Step step(startTime=200e-6) annotation (Placement(
19:         transformation(
20:         extent={{-10,-10},{10,10}},
```


## Execution evidence

[Rumoca commands, return codes, integrity hashes, bounded output and metadata](../evidence/21f9fcbcb956ec17.json). Baseline: **tool-error**.

No independent runtime override was executed for this target in this audit; this is not a pass.

## Recommended action

Resolve the intended parameter domain and enclosing equations; check inherited bounds, final/protected status, guards and aliases. Construct an otherwise-valid source-level witness, establish a clean baseline in a capable engine, then retranslate at the witness and compare with the runtime override. For equality claims use the actual partner value. Do not apply a blanket min>0 fix yet.

## Scope and limitations

A source-level verdict addresses the reported declaration/claim, not every possible connected system. Tests cover 0–0.5 seconds and are not a proof of long-run stability. Shared instances are not distinct root causes. A missing bound, timeout, compiler error or failed nominal run alone never counts as a verified bug or a false positive. Fixes are proposals; no library/compiler implementation was changed.

[Group and related reports](../groups/baseline-blocked.md) · [Index](../README.md)
