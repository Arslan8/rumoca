# BUG-037: `ElasticBearing.idealGear.ratio` fails at `0`, a value its declaration permits

| | |
|---|---|
| **Model** | `Modelica.Mechanics.Rotational.Examples.ElasticBearing` |
| **File** | `ModelicaStandardLibrary-4.1.0/Modelica 4.1.0/Mechanics/Rotational/Examples/ElasticBearing.mo:27` |
| **Instance** | `idealGear` |
| **Parameter** | `ratio` |
| **Trigger** | `idealGear.ratio = 0` |
| **Reach** | this trigger reproduces in 1 model |
| **Confirmed in** | Rumoca **and** OpenModelica 1.27.0-dev |
| **Status** | Reported, not fixed |

## The instance

```modelica
// ModelicaStandardLibrary-4.1.0/Modelica 4.1.0/Mechanics/Rotational/Examples/ElasticBearing.mo:27
Rotational.Components.IdealGear idealGear
```

`idealGear` is an instance of `Modelica.Mechanics.Rotational.Components.IdealGear`.

## What happens

The model simulates cleanly at its declared values in both tools. Overriding
`idealGear.ratio` to `0` — a value nothing in the declaration excludes — makes it fail in
both:

```console
$ rumoca compile-bitcode elasticbearing.rbc --simulate --check --param idealGear.ratio=0
```

## Root cause

`Real ratio` unbounded; at zero the gear decouples

The declaration to change is in the component, not in this model:
[BUG-015](BUG-015-idealgear-zero-ratio.md) carries the
argument and the suggested patch.

```modelica
// the fix, in IdealGear
parameter Real ratio(min=Modelica.Constants.eps, start=1);
```

## Why this instance has its own report

The root cause is one edit to `IdealGear`. This file exists because
that is not the only thing a developer needs: `ElasticBearing.mo` was proven to
fail at this specific instance, and a maintainer looking at that model needs to
know which of its components was exercised and at what value. Sibling instances
in the same file are reported separately for the same reason.
