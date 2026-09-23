# FINDING-04291: Tensor entries are not all strictly positive scalars

| Field | Value |
|---|---|
| Verdict | false-positives |
| Scope / group | signed-inertia-tensor |
| Model | Modelica.Mechanics.MultiBody.Examples.Systems.RobotR3.Utilities.MechanicalStructure |
| Target | b2.body.I_31 |
| Student classification | physical-domain-unenforced |
| Original report | `FINDING-04291-mechanicalstructure-b2-body-i-31.md` — [withdrawn](../../v2/bugs/withdrawn.md); a later run no longer makes this claim |
| Original SHA-256 | ea31d06291ac6a1288844d91cde70010ce9420c10d3ddbf4ec9aa36dfb6c5245 |

## Why this is a false positive

Off-diagonal inertia tensor entries are signed (the declaration explicitly allows negative infinity as a lower bound); zero off-diagonal entries describe principal axes. The assembled tensor must satisfy matrix-level physical constraints, not elementwise strict positivity. This does not dismiss a separate invalid diagonal/eigenvalue report.

## Source evidence

Compiler/source-resolved declaration: `Mechanics/MultiBody/Parts/Body.mo:25`. Role: `parameter`; binding: `b2.I_31`; effective min: `-1.7976931348623157e+308`; effective max: `None`. 

[Mechanics/MultiBody/Parts/Body.mo — source snapshot](../evidence/sources/2679a27d72bf2ff2-Body.mo)

```modelica
23:   parameter SI.Inertia I_21(min=-C.inf) = 0 "Element (2,1) of inertia tensor"
24:     annotation (Dialog(group="Inertia tensor (resolved in center of mass, parallel to frame_a)"));
25:   parameter SI.Inertia I_31(min=-C.inf) = 0 "Element (3,1) of inertia tensor"
26:     annotation (Dialog(group="Inertia tensor (resolved in center of mass, parallel to frame_a)"));
27:   parameter SI.Inertia I_32(min=-C.inf) = 0 "Element (3,2) of inertia tensor"
28:     annotation (Dialog(group="Inertia tensor (resolved in center of mass, parallel to frame_a)"));
```

[Mechanics/MultiBody/Parts/Body.mo — source snapshot](../evidence/sources/2679a27d72bf2ff2-Body.mo)

```modelica
23:   parameter SI.Inertia I_21(min=-C.inf) = 0 "Element (2,1) of inertia tensor"
24:     annotation (Dialog(group="Inertia tensor (resolved in center of mass, parallel to frame_a)"));
25:   parameter SI.Inertia I_31(min=-C.inf) = 0 "Element (3,1) of inertia tensor"
26:     annotation (Dialog(group="Inertia tensor (resolved in center of mass, parallel to frame_a)"));
27:   parameter SI.Inertia I_32(min=-C.inf) = 0 "Element (3,2) of inertia tensor"
28:     annotation (Dialog(group="Inertia tensor (resolved in center of mass, parallel to frame_a)"));
```


## Execution evidence

[Rumoca commands, return codes, integrity hashes, bounded output and metadata](../evidence/24c9ba888f1f8278.json). Baseline: **tool-error**.

No independent runtime override was executed for this target in this audit; this is not a pass.

## Recommended action

Correct the detector/adjudicator for this specific semantic case; do not impose a blanket strictly-positive bound on the library declaration.

## Scope and limitations

A source-level verdict addresses the reported declaration/claim, not every possible connected system. Tests cover 0–0.5 seconds and are not a proof of long-run stability. Shared instances are not distinct root causes. A missing bound, timeout, compiler error or failed nominal run alone never counts as a verified bug or a false positive. Fixes are proposals; no library/compiler implementation was changed.

[Group and related reports](../groups/signed-inertia-tensor.md) · [Index](../README.md)
