# FINDING-03962: MultiBody Newton/Euler equations use mass and inertia multiplicatively

| Field | Value |
|---|---|
| Verdict | false-positives |
| Scope / group | zero-multibody-inertia |
| Model | Modelica.Mechanics.MultiBody.Examples.Elementary.FreeBody |
| Target | body.body.I_22 |
| Student classification | physical-bound-permits-zero |
| Original report | `FINDING-03962-freebody-body-body-i-22.md` — [withdrawn](../../v2/bugs/withdrawn.md); a later run no longer makes this claim |
| Original SHA-256 | 2fbeafe57f09fd63fdd3572ea1c63a04adc7109b9833d283a5d9130cb833d49c |

## Why this is a false positive

The declaration intentionally has min=0. Newton/Euler equations are frame_a.f=m*(...) and frame_a.t=I*z_a+cross(w_a,I*w_a)+..., with no source reciprocal. Zero mass/inertia converts dynamics to algebraic balance constraints. A singular inertia tensor may make a chosen free-body state formulation unsuitable, but that topology/state-selection issue does not prove every zero bound is wrong.

## Source evidence

Compiler/source-resolved declaration: `Mechanics/MultiBody/Parts/Body.mo:19`. Role: `parameter`; binding: `1`; effective min: `0`; effective max: `None`. 

[Mechanics/MultiBody/Parts/Body.mo — source snapshot](../evidence/sources/2679a27d72bf2ff2-Body.mo)

```modelica
17:   parameter SI.Inertia I_11(min=0) = 0.001 "Element (1,1) of inertia tensor"
18:     annotation (Dialog(group="Inertia tensor (resolved in center of mass, parallel to frame_a)"));
19:   parameter SI.Inertia I_22(min=0) = 0.001 "Element (2,2) of inertia tensor"
20:     annotation (Dialog(group="Inertia tensor (resolved in center of mass, parallel to frame_a)"));
21:   parameter SI.Inertia I_33(min=0) = 0.001 "Element (3,3) of inertia tensor"
22:     annotation (Dialog(group="Inertia tensor (resolved in center of mass, parallel to frame_a)"));
```

[Mechanics/MultiBody/Parts/Body.mo — source snapshot](../evidence/sources/2679a27d72bf2ff2-Body.mo)

```modelica
14:   parameter SI.Position r_CM[3](start={0,0,0})
15:     "Vector from frame_a to center of mass, resolved in frame_a";
16:   parameter SI.Mass m(min=0, start=1) "Mass of rigid body";
17:   parameter SI.Inertia I_11(min=0) = 0.001 "Element (1,1) of inertia tensor"
18:     annotation (Dialog(group="Inertia tensor (resolved in center of mass, parallel to frame_a)"));
19:   parameter SI.Inertia I_22(min=0) = 0.001 "Element (2,2) of inertia tensor"
20:     annotation (Dialog(group="Inertia tensor (resolved in center of mass, parallel to frame_a)"));
21:   parameter SI.Inertia I_33(min=0) = 0.001 "Element (3,3) of inertia tensor"
22:     annotation (Dialog(group="Inertia tensor (resolved in center of mass, parallel to frame_a)"));
23:   parameter SI.Inertia I_21(min=-C.inf) = 0 "Element (2,1) of inertia tensor"
24:     annotation (Dialog(group="Inertia tensor (resolved in center of mass, parallel to frame_a)"));
25:   parameter SI.Inertia I_31(min=-C.inf) = 0 "Element (3,1) of inertia tensor"
26:     annotation (Dialog(group="Inertia tensor (resolved in center of mass, parallel to frame_a)"));
27:   parameter SI.Inertia I_32(min=-C.inf) = 0 "Element (3,2) of inertia tensor"
28:     annotation (Dialog(group="Inertia tensor (resolved in center of mass, parallel to frame_a)"));
29: 
30:   SI.Position r_0[3](start={0,0,0}, each stateSelect=if enforceStates then
```

[Mechanics/MultiBody/Parts/Body.mo — source snapshot](../evidence/sources/2679a27d72bf2ff2-Body.mo)

```modelica
239:   // gravity acceleration at center of mass resolved in world frame
240:   g_0 = world.gravityAcceleration(frame_a.r_0 + Frames.resolve1(frame_a.R,
241:     r_CM));
242: 
243:   // translational kinematic differential equations
244:   v_0 = der(frame_a.r_0);
245:   a_0 = der(v_0);
246: 
247:   // rotational kinematic differential equations
248:   w_a = Frames.angularVelocity2(frame_a.R);
249:   z_a = der(w_a);
250: 
251:   /* Newton/Euler equations with respect to center of mass
252:             a_CM = a_a + cross(z_a, r_CM) + cross(w_a, cross(w_a, r_CM));
253:             f_CM = m*(a_CM - g_a);
254:             t_CM = I*z_a + cross(w_a, I*w_a);
255:        frame_a.f = f_CM
256:        frame_a.t = t_CM + cross(r_CM, f_CM);
257:     Inserting the first three equations in the last two results in:
258:   */
259:   frame_a.f = m*(Frames.resolve2(frame_a.R, a_0 - g_0) + cross(z_a, r_CM) +
260:     cross(w_a, cross(w_a, r_CM)));
261:   frame_a.t = I*z_a + cross(w_a, I*w_a) + cross(r_CM, frame_a.f);
```


## Execution evidence

[Rumoca commands, return codes, integrity hashes, bounded output and metadata](../evidence/3ffcb12a5aceb937.json). Baseline: **tool-error**.

No independent runtime override was executed for this target in this audit; this is not a pass.

## Recommended action

Correct the detector/adjudicator for this specific semantic case; do not impose a blanket strictly-positive bound on the library declaration.

## Scope and limitations

A source-level verdict addresses the reported declaration/claim, not every possible connected system. Tests cover 0–0.5 seconds and are not a proof of long-run stability. Shared instances are not distinct root causes. A missing bound, timeout, compiler error or failed nominal run alone never counts as a verified bug or a false positive. Fixes are proposals; no library/compiler implementation was changed.

[Group and related reports](../groups/zero-multibody-inertia.md) · [Index](../README.md)
