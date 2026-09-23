# FINDING-03622: Converter switch parameters delegate to ideal semiconductor limits

| Field | Value |
|---|---|
| Verdict | false-positives |
| Scope / group | ideal-converter-switch-zero |
| Model | Modelica.Electrical.PowerConverters.Examples.DCDC.HBridge.HBridge_RL |
| Target | hbridge.inverter_p.RonTransistor |
| Student classification | physical-domain-unenforced |
| Original report | [FINDING-hbridge-rl-hbridge-inverter-p-rontransistor-ruleoff.md](../../v2/bugs/FINDING-hbridge-rl-hbridge-inverter-p-rontransistor-ruleoff.md) — reviewed as `FINDING-03622-hbridge-rl-hbridge-inverter-p-rontransistor.md`, which a later run renamed |
| Original SHA-256 | a640ea64cf4e7b5a8405ac292e487a3e5ff03e1063353ffc4af09b1d3be921cd |

## Why this is a false positive

These values are forwarded to IdealGTOThyristor/IdealDiode, whose IdealSemiconductor equations multiply by Ron or Goff rather than divide. Zero is the exact closed/open ideal limit. Some bridge topologies can become structurally singular, but that requires circuit-specific evidence and does not justify a blanket source-parameter positivity claim.

## Source evidence

Compiler/source-resolved declaration: `Electrical/PowerConverters/DCAC/SinglePhase2Level.mo:4`. Role: `parameter`; binding: `hbridge.RonTransistor`; effective min: `None`; effective max: `None`. 

[Electrical/PowerConverters/DCAC/SinglePhase2Level.mo — source snapshot](../evidence/sources/edbbac7772341692-SinglePhase2Level.mo)

```modelica
2: model SinglePhase2Level "Single-phase DC to AC converter"
3:   extends Modelica.Blocks.Icons.Block;
4:   parameter SI.Resistance RonTransistor=1e-05
5:     "Transistor closed resistance";
6:   parameter SI.Conductance GoffTransistor=1e-05
7:     "Transistor opened conductance";
```

[Electrical/PowerConverters/DCAC/SinglePhase2Level.mo — source snapshot](../evidence/sources/edbbac7772341692-SinglePhase2Level.mo)

```modelica
2: model SinglePhase2Level "Single-phase DC to AC converter"
3:   extends Modelica.Blocks.Icons.Block;
4:   parameter SI.Resistance RonTransistor=1e-05
5:     "Transistor closed resistance";
6:   parameter SI.Conductance GoffTransistor=1e-05
7:     "Transistor opened conductance";
8:   parameter SI.Voltage VkneeTransistor=0
9:     "Transistor threshold voltage";
10:   parameter SI.Resistance RonDiode=1e-05
11:     "Diode closed resistance";
12:   parameter SI.Conductance GoffDiode=1e-05
13:     "Diode opened conductance";
14:   parameter SI.Voltage VkneeDiode=0 "Diode threshold voltage";
15:   // parameter Boolean useEnable "Enables enable signal connector";
16:   extends PowerConverters.Interfaces.DCAC.DCtwoPin;
17:   extends PowerConverters.Interfaces.DCAC.ACpin;
18:   extends Modelica.Electrical.Analog.Interfaces.ConditionalHeatPort(final T=
19:        293.15);
20:   extends Interfaces.Enable.Enable2;
21:   Modelica.Electrical.Analog.Ideal.IdealGTOThyristor transistor_p(
22:     final Ron=RonTransistor,
23:     final Goff=GoffTransistor,
24:     final Vknee=VkneeTransistor,
25:     final useHeatPort=useHeatPort) annotation (Placement(transformation(
26:         extent={{-10,10},{10,-10}},
27:         rotation=270,
28:         origin={30,20})));
29:   Modelica.Electrical.Analog.Ideal.IdealDiode diode_p(
30:     final Ron=RonDiode,
31:     final Goff=GoffDiode,
32:     final Vknee=VkneeDiode,
33:     final useHeatPort=useHeatPort) annotation (Placement(transformation(
34:         extent={{-10,-10},{10,10}},
35:         rotation=90,
36:         origin={70,20})));
37:   Modelica.Electrical.Analog.Ideal.IdealGTOThyristor transistor_n(
38:     final Ron=RonTransistor,
39:     final Goff=GoffTransistor,
40:     final Vknee=VkneeTransistor,
41:     final useHeatPort=useHeatPort) annotation (Placement(transformation(
42:         extent={{-10,10},{10,-10}},
```

