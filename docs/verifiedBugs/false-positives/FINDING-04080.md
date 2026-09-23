# FINDING-04080: Tensor entries are not all strictly positive scalars

| Field | Value |
|---|---|
| Verdict | false-positives |
| Scope / group | signed-inertia-tensor |
| Model | Modelica.Mechanics.MultiBody.Examples.Elementary.PointGravityWithPointMasses2 |
| Target | referenceSystem.pointMass2.I |
| Student classification | physical-domain-unenforced |
| Original report | `FINDING-04080-pointgravitywithpointmasses2-referencesystem-pointmass2-i.md` — [withdrawn](../../v2/bugs/withdrawn.md); a later run no longer makes this claim |
| Original SHA-256 | 6e10c9a8a2efd84e73c312477ea3c28a122f67aba8a5ddb24dd2036183274f03 |

## Why this is a false positive

Off-diagonal inertia tensor entries are signed (the declaration explicitly allows negative infinity as a lower bound); zero off-diagonal entries describe principal axes. The assembled tensor must satisfy matrix-level physical constraints, not elementwise strict positivity. This does not dismiss a separate invalid diagonal/eigenvalue report.

## Source evidence

Compiler/source-resolved declaration: `Mechanics/MultiBody/Parts/Body.mo:114`. Role: `parameter`; binding: `cat1(cat2(referenceSystem.pointMass2.I_11, referenceSystem.pointMass2.I_21, referenceSystem.pointMass2.I_31), cat2(referenceSystem.pointMass2.I_21, referenceSystem.pointMass2.I_22, referenceSystem.pointMass2.I_32), cat2(referenceSystem.pointMass2.I_31, referenceSystem.pointMass2.I_32, referenceSystem.pointMass2.I_33))`; effective min: `None`; effective max: `None`. 

[Mechanics/MultiBody/Parts/Body.mo — source snapshot](../evidence/sources/2679a27d72bf2ff2-Body.mo)

```modelica
112:           useQuaternions));
113: 
114:   final parameter SI.Inertia I[3, 3]=[I_11, I_21, I_31; I_21, I_22, I_32;
115:       I_31, I_32, I_33] "Inertia tensor";
116:   final parameter Frames.Orientation R_start=
117:       Modelica.Mechanics.MultiBody.Frames.axesRotations(
```

[Mechanics/MultiBody/Parts/Body.mo — source snapshot](../evidence/sources/2679a27d72bf2ff2-Body.mo)

```modelica
112:           useQuaternions));
113: 
114:   final parameter SI.Inertia I[3, 3]=[I_11, I_21, I_31; I_21, I_22, I_32;
115:       I_31, I_32, I_33] "Inertia tensor";
116:   final parameter Frames.Orientation R_start=
117:       Modelica.Mechanics.MultiBody.Frames.axesRotations(
```


## Execution evidence

[Rumoca commands, return codes, integrity hashes, bounded output and metadata](../evidence/efeee42ee28141db.json). Baseline: **tool-error**.

No independent runtime override was executed for this target in this audit; this is not a pass.

## Recommended action

Correct the detector/adjudicator for this specific semantic case; do not impose a blanket strictly-positive bound on the library declaration.

## Scope and limitations

A source-level verdict addresses the reported declaration/claim, not every possible connected system. Tests cover 0–0.5 seconds and are not a proof of long-run stability. Shared instances are not distinct root causes. A missing bound, timeout, compiler error or failed nominal run alone never counts as a verified bug or a false positive. Fixes are proposals; no library/compiler implementation was changed.

[Group and related reports](../groups/signed-inertia-tensor.md) · [Index](../README.md)
