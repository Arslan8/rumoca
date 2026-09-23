# FINDING-00746: Not yet established as a bug or a false positive

| Field | Value |
|---|---|
| Verdict | unresolved |
| Scope / group | baseline-blocked |
| Model | Modelica.Electrical.Analog.Examples.Lines.SmoothStep |
| Target | N50 |
| Student classification | divisor-reachable-zero |
| Original report | `FINDING-00746-smoothstep-n50.md` — [withdrawn](../../v2/bugs/withdrawn.md); a later run no longer makes this claim |
| Original SHA-256 | 910e3a9361e1214a6539ac4cf4b60cc9b7e9b25fa8d53b99b5d9aeb4384a817c |

## What remains unresolved

The current Rumoca nominal run is tool-error, before any reported perturbation. This prevents causal attribution to this parameter. Source metadata was recovered, but none of the reviewed source proofs or counterexamples establishes this particular claim. A baseline failure/tool limitation is neither confirmation nor a false positive.

## Source evidence

Compiler/source-resolved declaration: `Electrical/Analog/Examples/Lines/SmoothStep.mo:14`. Role: `parameter`; binding: `50`; effective min: `None`; effective max: `None`. 

[Electrical/Analog/Examples/Lines/SmoothStep.mo — source snapshot](../evidence/sources/5f3b41af825e9949-SmoothStep.mo)

```modelica
12:   parameter Integer N1=1 "Number of lumped segments of oline1";
13:   parameter Integer N5=5 "Number of lumped segments of oline5";
14:   parameter Integer N50=50 "Number of lumped segments of oline50";
15:   parameter SI.Velocity c=1/sqrt(l1*c1) "Speed of EM wave";
16:   parameter SI.Time  td=len/c "Transmission delay";
17:   parameter SI.Impedance z0=sqrt(l1/c1) "Characteristic impedance for very high frequency";
```


## Execution evidence

[Rumoca commands, return codes, integrity hashes, bounded output and metadata](../evidence/21f9fcbcb956ec17.json). Baseline: **tool-error**.

No independent runtime override was executed for this target in this audit; this is not a pass.

## Recommended action

Resolve the intended parameter domain and enclosing equations; check inherited bounds, final/protected status, guards and aliases. Construct an otherwise-valid source-level witness, establish a clean baseline in a capable engine, then retranslate at the witness and compare with the runtime override. For equality claims use the actual partner value. Do not apply a blanket min>0 fix yet.

## Scope and limitations

A source-level verdict addresses the reported declaration/claim, not every possible connected system. Tests cover 0–0.5 seconds and are not a proof of long-run stability. Shared instances are not distinct root causes. A missing bound, timeout, compiler error or failed nominal run alone never counts as a verified bug or a false positive. Fixes are proposals; no library/compiler implementation was changed.

[Group and related reports](../groups/baseline-blocked.md) · [Index](../README.md)
