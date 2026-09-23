# FINDING-04221: Tensor entries are not all strictly positive scalars

| Field | Value |
|---|---|
| Verdict | false-positives |
| Scope / group | signed-inertia-tensor |
| Model | Modelica.Mechanics.MultiBody.Examples.Loops.PlanarFourbar |
| Target | body4.body.I_32 |
| Student classification | physical-domain-unenforced |
| Original report | `FINDING-04221-planarfourbar-body4-body-i-32.md` — [withdrawn](../../v2/bugs/withdrawn.md); a later run no longer makes this claim |
| Original SHA-256 | 6b0b96e53b9a011e248d235bf0715fa09ae0f8efa394e0fa34d69f414d8fad07 |

## Why this is a false positive

Off-diagonal inertia tensor entries are signed (the declaration explicitly allows negative infinity as a lower bound); zero off-diagonal entries describe principal axes. The assembled tensor must satisfy matrix-level physical constraints, not elementwise strict positivity. This does not dismiss a separate invalid diagonal/eigenvalue report.

## Source evidence

Compiler/source-resolved declaration: `Mechanics/MultiBody/Parts/Body.mo:27`. Role: `parameter`; binding: `body4.I[3, 2]`; effective min: `-1.7976931348623157e+308`; effective max: `None`. 

[Mechanics/MultiBody/Parts/Body.mo — source snapshot](../evidence/sources/2679a27d72bf2ff2-Body.mo)

```modelica
25:   parameter SI.Inertia I_31(min=-C.inf) = 0 "Element (3,1) of inertia tensor"
26:     annotation (Dialog(group="Inertia tensor (resolved in center of mass, parallel to frame_a)"));
27:   parameter SI.Inertia I_32(min=-C.inf) = 0 "Element (3,2) of inertia tensor"
28:     annotation (Dialog(group="Inertia tensor (resolved in center of mass, parallel to frame_a)"));
29: 
30:   SI.Position r_0[3](start={0,0,0}, each stateSelect=if enforceStates then
```

[Mechanics/MultiBody/Parts/Body.mo — source snapshot](../evidence/sources/2679a27d72bf2ff2-Body.mo)

```modelica
25:   parameter SI.Inertia I_31(min=-C.inf) = 0 "Element (3,1) of inertia tensor"
26:     annotation (Dialog(group="Inertia tensor (resolved in center of mass, parallel to frame_a)"));
27:   parameter SI.Inertia I_32(min=-C.inf) = 0 "Element (3,2) of inertia tensor"
28:     annotation (Dialog(group="Inertia tensor (resolved in center of mass, parallel to frame_a)"));
29: 
30:   SI.Position r_0[3](start={0,0,0}, each stateSelect=if enforceStates then
```


## Execution evidence

[Rumoca commands, return codes, integrity hashes, bounded output and metadata](../evidence/fe77c56e3bd2e90a.json). Baseline: **tool-error**.

No independent runtime override was executed for this target in this audit; this is not a pass.

## Recommended action

Correct the detector/adjudicator for this specific semantic case; do not impose a blanket strictly-positive bound on the library declaration.

## Scope and limitations

A source-level verdict addresses the reported declaration/claim, not every possible connected system. Tests cover 0–0.5 seconds and are not a proof of long-run stability. Shared instances are not distinct root causes. A missing bound, timeout, compiler error or failed nominal run alone never counts as a verified bug or a false positive. Fixes are proposals; no library/compiler implementation was changed.

[Group and related reports](../groups/signed-inertia-tensor.md) · [Index](../README.md)
