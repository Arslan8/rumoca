# FINDING-04447: Not yet established as a bug or a false positive

| Field | Value |
|---|---|
| Verdict | unresolved |
| Scope / group | baseline-blocked |
| Model | Modelica.Mechanics.Translational.Examples.GenerationOfFMUs |
| Target | springDamper.d |
| Student classification | physical-domain-unenforced |
| Original report | [FINDING-generationoffmus-springdamper-d-intent.md](../../v2/bugs/FINDING-generationoffmus-springdamper-d-intent.md) — reviewed as `FINDING-04447-generationoffmus-springdamper-d.md`, which a later run renamed |
| Original SHA-256 | 9f657a0783f59f9a96e301458c129f4001194b0ce7957bae7c51171e4fabfd33 |

## What remains unresolved

The current Rumoca nominal run is tool-error, before any reported perturbation. This prevents causal attribution to this parameter. Source metadata was recovered, but none of the reviewed source proofs or counterexamples establishes this particular claim. A baseline failure/tool limitation is neither confirmation nor a false positive.

## Source evidence

Compiler/source-resolved declaration: `Mechanics/Translational/Examples/Utilities/SpringDamper.mo:6`. Role: `parameter`; binding: `100`; effective min: `None`; effective max: `None`. 

[Mechanics/Translational/Examples/Utilities/SpringDamper.mo — source snapshot](../evidence/sources/531556cc9b984666-SpringDamper.mo)

```modelica
4:   parameter SI.TranslationalSpringConstant c=1e4
5:     "Spring constant";
6:   parameter SI.TranslationalDampingConstant d=1
7:     "Damping constant";
8:   parameter SI.Length s_rel0=0
9:     "Unstretched spring length";
```


## Execution evidence

[Rumoca commands, return codes, integrity hashes, bounded output and metadata](../evidence/6d8ae00caaf62637.json). Baseline: **tool-error**.

No independent runtime override was executed for this target in this audit; this is not a pass.

## Recommended action

Resolve the intended parameter domain and enclosing equations; check inherited bounds, final/protected status, guards and aliases. Construct an otherwise-valid source-level witness, establish a clean baseline in a capable engine, then retranslate at the witness and compare with the runtime override. For equality claims use the actual partner value. Do not apply a blanket min>0 fix yet.

## Scope and limitations

A source-level verdict addresses the reported declaration/claim, not every possible connected system. Tests cover 0–0.5 seconds and are not a proof of long-run stability. Shared instances are not distinct root causes. A missing bound, timeout, compiler error or failed nominal run alone never counts as a verified bug or a false positive. Fixes are proposals; no library/compiler implementation was changed.

[Group and related reports](../groups/baseline-blocked.md) · [Index](../README.md)
