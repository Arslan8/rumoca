# FINDING-00936: Example waveform timing divides by zero frequency

| Field | Value |
|---|---|
| Verdict | confirmed |
| Scope / group | trapezoid-frequency |
| Model | Modelica.Electrical.Analog.Examples.OpAmps.VoltageFollower |
| Target | f |
| Student classification | divisor-reachable-zero |
| Original report | [FINDING-voltagefollower-f-divzero-2.md](../../v2/bugs/FINDING-voltagefollower-f-divzero-2.md) — reviewed as `FINDING-00936-voltagefollower-f.md`, which a later run renamed |
| Original SHA-256 | 2b48333bf1e4383c97e5c996a42b2a7084205fd8cc795db5545e2b22a0c6e685 |

## Verification and root cause

The source uses f directly in trapezoid timing (rising=0.2/f, width=0.3/f, falling=0.2/f, period=1/f). f=0 is not handled and gives undefined parameter bindings. Rumoca reports non-finite evaluation after a clean baseline. OpenModelica baseline-executable overrides also report zero division; recompilation can instead hit a template/code-generation error, which is not counted as independent runtime confirmation.

## Source evidence

Compiler/source-resolved declaration: `Electrical/Analog/Examples/OpAmps/VoltageFollower.mo:7`. Role: `parameter`; binding: `10`; effective min: `None`; effective max: `None`. 

[Electrical/Analog/Examples/OpAmps/VoltageFollower.mo — source snapshot](../evidence/sources/9a2ef7ccb82a00cb-VoltageFollower.mo)

```modelica
5:   parameter SI.Voltage Vns=-15 "Negative supply";
6:   parameter SI.Voltage Vin=5 "Amplitude of input voltage";
7:   parameter SI.Frequency f=10 "Frequency of input voltage";
8:   parameter SI.Resistance Ri=1
9:     "Inner resistance of input voltage source";
10:   parameter SI.Resistance Rl=1 "Load resistance";
```

[Electrical/Analog/Examples/OpAmps/VoltageFollower.mo — source snapshot](../evidence/sources/9a2ef7ccb82a00cb-VoltageFollower.mo)

```modelica
1: within Modelica.Electrical.Analog.Examples.OpAmps;
2: model VoltageFollower "Reproduce input voltage"
3:   extends Modelica.Icons.Example;
4:   parameter SI.Voltage Vps=+15 "Positive supply";
5:   parameter SI.Voltage Vns=-15 "Negative supply";
6:   parameter SI.Voltage Vin=5 "Amplitude of input voltage";
7:   parameter SI.Frequency f=10 "Frequency of input voltage";
8:   parameter SI.Resistance Ri=1
9:     "Inner resistance of input voltage source";
10:   parameter SI.Resistance Rl=1 "Load resistance";
11:   Modelica.Electrical.Analog.Ideal.IdealizedOpAmpLimited opAmp(
12:     Vps=Vps,
13:     Vns=Vns,
14:     v_in(start=0))
15:     annotation (Placement(transformation(extent={{0,-10},{20,10}})));
16:   Modelica.Electrical.Analog.Basic.Ground ground
17:     annotation (Placement(transformation(extent={{-20,-100},{0,-80}})));
18:   Modelica.Electrical.Analog.Sources.TrapezoidVoltage vIn(
19:     V=2*Vin,
20:     rising=0.2/f,
21:     width=0.3/f,
22:     falling=0.2/f,
23:     period=1/f,
24:     nperiod=-1,
25:     offset=-Vin,
26:     startTime=-(vIn.rising + vIn.width/2)) annotation (Placement(
27:         transformation(
28:         extent={{-10,-10},{10,10}},
29:         rotation=270,
30:         origin={-80,0})));
31:   Modelica.Electrical.Analog.Sensors.VoltageSensor vOut annotation (Placement(
32:         transformation(
33:         extent={{-10,10},{10,-10}},
34:         rotation=270,
35:         origin={60,-20})));
36:   Modelica.Electrical.Analog.Basic.Resistor ri(R=Ri)
37:     annotation (Placement(transformation(extent={{-60,0},{-40,20}})));
38:   Modelica.Electrical.Analog.Basic.Resistor rl(R=Rl) annotation (Placement(
39:         transformation(
40:         extent={{-10,-10},{10,10}},
41:         rotation=270,
42:         origin={30,-18})));
43: equation
44:   connect(ground.p, vIn.n) annotation (Line(
45:       points={{-10,-80},{-80,-80},{-80,-10}}, color={0,0,255}));
```


## Execution evidence

[Rumoca commands, return codes, integrity hashes, bounded output and metadata](../evidence/e51ccafaf08188b5.json). Baseline: **clean**.

| Probe | Outcome |
|---|---|
| `f=0` | reported-failure |

Diagnostic: numeric evaluation produced a non-finite result

[Independent OpenModelica wrappers and complete output](../evidence/omc-extra-e51ccafaf08188b5.json). Baseline: simulation succeeded.

- `f=0` set before translation: "Error: Template error: A template call failed (/usr/bin/../lib/x86_64-linux-gnu/omc/libOpenModelicaCompiler.so: (null)). One possible reason could be that a template imported function call failed (which should not happen for functions called from within template code; templates assert pure 'match'/non-failing semantics)..
- Same value declared final, with final-parameter evaluation: "Error: Template error: A template call failed (/usr/bin/../lib/x86_64-linux-gnu/omc/libOpenModelicaCompiler.so: (null)). One possible reason could be that a template imported function call failed (which should not happen for functions called from within template code; templates assert pure 'match'/non-failing semantics)..

## Proposed fix

At the example frequency declaration, specify and assert f>0 and guard the timing calculations so the assertion can diagnose invalid input. If f=0 should mean DC, provide an explicit DC branch; do not silently clamp frequency to epsilon.

## Fix validation

Add a nominal regression and the exact boundary witness below. Require a clear domain diagnostic (or a documented finite limiting model), never NaN/Inf or an unrelated solver error. Re-run both engines.

## Scope and limitations

A source-level verdict addresses the reported declaration/claim, not every possible connected system. Tests cover 0–0.5 seconds and are not a proof of long-run stability. Shared instances are not distinct root causes. A missing bound, timeout, compiler error or failed nominal run alone never counts as a verified bug or a false positive. Fixes are proposals; no library/compiler implementation was changed.

[Group and related reports](../groups/trapezoid-frequency.md) · [Index](../README.md)
