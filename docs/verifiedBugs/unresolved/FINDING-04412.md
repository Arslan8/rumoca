# FINDING-04412: Not yet established as a bug or a false positive

| Field | Value |
|---|---|
| Verdict | unresolved |
| Scope / group | baseline-blocked |
| Model | Modelica.Mechanics.Rotational.Examples.Utilities.SpringDamper |
| Target | d |
| Student classification | physical-domain-unenforced |
| Original report | [FINDING-springdamper-d-zerolimit.md](../../v2/bugs/FINDING-springdamper-d-zerolimit.md) — reviewed as `FINDING-04412-springdamper-d.md`, which a later run renamed |
| Original SHA-256 | 10314e1cc1e0990bfba8b5290b82ad9b005ad07c0e0a5ce4aa6bef93c8d9245b |

## What remains unresolved

The current Rumoca nominal run is tool-error, before any reported perturbation. This prevents causal attribution to this parameter. Source metadata was recovered, but none of the reviewed source proofs or counterexamples establishes this particular claim. A baseline failure/tool limitation is neither confirmation nor a false positive.

## Source evidence

Compiler/source-resolved declaration: `Mechanics/Rotational/Examples/Utilities/SpringDamper.mo:6`. Role: `parameter`; binding: `1`; effective min: `None`; effective max: `None`. 

[Mechanics/Rotational/Examples/Utilities/SpringDamper.mo — source snapshot](../evidence/sources/d5eeb7c6a0b1de75-SpringDamper.mo)

```modelica
4:   parameter SI.RotationalSpringConstant c=1e4
5:     "Spring constant";
6:   parameter SI.RotationalDampingConstant d=1
7:     "Damping constant";
8:   parameter SI.Angle phi_rel0=0
9:     "Unstretched spring angle";
```


## Execution evidence

[Rumoca commands, return codes, integrity hashes, bounded output and metadata](../evidence/f985754e4d47d3dd.json). Baseline: **tool-error**.

No independent runtime override was executed for this target in this audit; this is not a pass.

## Recommended action

Resolve the intended parameter domain and enclosing equations; check inherited bounds, final/protected status, guards and aliases. Construct an otherwise-valid source-level witness, establish a clean baseline in a capable engine, then retranslate at the witness and compare with the runtime override. For equality claims use the actual partner value. Do not apply a blanket min>0 fix yet.

## Scope and limitations

A source-level verdict addresses the reported declaration/claim, not every possible connected system. Tests cover 0–0.5 seconds and are not a proof of long-run stability. Shared instances are not distinct root causes. A missing bound, timeout, compiler error or failed nominal run alone never counts as a verified bug or a false positive. Fixes are proposals; no library/compiler implementation was changed.

[Group and related reports](../groups/baseline-blocked.md) · [Index](../README.md)
