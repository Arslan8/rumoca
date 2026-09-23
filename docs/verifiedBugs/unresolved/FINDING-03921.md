# FINDING-03921: Not yet established as a bug or a false positive

| Field | Value |
|---|---|
| Verdict | unresolved |
| Scope / group | baseline-blocked |
| Model | Modelica.Mechanics.MultiBody.Examples.Elementary.DoublePendulum |
| Target | boxBody1.density |
| Student classification | physical-bound-permits-zero |
| Original report | [FINDING-doublependulum-boxbody1-density-zerolimit.md](../../v2/bugs/FINDING-doublependulum-boxbody1-density-zerolimit.md) — reviewed as `FINDING-03921-doublependulum-boxbody1-density.md`, which a later run renamed |
| Original SHA-256 | 0ce15be3ca4c94789af8f7495d1e0d83be47233aeb207334ddbb41c49e78ba0f |

## What remains unresolved

The current Rumoca nominal run is tool-error, before any reported perturbation. This prevents causal attribution to this parameter. Source metadata was recovered, but none of the reviewed source proofs or counterexamples establishes this particular claim. A baseline failure/tool limitation is neither confirmation nor a false positive.

## Source evidence

Compiler/source-resolved declaration: `Mechanics/MultiBody/Parts/BodyBox.mo:37`. Role: `parameter`; binding: `7700`; effective min: `0.0`; effective max: `None`. 

[Mechanics/MultiBody/Parts/BodyBox.mo — source snapshot](../evidence/sources/698eec27fd1d9230-BodyBox.mo)

```modelica
35:   parameter SI.Distance innerHeight=innerWidth
36:     "Height of inner box surface (0 <= innerHeight <= height)";
37:   parameter SI.Density density=7700
38:     "Density of cylinder (e.g., steel: 7700 .. 7900, wood : 400 .. 800)";
39:   input Modelica.Mechanics.MultiBody.Types.Color color=Modelica.Mechanics.MultiBody.Types.Defaults.BodyColor
40:     "Color of box" annotation (Dialog(colorSelector=true, enable=animation));
```


## Execution evidence

[Rumoca commands, return codes, integrity hashes, bounded output and metadata](../evidence/69ffce7f37cd1d7e.json). Baseline: **tool-error**.

No independent runtime override was executed for this target in this audit; this is not a pass.

## Recommended action

Resolve the intended parameter domain and enclosing equations; check inherited bounds, final/protected status, guards and aliases. Construct an otherwise-valid source-level witness, establish a clean baseline in a capable engine, then retranslate at the witness and compare with the runtime override. For equality claims use the actual partner value. Do not apply a blanket min>0 fix yet.

## Scope and limitations

A source-level verdict addresses the reported declaration/claim, not every possible connected system. Tests cover 0–0.5 seconds and are not a proof of long-run stability. Shared instances are not distinct root causes. A missing bound, timeout, compiler error or failed nominal run alone never counts as a verified bug or a false positive. Fixes are proposals; no library/compiler implementation was changed.

[Group and related reports](../groups/baseline-blocked.md) · [Index](../README.md)
