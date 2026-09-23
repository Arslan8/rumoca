# FINDING-00817: Example waveform timing divides by zero frequency

| Field | Value |
|---|---|
| Verdict | confirmed |
| Scope / group | trapezoid-frequency |
| Model | Modelica.Electrical.Analog.Examples.OpAmps.Differentiator |
| Target | f |
| Student classification | divisor-reachable-zero |
| Original report | [FINDING-differentiator-f-divzero-2.md](../../v2/bugs/FINDING-differentiator-f-divzero-2.md) — reviewed as `FINDING-00817-differentiator-f.md`, which a later run renamed |
| Original SHA-256 | ddf258242909ca0c1f0b4f5f84d08685d5251c2231c42b8e94e3500226648dbd |

## Verification and root cause

The source uses f directly in trapezoid timing (rising=0.2/f, width=0.3/f, falling=0.2/f, period=1/f). f=0 is not handled and gives undefined parameter bindings. Rumoca reports non-finite evaluation after a clean baseline. OpenModelica baseline-executable overrides also report zero division; recompilation can instead hit a template/code-generation error, which is not counted as independent runtime confirmation.

## Source evidence

Compiler/source-resolved declaration: `Electrical/Analog/Examples/OpAmps/Differentiator.mo:5`. Role: `parameter`; binding: `10`; effective min: `None`; effective max: `None`. 

[Electrical/Analog/Examples/OpAmps/Differentiator.mo — source snapshot](../evidence/sources/bbc64b22f66b444a-Differentiator.mo)

```modelica
3:   extends Modelica.Icons.Example;
4:   parameter SI.Voltage Vin=5 "Amplitude of input voltage";
5:   parameter SI.Frequency f=10 "Frequency of input voltage";
6:   Modelica.Electrical.Analog.Basic.Ground ground
7:     annotation (Placement(transformation(extent={{-20,-40},{0,-20}})));
8:   Sources.TrapezoidVoltage vIn(
```

[Electrical/Analog/Examples/OpAmps/Differentiator.mo — source snapshot](../evidence/sources/bbc64b22f66b444a-Differentiator.mo)

```modelica
1: within Modelica.Electrical.Analog.Examples.OpAmps;
2: model Differentiator "Differentiating amplifier"
3:   extends Modelica.Icons.Example;
4:   parameter SI.Voltage Vin=5 "Amplitude of input voltage";
5:   parameter SI.Frequency f=10 "Frequency of input voltage";
6:   Modelica.Electrical.Analog.Basic.Ground ground
7:     annotation (Placement(transformation(extent={{-20,-40},{0,-20}})));
8:   Sources.TrapezoidVoltage vIn(
9:     V=2*Vin,
10:     rising=0.2/f,
11:     width=0.3/f,
12:     falling=0.2/f,
13:     period=1/f,
14:     nperiod=-1,
15:     offset=-Vin,
16:     startTime=-(vIn.rising + vIn.width/2))
17:     annotation (Placement(
18:         transformation(
19:         extent={{-10,-10},{10,10}},
20:         rotation=270,
21:         origin={-40,0})));
22:   Modelica.Electrical.Analog.Sensors.VoltageSensor vOut annotation (Placement(
23:         transformation(
24:         extent={{-10,10},{10,-10}},
25:         rotation=270,
26:         origin={40,0})));
27:   OpAmpCircuits.Der der_(
28:     k=2,
29:     f=f,
30:     v(fixed=true))
31:     annotation (Placement(transformation(extent={{-10,-10},{10,10}})));
32: equation
33:   connect(vIn.p, der_.p1)
34:     annotation (Line(points={{-40,10},{-10,10}}, color={0,0,255}));
35:   connect(vIn.n, der_.n1)
36:     annotation (Line(points={{-40,-10},{-10,-10}}, color={0,0,255}));
37:   connect(der_.n1, ground.p)
38:     annotation (Line(points={{-10,-10},{-10,-20}}, color={0,0,255}));
39:   connect(der_.p2, vOut.p)
40:     annotation (Line(points={{10,10},{40,10}}, color={0,0,255}));
41:   connect(der_.n2, vOut.n)
42:     annotation (Line(points={{10,-10},{40,-10}}, color={0,0,255}));
43:   annotation (Documentation(info="<html>
44: <p>This is a (inverting) differentiating amplifier. Resistance R can be chosen, capacitance C is defined by the desired time constant resp. frequency.</p>
45: <p>Note: <code>vOut</code> measure the negative output voltage.</p>
```


## Execution evidence

[Rumoca commands, return codes, integrity hashes, bounded output and metadata](../evidence/9fb3c0f95a3c9b11.json). Baseline: **clean**.

| Probe | Outcome |
|---|---|
| `f=0` | reported-failure |

Diagnostic: numeric evaluation produced a non-finite result

[Independent OpenModelica wrappers and complete output](../evidence/omc-extra-9fb3c0f95a3c9b11.json). Baseline: simulation succeeded.

- `f=0` set before translation: "Error: Template error: A template call failed (/usr/bin/../lib/x86_64-linux-gnu/omc/libOpenModelicaCompiler.so: (null)). One possible reason could be that a template imported function call failed (which should not happen for functions called from within template code; templates assert pure 'match'/non-failing semantics)..
- Same value declared final, with final-parameter evaluation: "Error: Template error: A template call failed (/usr/bin/../lib/x86_64-linux-gnu/omc/libOpenModelicaCompiler.so: (null)). One possible reason could be that a template imported function call failed (which should not happen for functions called from within template code; templates assert pure 'match'/non-failing semantics)..

## Proposed fix

At the example frequency declaration, specify and assert f>0 and guard the timing calculations so the assertion can diagnose invalid input. If f=0 should mean DC, provide an explicit DC branch; do not silently clamp frequency to epsilon.

## Fix validation

Add a nominal regression and the exact boundary witness below. Require a clear domain diagnostic (or a documented finite limiting model), never NaN/Inf or an unrelated solver error. Re-run both engines.

## Scope and limitations

A source-level verdict addresses the reported declaration/claim, not every possible connected system. Tests cover 0–0.5 seconds and are not a proof of long-run stability. Shared instances are not distinct root causes. A missing bound, timeout, compiler error or failed nominal run alone never counts as a verified bug or a false positive. Fixes are proposals; no library/compiler implementation was changed.

[Group and related reports](../groups/trapezoid-frequency.md) · [Index](../README.md)
