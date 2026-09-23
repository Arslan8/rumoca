# FINDING-04425: Zero mass is a massless algebraic component, not an intrinsic division

| Field | Value |
|---|---|
| Verdict | false-positives |
| Scope / group | zero-translational-mass |
| Model | Modelica.Mechanics.Translational.Examples.Damper |
| Target | mass1.m |
| Student classification | physical-bound-permits-zero |
| Original report | [BUG-damper-mass1-m.md](../../v2/bugs/BUG-damper-mass1-m.md) — reviewed as `FINDING-04425-damper-mass1-m.md`, which a later run renamed |
| Original SHA-256 | 2d66056930e5943fa414c53d12f849556d19e782121469f62b3324c1174d9d6e |

## Why this is a false positive

The declared min is zero and the equation is m*a=flange_a.f+flange_b.f. At m=0 this becomes an algebraic force-balance constraint; the source does not divide by m. Independent controls retain m=0 and simulate after incompatible fixed initialization is removed. Some connected systems can be inconsistent, but the blanket strictly-positive attribution is false.

## Source evidence

Compiler/source-resolved declaration: `Mechanics/Translational/Components/Mass.mo:3`. Role: `parameter`; binding: `1`; effective min: `0`; effective max: `None`. 

[Mechanics/Translational/Components/Mass.mo — source snapshot](../evidence/sources/d34580bdea973245-Mass.mo)

```modelica
1: within Modelica.Mechanics.Translational.Components;
2: model Mass "Sliding mass with inertia"
3:   parameter SI.Mass m(min=0, start=1) "Mass of the sliding mass";
4:   parameter StateSelect stateSelect=StateSelect.default
5:     "Priority to use s and v as states" annotation (Dialog(tab="Advanced"));
6:   extends Translational.Interfaces.PartialRigid(L=0,s(start=0, stateSelect=
```

[Mechanics/Translational/Components/Mass.mo — source snapshot](../evidence/sources/d34580bdea973245-Mass.mo)

```modelica
2: model Mass "Sliding mass with inertia"
3:   parameter SI.Mass m(min=0, start=1) "Mass of the sliding mass";
4:   parameter StateSelect stateSelect=StateSelect.default
5:     "Priority to use s and v as states" annotation (Dialog(tab="Advanced"));
6:   extends Translational.Interfaces.PartialRigid(L=0,s(start=0, stateSelect=
7:           stateSelect));
8:   SI.Velocity v(start=0, stateSelect=stateSelect)
9:     "Absolute velocity of component";
10:   SI.Acceleration a(start=0) "Absolute acceleration of component";
11: 
12: equation
13:   v = der(s);
14:   a = der(v);
15:   m*a = flange_a.f + flange_b.f;
16:   annotation (
```


## Execution evidence

[Rumoca commands, return codes, integrity hashes, bounded output and metadata](../evidence/2f5c9ac506c1b046.json). Baseline: **clean**.

| Probe | Outcome |
|---|---|
| `mass1.m=0` | reported-failure |

Diagnostic: solve-IR evaluation failed: algebraic projection did not converge at event boundary: worst scaled residual row=4 target=mass1.a value=2.500000e2 ratio=2.500000e12 norm=2.500000e2 row_scale=1.000000e0 scaled_tolerance=1.000000e-10

[Independent OpenModelica wrappers and complete output](../evidence/omc-2f5c9ac506c1b046.json). Baseline: simulation succeeded.

- `mass1.m=0` set before translation: LOG_ASSERT        | debug   | division by zero at time 0, (a=-250) / (b=0), where divisor b expression is: mass1.m.
- Same value declared final, with final-parameter evaluation: LOG_INIT          | error   | The initialization problem is inconsistent due to the following equation: 0 != 10 = $START.mass1.v - mass1.v.

## Recommended action

Correct the detector/adjudicator for this specific semantic case; do not impose a blanket strictly-positive bound on the library declaration.

## Scope and limitations

A source-level verdict addresses the reported declaration/claim, not every possible connected system. Tests cover 0–0.5 seconds and are not a proof of long-run stability. Shared instances are not distinct root causes. A missing bound, timeout, compiler error or failed nominal run alone never counts as a verified bug or a false positive. Fixes are proposals; no library/compiler implementation was changed.

[Group and related reports](../groups/zero-translational-mass.md) · [Index](../README.md)