[Electrical/Analog/Interfaces/IdealSemiconductor.mo — source snapshot](../evidence/sources/267299b461382849-IdealSemiconductor.mo)

```modelica
1: within Modelica.Electrical.Analog.Interfaces;
2: partial model IdealSemiconductor "Ideal semiconductor"
3:   extends Modelica.Electrical.Analog.Interfaces.OnePort;
4:   parameter SI.Resistance Ron(final min=0) = 1e-5
5:     "Forward state-on differential resistance (closed resistance)";
6:   parameter SI.Conductance Goff(final min=0) = 1e-5
7:     "Backward state-off conductance (opened conductance)";
8:   parameter SI.Voltage Vknee(final min=0) = 0
9:     "Forward threshold voltage";
10:   extends Modelica.Electrical.Analog.Interfaces.ConditionalHeatPort;
11:   Boolean off(start=true) "Switching state";
12: protected
13:   Real s(start=0, final unit="1")
14:     "Auxiliary variable for actual position on the ideal diode characteristic";
15:   /* s = 0: knee point
16:      s < 0: below knee point, blocking
17:      s > 0: above knee point, conducting */
18:   constant SI.Voltage unitVoltage=1 annotation (HideResult=true);
19:   constant SI.Current unitCurrent=1 annotation (HideResult=true);
20: equation
21:   v = (s*unitCurrent)*(if off then 1 else Ron) + Vknee;
22:   i = (s*unitVoltage)*(if off then Goff else 1) + Goff*Vknee;
23:   LossPower = v*i;
24:   annotation (
25:     Documentation(info="<html>
26: <p>
27: This is an ideal semiconductor which is<br><br>
28: <strong>open </strong>(off), if it is reversed biased (voltage drop less than 0)<br>
29: <strong>closed</strong> (on), if it is conducting (current > 0).<br>
30: <br>
31: This is the behaviour if all parameters are exactly zero.<br><br>
32: Note, there are circuits, where this ideal description
33: with zero resistance and zero conductance is not possible.
34: In order to prevent singularities during switching, the opened
35: semiconductor has a small conductance <em>Gon</em>
36: and the closed semiconductor has a low resistance <em>Roff</em> which is default.
37: </p>
38: <p>
39: The parameter <em>Vknee</em> which is the forward threshold voltage, allows to displace
40: the knee point<br> along  the <em>Gon</em>-characteristic until <em>v = Vknee</em>.
41: <br><br>
42: <strong>Please note:</strong>
43: In case of useHeatPort=true the temperature dependence of the electrical
44: behavior is <strong>not</strong> modelled.
45: </p>
46: </html>",
47:         revisions="<html>
48: <ul>
```


## Execution evidence

[Rumoca commands, return codes, integrity hashes, bounded output and metadata](../evidence/ab2cc6b174d1b7a8.json). Baseline: **tool-error**.

No independent runtime override was executed for this target in this audit; this is not a pass.

## Recommended action

Correct the detector/adjudicator for this specific semantic case; do not impose a blanket strictly-positive bound on the library declaration.

## Scope and limitations

A source-level verdict addresses the reported declaration/claim, not every possible connected system. Tests cover 0–0.5 seconds and are not a proof of long-run stability. Shared instances are not distinct root causes. A missing bound, timeout, compiler error or failed nominal run alone never counts as a verified bug or a false positive. Fixes are proposals; no library/compiler implementation was changed.

[Group and related reports](../groups/ideal-converter-switch-zero.md) · [Index](../README.md)
