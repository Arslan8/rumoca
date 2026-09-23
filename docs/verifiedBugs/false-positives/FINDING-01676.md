# FINDING-01676: Zero on-resistance/off-conductance is an intended ideal limit

| Field | Value |
|---|---|
| Verdict | false-positives |
| Scope / group | ideal-zero |
| Model | Modelica.Electrical.Machines.Examples.InductionMachines.IMC_InverterDrive |
| Target | rectifier.diode_n.idealDiode[2].Ron |
| Student classification | physical-bound-permits-zero |
| Original report | [FINDING-imc-inverterdrive-rectifier-diode-n-idealdiode-2-ron-ruleoff.md](../../v2/bugs/FINDING-imc-inverterdrive-rectifier-diode-n-idealdiode-2-ron-ruleoff.md) — reviewed as `FINDING-01676-imc-inverterdrive-rectifier-diode-n-idealdiode-2-ron.md`, which a later run renamed |
| Original SHA-256 | 5eb98856c1667331c1cc3a4cad92187eed411862133ff2a404ea9bc161d1bc8e |

## Why this is a false positive

The scalar ideal component explicitly permits Ron=0 and Goff=0 and uses switching equations that do not unconditionally divide by either. Polyphase declarations use vector nonnegative bounds and delegate to those scalar components. The documentation warns that some connected circuits are singular: that is not evidence that every component must have strictly positive values. The reported blanket positivity/missing-bound claim is false.

## Source evidence

Compiler/source-resolved declaration: `Electrical/Analog/Interfaces/IdealSemiconductor.mo:4`. Role: `parameter`; binding: `rectifier.diode_n.Ron[2]`; effective min: `0`; effective max: `None`. 

[Electrical/Analog/Interfaces/IdealSemiconductor.mo — source snapshot](../evidence/sources/267299b461382849-IdealSemiconductor.mo)

```modelica
2: partial model IdealSemiconductor "Ideal semiconductor"
3:   extends Modelica.Electrical.Analog.Interfaces.OnePort;
4:   parameter SI.Resistance Ron(final min=0) = 1e-5
5:     "Forward state-on differential resistance (closed resistance)";
6:   parameter SI.Conductance Goff(final min=0) = 1e-5
7:     "Backward state-off conductance (opened conductance)";
```

[Electrical/Analog/Interfaces/IdealSwitch.mo — source snapshot](../evidence/sources/ddf9c35a45d16f3d-IdealSwitch.mo)

```modelica
14: equation
15:   v = (s*unitCurrent)*(if off then 1 else Ron);
16:   i = (s*unitVoltage)*(if off then Goff else 1);
17:   LossPower = v*i;
18:   annotation (
19:     Documentation(info="<html>
20: <p>
21: The ideal switch has a positive pin p and a negative pin n.
22: The switching behaviour is controlled by the boolean signal off.
23: If off is true, pin p is not connected with negative pin n.
24: Otherwise, pin p is connected with negative pin n.<br><br>
25: In order to prevent singularities during switching, the opened
26: switch has a (very low) conductance Goff
27: and the closed switch has a (very low) resistance Ron.
28: The limiting case is also allowed, i.e., the resistance Ron of the
29: closed switch could be exactly zero and the conductance Goff of the
30: open switch could be also exactly zero. Note, there are circuits,
31: where a description with zero Ron or zero Goff is not possible.
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

[Rumoca commands, return codes, integrity hashes, bounded output and metadata](../evidence/f1b3b20d1746a2aa.json). Baseline: **tool-error**.

No independent runtime override was executed for this target in this audit; this is not a pass.

## Recommended action

Correct the detector/adjudicator for this specific semantic case; do not impose a blanket strictly-positive bound on the library declaration.

## Scope and limitations

A source-level verdict addresses the reported declaration/claim, not every possible connected system. Tests cover 0–0.5 seconds and are not a proof of long-run stability. Shared instances are not distinct root causes. A missing bound, timeout, compiler error or failed nominal run alone never counts as a verified bug or a false positive. Fixes are proposals; no library/compiler implementation was changed.

[Group and related reports](../groups/ideal-zero.md) · [Index](../README.md)
