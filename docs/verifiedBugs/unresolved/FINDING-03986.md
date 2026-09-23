# FINDING-03986: Not yet established as a bug or a false positive

| Field | Value |
|---|---|
| Verdict | unresolved |
| Scope / group | baseline-blocked |
| Model | Modelica.Mechanics.MultiBody.Examples.Elementary.HeatLosses |
| Target | springDamper.c |
| Student classification | physical-bound-permits-zero |
| Original report | [FINDING-heatlosses-springdamper-c-zerolimit.md](../../v2/bugs/FINDING-heatlosses-springdamper-c-zerolimit.md) — reviewed as `FINDING-03986-heatlosses-springdamper-c.md`, which a later run renamed |
| Original SHA-256 | 1151d05431c5f991e17716e7e51612ef53e9dfd95b086978ea2c2843e9fd3dcd |

## What remains unresolved

The current Rumoca nominal run is tool-error, before any reported perturbation. This prevents causal attribution to this parameter. Source metadata was recovered, but none of the reviewed source proofs or counterexamples establishes this particular claim. A baseline failure/tool limitation is neither confirmation nor a false positive.

## Source evidence

Compiler/source-resolved declaration: `Mechanics/MultiBody/Forces/SpringDamperParallel.mo:5`. Role: `parameter`; binding: `30`; effective min: `0`; effective max: `None`. 

[Mechanics/MultiBody/Forces/SpringDamperParallel.mo — source snapshot](../evidence/sources/90330b20603b785d-SpringDamperParallel.mo)

```modelica
3:   import Modelica.Mechanics.MultiBody.Types;
4:   parameter Boolean animation=true "= true, if animation shall be enabled";
5:   parameter SI.TranslationalSpringConstant c(final min=0) "Spring constant";
6:   parameter SI.Length s_unstretched=0 "Unstretched spring length";
7:   parameter SI.TranslationalDampingConstant d(final min=0) = 0
8:     "Damping constant";
```


## Execution evidence

[Rumoca commands, return codes, integrity hashes, bounded output and metadata](../evidence/2c68b447bcac4844.json). Baseline: **tool-error**.

No independent runtime override was executed for this target in this audit; this is not a pass.

## Recommended action

Resolve the intended parameter domain and enclosing equations; check inherited bounds, final/protected status, guards and aliases. Construct an otherwise-valid source-level witness, establish a clean baseline in a capable engine, then retranslate at the witness and compare with the runtime override. For equality claims use the actual partner value. Do not apply a blanket min>0 fix yet.

## Scope and limitations

A source-level verdict addresses the reported declaration/claim, not every possible connected system. Tests cover 0–0.5 seconds and are not a proof of long-run stability. Shared instances are not distinct root causes. A missing bound, timeout, compiler error or failed nominal run alone never counts as a verified bug or a false positive. Fixes are proposals; no library/compiler implementation was changed.

[Group and related reports](../groups/baseline-blocked.md) · [Index](../README.md)
