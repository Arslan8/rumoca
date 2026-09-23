# FINDING-01479: Zero armature resistance is an ideal algebraic limit

| Field | Value |
|---|---|
| Verdict | false-positives |
| Scope / group | ideal-dc-armature-ra |
| Model | Modelica.Electrical.Machines.Examples.DCMachines.DCSE_SinglePhase |
| Target | dcse.Ra |
| Student classification | physical-domain-unenforced |
| Original report | [FINDING-dcse-singlephase-dcse-ra-unbounded.md](../../v2/bugs/FINDING-dcse-singlephase-dcse-ra-unbounded.md) — reviewed as `FINDING-01479-dcse-singlephase-dcse-ra.md`, which a later run renamed |
| Original SHA-256 | b0eeeba2306def414105f48876445ee54a8274ceb9991083d901b3db1567f528 |

## Why this is a false positive

Ra is passed to Basic.Resistor, whose contract explicitly supports zero and signed resistance; zero removes armature copper loss. The partial machine source has no unconditional reciprocal of this parameter. A particular initialization can still be topology-dependent.

## Source evidence

Compiler/source-resolved declaration: `Electrical/Machines/Interfaces/PartialBasicDCMachine.mo:17`. Role: `parameter`; binding: `dcseData.Ra`; effective min: `None`; effective max: `None`. 

[Electrical/Machines/Interfaces/PartialBasicDCMachine.mo — source snapshot](../evidence/sources/4db8b5f43a5834a2-PartialBasicDCMachine.mo)

```modelica
15:     "Nominal armature temperature"
16:     annotation (Dialog(tab="Nominal parameters"));
17:   parameter SI.Resistance Ra(start=0.05)
18:     "Armature resistance at TaRef"
19:     annotation (Dialog(tab="Armature"));
20:   parameter SI.Temperature TaRef(start=293.15)
```

[Electrical/Machines/Interfaces/PartialBasicDCMachine.mo — source snapshot](../evidence/sources/4db8b5f43a5834a2-PartialBasicDCMachine.mo)

```modelica
13:     annotation (Dialog(tab="Nominal parameters"));
14:   parameter SI.Temperature TaNominal(start=293.15)
15:     "Nominal armature temperature"
16:     annotation (Dialog(tab="Nominal parameters"));
17:   parameter SI.Resistance Ra(start=0.05)
18:     "Armature resistance at TaRef"
19:     annotation (Dialog(tab="Armature"));
20:   parameter SI.Temperature TaRef(start=293.15)
21:     "Reference temperature of armature resistance"
22:     annotation (Dialog(tab="Armature"));
23:   parameter Machines.Thermal.LinearTemperatureCoefficient20 alpha20a(start=0)
24:     "Temperature coefficient of armature resistance"
25:     annotation (Dialog(tab="Armature"));
26:   parameter SI.Inductance La(start=0.0015)
```

[Electrical/Analog/Basic/Resistor.mo — source snapshot](../evidence/sources/f3257fcb99588782-Resistor.mo)

```modelica
2: model Resistor "Ideal linear electrical resistor"
3:   parameter SI.Resistance R(start=1)
4:     "Resistance at temperature T_ref";
5:   parameter SI.Temperature T_ref=300.15 "Reference temperature";
6:   parameter SI.LinearTemperatureCoefficient alpha=0
7:     "Temperature coefficient of resistance (R_actual = R*(1 + alpha*(T_heatPort - T_ref))";
8: 
9:   extends Modelica.Electrical.Analog.Interfaces.OnePort;
10:   extends Modelica.Electrical.Analog.Interfaces.ConditionalHeatPort(T=T_ref);
11:   SI.Resistance R_actual
12:     "Actual resistance = R*(1 + alpha*(T_heatPort - T_ref))";
13: 
14: equation
15:   assert((1 + alpha*(T_heatPort - T_ref)) >= Modelica.Constants.eps,
16:     "Temperature outside scope of model!");
17:   R_actual = R*(1 + alpha*(T_heatPort - T_ref));
18:   v = R_actual*i;
19:   LossPower = v*i;
20:   annotation (
21:     Documentation(info="<html>
22: <p>The linear resistor connects the branch voltage <em>v</em> with the branch current <em>i</em> by <em>i*R = v</em>. The Resistance <em>R</em> is allowed to be positive, zero, or negative.</p>
```


## Execution evidence

[Rumoca commands, return codes, integrity hashes, bounded output and metadata](../evidence/f00103fd4bc29b1a.json). Baseline: **tool-error**.

No independent runtime override was executed for this target in this audit; this is not a pass.

## Recommended action

Correct the detector/adjudicator for this specific semantic case; do not impose a blanket strictly-positive bound on the library declaration.

## Scope and limitations

A source-level verdict addresses the reported declaration/claim, not every possible connected system. Tests cover 0–0.5 seconds and are not a proof of long-run stability. Shared instances are not distinct root causes. A missing bound, timeout, compiler error or failed nominal run alone never counts as a verified bug or a false positive. Fixes are proposals; no library/compiler implementation was changed.

[Group and related reports](../groups/ideal-dc-armature-ra.md) · [Index](../README.md)
