# BUG-028: `InvertingAmp.f` fails at `0`, a value its declaration permits

| | |
|---|---|
| **Model** | `Modelica.Electrical.Analog.Examples.InvertingAmp` |
| **File** | `ModelicaStandardLibrary-4.1.0/Modelica 4.1.0/Electrical/Analog/Examples/InvertingAmp.mo:7` |
| **Instance** | `(model parameter)` |
| **Parameter** | `f` |
| **Trigger** | `f = 0` |
| **Reach** | this trigger reproduces in 3 models |
| **Confirmed in** | Rumoca **and** OpenModelica 1.27.0-dev |
| **Status** | Reported, not fixed |

## The instance

```modelica
// ModelicaStandardLibrary-4.1.0/Modelica 4.1.0/Electrical/Analog/Examples/InvertingAmp.mo:7
parameter SI.Frequency f=
```

`InvertingAmp` is an instance of `Modelica.Electrical.Analog.Examples.InvertingAmp`.

## What happens

The model simulates cleanly at its declared values in both tools. Overriding
`f` to `0` — a value nothing in the declaration excludes — makes it fail in
both:

```console
$ rumoca compile-bitcode invertingamp.rbc --simulate --check --param f=0
```

## Root cause

`SI.Frequency f` with no bound, reaching four divisions

The declaration to change is in the component, not in this model:
[BUG-019](BUG-019-invertingamp-frequency-unbounded-divisor.md) carries the
argument and the suggested patch.

```modelica
// the fix, in InvertingAmp
parameter SI.Frequency f(min=Modelica.Constants.eps) = 10;
```

## Why this instance has its own report

The root cause is one edit to `InvertingAmp`. This file exists because
that is not the only thing a developer needs: `InvertingAmp.mo` was proven to
fail at this specific instance, and a maintainer looking at that model needs to
know which of its components was exercised and at what value. Sibling instances
in the same file are reported separately for the same reason.
