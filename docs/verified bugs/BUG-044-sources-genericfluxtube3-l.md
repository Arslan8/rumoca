# BUG-044: `Sources.genericFluxTube3.l` fails at `0`, a value its declaration permits

| | |
|---|---|
| **Model** | `ModelicaTest.Magnetic.FluxTubes.Sources` |
| **File** | `ModelicaStandardLibrary-4.1.0/ModelicaTest/Magnetic/FluxTubes.mo:591` |
| **Instance** | `genericFluxTube3` |
| **Parameter** | `l` |
| **Trigger** | `genericFluxTube3.l = 0` |
| **Reach** | this trigger reproduces in 1 model |
| **Confirmed in** | Rumoca **and** OpenModelica 1.27.0-dev |
| **Status** | Reported, not fixed |

## The instance

```modelica
// ModelicaStandardLibrary-4.1.0/ModelicaTest/Magnetic/FluxTubes.mo:591
Modelica.Magnetic.FluxTubes.Shapes.FixedShape.GenericFluxTube genericFluxTube3
```

`genericFluxTube3` is an instance of `Modelica.Magnetic.FluxTubes.Shapes.FixedShape.GenericFluxTube`.

## What happens

The model simulates cleanly at its declared values in both tools. Overriding
`genericFluxTube3.l` to `0` — a value nothing in the declaration excludes — makes it fail in
both:

```console
$ rumoca compile-bitcode sources.rbc --simulate --check --param genericFluxTube3.l=0
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
