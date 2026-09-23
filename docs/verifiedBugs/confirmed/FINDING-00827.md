# FINDING-00827: Example waveform timing divides by zero frequency

| Field | Value |
|---|---|
| Verdict | confirmed |
| Scope / group | trapezoid-frequency |
| Model | Modelica.Electrical.Analog.Examples.OpAmps.HighPass |
| Target | f |
| Student classification | divisor-reachable-zero |
| Original report | [FINDING-highpass-f-divzero-2.md](../../v2/bugs/FINDING-highpass-f-divzero-2.md) — reviewed as `FINDING-00827-highpass-f.md`, which a later run renamed |
| Original SHA-256 | ae35d84950fda2f6be340d0f982c346df09d88ccccede3175227b86a6fe795ee |

## Verification and root cause

The source uses f directly in trapezoid timing (rising=0.2/f, width=0.3/f, falling=0.2/f, period=1/f). f=0 is not handled and gives undefined parameter bindings. Rumoca reports non-finite evaluation after a clean baseline. OpenModelica baseline-executable overrides also report zero division; recompilation can instead hit a template/code-generation error, which is not counted as independent runtime confirmation.

## Source evidence

Compiler/source-resolved declaration: `Electrical/Analog/Examples/OpAmps/HighPass.mo:6`. Role: `parameter`; binding: `10`; effective min: `None`; effective max: `None`. 

[Electrical/Analog/Examples/OpAmps/HighPass.mo — source snapshot](../evidence/sources/bb3fdc565981731e-HighPass.mo)

```modelica
4:   import Modelica.Constants.pi;
5:   parameter SI.Voltage Vin=5 "Amplitude of input voltage";
6:   parameter SI.Frequency f=10 "Frequency of input voltage";
7:   parameter SI.Frequency fG=f/10 "Limiting frequency";
8:   Modelica.Electrical.Analog.Basic.Ground ground
9:     annotation (Placement(transformation(extent={{-20,-40},{0,-20}})));
```

[Electrical/Analog/Examples/OpAmps/HighPass.mo — source snapshot](../evidence/sources/bb3fdc565981731e-HighPass.mo)

```modelica
1: within Modelica.Electrical.Analog.Examples.OpAmps;
2: model HighPass "High-pass filter"
3:   extends Modelica.Icons.Example;
4:   import Modelica.Constants.pi;
5:   parameter SI.Voltage Vin=5 "Amplitude of input voltage";
6:   parameter SI.Frequency f=10 "Frequency of input voltage";
7:   parameter SI.Frequency fG=f/10 "Limiting frequency";
8:   Modelica.Electrical.Analog.Basic.Ground ground
9:     annotation (Placement(transformation(extent={{-20,-40},{0,-20}})));
10:   Modelica.Electrical.Analog.Sensors.VoltageSensor vOut annotation (Placement(
11:         transformation(
12:         extent={{-10,10},{10,-10}},
13:         rotation=270,
14:         origin={40,0})));
15:   OpAmpCircuits.Derivative derivative(T=1/(2*pi*fG),
16:     v(fixed=true))
17:     annotation (Placement(transformation(extent={{-10,-10},{10,10}})));
18:   Sources.TrapezoidVoltage vIn(
19:     V=Vin,
20:     rising=0.2/f,
21:     width=0.3/f,
22:     falling=0.2/f,
23:     period=1/f,
24:     nperiod=-1,
25:     offset=0,
26:     startTime=-(vIn.rising + vIn.width/2))
27:     annotation (Placement(
28:         transformation(
29:         extent={{-10,-10},{10,10}},
30:         rotation=270,
31:         origin={-40,0})));
32: equation
33:   connect(derivative.n1, ground.p)
34:     annotation (Line(points={{-10,-10},{-10,-20},{-10,-20}}, color={0,0,255}));
35:   connect(derivative.p2, vOut.p)
36:     annotation (Line(points={{10,10},{40,10}}, color={0,0,255}));
37:   connect(derivative.n2, vOut.n)
38:     annotation (Line(points={{10,-10},{40,-10}}, color={0,0,255}));
39:   connect(vIn.p, derivative.p1)
40:     annotation (Line(points={{-40,10},{-10,10}}, color={0,0,255}));
41:   connect(vIn.n, derivative.n1)
42:     annotation (Line(points={{-40,-10},{-10,-10}}, color={0,0,255}));
43:   annotation (Documentation(info="<html>
44: <p>This is a (inverting) high pass filter. Resistance R1 can be chosen, resistance R2 is defined by the desired amplification k, capacitance C is defined by the desired cut-off frequency.</p>
45: <p>The example is taken from: U. Tietze and C. Schenk, Halbleiter-Schaltungstechnik (German), 11th edition, Springer 1999, Chapter 13.3</p>
```


## Execution evidence

[Rumoca commands, return codes, integrity hashes, bounded output and metadata](../evidence/c5eb5de89833fa1e.json). Baseline: **clean**.

| Probe | Outcome |
|---|---|
| `f=0` | reported-failure |

Diagnostic: numeric evaluation produced a non-finite result

[Independent OpenModelica wrappers and complete output](../evidence/omc-extra-c5eb5de89833fa1e.json). Baseline: simulation succeeded.

- `f=0` set before translation: "Error: Template error: A template call failed (/usr/bin/../lib/x86_64-linux-gnu/omc/libOpenModelicaCompiler.so: (null)). One possible reason could be that a template imported function call failed (which should not happen for functions called from within template code; templates assert pure 'match'/non-failing semantics)..
- Same value declared final, with final-parameter evaluation: "Error: Template error: A template call failed (/usr/bin/../lib/x86_64-linux-gnu/omc/libOpenModelicaCompiler.so: (null)). One possible reason could be that a template imported function call failed (which should not happen for functions called from within template code; templates assert pure 'match'/non-failing semantics)..

## Proposed fix

At the example frequency declaration, specify and assert f>0 and guard the timing calculations so the assertion can diagnose invalid input. If f=0 should mean DC, provide an explicit DC branch; do not silently clamp frequency to epsilon.

## Fix validation

Add a nominal regression and the exact boundary witness below. Require a clear domain diagnostic (or a documented finite limiting model), never NaN/Inf or an unrelated solver error. Re-run both engines.

## Scope and limitations

A source-level verdict addresses the reported declaration/claim, not every possible connected system. Tests cover 0–0.5 seconds and are not a proof of long-run stability. Shared instances are not distinct root causes. A missing bound, timeout, compiler error or failed nominal run alone never counts as a verified bug or a false positive. Fixes are proposals; no library/compiler implementation was changed.

[Group and related reports](../groups/trapezoid-frequency.md) · [Index](../README.md)
