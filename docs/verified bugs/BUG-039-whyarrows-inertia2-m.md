# BUG-039: `WhyArrows.inertia2.m` fails at `0`, a value its declaration permits

| | |
|---|---|
| **Model** | `Modelica.Mechanics.Translational.Examples.WhyArrows` |
| **File** | `ModelicaStandardLibrary-4.1.0/Modelica 4.1.0/Mechanics/Translational/Examples/WhyArrows.mo:33` |
| **Instance** | `inertia2` |
| **Parameter** | `m` |
| **Trigger** | `inertia2.m = 0` |
| **Reach** | this trigger reproduces in 1 model |
| **Confirmed in** | Rumoca **and** OpenModelica 1.27.0-dev |
| **Status** | Reported, not fixed |

## The instance

```modelica
// ModelicaStandardLibrary-4.1.0/Modelica 4.1.0/Mechanics/Translational/Examples/WhyArrows.mo:33
Translational.Components.Mass inertia2
```

`inertia2` is an instance of `Modelica.Mechanics.Translational.Components.Mass`.

## What happens

The model simulates cleanly at its declared values in both tools. Overriding
`inertia2.m` to `0` — a value nothing in the declaration excludes — makes it fail in
both:

```console
$ rumoca compile-bitcode whyarrows.rbc --simulate --check --param inertia2.m=0
```

## Root cause

`SI.Mass m(min=0)` — the bound permits the value that degenerates `m*a = f`

The declaration to change is in the component, not in this model:
[BUG-002](BUG-002-msl-zero-mass-within-declared-bound.md) carries the
argument and the suggested patch.

```modelica
// the fix, in Mass
parameter SI.Mass m(min=Modelica.Constants.small, start=1);
```

## Why this instance has its own report

The root cause is one edit to `Mass`. This file exists because
that is not the only thing a developer needs: `WhyArrows.mo` was proven to
fail at this specific instance, and a maintainer looking at that model needs to
know which of its components was exercised and at what value. Sibling instances
in the same file are reported separately for the same reason.
