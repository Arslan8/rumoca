# FINDING-03923: Not yet established as a bug or a false positive

| Field | Value |
|---|---|
| Verdict | unresolved |
| Scope / group | baseline-blocked |
| Model | Modelica.Mechanics.MultiBody.Examples.Elementary.DoublePendulum |
| Target | boxBody1.mi |
| Student classification | physical-bound-permits-zero |
| Original report | [FINDING-doublependulum-boxbody1-mi-zerolimit.md](../../v2/bugs/FINDING-doublependulum-boxbody1-mi-zerolimit.md) — reviewed as `FINDING-03923-doublependulum-boxbody1-mi.md`, which a later run renamed |
| Original SHA-256 | b325f9d037c178ff656669f469b92b0d2ab97e650f907b62d3f5ad4a215e1f2f |

## What remains unresolved

The current Rumoca nominal run is tool-error, before any reported perturbation. This prevents causal attribution to this parameter. Source metadata was recovered, but none of the reviewed source proofs or counterexamples establishes this particular claim. A baseline failure/tool limitation is neither confirmation nor a false positive.

## Source evidence

Compiler/source-resolved declaration: `Mechanics/MultiBody/Parts/BodyBox.mo:103`. Role: `parameter`; binding: `(((boxBody1.density * boxBody1.length) * boxBody1.innerWidth) * boxBody1.innerHeight)`; effective min: `0`; effective max: `None`. 

[Mechanics/MultiBody/Parts/BodyBox.mo — source snapshot](../evidence/sources/698eec27fd1d9230-BodyBox.mo)

```modelica
101:   final parameter SI.Mass mo(min=0) = density*length*width*height
102:     "Mass of box without hole";
103:   final parameter SI.Mass mi(min=0) = density*length*innerWidth*innerHeight
104:     "Mass of hole of box";
105:   final parameter SI.Mass m(min=0) = mo - mi "Mass of box";
106:   final parameter Frames.Orientation R=Frames.from_nxy(r, widthDirection)
```


## Execution evidence

[Rumoca commands, return codes, integrity hashes, bounded output and metadata](../evidence/69ffce7f37cd1d7e.json). Baseline: **tool-error**.

No independent runtime override was executed for this target in this audit; this is not a pass.

## Recommended action

Resolve the intended parameter domain and enclosing equations; check inherited bounds, final/protected status, guards and aliases. Construct an otherwise-valid source-level witness, establish a clean baseline in a capable engine, then retranslate at the witness and compare with the runtime override. For equality claims use the actual partner value. Do not apply a blanket min>0 fix yet.

## Scope and limitations

A source-level verdict addresses the reported declaration/claim, not every possible connected system. Tests cover 0–0.5 seconds and are not a proof of long-run stability. Shared instances are not distinct root causes. A missing bound, timeout, compiler error or failed nominal run alone never counts as a verified bug or a false positive. Fixes are proposals; no library/compiler implementation was changed.

[Group and related reports](../groups/baseline-blocked.md) · [Index](../README.md)
