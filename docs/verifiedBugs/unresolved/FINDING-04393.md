# FINDING-04393: Not yet established as a bug or a false positive

| Field | Value |
|---|---|
| Verdict | unresolved |
| Scope / group | baseline-blocked |
| Model | Modelica.Mechanics.Rotational.Examples.FirstGrounded |
| Target | Jmotor |
| Student classification | physical-bound-permits-zero |
| Original report | [FINDING-firstgrounded-jmotor-zerolimit.md](../../v2/bugs/FINDING-firstgrounded-jmotor-zerolimit.md) — reviewed as `FINDING-04393-firstgrounded-jmotor.md`, which a later run renamed |
| Original SHA-256 | b34467db5fc97dc8ee8eb425802fca98dbaaa8a10dc7fe9c6bb532ad9523b8cd |

## What remains unresolved

The current Rumoca nominal run is tool-error, before any reported perturbation. This prevents causal attribution to this parameter. Source metadata was recovered, but none of the reviewed source proofs or counterexamples establishes this particular claim. A baseline failure/tool limitation is neither confirmation nor a false positive.

## Source evidence

Compiler/source-resolved declaration: `Mechanics/Rotational/Examples/FirstGrounded.mo:8`. Role: `parameter`; binding: `0.1`; effective min: `0`; effective max: `None`. 

[Mechanics/Rotational/Examples/FirstGrounded.mo — source snapshot](../evidence/sources/936d50069df62dfd-FirstGrounded.mo)

```modelica
6:     "Amplitude of driving torque";
7:   parameter SI.Frequency f=5 "Frequency of driving torque";
8:   parameter SI.Inertia Jmotor(min=0) = 0.1 "Motor inertia";
9:   parameter SI.Inertia Jload(min=0) = 2 "Load inertia";
10:   parameter Real ratio=10 "Gear ratio";
11:   parameter Real damping=10 "Damping in bearing of gear";
```


## Execution evidence

[Rumoca commands, return codes, integrity hashes, bounded output and metadata](../evidence/078c657a65dbf3e1.json). Baseline: **tool-error**.

No independent runtime override was executed for this target in this audit; this is not a pass.

## Recommended action

Resolve the intended parameter domain and enclosing equations; check inherited bounds, final/protected status, guards and aliases. Construct an otherwise-valid source-level witness, establish a clean baseline in a capable engine, then retranslate at the witness and compare with the runtime override. For equality claims use the actual partner value. Do not apply a blanket min>0 fix yet.

## Scope and limitations

A source-level verdict addresses the reported declaration/claim, not every possible connected system. Tests cover 0–0.5 seconds and are not a proof of long-run stability. Shared instances are not distinct root causes. A missing bound, timeout, compiler error or failed nominal run alone never counts as a verified bug or a false positive. Fixes are proposals; no library/compiler implementation was changed.

[Group and related reports](../groups/baseline-blocked.md) · [Index](../README.md)
