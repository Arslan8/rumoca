# BUG-029: `Sensors.genericFluxTube.area` fails at `0`, a value its declaration permits

| | |
|---|---|
| **Model** | `ModelicaTest.Magnetic.FluxTubes.Sensors` |
| **File** | `ModelicaStandardLibrary-4.1.0/ModelicaTest/Magnetic/FluxTubes.mo:120` |
| **Instance** | `genericFluxTube` |
| **Parameter** | `area` |
| **Trigger** | `genericFluxTube.area = 0` |
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
`genericFluxTube.area` to `0` — a value nothing in the declaration excludes — makes it fail in
both:

```console
$ rumoca compile-bitcode sensors.rbc --simulate --check --param genericFluxTube.area=0
```

## Root cause

`SI.CrossSection area` with no bound, reaching `1/G_m` two classes away

The declaration to change is in the component, not in this model:
[BUG-017](BUG-017-genericfluxtube-area-chain-divisor.md) carries the
argument and the suggested patch.

```modelica
// the fix, in GenericFluxTube
parameter SI.CrossSection area(min=Modelica.Constants.small) = 0.0001;
```

## Why this instance has its own report

The root cause is one edit to `GenericFluxTube`. This file exists because
that is not the only thing a developer needs: `FluxTubes.mo` was proven to
fail at this specific instance, and a maintainer looking at that model needs to
know which of its components was exercised and at what value. Sibling instances
in the same file are reported separately for the same reason.
