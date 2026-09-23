# BUG-019: `InvertingAmp.f` is an unbounded frequency reaching four divisors

| | |
|---|---|
| **Severity** | Low–Medium — an example model, but one users copy as a template |
| **Component** | Modelica Standard Library 4.1.0, not Rumoca |
| **Fix site** | `Electrical/Analog/Examples/InvertingAmp.mo:7`, the `f` declaration |
| **Trigger** | `f = 0` |
| **Confirmed in** | Rumoca **and** OpenModelica 1.27.0-dev, 3 models |
| **Found by** | DivisorSan over the full corpus, batch cross-confirmed, 2026-09-14 |
| **Status** | Reported, not fixed |

## Summary

```modelica
// Electrical/Analog/Examples/InvertingAmp.mo
parameter SI.Frequency f=10 "Frequency of input voltage";
...
Modelica.Electrical.Analog.Sources.TrapezoidVoltage vIn(
    V=2*Vin,
    rising=0.2/f,
    width=0.3/f,
    falling=0.2/f,
    period=1/f,
    ...
```

`f` reaches **four** separate divisions, all in one modification block, and
neither the declaration nor `SI.Frequency` bounds it:

```
SI.Frequency -> final quantity="Frequency", final unit="Hz"   (no min)
```

`f = 0` makes all four infinite. A negative `f` is quieter and worse: the trapezoid
gets negative `rising`, `width` and `falling` times and a negative `period`,
which is not a waveform at all.

## Why this is worth filing despite being an example

Two reasons.

**It is a divisor with no bound anywhere on the path.** Unlike
[BUG-002](BUG-002-msl-zero-mass-within-declared-bound.md), where `min=0` is
present but too weak, here nothing is written at any level — not on the
parameter, not on the type.

**Example models are templates.** `InvertingAmp` is what a user copies when
building an op-amp circuit, and the `0.2/f` idiom copies with it.

## Confirmed

```console
$ rumoca compile-bitcode invertingamp.rbc --simulate --check --param f=0
```

The model runs cleanly at its declared values in both tools and fails at the
trigger in both. Reached 3 models in the sweep.

## Suggested fix

```modelica
parameter SI.Frequency f(min=Modelica.Constants.eps)=10 "Frequency of input voltage";
```

`Modelica.Constants.eps` rather than `small` because `f` is a divisor, matching
what `QuadraticSpeedDependentForce` already does for `v_nominal`.

## Related

The same file declares `Vps=+15` and `Vns=-15`, whose *difference* is a divisor
inside `IdealizedOpAmpLimited` — a constraint between two parameters that no
`min` can express. That is
[BUG-016](BUG-016-relational-invariant-between-two-parameters.md), a separate
fix in a separate component.
