# BUG-032: `ParallelResonance.capacitor2.C` fails at `0`, a value its declaration permits

| | |
|---|---|
| **Model** | `Modelica.Electrical.Analog.Examples.ParallelResonance` |
| **File** | `ModelicaStandardLibrary-4.1.0/Modelica 4.1.0/Electrical/Analog/Examples/ParallelResonance.mo:54` |
| **Instance** | `capacitor2` |
| **Parameter** | `C` |
| **Trigger** | `capacitor2.C = 0` |
| **Reach** | this trigger reproduces in 2 models |
| **Confirmed in** | Rumoca **and** OpenModelica 1.27.0-dev |
| **Status** | Reported, not fixed |

## The instance

```modelica
// ModelicaStandardLibrary-4.1.0/Modelica 4.1.0/Electrical/Analog/Examples/ParallelResonance.mo:54
Basic.Capacitor capacitor2
```

`capacitor2` is an instance of `Modelica.Electrical.Analog.Basic.Capacitor`.

## What happens

The model simulates cleanly at its declared values in both tools. Overriding
`capacitor2.C` to `0` — a value nothing in the declaration excludes — makes it fail in
both:

```console
$ rumoca compile-bitcode parallelresonance.rbc --simulate --check --param capacitor2.C=0
```

## Root cause

`SI.Capacitance C` with no bound, documented as permitting zero

The declaration to change is in the component, not in this model:
[BUG-013](BUG-013-capacitor-zero-capacitance-topology-dependent.md) carries the
argument and the suggested patch.

```modelica
// the fix, in Capacitor
parameter SI.Capacitance C(min=Modelica.Constants.small, start=1);
```

## Why this instance has its own report

The root cause is one edit to `Capacitor`. This file exists because
that is not the only thing a developer needs: `ParallelResonance.mo` was proven to
fail at this specific instance, and a maintainer looking at that model needs to
know which of its components was exercised and at what value. Sibling instances
in the same file are reported separately for the same reason.
