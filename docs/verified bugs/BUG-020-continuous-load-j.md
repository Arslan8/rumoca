# BUG-020: `Continuous.load.J` fails at `0`, a value its declaration permits

| | |
|---|---|
| **Model** | `Modelica.Clocked.Examples.SimpleControlledDrive.Continuous` |
| **File** | `ModelicaStandardLibrary-4.1.0/Modelica 4.1.0/Clocked/Examples/SimpleControlledDrive/Continuous.mo:5` |
| **Instance** | `load` |
| **Parameter** | `J` |
| **Trigger** | `load.J = 0` |
| **Reach** | this trigger reproduces in 32 models |
| **Confirmed in** | Rumoca **and** OpenModelica 1.27.0-dev |
| **Status** | Reported, not fixed |

## The instance

```modelica
// ModelicaStandardLibrary-4.1.0/Modelica 4.1.0/Clocked/Examples/SimpleControlledDrive/Continuous.mo:5
Modelica.Mechanics.Rotational.Components.Inertia load
```

`load` is an instance of `Modelica.Mechanics.Rotational.Components.Inertia`.

## What happens

The model simulates cleanly at its declared values in both tools. Overriding
`load.J` to `0` — a value nothing in the declaration excludes — makes it fail in
both:

```console
$ rumoca compile-bitcode continuous.rbc --simulate --check --param load.J=0
```

## Root cause

`SI.Inertia J(min=0)` — the bound permits the value that degenerates `J*a = tau`

The declaration to change is in the component, not in this model:
[BUG-018](BUG-018-rotational-inertia-zero-within-declared-bound.md) carries the
argument and the suggested patch.

```modelica
// the fix, in Inertia
parameter SI.Inertia J(min=Modelica.Constants.small, start=1);
```

## Why this instance has its own report

The root cause is one edit to `Inertia`. This file exists because
that is not the only thing a developer needs: `Continuous.mo` was proven to
fail at this specific instance, and a maintainer looking at that model needs to
know which of its components was exercised and at what value. Sibling instances
in the same file are reported separately for the same reason.
