# FINDING-00846: LC oscillator design divides by zero

| Field | Value |
|---|---|
| Verdict | confirmed |
| Scope / group | oscillator-design |
| Model | Modelica.Electrical.Analog.Examples.OpAmps.LCOscillator |
| Target | L |
| Student classification | physical-domain-unenforced |
| Original report | [FINDING-lcoscillator-l-unbounded.md](../../v2/bugs/FINDING-lcoscillator-l-unbounded.md) — reviewed as `FINDING-00846-lcoscillator-l.md`, which a later run renamed |
| Original SHA-256 | b250ff3e8b6c9442542d969528f98f191543a1d1db915a2c0d872da2ec5f27d7 |

## Verification and root cause

The source computes C=1/((2*pi*f)^2*L) and gamma=(1-A)/(2*R*C). Setting the reported design parameter to zero makes an explicit denominator zero. This is separate from the zero-storage behavior of Basic.Capacitor/Inductor. The nominal example passes; the selected design-parameter perturbation fails.

## Source evidence

Compiler/source-resolved declaration: `Electrical/Analog/Examples/OpAmps/LCOscillator.mo:8`. Role: `parameter`; binding: `0.001`; effective min: `None`; effective max: `None`. 

[Electrical/Analog/Examples/OpAmps/LCOscillator.mo — source snapshot](../evidence/sources/3c553b6c97a587b8-LCOscillator.mo)

```modelica
6:   parameter SI.Frequency f=1000 "Desired frequency";
7:   parameter Real A=1.001 "Amplification constant: A > 1 amplification, A = 1 pure sinusoidal oscillation, A < 0 damping";
8:   parameter SI.Inductance L=0.001 "Arbitrary inductance > 0";
9:   parameter SI.Capacitance C=1/((2*pi*f)^2*L) "Calculated capacitance to reach frequency f";
10:   parameter SI.Resistance R=10000.0 "Damping resistance";
11:   parameter SI.Resistance R1=10000.0 "Arbitrary high resistance";
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
| `L=0` | reported-failure |

Diagnostic: numeric evaluation produced a non-finite result

[Independent OpenModelica wrappers and complete output](../evidence/omc-extra-8425a760f9ce6583.json). Baseline: simulation succeeded.

- `L=0` set before translation: LOG_ASSERT        | debug   | division by zero at time 0, (a=2.533029591058445e-08) / (b=0), where divisor b expression is: L.
- Same value declared final, with final-parameter evaluation: LOG_ASSERT        | debug   | division by zero at time 0, (a=2.533029591058445e-08) / (b=0), where divisor b expression is: 0.0.

## Proposed fix

Validate f>0, L>0, C>0 and R>0 at this example/design layer, with guarded derived-parameter calculations and actionable assertions. Do not prohibit zero in every primitive capacitor/inductor/resistor.

## Fix validation

Add a nominal regression and the exact boundary witness below. Require a clear domain diagnostic (or a documented finite limiting model), never NaN/Inf or an unrelated solver error. Re-run both engines.

## Scope and limitations

A source-level verdict addresses the reported declaration/claim, not every possible connected system. Tests cover 0–0.5 seconds and are not a proof of long-run stability. Shared instances are not distinct root causes. A missing bound, timeout, compiler error or failed nominal run alone never counts as a verified bug or a false positive. Fixes are proposals; no library/compiler implementation was changed.

[Group and related reports](../groups/oscillator-design.md) · [Index](../README.md)
