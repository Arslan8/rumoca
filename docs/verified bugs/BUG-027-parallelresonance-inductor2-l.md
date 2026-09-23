# BUG-027: `ParallelResonance.inductor2.L` fails at `0`, a value its declaration permits

| | |
|---|---|
| **Model** | `Modelica.Electrical.Analog.Examples.ParallelResonance` |
| **File** | `ModelicaStandardLibrary-4.1.0/Modelica 4.1.0/Electrical/Analog/Examples/ParallelResonance.mo:49` |
| **Instance** | `inductor2` |
| **Parameter** | `L` |
| **Trigger** | `inductor2.L = 0` |
| **Reach** | this trigger reproduces in 4 models |
| **Confirmed in** | Rumoca **and** OpenModelica 1.27.0-dev |
| **Status** | Reported, not fixed |

## The instance

```modelica
// ModelicaStandardLibrary-4.1.0/Modelica 4.1.0/Electrical/Analog/Examples/ParallelResonance.mo:49
Basic.Inductor inductor2
```

`inductor2` is an instance of `Modelica.Electrical.Analog.Basic.Inductor`.

## What happens

The model simulates cleanly at its declared values in both tools. Overriding
`inductor2.L` to `0` — a value nothing in the declaration excludes — makes it fail in
both:

```console
$ rumoca compile-bitcode parallelresonance.rbc --simulate --check --param inductor2.L=0
```

## Root cause

`SI.Inductance L` with no bound, documented as permitting zero

The declaration to change is in the component, not in this model:
[BUG-010](BUG-010-inductor-documents-zero-it-cannot-honour.md) carries the
argument and the suggested patch.

```modelica
// the fix, in Inductor
parameter SI.Inductance L(min=Modelica.Constants.small, start=1);
```

## Why this instance has its own report

The root cause is one edit to `Inductor`. This file exists because
that is not the only thing a developer needs: `ParallelResonance.mo` was proven to
fail at this specific instance, and a maintainer looking at that model needs to
know which of its components was exercised and at what value. Sibling instances
in the same file are reported separately for the same reason.
