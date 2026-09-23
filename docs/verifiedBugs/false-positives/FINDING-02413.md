# FINDING-02413: Machine-data inertia is not intrinsically a positive divisor

| Field | Value |
|---|---|
| Verdict | false-positives |
| Scope / group | zero-machine-data-inertia |
| Model | Modelica.Electrical.Machines.Examples.SynchronousMachines.SMPM_NoLoad |
| Target | smpmData.Jr |
| Student classification | physical-domain-unenforced |
| Original report | [FINDING-smpm-noload-smpmdata-jr-intent.md](../../v2/bugs/FINDING-smpm-noload-smpmdata-jr-intent.md) — reviewed as `FINDING-02413-smpm-noload-smpmdata-jr.md`, which a later run renamed |
| Original SHA-256 | 5bdf24ad5d0fead0d558d5f0b4ca9251590edbc30b17676382b16b9d0d0809e2 |

## Why this is a false positive

These record fields are forwarded as Jr/Js to machine inertias. The consumer component uses J as a multiplier in torque balance, so zero is a massless algebraic limit. A report needs a specific incompatible drive-train topology or initialization; absence of a strictly-positive record bound alone is not a verified defect.

## Source evidence

Compiler/source-resolved declaration: `Electrical/Machines/Utilities/ParameterRecords/InductionMachineData.mo:6`. Role: `parameter`; binding: `0.29`; effective min: `None`; effective max: `None`. 

[Electrical/Machines/Utilities/ParameterRecords/InductionMachineData.mo — source snapshot](../evidence/sources/8d312108fd6330eb-InductionMachineData.mo)

```modelica
4:   import Modelica.Constants.pi;
5:   parameter Integer m=3 "Number of phases" annotation(Evaluate=true);
6:   parameter SI.Inertia Jr=0.29 "Rotor's moment of inertia";
7:   parameter SI.Inertia Js=Jr "Stator's moment of inertia";
8:   parameter Integer p(min=1) = 2 "Number of pole pairs (Integer)";
9:   parameter SI.Frequency fsNominal=50 "Nominal frequency";
```

[Electrical/Machines/Utilities/ParameterRecords/InductionMachineData.mo — source snapshot](../evidence/sources/8d312108fd6330eb-InductionMachineData.mo)

```modelica
4:   import Modelica.Constants.pi;
5:   parameter Integer m=3 "Number of phases" annotation(Evaluate=true);
6:   parameter SI.Inertia Jr=0.29 "Rotor's moment of inertia";
7:   parameter SI.Inertia Js=Jr "Stator's moment of inertia";
8:   parameter Integer p(min=1) = 2 "Number of pole pairs (Integer)";
9:   parameter SI.Frequency fsNominal=50 "Nominal frequency";
10:   parameter SI.Resistance Rs=0.03
```

[Electrical/Machines/Interfaces/PartialBasicMachine.mo — source snapshot](../evidence/sources/b5bf16a07237f12f-PartialBasicMachine.mo)

```modelica
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


## Execution evidence

[Rumoca commands, return codes, integrity hashes, bounded output and metadata](../evidence/dd1bf4e5a4d0a401.json). Baseline: **tool-error**.

No independent runtime override was executed for this target in this audit; this is not a pass.

## Recommended action

Correct the detector/adjudicator for this specific semantic case; do not impose a blanket strictly-positive bound on the library declaration.

## Scope and limitations

A source-level verdict addresses the reported declaration/claim, not every possible connected system. Tests cover 0–0.5 seconds and are not a proof of long-run stability. Shared instances are not distinct root causes. A missing bound, timeout, compiler error or failed nominal run alone never counts as a verified bug or a false positive. Fixes are proposals; no library/compiler implementation was changed.

[Group and related reports](../groups/zero-machine-data-inertia.md) · [Index](../README.md)
