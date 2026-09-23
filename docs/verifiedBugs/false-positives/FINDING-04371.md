# FINDING-04371: Zero rotational stiffness/damping disables one torque term

| Field | Value |
|---|---|
| Verdict | false-positives |
| Scope / group | zero-rotational-spring-damper |
| Model | Modelica.Mechanics.Rotational.Examples.Backlash |
| Target | springDamper.c |
| Student classification | physical-bound-permits-zero |
| Original report | [FINDING-backlash-springdamper-c-zerolimit.md](../../v2/bugs/FINDING-backlash-springdamper-c-zerolimit.md) — reviewed as `FINDING-04371-backlash-springdamper-c.md`, which a later run renamed |
| Original SHA-256 | 9ae6b0ac019eab11b2d72cebfe04a5ab4feb95044ae25d98bfde4faee182e19a |

## Why this is a false positive

The component torque is the sum of c*phi_rel and d*w_rel terms. c and d have min=0 and are multipliers, so zero cleanly removes elasticity or damping; it is not an unguarded divisor.

## Source evidence

Compiler/source-resolved declaration: `Mechanics/Rotational/Components/SpringDamper.mo:3`. Role: `parameter`; binding: `20000.0`; effective min: `0`; effective max: `None`. 

[Mechanics/Rotational/Components/SpringDamper.mo — source snapshot](../evidence/sources/3d8c666da73c7e12-SpringDamper.mo)

```modelica
1: within Modelica.Mechanics.Rotational.Components;
2: model SpringDamper "Linear 1D rotational spring and damper in parallel"
3:   parameter SI.RotationalSpringConstant c(final min=0, start=1.0e5)
4:     "Spring constant";
5:   parameter SI.RotationalDampingConstant d(final min=0, start=0)
6:     "Damping constant";
```

[Mechanics/Rotational/Components/SpringDamper.mo — source snapshot](../evidence/sources/3d8c666da73c7e12-SpringDamper.mo)

```modelica
2: model SpringDamper "Linear 1D rotational spring and damper in parallel"
3:   parameter SI.RotationalSpringConstant c(final min=0, start=1.0e5)
4:     "Spring constant";
5:   parameter SI.RotationalDampingConstant d(final min=0, start=0)
6:     "Damping constant";
7:   parameter SI.Angle phi_rel0=0 "Unstretched spring angle";
8:   extends
9:     Modelica.Mechanics.Rotational.Interfaces.PartialCompliantWithRelativeStates;
10:   extends
11:     Modelica.Thermal.HeatTransfer.Interfaces.PartialElementaryConditionalHeatPortWithoutT;
12: protected
13:   SI.Torque tau_c "Spring torque";
14:   SI.Torque tau_d "Damping torque";
15: equation
16:   tau_c = c*(phi_rel - phi_rel0);
17:   tau_d = d*w_rel;
18:   tau = tau_c + tau_d;
```


## Execution evidence

[Rumoca commands, return codes, integrity hashes, bounded output and metadata](../evidence/9e815ee071e762a2.json). Baseline: **clean**.

| Probe | Outcome |
|---|---|
| `springDamper.c=0` | clean |

## Recommended action

Correct the detector/adjudicator for this specific semantic case; do not impose a blanket strictly-positive bound on the library declaration.

## Scope and limitations

A source-level verdict addresses the reported declaration/claim, not every possible connected system. Tests cover 0–0.5 seconds and are not a proof of long-run stability. Shared instances are not distinct root causes. A missing bound, timeout, compiler error or failed nominal run alone never counts as a verified bug or a false positive. Fixes are proposals; no library/compiler implementation was changed.

[Group and related reports](../groups/zero-rotational-spring-damper.md) · [Index](../README.md)
