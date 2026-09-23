# FINDING-04229: Not yet established as a bug or a false positive

| Field | Value |
|---|---|
| Verdict | unresolved |
| Scope / group | baseline-blocked |
| Model | Modelica.Mechanics.MultiBody.Examples.Rotational3DEffects.BevelGear1D |
| Target | inertia1.rotorWith3DEffects.nJ |
| Student classification | physical-domain-unenforced |
| Original report | [FINDING-bevelgear1d-inertia1-rotorwith3deffects-nj-zerolimit.md](../../v2/bugs/FINDING-bevelgear1d-inertia1-rotorwith3deffects-nj-zerolimit.md) — reviewed as `FINDING-04229-bevelgear1d-inertia1-rotorwith3deffects-nj.md`, which a later run renamed |
| Original SHA-256 | dc412a59e07d16e20a7a45b771e74ebd15b20c6ee6cf458b94085d98afc90dcb |

## What remains unresolved

The current Rumoca nominal run is tool-error, before any reported perturbation. This prevents causal attribution to this parameter. Source metadata was recovered, but none of the reviewed source proofs or counterexamples establishes this particular claim. A baseline failure/tool limitation is neither confirmation nor a false positive.

## Source evidence

Compiler/source-resolved declaration: `Mechanics/MultiBody/Parts/Rotor1D.mo:147`. Role: `parameter`; binding: `(inertia1.rotorWith3DEffects.J * inertia1.rotorWith3DEffects.e)`; effective min: `None`; effective max: `None`. 

[Mechanics/MultiBody/Parts/Rotor1D.mo — source snapshot](../evidence/sources/d1e4105384b37714-Rotor1D.mo)

```modelica
145:       Modelica.Math.Vectors.normalizeWithAssert(n)
146:       "Unit vector in direction of rotor axis, resolved in frame_a";
147:     parameter SI.Inertia nJ[3]=J*e;
148:     Modelica.Mechanics.MultiBody.Visualizers.Advanced.Shape cylinder(
149:       shapeType="cylinder",
150:       color=cylinderColor,
```


## Execution evidence

[Rumoca commands, return codes, integrity hashes, bounded output and metadata](../evidence/26b9a2fb6232f828.json). Baseline: **tool-error**.

No independent runtime override was executed for this target in this audit; this is not a pass.

## Recommended action

Resolve the intended parameter domain and enclosing equations; check inherited bounds, final/protected status, guards and aliases. Construct an otherwise-valid source-level witness, establish a clean baseline in a capable engine, then retranslate at the witness and compare with the runtime override. For equality claims use the actual partner value. Do not apply a blanket min>0 fix yet.

## Scope and limitations

A source-level verdict addresses the reported declaration/claim, not every possible connected system. Tests cover 0–0.5 seconds and are not a proof of long-run stability. Shared instances are not distinct root causes. A missing bound, timeout, compiler error or failed nominal run alone never counts as a verified bug or a false positive. Fixes are proposals; no library/compiler implementation was changed.

[Group and related reports](../groups/baseline-blocked.md) · [Index](../README.md)
