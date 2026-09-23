# FINDING-00866: Multivibrator capacitance formula has zero divisors

| Field | Value |
|---|---|
| Verdict | confirmed |
| Scope / group | multivibrator-design |
| Model | Modelica.Electrical.Analog.Examples.OpAmps.Multivibrator |
| Target | R1 |
| Student classification | physical-domain-unenforced |
| Original report | [FINDING-multivibrator-r1-unbounded.md](../../v2/bugs/FINDING-multivibrator-r1-unbounded.md) — reviewed as `FINDING-00866-multivibrator-r1.md`, which a later run renamed |
| Original SHA-256 | eff9032be85df53fb146298de4caf46bbf6bb3573f6fe0c4504f8edf5ceaf9cd |

## Verification and root cause

C=1/f/(2*R*log(1+2*R1/R2)). f=0 or R=0 zeros a factor, R2=0 divides inside the logarithm, and R1=0 makes log(1)=0. All four witnesses fail independently after successful baselines, including final-evaluated recompilation.

## Source evidence

Compiler/source-resolved declaration: `Electrical/Analog/Examples/OpAmps/Multivibrator.mo:7`. Role: `parameter`; binding: `1000`; effective min: `None`; effective max: `None`. 

[Electrical/Analog/Examples/OpAmps/Multivibrator.mo — source snapshot](../evidence/sources/9b4c9c1643c6e629-Multivibrator.mo)

```modelica
5:   parameter SI.Voltage Vns=-15 "Negative supply";
6:   parameter SI.Frequency f=10 "Desired frequency";
7:   parameter SI.Resistance R1=1000 "Resistance 1 for adjusting the Schmitt trigger voltage level";
8:   parameter SI.Resistance R2=1000 "Resistance 2 for adjusting the Schmitt trigger voltage level";
9:   parameter SI.Resistance R=1000 "Arbitrary resistance";
10:   parameter SI.Capacitance C=1/f/(2*R*log(1 + 2*R1/R2)) "Calculated capacitance to reach the desired frequency f";
```

[Electrical/Analog/Examples/OpAmps/Multivibrator.mo — source snapshot](../evidence/sources/9b4c9c1643c6e629-Multivibrator.mo)

```modelica
4:   parameter SI.Voltage Vps=+15 "Positive supply";
5:   parameter SI.Voltage Vns=-15 "Negative supply";
6:   parameter SI.Frequency f=10 "Desired frequency";
7:   parameter SI.Resistance R1=1000 "Resistance 1 for adjusting the Schmitt trigger voltage level";
8:   parameter SI.Resistance R2=1000 "Resistance 2 for adjusting the Schmitt trigger voltage level";
9:   parameter SI.Resistance R=1000 "Arbitrary resistance";
10:   parameter SI.Capacitance C=1/f/(2*R*log(1 + 2*R1/R2)) "Calculated capacitance to reach the desired frequency f";
```


## Execution evidence

[Rumoca commands, return codes, integrity hashes, bounded output and metadata](../evidence/03f0a994c6cd5a22.json). Baseline: **clean**.

| Probe | Outcome |
|---|---|
| `R1=0` | reported-failure |

Diagnostic: numeric evaluation produced a non-finite result

[Independent OpenModelica wrappers and complete output](../evidence/omc-extra-03f0a994c6cd5a22.json). Baseline: simulation succeeded.

- `R1=0` set before translation: LOG_ASSERT        | debug   | division by zero at time 0, (a=0.5) / (b=0), where divisor b expression is: log(1.0 + 2.0 * R1 / R2) * R * f.
- Same value declared final, with final-parameter evaluation: LOG_ASSERT        | debug   | division by zero at time 0, (a=0.5) / (b=0), where divisor b expression is: 0.0.

## Proposed fix

Validate strictly positive f,R,R1,R2 for this positive-resistance oscillator design before computing C; guard the derived expression and issue a clear domain assertion. If other sign combinations are supported, validate both the logarithm argument and the complete denominator explicitly.

## Fix validation

Regression-test each zero independently and a negative log argument, as well as positive nominal values.

## Scope and limitations

A source-level verdict addresses the reported declaration/claim, not every possible connected system. Tests cover 0–0.5 seconds and are not a proof of long-run stability. Shared instances are not distinct root causes. A missing bound, timeout, compiler error or failed nominal run alone never counts as a verified bug or a false positive. Fixes are proposals; no library/compiler implementation was changed.

[Group and related reports](../groups/multivibrator-design.md) · [Index](../README.md)
