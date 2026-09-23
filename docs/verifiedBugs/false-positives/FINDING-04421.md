# FINDING-04421: Zero mass is a massless algebraic component, not an intrinsic division

| Field | Value |
|---|---|
| Verdict | false-positives |
| Scope / group | zero-translational-mass |
| Model | Modelica.Mechanics.Translational.Examples.CompareBrakingForce |
| Target | mass3.m |
| Student classification | physical-bound-permits-zero |
| Original report | [FINDING-comparebrakingforce-mass3-m-zerolimit.md](../../v2/bugs/FINDING-comparebrakingforce-mass3-m-zerolimit.md) — reviewed as `FINDING-04421-comparebrakingforce-mass3-m.md`, which a later run renamed |
| Original SHA-256 | 43659bc8b85b49518eda5be7e08d07e70f73b4eb3362870b3a6fd94ea62cf7b9 |

## Why this is a false positive

The declared min is zero and the equation is m*a=flange_a.f+flange_b.f. At m=0 this becomes an algebraic force-balance constraint; the source does not divide by m. Independent controls retain m=0 and simulate after incompatible fixed initialization is removed. Some connected systems can be inconsistent, but the blanket strictly-positive attribution is false.

## Source evidence

Compiler/source-resolved declaration: `Mechanics/Translational/Components/Mass.mo:3`. Role: `parameter`; binding: `m`; effective min: `0`; effective max: `None`. 

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

[Rumoca commands, return codes, integrity hashes, bounded output and metadata](../evidence/a87b7cf9305a618d.json). Baseline: **clean**.

| Probe | Outcome |
|---|---|
| `mass3.m=0` | reported-failure |

Diagnostic: solve-IR evaluation failed: algebraic projection did not converge at event boundary: worst scaled residual row=24 target=mass3.a value=1.000000e2 ratio=1.000000e12 norm=1.000000e2 row_scale=1.000000e0 scaled_tolerance=1.000000e-10

## Recommended action

Correct the detector/adjudicator for this specific semantic case; do not impose a blanket strictly-positive bound on the library declaration.

## Scope and limitations

A source-level verdict addresses the reported declaration/claim, not every possible connected system. Tests cover 0–0.5 seconds and are not a proof of long-run stability. Shared instances are not distinct root causes. A missing bound, timeout, compiler error or failed nominal run alone never counts as a verified bug or a false positive. Fixes are proposals; no library/compiler implementation was changed.

[Group and related reports](../groups/zero-translational-mass.md) · [Index](../README.md)
