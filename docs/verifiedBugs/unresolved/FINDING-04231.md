# FINDING-04231: Not yet established as a bug or a false positive

| Field | Value |
|---|---|
| Verdict | unresolved |
| Scope / group | baseline-blocked |
| Model | Modelica.Mechanics.MultiBody.Examples.Rotational3DEffects.BevelGear1D |
| Target | inertia2.rotorWith3DEffects.J |
| Student classification | physical-bound-permits-zero |
| Original report | [FINDING-bevelgear1d-inertia2-rotorwith3deffects-j-zerolimit.md](../../v2/bugs/FINDING-bevelgear1d-inertia2-rotorwith3deffects-j-zerolimit.md) — reviewed as `FINDING-04231-bevelgear1d-inertia2-rotorwith3deffects-j.md`, which a later run renamed |
| Original SHA-256 | 52d4c38098f78692a976727f540efceb83dc08fdbf9e4c34175660c22506f702 |

## What remains unresolved

The current Rumoca nominal run is tool-error, before any reported perturbation. This prevents causal attribution to this parameter. Source metadata was recovered, but none of the reviewed source proofs or counterexamples establishes this particular claim. A baseline failure/tool limitation is neither confirmation nor a false positive.

## Source evidence

Compiler/source-resolved declaration: `Mechanics/MultiBody/Parts/Rotor1D.mo:78`. Role: `parameter`; binding: `18.2`; effective min: `0`; effective max: `None`. 

[Mechanics/MultiBody/Parts/Rotor1D.mo — source snapshot](../evidence/sources/d1e4105384b37714-Rotor1D.mo)

```modelica
76:     parameter Boolean animation=true
77:       "= true, if animation shall be enabled (show rotor as cylinder)";
78:     parameter SI.Inertia J(min=0) = 1
79:       "Moment of inertia of rotor around its axis of rotation";
80:     parameter Types.Axis n={1,0,0} "Axis of rotation resolved in frame_a";
81:     parameter SI.Position r_center[3]=zeros(3)
```


## Execution evidence

[Rumoca commands, return codes, integrity hashes, bounded output and metadata](../evidence/26b9a2fb6232f828.json). Baseline: **tool-error**.

No independent runtime override was executed for this target in this audit; this is not a pass.

## Recommended action

Resolve the intended parameter domain and enclosing equations; check inherited bounds, final/protected status, guards and aliases. Construct an otherwise-valid source-level witness, establish a clean baseline in a capable engine, then retranslate at the witness and compare with the runtime override. For equality claims use the actual partner value. Do not apply a blanket min>0 fix yet.

## Scope and limitations

A source-level verdict addresses the reported declaration/claim, not every possible connected system. Tests cover 0–0.5 seconds and are not a proof of long-run stability. Shared instances are not distinct root causes. A missing bound, timeout, compiler error or failed nominal run alone never counts as a verified bug or a false positive. Fixes are proposals; no library/compiler implementation was changed.

[Group and related reports](../groups/baseline-blocked.md) · [Index](../README.md)
