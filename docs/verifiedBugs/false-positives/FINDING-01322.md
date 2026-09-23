# FINDING-01322: Zero inertia is a massless algebraic component, not an intrinsic division

| Field | Value |
|---|---|
| Verdict | false-positives |
| Scope / group | zero-rotational-inertia |
| Model | Modelica.Electrical.Machines.Examples.DCMachines.DCPM_Drive |
| Target | dcpm2.inertiaStator.J |
| Student classification | physical-bound-permits-zero |
| Original report | [FINDING-dcpm-drive-dcpm2-inertiastator-j-zerolimit.md](../../v2/bugs/FINDING-dcpm-drive-dcpm2-inertiastator-j-zerolimit.md) — reviewed as `FINDING-01322-dcpm-drive-dcpm2-inertiastator-j.md`, which a later run renamed |
| Original SHA-256 | 622c532c82ba9e365edf0ff41ebf5176e68143fe961703e92cb208f5e76d6cf9 |

## Why this is a false positive

The declared min is zero and the equation is J*a=flange_a.tau+flange_b.tau. At J=0 this becomes an algebraic torque-balance constraint; the source does not divide by J. Independent controls retain J=0 and simulate after incompatible fixed initialization is removed. Some topologies can be over/under-constrained, but that does not establish a universal J>0 defect.

## Source evidence

Compiler/source-resolved declaration: `Mechanics/Rotational/Components/Inertia.mo:4`. Role: `parameter`; binding: `dcpm2.Js`; effective min: `0`; effective max: `None`. 

[Mechanics/Rotational/Components/Inertia.mo — source snapshot](../evidence/sources/f3686d31c0612222-Inertia.mo)

```modelica
2: model Inertia "1D-rotational component with inertia"
3:   extends Rotational.Interfaces.PartialTwoFlanges;
4:   parameter SI.Inertia J(min=0, start=1) "Moment of inertia";
5:   parameter StateSelect stateSelect=StateSelect.default
6:     "Priority to use phi and w as states"
7:     annotation (HideResult=true, Dialog(tab="Advanced"));
```

[Mechanics/Rotational/Components/Inertia.mo — source snapshot](../evidence/sources/f3686d31c0612222-Inertia.mo)

```modelica
2: model Inertia "1D-rotational component with inertia"
3:   extends Rotational.Interfaces.PartialTwoFlanges;
4:   parameter SI.Inertia J(min=0, start=1) "Moment of inertia";
5:   parameter StateSelect stateSelect=StateSelect.default
6:     "Priority to use phi and w as states"
7:     annotation (HideResult=true, Dialog(tab="Advanced"));
8:   SI.Angle phi(stateSelect=stateSelect)
9:     "Absolute rotation angle of component"
10:     annotation (Dialog(group="Initialization", showStartAttribute=true));
11:   SI.AngularVelocity w(stateSelect=stateSelect)
12:     "Absolute angular velocity of component (= der(phi))"
13:     annotation (Dialog(group="Initialization", showStartAttribute=true));
14:   SI.AngularAcceleration a
15:     "Absolute angular acceleration of component (= der(w))"
16:     annotation (Dialog(group="Initialization", showStartAttribute=true));
17: 
18: equation
19:   phi = flange_a.phi;
20:   phi = flange_b.phi;
21:   w = der(phi);
22:   a = der(w);
23:   J*a = flange_a.tau + flange_b.tau;
24:   annotation (Documentation(info="<html>
25: <p>
26: Rotational component with <strong>inertia</strong> and two rigidly connected flanges.
```


## Execution evidence

[Rumoca commands, return codes, integrity hashes, bounded output and metadata](../evidence/3f243142a2b979d6.json). Baseline: **tool-error**.

No independent runtime override was executed for this target in this audit; this is not a pass.

## Recommended action

Correct the detector/adjudicator for this specific semantic case; do not impose a blanket strictly-positive bound on the library declaration.

## Scope and limitations

A source-level verdict addresses the reported declaration/claim, not every possible connected system. Tests cover 0–0.5 seconds and are not a proof of long-run stability. Shared instances are not distinct root causes. A missing bound, timeout, compiler error or failed nominal run alone never counts as a verified bug or a false positive. Fixes are proposals; no library/compiler implementation was changed.

[Group and related reports](../groups/zero-rotational-inertia.md) · [Index](../README.md)
