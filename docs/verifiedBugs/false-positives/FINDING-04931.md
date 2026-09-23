# FINDING-04931: Bridge parameters explicitly allow the ideal thyristor limit

| Field | Value |
|---|---|
| Verdict | false-positives |
| Scope / group | ideal-thyristor-bridge-zero |
| Model | ModelicaTest.Electrical.PowerConverters.ThyristorBridge2mPulse_R |
| Target | rectifier.RonThyristor |
| Student classification | physical-bound-permits-zero |
| Original report | [FINDING-thyristorbridge2mpulse-r-rectifier-ronthyristor-ruleoff-2.md](../../v2/bugs/FINDING-thyristorbridge2mpulse-r-rectifier-ronthyristor-ruleoff-2.md) — reviewed as `FINDING-04931-thyristorbridge2mpulse-r-rectifier-ronthyristor.md`, which a later run renamed |
| Original SHA-256 | 613c7d58372b3ac8a36f73a0f2dcde2a374aa4803f86ed5ae5264021a1347209 |

## Why this is a false positive

RonThyristor and GoffThyristor have final min=0 and are forwarded to polyphase IdealThyristor, ultimately using IdealSemiconductor multiplicative switching equations. Zero is an intended ideal limit; a specific bridge/network may still require nonzero regularization for numerical structure.

## Source evidence

Compiler/source-resolved declaration: `Electrical/PowerConverters/ACDC/ThyristorBridge2mPulse.mo:6`. Role: `parameter`; binding: `1e-05`; effective min: `0`; effective max: `None`. 

[Electrical/PowerConverters/ACDC/ThyristorBridge2mPulse.mo — source snapshot](../evidence/sources/e11f8c98bff05b32-ThyristorBridge2mPulse.mo)

```modelica
4:   import Modelica.Constants.pi;
5:   // parameter Integer m(final min=3) = 3 "Number of phases" annotation(Evaluate=true);
6:   parameter SI.Resistance RonThyristor(final min=0) = 1e-05
7:     "Closed thyristor resistance";
8:   parameter SI.Conductance GoffThyristor(final min=0) = 1e-05
9:     "Opened thyristor conductance";
```

[Electrical/PowerConverters/ACDC/ThyristorBridge2mPulse.mo — source snapshot](../evidence/sources/e11f8c98bff05b32-ThyristorBridge2mPulse.mo)

```modelica
2: model ThyristorBridge2mPulse "2*m pulse thyristor rectifier bridge"
3:   extends Icons.Converter;
4:   import Modelica.Constants.pi;
5:   // parameter Integer m(final min=3) = 3 "Number of phases" annotation(Evaluate=true);
6:   parameter SI.Resistance RonThyristor(final min=0) = 1e-05
7:     "Closed thyristor resistance";
8:   parameter SI.Conductance GoffThyristor(final min=0) = 1e-05
9:     "Opened thyristor conductance";
10:   parameter SI.Voltage VkneeThyristor(final min=0) = 0
11:     "Thyristor forward threshold voltage";
12:   parameter Boolean offStart_p[m]=fill(true, m)
13:     "Boolean start value of variable thyristor_p[:].off"
14:     annotation (choices(checkBox=true));
15:   parameter Boolean offStart_n[m]=fill(true, m)
16:     "Boolean start value of variable thyristor_n[:].off"
17:     annotation (choices(checkBox=true));
18:   extends PowerConverters.Interfaces.ACDC.ACplug;
19:   extends PowerConverters.Interfaces.ACDC.DCtwoPin;
20:   extends Modelica.Electrical.Analog.Interfaces.ConditionalHeatPort(final T=293.15);
21:   extends Interfaces.Enable.Enable2m;
22:   Modelica.Electrical.Polyphase.Ideal.IdealThyristor thyristor_p(
23:     final m=m,
24:     final Ron=fill(RonThyristor, m),
25:     final Goff=fill(GoffThyristor, m),
26:     final Vknee=fill(VkneeThyristor, m),
27:     final useHeatPort=useHeatPort,
28:     final idealThyristor(off(start=offStart_p, fixed=fill(true, m))))
29:     "Thyristors connected to positive DC potential" annotation (Placement(
30:         transformation(
31:         origin={0,40},
32:         extent={{-10,-10},{10,10}},
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

[Rumoca commands, return codes, integrity hashes, bounded output and metadata](../evidence/3e4bc4f4aebf899e.json). Baseline: **tool-error**.

No independent runtime override was executed for this target in this audit; this is not a pass.

## Recommended action

Correct the detector/adjudicator for this specific semantic case; do not impose a blanket strictly-positive bound on the library declaration.

## Scope and limitations

A source-level verdict addresses the reported declaration/claim, not every possible connected system. Tests cover 0–0.5 seconds and are not a proof of long-run stability. Shared instances are not distinct root causes. A missing bound, timeout, compiler error or failed nominal run alone never counts as a verified bug or a false positive. Fixes are proposals; no library/compiler implementation was changed.

[Group and related reports](../groups/ideal-thyristor-bridge-zero.md) · [Index](../README.md)
