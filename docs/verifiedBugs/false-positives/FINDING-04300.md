# FINDING-04300: Tensor entries are not all strictly positive scalars

| Field | Value |
|---|---|
| Verdict | false-positives |
| Scope / group | signed-inertia-tensor |
| Model | Modelica.Mechanics.MultiBody.Examples.Systems.RobotR3.Utilities.MechanicalStructure |
| Target | b3.I_32 |
| Student classification | physical-domain-unenforced |
| Original report | `FINDING-04300-mechanicalstructure-b3-i-32.md` — [withdrawn](../../v2/bugs/withdrawn.md); a later run no longer makes this claim |
| Original SHA-256 | 2dc2b12dc02e3ec77a7fca3107782c17130968dff018ed456fb7f10bce9d6dd6 |

## Why this is a false positive

Off-diagonal inertia tensor entries are signed (the declaration explicitly allows negative infinity as a lower bound); zero off-diagonal entries describe principal axes. The assembled tensor must satisfy matrix-level physical constraints, not elementwise strict positivity. This does not dismiss a separate invalid diagonal/eigenvalue report.

## Source evidence

Compiler/source-resolved declaration: `Mechanics/MultiBody/Parts/BodyShape.mo:34`. Role: `parameter`; binding: `0`; effective min: `-1.7976931348623157e+308`; effective max: `None`. 

[Mechanics/MultiBody/Parts/BodyShape.mo — source snapshot](../evidence/sources/90d48d37a154ba16-BodyShape.mo)

```modelica
32:   parameter SI.Inertia I_31(min=-C.inf) = 0 "Element (3,1) of inertia tensor"
33:     annotation (Dialog(group="Inertia tensor (resolved in center of mass, parallel to frame_a)"));
34:   parameter SI.Inertia I_32(min=-C.inf) = 0 "Element (3,2) of inertia tensor"
35:     annotation (Dialog(group="Inertia tensor (resolved in center of mass, parallel to frame_a)"));
36: 
37:   SI.Position r_0[3](start={0,0,0}, each stateSelect=if enforceStates then
```

[Mechanics/MultiBody/Parts/BodyShape.mo — source snapshot](../evidence/sources/90d48d37a154ba16-BodyShape.mo)

```modelica
32:   parameter SI.Inertia I_31(min=-C.inf) = 0 "Element (3,1) of inertia tensor"
33:     annotation (Dialog(group="Inertia tensor (resolved in center of mass, parallel to frame_a)"));
34:   parameter SI.Inertia I_32(min=-C.inf) = 0 "Element (3,2) of inertia tensor"
35:     annotation (Dialog(group="Inertia tensor (resolved in center of mass, parallel to frame_a)"));
36: 
37:   SI.Position r_0[3](start={0,0,0}, each stateSelect=if enforceStates then
```


## Execution evidence

[Rumoca commands, return codes, integrity hashes, bounded output and metadata](../evidence/24c9ba888f1f8278.json). Baseline: **tool-error**.

No independent runtime override was executed for this target in this audit; this is not a pass.

## Recommended action

Correct the detector/adjudicator for this specific semantic case; do not impose a blanket strictly-positive bound on the library declaration.

## Scope and limitations

A source-level verdict addresses the reported declaration/claim, not every possible connected system. Tests cover 0–0.5 seconds and are not a proof of long-run stability. Shared instances are not distinct root causes. A missing bound, timeout, compiler error or failed nominal run alone never counts as a verified bug or a false positive. Fixes are proposals; no library/compiler implementation was changed.

[Group and related reports](../groups/signed-inertia-tensor.md) · [Index](../README.md)
