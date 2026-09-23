# FINDING-00782: Example waveform timing divides by zero frequency

| Field | Value |
|---|---|
| Verdict | confirmed |
| Scope / group | trapezoid-frequency |
| Model | Modelica.Electrical.Analog.Examples.OpAmps.Comparator |
| Target | f |
| Student classification | divisor-reachable-zero |
| Original report | [FINDING-comparator-f-divzero-2.md](../../v2/bugs/FINDING-comparator-f-divzero-2.md) — reviewed as `FINDING-00782-comparator-f.md`, which a later run renamed |
| Original SHA-256 | dbbdc8a4aa7995fc8ac0691b207f62a3ba233724657705abe44bf36865432988 |

## Verification and root cause

The source uses f directly in trapezoid timing (rising=0.2/f, width=0.3/f, falling=0.2/f, period=1/f). f=0 is not handled and gives undefined parameter bindings. Rumoca reports non-finite evaluation after a clean baseline. OpenModelica baseline-executable overrides also report zero division; recompilation can instead hit a template/code-generation error, which is not counted as independent runtime confirmation.

## Source evidence

Compiler/source-resolved declaration: `Electrical/Analog/Examples/OpAmps/Comparator.mo:7`. Role: `parameter`; binding: `10`; effective min: `None`; effective max: `None`. 

[Electrical/Analog/Examples/OpAmps/Comparator.mo — source snapshot](../evidence/sources/c3b4a9d44d7708f1-Comparator.mo)

```modelica
5:   parameter SI.Voltage Vns=-15 "Negative supply";
6:   parameter SI.Voltage Vin=5 "Amplitude of input voltage";
7:   parameter SI.Frequency f=10 "Frequency of input voltage";
8:   parameter SI.Voltage Vref=0 "Reference voltage";
9:   parameter Real k=(Vref - Vns)/(Vps - Vns) "Calculated potentiometer ratio to reach Vref";
10:   parameter SI.Resistance R=1000 "Resistance of potentiometer";
```

[Electrical/Analog/Examples/OpAmps/Comparator.mo — source snapshot](../evidence/sources/c3b4a9d44d7708f1-Comparator.mo)

```modelica
1: within Modelica.Electrical.Analog.Examples.OpAmps;
2: model Comparator "Comparator"
3:   extends Modelica.Icons.Example;
4:   parameter SI.Voltage Vps=+15 "Positive supply";
5:   parameter SI.Voltage Vns=-15 "Negative supply";
6:   parameter SI.Voltage Vin=5 "Amplitude of input voltage";
7:   parameter SI.Frequency f=10 "Frequency of input voltage";
8:   parameter SI.Voltage Vref=0 "Reference voltage";
9:   parameter Real k=(Vref - Vns)/(Vps - Vns) "Calculated potentiometer ratio to reach Vref";
10:   parameter SI.Resistance R=1000 "Resistance of potentiometer";
11:   Modelica.Electrical.Analog.Ideal.IdealizedOpAmpLimited opAmp(Vps=Vps, Vns=
12:         Vns) annotation (Placement(transformation(extent={{0,10},{20,-10}})));
13:   Modelica.Electrical.Analog.Basic.Ground ground
14:     annotation (Placement(transformation(extent={{-20,-100},{0,-80}})));
15:   Modelica.Electrical.Analog.Sources.TrapezoidVoltage vIn(
16:     rising=0.2/f,
17:     width=0.3/f,
18:     falling=0.2/f,
19:     period=1/f,
20:     nperiod=-1,
21:     startTime=-(vIn.rising + vIn.width/2),
22:     V=2*Vin,
23:     offset=-Vin) annotation (Placement(transformation(
24:         extent={{-10,-10},{10,10}},
25:         rotation=270,
26:         origin={-80,0})));
27:   Modelica.Electrical.Analog.Sensors.VoltageSensor vOut annotation (Placement(
28:         transformation(
29:         extent={{-10,10},{10,-10}},
30:         rotation=270,
31:         origin={50,-20})));
32:   Modelica.Electrical.Analog.Basic.Potentiometer potentiometer(R=R, rConstant=
33:        k) annotation (Placement(transformation(
34:         extent={{-10,10},{10,-10}},
35:         origin={-10,-30})));
36:   Modelica.Electrical.Analog.Sources.SupplyVoltage supplyVoltage(Vps=Vps, Vns=
37:        Vns) annotation (Placement(transformation(
38:         extent={{-10,-10},{10,10}},
39:         origin={-10,-50})));
40: equation
41:   connect(vIn.p, opAmp.in_p) annotation (Line(
42:       points={{-80,10},{-10,10},{-10,6},{0,6}}, color={0,0,255}));
43:   connect(opAmp.out, vOut.p) annotation (Line(
44:       points={{20,0},{50,0},{50,-10}}, color={0,0,255}));
45:   connect(ground.p, vOut.n) annotation (Line(
```


## Execution evidence

[Rumoca commands, return codes, integrity hashes, bounded output and metadata](../evidence/7def794e383a0da2.json). Baseline: **clean**.

| Probe | Outcome |
|---|---|
| `f=0` | reported-failure |

Diagnostic: numeric evaluation produced a non-finite result

[Independent OpenModelica wrappers and complete output](../evidence/omc-extra-7def794e383a0da2.json). Baseline: simulation succeeded.

- `f=0` set before translation: "Error: Template error: A template call failed (/usr/bin/../lib/x86_64-linux-gnu/omc/libOpenModelicaCompiler.so: (null)). One possible reason could be that a template imported function call failed (which should not happen for functions called from within template code; templates assert pure 'match'/non-failing semantics)..
- Same value declared final, with final-parameter evaluation: "Error: Template error: A template call failed (/usr/bin/../lib/x86_64-linux-gnu/omc/libOpenModelicaCompiler.so: (null)). One possible reason could be that a template imported function call failed (which should not happen for functions called from within template code; templates assert pure 'match'/non-failing semantics)..

## Proposed fix

At the example frequency declaration, specify and assert f>0 and guard the timing calculations so the assertion can diagnose invalid input. If f=0 should mean DC, provide an explicit DC branch; do not silently clamp frequency to epsilon.

## Fix validation

Add a nominal regression and the exact boundary witness below. Require a clear domain diagnostic (or a documented finite limiting model), never NaN/Inf or an unrelated solver error. Re-run both engines.

## Scope and limitations

A source-level verdict addresses the reported declaration/claim, not every possible connected system. Tests cover 0–0.5 seconds and are not a proof of long-run stability. Shared instances are not distinct root causes. A missing bound, timeout, compiler error or failed nominal run alone never counts as a verified bug or a false positive. Fixes are proposals; no library/compiler implementation was changed.

[Group and related reports](../groups/trapezoid-frequency.md) · [Index](../README.md)
