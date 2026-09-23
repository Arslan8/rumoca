# FINDING-00853: LC oscillator design divides by zero

| Field | Value |
|---|---|
| Verdict | confirmed |
| Scope / group | oscillator-design |
| Model | Modelica.Electrical.Analog.Examples.OpAmps.LCOscillator |
| Target | f |
| Student classification | divisor-reachable-zero |
| Original report | [FINDING-lcoscillator-f-divzero-2.md](../../v2/bugs/FINDING-lcoscillator-f-divzero-2.md) — reviewed as `FINDING-00853-lcoscillator-f.md`, which a later run renamed |
| Original SHA-256 | 99aec6ad60cb8ff0a17de28290f548ba1236c44e123d31d28cc9493ff1eddd26 |

## Verification and root cause

The source computes C=1/((2*pi*f)^2*L) and gamma=(1-A)/(2*R*C). Setting the reported design parameter to zero makes an explicit denominator zero. This is separate from the zero-storage behavior of Basic.Capacitor/Inductor. The nominal example passes; the selected design-parameter perturbation fails.

## Source evidence

Compiler/source-resolved declaration: `Electrical/Analog/Examples/OpAmps/LCOscillator.mo:6`. Role: `parameter`; binding: `1000`; effective min: `None`; effective max: `None`. 

[Electrical/Analog/Examples/OpAmps/LCOscillator.mo — source snapshot](../evidence/sources/3c553b6c97a587b8-LCOscillator.mo)

```modelica
4:   import Modelica.Constants.pi;
5:   parameter SI.Voltage VAmp=10 "Amplitude of output";
6:   parameter SI.Frequency f=1000 "Desired frequency";
7:   parameter Real A=1.001 "Amplification constant: A > 1 amplification, A = 1 pure sinusoidal oscillation, A < 0 damping";
8:   parameter SI.Inductance L=0.001 "Arbitrary inductance > 0";
9:   parameter SI.Capacitance C=1/((2*pi*f)^2*L) "Calculated capacitance to reach frequency f";
```

[Electrical/Analog/Examples/OpAmps/LCOscillator.mo — source snapshot](../evidence/sources/3c553b6c97a587b8-LCOscillator.mo)

```modelica
5:   parameter SI.Voltage VAmp=10 "Amplitude of output";
6:   parameter SI.Frequency f=1000 "Desired frequency";
7:   parameter Real A=1.001 "Amplification constant: A > 1 amplification, A = 1 pure sinusoidal oscillation, A < 0 damping";
8:   parameter SI.Inductance L=0.001 "Arbitrary inductance > 0";
9:   parameter SI.Capacitance C=1/((2*pi*f)^2*L) "Calculated capacitance to reach frequency f";
10:   parameter SI.Resistance R=10000.0 "Damping resistance";
11:   parameter SI.Resistance R1=10000.0 "Arbitrary high resistance";
12:   parameter SI.Resistance R2=(A - 1)*R1 "Calculated resistance to reach amplification A";
13:   parameter Real gamma=(1 - A)/(2*R*C) "Calculated characteristical parameter";
```


## Execution evidence

[Rumoca commands, return codes, integrity hashes, bounded output and metadata](../evidence/8425a760f9ce6583.json). Baseline: **clean**.

| Probe | Outcome |
|---|---|
| `f=0` | reported-failure |

Diagnostic: numeric evaluation produced a non-finite result

[Independent OpenModelica wrappers and complete output](../evidence/omc-extra-8425a760f9ce6583.json). Baseline: simulation succeeded.

- `f=0` set before translation: LOG_ASSERT        | info    | simulation terminated by an assertion at initialization.
- Same value declared final, with final-parameter evaluation: LOG_ASSERT        | info    | simulation terminated by an assertion at initialization.

## Proposed fix

Validate f>0, L>0, C>0 and R>0 at this example/design layer, with guarded derived-parameter calculations and actionable assertions. Do not prohibit zero in every primitive capacitor/inductor/resistor.

## Fix validation

Add a nominal regression and the exact boundary witness below. Require a clear domain diagnostic (or a documented finite limiting model), never NaN/Inf or an unrelated solver error. Re-run both engines.

## Scope and limitations

A source-level verdict addresses the reported declaration/claim, not every possible connected system. Tests cover 0–0.5 seconds and are not a proof of long-run stability. Shared instances are not distinct root causes. A missing bound, timeout, compiler error or failed nominal run alone never counts as a verified bug or a false positive. Fixes are proposals; no library/compiler implementation was changed.

[Group and related reports](../groups/oscillator-design.md) · [Index](../README.md)
