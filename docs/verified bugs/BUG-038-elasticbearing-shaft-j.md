# BUG-038: `ElasticBearing.shaft.J` fails at `0`, a value its declaration permits

| | |
|---|---|
| **Model** | `Modelica.Mechanics.Rotational.Examples.ElasticBearing` |
| **File** | `ModelicaStandardLibrary-4.1.0/Modelica 4.1.0/Mechanics/Rotational/Examples/ElasticBearing.mo:4` |
| **Instance** | `shaft` |
| **Parameter** | `J` |
| **Trigger** | `shaft.J = 0` |
| **Reach** | this trigger reproduces in 1 model |
| **Confirmed in** | Rumoca **and** OpenModelica 1.27.0-dev |
| **Status** | Reported, not fixed |

## The instance

```modelica
// ModelicaStandardLibrary-4.1.0/Modelica 4.1.0/Mechanics/Rotational/Examples/ElasticBearing.mo:4
Rotational.Components.Inertia shaft
```

`shaft` is an instance of `Modelica.Mechanics.Rotational.Components.Inertia`.

## What happens

The model simulates cleanly at its declared values in both tools. Overriding
`shaft.J` to `0` — a value nothing in the declaration excludes — makes it fail in
both:

```console
$ rumoca compile-bitcode elasticbearing.rbc --simulate --check --param shaft.J=0
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
that is not the only thing a developer needs: `ElasticBearing.mo` was proven to
fail at this specific instance, and a maintainer looking at that model needs to
know which of its components was exercised and at what value. Sibling instances
in the same file are reported separately for the same reason.
