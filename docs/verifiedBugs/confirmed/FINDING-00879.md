# FINDING-00879: Example waveform timing divides by zero frequency

| Field | Value |
|---|---|
| Verdict | confirmed |
| Scope / group | trapezoid-frequency |
| Model | Modelica.Electrical.Analog.Examples.OpAmps.NonInvertingAmplifier |
| Target | f |
| Student classification | divisor-reachable-zero |
| Original report | [FINDING-noninvertingamplifier-f-divzero-2.md](../../v2/bugs/FINDING-noninvertingamplifier-f-divzero-2.md) — reviewed as `FINDING-00879-noninvertingamplifier-f.md`, which a later run renamed |
| Original SHA-256 | cb83f623fc6e518c68963ab3b882b2d7e10677b63065796a6a14c0f67da3e8a5 |

## Verification and root cause

The source uses f directly in trapezoid timing (rising=0.2/f, width=0.3/f, falling=0.2/f, period=1/f). f=0 is not handled and gives undefined parameter bindings. Rumoca reports non-finite evaluation after a clean baseline. OpenModelica baseline-executable overrides also report zero division; recompilation can instead hit a template/code-generation error, which is not counted as independent runtime confirmation.

## Source evidence

Compiler/source-resolved declaration: `Electrical/Analog/Examples/OpAmps/NonInvertingAmplifier.mo:5`. Role: `parameter`; binding: `10`; effective min: `None`; effective max: `None`. 

[Electrical/Analog/Examples/OpAmps/NonInvertingAmplifier.mo — source snapshot](../evidence/sources/a23b5c42bfbffa5c-NonInvertingAmplifier.mo)

```modelica
3:   extends Modelica.Icons.Example;
4:   parameter SI.Voltage Vin=5 "Amplitude of input voltage";
5:   parameter SI.Frequency f=10 "Frequency of input voltage";
6:   Modelica.Electrical.Analog.Basic.Ground ground
7:     annotation (Placement(transformation(extent={{-20,-40},{0,-20}})));
8:   Modelica.Electrical.Analog.Sources.TrapezoidVoltage vIn(
```

[Electrical/Analog/Examples/OpAmps/NonInvertingAmplifier.mo — source snapshot](../evidence/sources/a23b5c42bfbffa5c-NonInvertingAmplifier.mo)

```modelica
1: within Modelica.Electrical.Analog.Examples.OpAmps;
2: model NonInvertingAmplifier "Non-inverting amplifier"
3:   extends Modelica.Icons.Example;
4:   parameter SI.Voltage Vin=5 "Amplitude of input voltage";
5:   parameter SI.Frequency f=10 "Frequency of input voltage";
6:   Modelica.Electrical.Analog.Basic.Ground ground
7:     annotation (Placement(transformation(extent={{-20,-40},{0,-20}})));
8:   Modelica.Electrical.Analog.Sources.TrapezoidVoltage vIn(
9:     V=2*Vin,
10:     rising=0.2/f,
11:     width=0.3/f,
12:     falling=0.2/f,
13:     period=1/f,
14:     nperiod=-1,
15:     offset=-Vin,
16:     startTime=-(vIn.rising + vIn.width/2)) annotation (Placement(
17:         transformation(
18:         extent={{-10,-10},{10,10}},
19:         rotation=270,
20:         origin={-40,0})));
21:   Modelica.Electrical.Analog.Sensors.VoltageSensor vOut annotation (Placement(
22:         transformation(
23:         extent={{-10,10},{10,-10}},
24:         rotation=270,
25:         origin={40,0})));
26:   OpAmpCircuits.Buffer buffer(k=2)
27:     annotation (Placement(transformation(extent={{-10,-10},{10,10}})));
28: equation
29:   connect(vIn.n, buffer.n1)
30:     annotation (Line(points={{-40,-10},{-10,-10}}, color={0,0,255}));
31:   connect(vIn.p, buffer.p1)
32:     annotation (Line(points={{-40,10},{-10,10}}, color={0,0,255}));
33:   connect(buffer.p2, vOut.p)
34:     annotation (Line(points={{10,10},{40,10}}, color={0,0,255}));
35:   connect(buffer.n2, vOut.n)
36:     annotation (Line(points={{10,-10},{40,-10}}, color={0,0,255}));
37:   connect(buffer.n1, ground.p)
38:     annotation (Line(points={{-10,-10},{-10,-20}}, color={0,0,255}));
39:   annotation (Documentation(info="<html>
40: <p>This is a non inverting amplifier.</p>
41: </html>"),
42:     experiment(
43:       StartTime=0,
44:       StopTime=1,
45:       Tolerance=1e-006,
```


## Execution evidence

[Rumoca commands, return codes, integrity hashes, bounded output and metadata](../evidence/368e14d0116ecee5.json). Baseline: **clean**.

| Probe | Outcome |
|---|---|
| `f=0` | reported-failure |

Diagnostic: numeric evaluation produced a non-finite result

[Independent OpenModelica wrappers and complete output](../evidence/omc-extra-368e14d0116ecee5.json). Baseline: simulation succeeded.

- `f=0` set before translation: "Error: Template error: A template call failed (/usr/bin/../lib/x86_64-linux-gnu/omc/libOpenModelicaCompiler.so: (null)). One possible reason could be that a template imported function call failed (which should not happen for functions called from within template code; templates assert pure 'match'/non-failing semantics)..
- Same value declared final, with final-parameter evaluation: "Error: Template error: A template call failed (/usr/bin/../lib/x86_64-linux-gnu/omc/libOpenModelicaCompiler.so: (null)). One possible reason could be that a template imported function call failed (which should not happen for functions called from within template code; templates assert pure 'match'/non-failing semantics)..

## Proposed fix

At the example frequency declaration, specify and assert f>0 and guard the timing calculations so the assertion can diagnose invalid input. If f=0 should mean DC, provide an explicit DC branch; do not silently clamp frequency to epsilon.

## Fix validation

Add a nominal regression and the exact boundary witness below. Require a clear domain diagnostic (or a documented finite limiting model), never NaN/Inf or an unrelated solver error. Re-run both engines.

## Scope and limitations

A source-level verdict addresses the reported declaration/claim, not every possible connected system. Tests cover 0–0.5 seconds and are not a proof of long-run stability. Shared instances are not distinct root causes. A missing bound, timeout, compiler error or failed nominal run alone never counts as a verified bug or a false positive. Fixes are proposals; no library/compiler implementation was changed.

[Group and related reports](../groups/trapezoid-frequency.md) · [Index](../README.md)
