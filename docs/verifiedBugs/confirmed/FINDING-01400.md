# FINDING-01400: Zero nominal speed makes DC-machine scaling undefined

| Field | Value |
|---|---|
| Verdict | confirmed |
| Scope / group | dc-data-nominal-speed |
| Model | Modelica.Electrical.Machines.Examples.DCMachines.DCPM_Start |
| Target | dcpmData.wNominal |
| Student classification | divisor-reachable-zero |
| Original report | `FINDING-01400-dcpm-start-dcpmdata-wnominal.md` — [withdrawn](../../v2/bugs/withdrawn.md); a later run no longer makes this claim |
| Original SHA-256 | 91b672d525cd49fc50e1f328753a3e772a1bd23f08f7d59d904dbba3d4ec217d |

## Verification and root cause

DcPermanentMagnetData leaves wNominal unconstrained and forwards it to the machine/loss records. PartialBasicDCMachine computes turnsRatio=ViNominal/(wNominal*psi_eNominal). The data record therefore admits a value that makes a common consumer divide by zero.

## Source evidence

Compiler/source-resolved declaration: `Electrical/Machines/Utilities/ParameterRecords/DcPermanentMagnetData.mo:13`. Role: `parameter`; binding: `(((1425 * 2) * (2 * asin(1.0))) / 60)`; effective min: `None`; effective max: `None`. 

[Electrical/Machines/Utilities/ParameterRecords/DcPermanentMagnetData.mo — source snapshot](../evidence/sources/dd335b6f66800523-DcPermanentMagnetData.mo)

```modelica
11:     "Nominal armature current (>0..Motor, <0..Generator)"
12:     annotation (Dialog(tab="Nominal parameters"));
13:   parameter SI.AngularVelocity wNominal(displayUnit="rev/min")=
14:        1425*2*pi/60 "Nominal speed"
15:     annotation (Dialog(tab="Nominal parameters"));
16:   parameter SI.Temperature TaNominal=293.15
```

[Electrical/Machines/Utilities/ParameterRecords/DcPermanentMagnetData.mo — source snapshot](../evidence/sources/dd335b6f66800523-DcPermanentMagnetData.mo)

```modelica
5:   parameter SI.Inertia Jr=0.15 "Rotor's moment of inertia";
6:   parameter SI.Inertia Js=Jr "Stator's moment of inertia";
7:   parameter SI.Voltage VaNominal=100
8:     "Nominal armature voltage"
9:     annotation (Dialog(tab="Nominal parameters"));
10:   parameter SI.Current IaNominal=100
11:     "Nominal armature current (>0..Motor, <0..Generator)"
12:     annotation (Dialog(tab="Nominal parameters"));
13:   parameter SI.AngularVelocity wNominal(displayUnit="rev/min")=
14:        1425*2*pi/60 "Nominal speed"
15:     annotation (Dialog(tab="Nominal parameters"));
16:   parameter SI.Temperature TaNominal=293.15
17:     "Nominal armature temperature"
18:     annotation (Dialog(tab="Nominal parameters"));
```

[Electrical/Machines/Interfaces/PartialBasicDCMachine.mo — source snapshot](../evidence/sources/4db8b5f43a5834a2-PartialBasicDCMachine.mo)

```modelica
94:   constant Real pi = Modelica.Constants.pi;
95:   constant Boolean quasiStatic=false "No electrical transients if true"
96:     annotation (Evaluate=true);
97:   parameter SI.Voltage ViNominal "Nominal induced Voltage";
98:   parameter SI.MagneticFlux psi_eNominal
99:     "Nominal magnetic flux";
100:   parameter Real turnsRatio=ViNominal/(wNominal*psi_eNominal)
101:     "Ratio of armature turns over number of turns of the excitation winding";
102:   replaceable Machines.Interfaces.DCMachines.PartialThermalPortDCMachines internalThermalPort
103:     annotation (Placement(transformation(extent={{-4,-84},{4,-76}})));
```


## Execution evidence

[Rumoca commands, return codes, integrity hashes, bounded output and metadata](../evidence/58aaee5fa3eb7c79.json). Baseline: **tool-error**.

No independent runtime override was executed for this target in this audit; this is not a pass.

## Proposed fix

Require and validate a nonzero nominal speed using the documented motor/generator sign convention before turns-ratio and loss-reference calculations. If standstill data are needed, define a different identification input rather than dividing by speed.

## Fix validation

Test positive nominal speed, supported reverse sign, zero, and near-zero speed in a minimal DC permanent-magnet machine/data projection.

## Scope and limitations

A source-level verdict addresses the reported declaration/claim, not every possible connected system. Tests cover 0–0.5 seconds and are not a proof of long-run stability. Shared instances are not distinct root causes. A missing bound, timeout, compiler error or failed nominal run alone never counts as a verified bug or a false positive. Fixes are proposals; no library/compiler implementation was changed.

[Group and related reports](../groups/dc-data-nominal-speed.md) · [Index](../README.md)
