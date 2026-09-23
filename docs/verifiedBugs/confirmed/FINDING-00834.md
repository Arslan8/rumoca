# FINDING-00834: Example waveform timing divides by zero frequency

| Field | Value |
|---|---|
| Verdict | confirmed |
| Scope / group | trapezoid-frequency |
| Model | Modelica.Electrical.Analog.Examples.OpAmps.Integrator |
| Target | f |
| Student classification | divisor-reachable-zero |
| Original report | [FINDING-integrator-f-divzero-2.md](../../v2/bugs/FINDING-integrator-f-divzero-2.md) — reviewed as `FINDING-00834-integrator-f.md`, which a later run renamed |
| Original SHA-256 | ea9eba0c13490a11760c9ddc664ff995844e5c8ac115e7d410e12bbf495fcea0 |

## Verification and root cause

The source uses f directly in trapezoid timing (rising=0.2/f, width=0.3/f, falling=0.2/f, period=1/f). f=0 is not handled and gives undefined parameter bindings. Rumoca reports non-finite evaluation after a clean baseline. OpenModelica baseline-executable overrides also report zero division; recompilation can instead hit a template/code-generation error, which is not counted as independent runtime confirmation.

## Source evidence

Compiler/source-resolved declaration: `Electrical/Analog/Examples/OpAmps/Integrator.mo:5`. Role: `parameter`; binding: `10`; effective min: `None`; effective max: `None`. 

[Electrical/Analog/Examples/OpAmps/Integrator.mo — source snapshot](../evidence/sources/a9c9af31d2a6be68-Integrator.mo)

```modelica
3:   extends Modelica.Icons.Example;
4:   parameter SI.Voltage Vin=5 "Amplitude of input voltage";
5:   parameter SI.Frequency f=10 "Frequency of input voltage";
6:   Modelica.Electrical.Analog.Basic.Ground ground
7:     annotation (Placement(transformation(extent={{-20,-40},{0,-20}})));
8:   Modelica.Electrical.Analog.Sensors.VoltageSensor vOut annotation (Placement(
```

[Electrical/Analog/Examples/OpAmps/Integrator.mo — source snapshot](../evidence/sources/a9c9af31d2a6be68-Integrator.mo)

```modelica
1: within Modelica.Electrical.Analog.Examples.OpAmps;
2: model Integrator "Integrating amplifier"
3:   extends Modelica.Icons.Example;
4:   parameter SI.Voltage Vin=5 "Amplitude of input voltage";
5:   parameter SI.Frequency f=10 "Frequency of input voltage";
6:   Modelica.Electrical.Analog.Basic.Ground ground
7:     annotation (Placement(transformation(extent={{-20,-40},{0,-20}})));
8:   Modelica.Electrical.Analog.Sensors.VoltageSensor vOut annotation (Placement(
9:         transformation(
10:         extent={{-10,10},{10,-10}},
11:         rotation=270,
12:         origin={40,0})));
13:   OpAmpCircuits.Integrator integrator(
14:     k=2,
15:     f=f,
16:     v(fixed=true))
17:     annotation (Placement(transformation(extent={{-10,-10},{10,10}})));
18:   Sources.TrapezoidVoltage vIn(
19:     V=2*Vin,
20:     rising=0.2/f,
21:     width=0.3/f,
22:     falling=0.2/f,
23:     period=1/f,
24:     nperiod=-1,
25:     offset=-Vin,
26:     startTime=-(vIn.rising + vIn.width/2))
27:     annotation (Placement(
28:         transformation(
29:         extent={{-10,-10},{10,10}},
30:         rotation=270,
31:         origin={-40,0})));
32: equation
33:   connect(integrator.n1, ground.p)
34:     annotation (Line(points={{-10,-10},{-10,-20}}, color={0,0,255}));
35:   connect(integrator.p2, vOut.p)
36:     annotation (Line(points={{10,10},{40,10}}, color={0,0,255}));
37:   connect(integrator.n2, vOut.n)
38:     annotation (Line(points={{10,-10},{40,-10}}, color={0,0,255}));
39:   connect(vIn.p, integrator.p1)
40:     annotation (Line(points={{-40,10},{-10,10}}, color={0,0,255}));
41:   connect(vIn.n, integrator.n1)
42:     annotation (Line(points={{-40,-10},{-10,-10}}, color={0,0,255}));
43:   annotation (Documentation(info="<html>
44: <p>This is an (inverting) integrating amplifier. Resistance R can be chosen, capacitance C is defined by the desired time constant resp. frequency.</p>
45: <p>Note: <code>vOut</code> measure the negative output voltage.</p>
```


## Execution evidence

[Rumoca commands, return codes, integrity hashes, bounded output and metadata](../evidence/1e4f5d7bf77ea670.json). Baseline: **clean**.

| Probe | Outcome |
|---|---|
| `f=0` | reported-failure |

Diagnostic: numeric evaluation produced a non-finite result

[Independent OpenModelica wrappers and complete output](../evidence/omc-extra-1e4f5d7bf77ea670.json). Baseline: simulation succeeded.

- `f=0` set before translation: Error: Template error: A template call failed (/usr/bin/../lib/x86_64-linux-gnu/omc/libOpenModelicaCompiler.so: (null)). One possible reason could be that a template imported function call failed (which should not happen for functions called from within template code; templates assert pure 'match'/non-failing semantics)..
- Same value declared final, with final-parameter evaluation: Error: Template error: A template call failed (/usr/bin/../lib/x86_64-linux-gnu/omc/libOpenModelicaCompiler.so: (null)). One possible reason could be that a template imported function call failed (which should not happen for functions called from within template code; templates assert pure 'match'/non-failing semantics)..

## Proposed fix

At the example frequency declaration, specify and assert f>0 and guard the timing calculations so the assertion can diagnose invalid input. If f=0 should mean DC, provide an explicit DC branch; do not silently clamp frequency to epsilon.

## Fix validation

Add a nominal regression and the exact boundary witness below. Require a clear domain diagnostic (or a documented finite limiting model), never NaN/Inf or an unrelated solver error. Re-run both engines.

## Scope and limitations

A source-level verdict addresses the reported declaration/claim, not every possible connected system. Tests cover 0–0.5 seconds and are not a proof of long-run stability. Shared instances are not distinct root causes. A missing bound, timeout, compiler error or failed nominal run alone never counts as a verified bug or a false positive. Fixes are proposals; no library/compiler implementation was changed.

[Group and related reports](../groups/trapezoid-frequency.md) · [Index](../README.md)
