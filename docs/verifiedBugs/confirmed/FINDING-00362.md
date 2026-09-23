# FINDING-00362: Example waveform timing divides by zero frequency

| Field | Value |
|---|---|
| Verdict | confirmed |
| Scope / group | trapezoid-frequency |
| Model | Modelica.Electrical.Analog.Examples.InvertingAmp |
| Target | f |
| Student classification | divisor-reachable-zero |
| Original report | [BUG-invertingamp-f.md](../../v2/bugs/BUG-invertingamp-f.md) — reviewed as `FINDING-00362-invertingamp-f.md`, which a later run renamed |
| Original SHA-256 | 03763b1ae20b186ff821e127a10ca2d8689ce9635495b0b0a17274afe872a3e1 |

## Verification and root cause

The source uses f directly in trapezoid timing (rising=0.2/f, width=0.3/f, falling=0.2/f, period=1/f). f=0 is not handled and gives undefined parameter bindings. Rumoca reports non-finite evaluation after a clean baseline. OpenModelica baseline-executable overrides also report zero division; recompilation can instead hit a template/code-generation error, which is not counted as independent runtime confirmation.

## Source evidence

Compiler/source-resolved declaration: `Electrical/Analog/Examples/InvertingAmp.mo:7`. Role: `parameter`; binding: `10`; effective min: `None`; effective max: `None`. 

[Electrical/Analog/Examples/InvertingAmp.mo — source snapshot](../evidence/sources/0a7701dc2c4c8d4f-InvertingAmp.mo)

```modelica
5:   parameter SI.Voltage Vns=-15 "Negative supply";
6:   parameter SI.Voltage Vin=5 "Amplitude of input voltage";
7:   parameter SI.Frequency f=10 "Frequency of input voltage";
8:   parameter Real k=2 "Desired amplification";
9:   parameter SI.Resistance R1=1000 "Arbitrary resistance";
10:   parameter SI.Resistance R2=k*R1 "Calculated resistance to reach desired amplification k";
```

[Electrical/Analog/Examples/InvertingAmp.mo — source snapshot](../evidence/sources/0a7701dc2c4c8d4f-InvertingAmp.mo)

```modelica
1: within Modelica.Electrical.Analog.Examples;
2: model InvertingAmp "Inverting amplifier"
3:   extends Modelica.Icons.Example;
4:   parameter SI.Voltage Vps=+15 "Positive supply";
5:   parameter SI.Voltage Vns=-15 "Negative supply";
6:   parameter SI.Voltage Vin=5 "Amplitude of input voltage";
7:   parameter SI.Frequency f=10 "Frequency of input voltage";
8:   parameter Real k=2 "Desired amplification";
9:   parameter SI.Resistance R1=1000 "Arbitrary resistance";
10:   parameter SI.Resistance R2=k*R1 "Calculated resistance to reach desired amplification k";
11:   Modelica.Electrical.Analog.Ideal.IdealOpAmpLimited opAmp(
12:     out(i(start=0, fixed=false)))
13:     annotation (Placement(transformation(extent={{0,-10},{20,10}})));
14:   Modelica.Electrical.Analog.Basic.Ground ground
15:     annotation (Placement(transformation(extent={{-20,-80},{0,-60}})));
16:   Modelica.Electrical.Analog.Sources.TrapezoidVoltage vIn(
17:     V=2*Vin,
18:     rising=0.2/f,
19:     width=0.3/f,
20:     falling=0.2/f,
21:     period=1/f,
22:     nperiod=-1,
23:     offset=-Vin,
24:     startTime=-(vIn.rising + vIn.width/2)) annotation (Placement(
25:         transformation(
26:         extent={{-10,-10},{10,10}},
27:         rotation=270,
28:         origin={-80,0})));
29:   Modelica.Electrical.Analog.Sensors.VoltageSensor vOut annotation (Placement(
30:         transformation(
31:         extent={{-10,10},{10,-10}},
32:         rotation=270,
33:         origin={50,-20})));
34:   Modelica.Electrical.Analog.Basic.Resistor r1(R=R1)
35:     annotation (Placement(transformation(extent={{-40,50},{-20,70}})));
36:   Modelica.Electrical.Analog.Basic.Resistor r2(R=R2)
37:     annotation (Placement(transformation(extent={{20,50},{0,70}})));
38:   Modelica.Electrical.Analog.Basic.Ground ground1
39:     annotation (Placement(transformation(extent={{-10,-10},{10,10}},
40:         rotation=270,
41:         origin={-60,0})));
42:   Modelica.Electrical.Analog.Sources.ConstantVoltage vSourcePos(V=Vps) annotation (Placement(
43:         transformation(
44:         extent={{-10,-10},{10,10}},
45:         rotation=270,
```


## Execution evidence

[Rumoca commands, return codes, integrity hashes, bounded output and metadata](../evidence/87d4e09ed047dc9f.json). Baseline: **clean**.

| Probe | Outcome |
|---|---|
| `f=0` | reported-failure |

Diagnostic: numeric evaluation produced a non-finite result

[Independent OpenModelica wrappers and complete output](../evidence/omc-87d4e09ed047dc9f.json). Baseline: simulation succeeded.

- `f=0` set before translation: "Error: Template error: A template call failed (/usr/bin/../lib/x86_64-linux-gnu/omc/libOpenModelicaCompiler.so: (null)). One possible reason could be that a template imported function call failed (which should not happen for functions called from within template code; templates assert pure 'match'/non-failing semantics)..
- Same value declared final, with final-parameter evaluation: "Error: Template error: A template call failed (/usr/bin/../lib/x86_64-linux-gnu/omc/libOpenModelicaCompiler.so: (null)). One possible reason could be that a template imported function call failed (which should not happen for functions called from within template code; templates assert pure 'match'/non-failing semantics)..

## Proposed fix

At the example frequency declaration, specify and assert f>0 and guard the timing calculations so the assertion can diagnose invalid input. If f=0 should mean DC, provide an explicit DC branch; do not silently clamp frequency to epsilon.

## Fix validation

Add a nominal regression and the exact boundary witness below. Require a clear domain diagnostic (or a documented finite limiting model), never NaN/Inf or an unrelated solver error. Re-run both engines.

## Scope and limitations

A source-level verdict addresses the reported declaration/claim, not every possible connected system. Tests cover 0–0.5 seconds and are not a proof of long-run stability. Shared instances are not distinct root causes. A missing bound, timeout, compiler error or failed nominal run alone never counts as a verified bug or a false positive. Fixes are proposals; no library/compiler implementation was changed.

[Group and related reports](../groups/trapezoid-frequency.md) · [Index](../README.md)
