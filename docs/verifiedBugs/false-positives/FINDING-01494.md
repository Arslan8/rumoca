# FINDING-01494: DC machine-data field has a supported ideal limit

| Field | Value |
|---|---|
| Verdict | false-positives |
| Scope / group | ideal-dc-machine-data |
| Model | Modelica.Electrical.Machines.Examples.DCMachines.DCSE_SinglePhase |
| Target | dcseData.La |
| Student classification | physical-domain-unenforced |
| Original report | [FINDING-dcse-singlephase-dcsedata-la-intent.md](../../v2/bugs/FINDING-dcse-singlephase-dcsedata-la-intent.md) — reviewed as `FINDING-01494-dcse-singlephase-dcsedata-la.md`, which a later run renamed |
| Original SHA-256 | 5b52ef94ea21c5eed127a95002676ac5f9718d9d2491060182b9dd3cff09dbc5 |

## Why this is a false positive

This field represents zero armature inductance and is forwarded to a component that uses it multiplicatively: torque balance for inertia, v=R*i for resistance, or v=L*der(i) for inductance. None intrinsically requires division by the field. A specific drive train can still be inconsistent; the missing strictly-positive record bound alone is not a bug.

## Source evidence

Compiler/source-resolved declaration: `Electrical/Machines/Utilities/ParameterRecords/DcPermanentMagnetData.mo:28`. Role: `parameter`; binding: `0.0015`; effective min: `None`; effective max: `None`. 

[Electrical/Machines/Utilities/ParameterRecords/DcPermanentMagnetData.mo — source snapshot](../evidence/sources/dd335b6f66800523-DcPermanentMagnetData.mo)

```modelica
26:     "Temperature coefficient of armature resistance"
27:     annotation (Dialog(tab="Armature"));
28:   parameter SI.Inductance La=0.0015 "Armature inductance"
29:     annotation (Dialog(tab="Armature"));
30:   parameter Machines.Losses.FrictionParameters frictionParameters(PRef=0, wRef=
31:         wNominal) "Friction loss parameter record"
```

[Electrical/Machines/Utilities/ParameterRecords/DcPermanentMagnetData.mo — source snapshot](../evidence/sources/dd335b6f66800523-DcPermanentMagnetData.mo)

```modelica
4:   import Modelica.Constants.pi;
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
19:   parameter SI.Resistance Ra=0.05
20:     "Armature resistance at TaRef"
21:     annotation (Dialog(tab="Armature"));
22:   parameter SI.Temperature TaRef=293.15
23:     "Reference temperature of armature resistance"
24:     annotation (Dialog(tab="Armature"));
25:   parameter Machines.Thermal.LinearTemperatureCoefficient20 alpha20a=0
26:     "Temperature coefficient of armature resistance"
27:     annotation (Dialog(tab="Armature"));
28:   parameter SI.Inductance La=0.0015 "Armature inductance"
29:     annotation (Dialog(tab="Armature"));
30:   parameter Machines.Losses.FrictionParameters frictionParameters(PRef=0, wRef=
```


## Execution evidence

[Rumoca commands, return codes, integrity hashes, bounded output and metadata](../evidence/f00103fd4bc29b1a.json). Baseline: **tool-error**.

No independent runtime override was executed for this target in this audit; this is not a pass.

## Recommended action

Correct the detector/adjudicator for this specific semantic case; do not impose a blanket strictly-positive bound on the library declaration.

## Scope and limitations

A source-level verdict addresses the reported declaration/claim, not every possible connected system. Tests cover 0–0.5 seconds and are not a proof of long-run stability. Shared instances are not distinct root causes. A missing bound, timeout, compiler error or failed nominal run alone never counts as a verified bug or a false positive. Fixes are proposals; no library/compiler implementation was changed.

[Group and related reports](../groups/ideal-dc-machine-data.md) · [Index](../README.md)
