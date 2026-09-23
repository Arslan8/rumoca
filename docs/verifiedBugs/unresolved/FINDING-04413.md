# FINDING-04413: Not yet established as a bug or a false positive

| Field | Value |
|---|---|
| Verdict | unresolved |
| Scope / group | baseline-blocked |
| Model | Modelica.Mechanics.Rotational.Examples.Utilities.SpringDamper |
| Target | springDamper.c |
| Student classification | physical-bound-permits-zero |
| Original report | [FINDING-springdamper-springdamper-c-zerolimit.md](../../v2/bugs/FINDING-springdamper-springdamper-c-zerolimit.md) — reviewed as `FINDING-04413-springdamper-springdamper-c.md`, which a later run renamed |
| Original SHA-256 | e03345e40d3e2d18d640ce2dff87144fee9eeda07a1fadd17b711c98d9e79571 |

## What remains unresolved

The current Rumoca nominal run is tool-error, before any reported perturbation. This prevents causal attribution to this parameter. Source metadata was recovered, but none of the reviewed source proofs or counterexamples establishes this particular claim. A baseline failure/tool limitation is neither confirmation nor a false positive.

## Source evidence

Compiler/source-resolved declaration: `Mechanics/Rotational/Examples/Utilities/SpringDamperNoRelativeStates.mo:4`. Role: `parameter`; binding: `c`; effective min: `0`; effective max: `None`. 

[Mechanics/Rotational/Examples/Utilities/SpringDamperNoRelativeStates.mo — source snapshot](../evidence/sources/c37e51068a8ce72a-SpringDamperNoRelativeStates.mo)

```modelica
2: model SpringDamperNoRelativeStates
3:   "Linear 1D rotational spring and damper in parallel (phi and w are not used as states)"
4:   parameter SI.RotationalSpringConstant c(final min=0, start=1.0e5) "Spring constant";
5:   parameter SI.RotationalDampingConstant d(final min=0, start=0) "Damping constant";
6:   parameter SI.Angle phi_rel0=0
7:     "Unstretched spring angle";
```


## Execution evidence

[Rumoca commands, return codes, integrity hashes, bounded output and metadata](../evidence/f985754e4d47d3dd.json). Baseline: **tool-error**.

No independent runtime override was executed for this target in this audit; this is not a pass.

## Recommended action

Resolve the intended parameter domain and enclosing equations; check inherited bounds, final/protected status, guards and aliases. Construct an otherwise-valid source-level witness, establish a clean baseline in a capable engine, then retranslate at the witness and compare with the runtime override. For equality claims use the actual partner value. Do not apply a blanket min>0 fix yet.

## Scope and limitations

A source-level verdict addresses the reported declaration/claim, not every possible connected system. Tests cover 0–0.5 seconds and are not a proof of long-run stability. Shared instances are not distinct root causes. A missing bound, timeout, compiler error or failed nominal run alone never counts as a verified bug or a false positive. Fixes are proposals; no library/compiler implementation was changed.

[Group and related reports](../groups/baseline-blocked.md) · [Index](../README.md)
