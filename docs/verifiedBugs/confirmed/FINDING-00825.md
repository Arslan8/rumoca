# FINDING-00825: Filter cutoff frequency divides by zero

| Field | Value |
|---|---|
| Verdict | confirmed |
| Scope / group | cutoff-frequency |
| Model | Modelica.Electrical.Analog.Examples.OpAmps.HighPass |
| Target | fG |
| Student classification | divisor-reachable-zero |
| Original report | [FINDING-highpass-fg-divzero.md](../../v2/bugs/FINDING-highpass-fg-divzero.md) — reviewed as `FINDING-00825-highpass-fg.md`, which a later run renamed |
| Original SHA-256 | 5804b42051235153e452e93489754f4acfd84a5f180130c29f1bcf80355de4ff |

## Verification and root cause

The component is instantiated with T=1/(2*pi*fG). fG=0 gives a literal zero denominator and no finite time constant. Both engines fail after clean baselines; OpenModelica also fails with final-evaluated fG=0.

## Source evidence

Compiler/source-resolved declaration: `Electrical/Analog/Examples/OpAmps/HighPass.mo:7`. Role: `parameter`; binding: `1`; effective min: `None`; effective max: `None`. 

[Electrical/Analog/Examples/OpAmps/HighPass.mo — source snapshot](../evidence/sources/bb3fdc565981731e-HighPass.mo)

```modelica
5:   parameter SI.Voltage Vin=5 "Amplitude of input voltage";
6:   parameter SI.Frequency f=10 "Frequency of input voltage";
7:   parameter SI.Frequency fG=f/10 "Limiting frequency";
8:   Modelica.Electrical.Analog.Basic.Ground ground
9:     annotation (Placement(transformation(extent={{-20,-40},{0,-20}})));
10:   Modelica.Electrical.Analog.Sensors.VoltageSensor vOut annotation (Placement(
```

[Electrical/Analog/Examples/OpAmps/HighPass.mo — source snapshot](../evidence/sources/bb3fdc565981731e-HighPass.mo)

```modelica
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
```


## Execution evidence

[Rumoca commands, return codes, integrity hashes, bounded output and metadata](../evidence/c5eb5de89833fa1e.json). Baseline: **clean**.

| Probe | Outcome |
|---|---|
| `fG=0` | reported-failure |

Diagnostic: numeric evaluation produced a non-finite result

[Independent OpenModelica wrappers and complete output](../evidence/omc-extra-c5eb5de89833fa1e.json). Baseline: simulation succeeded.

- `fG=0` set before translation: LOG_ASSERT        | debug   | division by zero at time 0, (a=0.1591549430918953) / (b=0), where divisor b expression is: fG.
- Same value declared final, with final-parameter evaluation: LOG_ASSERT        | debug   | division by zero at time 0, (a=0.1591549430918953) / (b=0), where divisor b expression is: 0.0.

## Proposed fix

Require and assert fG>0 at the example design interface; guard the T calculation. If a zero-cutoff limiting filter is wanted, implement its limiting equations separately.

## Fix validation

Add a nominal regression and the exact boundary witness below. Require a clear domain diagnostic (or a documented finite limiting model), never NaN/Inf or an unrelated solver error. Re-run both engines.

## Scope and limitations

A source-level verdict addresses the reported declaration/claim, not every possible connected system. Tests cover 0–0.5 seconds and are not a proof of long-run stability. Shared instances are not distinct root causes. A missing bound, timeout, compiler error or failed nominal run alone never counts as a verified bug or a false positive. Fixes are proposals; no library/compiler implementation was changed.

[Group and related reports](../groups/cutoff-frequency.md) · [Index](../README.md)
