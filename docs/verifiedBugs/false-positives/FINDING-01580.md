# FINDING-01580: Machine inertia delegates to the zero-capable algebraic inertia component

| Field | Value |
|---|---|
| Verdict | false-positives |
| Scope / group | zero-machine-inertia |
| Model | Modelica.Electrical.Machines.Examples.InductionMachines.IMC_DOL |
| Target | aimc.Jr |
| Student classification | physical-domain-unenforced |
| Original report | [FINDING-imc-dol-aimc-jr-zerolimit.md](../../v2/bugs/FINDING-imc-dol-aimc-jr-zerolimit.md) — reviewed as `FINDING-01580-imc-dol-aimc-jr.md`, which a later run renamed |
| Original SHA-256 | c877408ee0644cba3cc2db1dfe60728f90b08e078dd6f1604c144eb11ce83a2d |

## Why this is a false positive

Jr and Js are passed directly to Rotational.Components.Inertia. That component uses J*a=sum(tau), so J=0 produces an algebraic torque balance rather than an intrinsic reciprocal. Js is relevant only when the stator rotates. A particular drive train can have incompatible starts or constraints, but the declaration alone does not establish that both machine inertias must be strictly positive.

## Source evidence

Compiler/source-resolved declaration: `Electrical/Machines/Interfaces/PartialBasicMachine.mo:5`. Role: `parameter`; binding: `aimcData.Jr`; effective min: `None`; effective max: `None`. 

[Electrical/Machines/Interfaces/PartialBasicMachine.mo — source snapshot](../evidence/sources/b5bf16a07237f12f-PartialBasicMachine.mo)

```modelica
3:   import Modelica.Constants.pi;
4:   extends Machines.Icons.TransientMachine;
5:   parameter SI.Inertia Jr "Rotor's moment of inertia";
6:   parameter Boolean useSupport=false
7:     "Enable / disable (=fixed stator) support" annotation (Evaluate=true);
8:   parameter SI.Inertia Js=Jr "Stator's moment of inertia"
```

[Electrical/Machines/Interfaces/PartialBasicMachine.mo — source snapshot](../evidence/sources/b5bf16a07237f12f-PartialBasicMachine.mo)

```modelica
2: partial model PartialBasicMachine "Partial model for all machines"
3:   import Modelica.Constants.pi;
4:   extends Machines.Icons.TransientMachine;
5:   parameter SI.Inertia Jr "Rotor's moment of inertia";
6:   parameter Boolean useSupport=false
7:     "Enable / disable (=fixed stator) support" annotation (Evaluate=true);
8:   parameter SI.Inertia Js=Jr "Stator's moment of inertia"
9:                                  annotation (Dialog(enable=useSupport));
10:   parameter Boolean useThermalPort=false
11:     "Enable / disable (=fixed temperatures) thermal port"
12:     annotation (Evaluate=true);
13:   parameter Machines.Losses.FrictionParameters frictionParameters
14:     "Friction loss parameter record" annotation (Dialog(tab="Losses"));
15:   output SI.Angle phiMechanical(start=0) = flange.phi -
16:     internalSupport.phi "Mechanical angle of rotor against stator";
17:   output SI.AngularVelocity wMechanical(
18:     displayUnit="rev/min",
19:     start=0) = der(phiMechanical)
20:     "Mechanical angular velocity of rotor against stator";
21:   output SI.Torque tauElectrical=inertiaRotor.flange_a.tau
22:     "Electromagnetic torque";
23:   output SI.Torque tauShaft=-flange.tau "Shaft torque";
24:   Modelica.Mechanics.Rotational.Interfaces.Flange_a flange "Shaft"
25:     annotation (Placement(transformation(extent={{90,-10},{110,10}})));
26:   Modelica.Mechanics.Rotational.Components.Inertia inertiaRotor(final J=Jr)
27:     annotation (Placement(transformation(
28:         origin={80,0},
29:         extent={{10,10},{-10,-10}},
30:         rotation=180)));
31:   Modelica.Mechanics.Rotational.Interfaces.Flange_a support if useSupport
32:     "Support at which the reaction torque is acting" annotation (Placement(
33:         transformation(extent={{90,-110},{110,-90}})));
34:   Modelica.Mechanics.Rotational.Components.Inertia inertiaStator(final J=Js)
35:     annotation (Placement(transformation(
36:         origin={80,-100},
37:         extent={{10,10},{-10,-10}},
38:         rotation=180)));
39:   Modelica.Mechanics.Rotational.Components.Fixed fixed if (not useSupport)
40:     annotation (Placement(transformation(
```

[Mechanics/Rotational/Components/Inertia.mo — source snapshot](../evidence/sources/f3686d31c0612222-Inertia.mo)

```modelica
20:   phi = flange_b.phi;
21:   w = der(phi);
22:   a = der(w);
23:   J*a = flange_a.tau + flange_b.tau;
24:   annotation (Documentation(info="<html>
25: <p>
26: Rotational component with <strong>inertia</strong> and two rigidly connected flanges.
```


## Execution evidence

[Rumoca commands, return codes, integrity hashes, bounded output and metadata](../evidence/3bb307101f6982f2.json). Baseline: **tool-error**.

No independent runtime override was executed for this target in this audit; this is not a pass.

## Recommended action

Correct the detector/adjudicator for this specific semantic case; do not impose a blanket strictly-positive bound on the library declaration.

## Scope and limitations

A source-level verdict addresses the reported declaration/claim, not every possible connected system. Tests cover 0–0.5 seconds and are not a proof of long-run stability. Shared instances are not distinct root causes. A missing bound, timeout, compiler error or failed nominal run alone never counts as a verified bug or a false positive. Fixes are proposals; no library/compiler implementation was changed.

[Group and related reports](../groups/zero-machine-inertia.md) · [Index](../README.md)
