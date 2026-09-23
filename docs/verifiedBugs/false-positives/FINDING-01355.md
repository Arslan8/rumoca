# FINDING-01355: Zero armature inductance is an ideal algebraic limit

| Field | Value |
|---|---|
| Verdict | false-positives |
| Scope / group | ideal-dc-armature-la |
| Model | Modelica.Electrical.Machines.Examples.DCMachines.DCPM_QuasiStatic |
| Target | dcpm1.La |
| Student classification | physical-domain-unenforced |
| Original report | [FINDING-dcpm-quasistatic-dcpm1-la-zerolimit.md](../../v2/bugs/FINDING-dcpm-quasistatic-dcpm1-la-zerolimit.md) — reviewed as `FINDING-01355-dcpm-quasistatic-dcpm1-la.md`, which a later run renamed |
| Original SHA-256 | bdcdd2da571961f955cd5028e8564ecd86eaeb3d497022614a316380e6fe71b1 |

## Why this is a false positive

La is passed to InductorDC, whose equation is v=L*der(i) outside quasi-static mode; zero removes the inductive voltage drop. The partial machine source has no unconditional reciprocal of this parameter. A particular initialization can still be topology-dependent.

## Source evidence

Compiler/source-resolved declaration: `Electrical/Machines/Interfaces/PartialBasicDCMachine.mo:26`. Role: `parameter`; binding: `dcpmData.La`; effective min: `None`; effective max: `None`. 

[Electrical/Machines/Interfaces/PartialBasicDCMachine.mo — source snapshot](../evidence/sources/4db8b5f43a5834a2-PartialBasicDCMachine.mo)

```modelica
24:     "Temperature coefficient of armature resistance"
25:     annotation (Dialog(tab="Armature"));
26:   parameter SI.Inductance La(start=0.0015)
27:     "Armature inductance"
28:     annotation (Dialog(tab="Armature"));
29:   extends PartialBasicMachine(
```

[Electrical/Machines/Interfaces/PartialBasicDCMachine.mo — source snapshot](../evidence/sources/4db8b5f43a5834a2-PartialBasicDCMachine.mo)

```modelica
22:     annotation (Dialog(tab="Armature"));
23:   parameter Machines.Thermal.LinearTemperatureCoefficient20 alpha20a(start=0)
24:     "Temperature coefficient of armature resistance"
25:     annotation (Dialog(tab="Armature"));
26:   parameter SI.Inductance La(start=0.0015)
27:     "Armature inductance"
28:     annotation (Dialog(tab="Armature"));
29:   extends PartialBasicMachine(
30:     Jr(start=0.15),
```

[Electrical/Machines/BasicMachines/Components/InductorDC.mo — source snapshot](../evidence/sources/72ab8f755e24ff0e-InductorDC.mo)

```modelica
2: model InductorDC
3:   "Ideal linear electrical inductor for electrical DC machines"
4:   extends Modelica.Electrical.Analog.Interfaces.OnePort;
5:   parameter SI.Inductance L(start=1) "Inductance";
6:   parameter Boolean quasiStatic(start=false)
7:     "No electrical transients if true" annotation (Evaluate=true);
8: equation
9:   v = if quasiStatic then 0 else L*der(i);
10:   annotation (defaultComponentName="inductor",
11:     Documentation(info="<html>
12: <p>The linear inductor connects the branch voltage <em>v</em> with the branch current <em>i</em> by <em>v = L * di/dt</em>.
13: If <code>quasiStatic == false</code>, the electrical transients are neglected, i.e., the voltage drop is zero.</p>
14: </html>"),
15:     Icon(coordinateSystem(preserveAspectRatio=true, extent={{-100,-100},{
16:             100,100}}), graphics={Ellipse(extent={{-60,-15},{-30,15}},
17:           lineColor={0,0,255}),Ellipse(extent={{-30,-15},{0,15}},
18:           lineColor={0,0,255}),Ellipse(extent={{0,-15},{30,15}},
19:           lineColor={0,0,255}),Ellipse(extent={{30,-15},{60,15}},
20:           lineColor={0,0,255}),Rectangle(
21:                 extent={{-60,-30},{60,0}},
22:                 lineColor={255,255,255},
```


## Execution evidence

[Rumoca commands, return codes, integrity hashes, bounded output and metadata](../evidence/aea5ee8f9a92fcb1.json). Baseline: **tool-error**.

No independent runtime override was executed for this target in this audit; this is not a pass.

## Recommended action

Correct the detector/adjudicator for this specific semantic case; do not impose a blanket strictly-positive bound on the library declaration.

## Scope and limitations

A source-level verdict addresses the reported declaration/claim, not every possible connected system. Tests cover 0–0.5 seconds and are not a proof of long-run stability. Shared instances are not distinct root causes. A missing bound, timeout, compiler error or failed nominal run alone never counts as a verified bug or a false positive. Fixes are proposals; no library/compiler implementation was changed.

[Group and related reports](../groups/ideal-dc-armature-la.md) · [Index](../README.md)
