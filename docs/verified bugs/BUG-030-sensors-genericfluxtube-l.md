# BUG-030: `Sensors.genericFluxTube.l` fails at `0`, a value its declaration permits

| | |
|---|---|
| **Model** | `ModelicaTest.Magnetic.FluxTubes.Sensors` |
| **File** | `ModelicaStandardLibrary-4.1.0/ModelicaTest/Magnetic/FluxTubes.mo:120` |
| **Instance** | `genericFluxTube` |
| **Parameter** | `l` |
| **Trigger** | `genericFluxTube.l = 0` |
| **Reach** | this trigger reproduces in 3 models |
| **Confirmed in** | Rumoca **and** OpenModelica 1.27.0-dev |
| **Status** | Reported, not fixed |

## The instance

```modelica
// ModelicaStandardLibrary-4.1.0/ModelicaTest/Magnetic/FluxTubes.mo:120
Modelica.Magnetic.FluxTubes.Shapes.FixedShape.GenericFluxTube genericFluxTube
```

`genericFluxTube` is an instance of `Modelica.Magnetic.FluxTubes.Shapes.FixedShape.GenericFluxTube`.

## What happens

The model simulates cleanly at its declared values in both tools. Overriding
`genericFluxTube.l` to `0` — a value nothing in the declaration excludes — makes it fail in
both:

```console
$ rumoca compile-bitcode sensors.rbc --simulate --check --param genericFluxTube.l=0
```

## Root cause

`SI.Length l` with no bound, used directly as a divisor

The declaration to change is in the component, not in this model:
[BUG-014](BUG-014-genericfluxtube-l-unbounded-divisor.md) carries the
argument and the suggested patch.

```modelica
// the fix, in GenericFluxTube
parameter SI.Length l(min=Modelica.Constants.small) = 0.01;
```

## Why this instance has its own report

The root cause is one edit to `GenericFluxTube`. This file exists because
that is not the only thing a developer needs: `FluxTubes.mo` was proven to
fail at this specific instance, and a maintainer looking at that model needs to
know which of its components was exercised and at what value. Sibling instances
in the same file are reported separately for the same reason.
