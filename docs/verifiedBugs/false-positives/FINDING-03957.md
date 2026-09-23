# FINDING-03957: Tensor entries are not all strictly positive scalars

| Field | Value |
|---|---|
| Verdict | false-positives |
| Scope / group | signed-inertia-tensor |
| Model | Modelica.Mechanics.MultiBody.Examples.Elementary.FreeBody |
| Target | body.I_21 |
| Student classification | physical-domain-unenforced |
| Original report | `FINDING-03957-freebody-body-i-21.md` — [withdrawn](../../v2/bugs/withdrawn.md); a later run no longer makes this claim |
| Original SHA-256 | 7252f6691114724b92d47148a5c385049182ba11bf9a59987ed6a700dee75075 |

## Why this is a false positive

Off-diagonal inertia tensor entries are signed (the declaration explicitly allows negative infinity as a lower bound); zero off-diagonal entries describe principal axes. The assembled tensor must satisfy matrix-level physical constraints, not elementwise strict positivity. This does not dismiss a separate invalid diagonal/eigenvalue report.

## Source evidence

Compiler/source-resolved declaration: `Mechanics/MultiBody/Parts/BodyShape.mo:30`. Role: `parameter`; binding: `0`; effective min: `-1.7976931348623157e+308`; effective max: `None`. 

[Mechanics/MultiBody/Parts/BodyShape.mo — source snapshot](../evidence/sources/90d48d37a154ba16-BodyShape.mo)

```modelica
28:   parameter SI.Inertia I_33(min=0) = 0.001 "Element (3,3) of inertia tensor"
29:     annotation (Dialog(group="Inertia tensor (resolved in center of mass, parallel to frame_a)"));
30:   parameter SI.Inertia I_21(min=-C.inf) = 0 "Element (2,1) of inertia tensor"
31:     annotation (Dialog(group="Inertia tensor (resolved in center of mass, parallel to frame_a)"));
32:   parameter SI.Inertia I_31(min=-C.inf) = 0 "Element (3,1) of inertia tensor"
33:     annotation (Dialog(group="Inertia tensor (resolved in center of mass, parallel to frame_a)"));
```

[Mechanics/MultiBody/Parts/BodyShape.mo — source snapshot](../evidence/sources/90d48d37a154ba16-BodyShape.mo)

```modelica
28:   parameter SI.Inertia I_33(min=0) = 0.001 "Element (3,3) of inertia tensor"
29:     annotation (Dialog(group="Inertia tensor (resolved in center of mass, parallel to frame_a)"));
30:   parameter SI.Inertia I_21(min=-C.inf) = 0 "Element (2,1) of inertia tensor"
31:     annotation (Dialog(group="Inertia tensor (resolved in center of mass, parallel to frame_a)"));
32:   parameter SI.Inertia I_31(min=-C.inf) = 0 "Element (3,1) of inertia tensor"
33:     annotation (Dialog(group="Inertia tensor (resolved in center of mass, parallel to frame_a)"));
```


## Execution evidence

[Rumoca commands, return codes, integrity hashes, bounded output and metadata](../evidence/3ffcb12a5aceb937.json). Baseline: **tool-error**.

No independent runtime override was executed for this target in this audit; this is not a pass.

## Recommended action

Correct the detector/adjudicator for this specific semantic case; do not impose a blanket strictly-positive bound on the library declaration.

## Scope and limitations

A source-level verdict addresses the reported declaration/claim, not every possible connected system. Tests cover 0–0.5 seconds and are not a proof of long-run stability. Shared instances are not distinct root causes. A missing bound, timeout, compiler error or failed nominal run alone never counts as a verified bug or a false positive. Fixes are proposals; no library/compiler implementation was changed.

[Group and related reports](../groups/signed-inertia-tensor.md) · [Index](../README.md)
