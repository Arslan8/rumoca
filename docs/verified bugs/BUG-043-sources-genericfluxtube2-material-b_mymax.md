# BUG-043: `Sources.genericFluxTube2.material.B_myMax` fails at `0`, a value its declaration permits

| | |
|---|---|
| **Model** | `ModelicaTest.Magnetic.FluxTubes.Sources` |
| **File** | `ModelicaStandardLibrary-4.1.0/ModelicaTest/Magnetic/FluxTubes.mo:582` |
| **Instance** | `genericFluxTube2.material` |
| **Parameter** | `B_myMax` |
| **Trigger** | `genericFluxTube2.material.B_myMax = 0` |
| **Reach** | this trigger reproduces in 1 model |
| **Confirmed in** | Rumoca **and** OpenModelica 1.27.0-dev |
| **Status** | Reported, not fixed |

## The instance

```modelica
// ModelicaStandardLibrary-4.1.0/ModelicaTest/Magnetic/FluxTubes.mo:582
Modelica.Magnetic.FluxTubes.Shapes.FixedShape.GenericFluxTube genericFluxTube2
```

`genericFluxTube2.material` is an instance of `Modelica.Magnetic.FluxTubes.Material.SoftMagnetic.BaseData`.

## What happens

The model simulates cleanly at its declared values in both tools. Overriding
`genericFluxTube2.material.B_myMax` to `0` — a value nothing in the declaration excludes — makes it fail in
both:

```console
$ rumoca compile-bitcode sources.rbc --simulate --check --param genericFluxTube2.material.B_myMax=0
```

## Root cause

`SI.MagneticFluxDensity B_myMax` with no bound, used as a divisor

The declaration to change is in the component, not in this model:
[BUG-011](BUG-011-fluxtubes-b-mymax-unguarded-divisor.md) carries the
argument and the suggested patch.

```modelica
// the fix, in BaseData
parameter SI.MagneticFluxDensity B_myMax(min=Modelica.Constants.eps);
```

## Why this instance has its own report

The root cause is one edit to `BaseData`. This file exists because
that is not the only thing a developer needs: `FluxTubes.mo` was proven to
fail at this specific instance, and a maintainer looking at that model needs to
know which of its components was exercised and at what value. Sibling instances
in the same file are reported separately for the same reason.
