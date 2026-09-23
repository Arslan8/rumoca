# FINDING-04411: Not yet established as a bug or a false positive

| Field | Value |
|---|---|
| Verdict | unresolved |
| Scope / group | baseline-blocked |
| Model | Modelica.Mechanics.Rotational.Examples.Utilities.SpringDamper |
| Target | c |
| Student classification | physical-domain-unenforced |
| Original report | [FINDING-springdamper-c-zerolimit.md](../../v2/bugs/FINDING-springdamper-c-zerolimit.md) — reviewed as `FINDING-04411-springdamper-c.md`, which a later run renamed |
| Original SHA-256 | aafe766bae176fae3db41304b94a6c7fd75e8f8cf71c7fd6555d1fecc616bfd9 |

## What remains unresolved

The current Rumoca nominal run is tool-error, before any reported perturbation. This prevents causal attribution to this parameter. Source metadata was recovered, but none of the reviewed source proofs or counterexamples establishes this particular claim. A baseline failure/tool limitation is neither confirmation nor a false positive.

## Source evidence

Compiler/source-resolved declaration: `Mechanics/Rotational/Examples/Utilities/SpringDamper.mo:4`. Role: `parameter`; binding: `10000.0`; effective min: `None`; effective max: `None`. 

[Mechanics/Rotational/Examples/Utilities/SpringDamper.mo — source snapshot](../evidence/sources/d5eeb7c6a0b1de75-SpringDamper.mo)

```modelica
2: model SpringDamper "Input/output block of a spring/damper model"
3:   extends Modelica.Blocks.Icons.Block;
4:   parameter SI.RotationalSpringConstant c=1e4
5:     "Spring constant";
6:   parameter SI.RotationalDampingConstant d=1
7:     "Damping constant";
```


## Execution evidence

[Rumoca commands, return codes, integrity hashes, bounded output and metadata](../evidence/f985754e4d47d3dd.json). Baseline: **tool-error**.

No independent runtime override was executed for this target in this audit; this is not a pass.

## Recommended action

Resolve the intended parameter domain and enclosing equations; check inherited bounds, final/protected status, guards and aliases. Construct an otherwise-valid source-level witness, establish a clean baseline in a capable engine, then retranslate at the witness and compare with the runtime override. For equality claims use the actual partner value. Do not apply a blanket min>0 fix yet.

## Scope and limitations

A source-level verdict addresses the reported declaration/claim, not every possible connected system. Tests cover 0–0.5 seconds and are not a proof of long-run stability. Shared instances are not distinct root causes. A missing bound, timeout, compiler error or failed nominal run alone never counts as a verified bug or a false positive. Fixes are proposals; no library/compiler implementation was changed.

[Group and related reports](../groups/baseline-blocked.md) · [Index](../README.md)
