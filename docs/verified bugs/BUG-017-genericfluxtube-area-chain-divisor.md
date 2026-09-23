# BUG-017: `GenericFluxTube.area` reaches a divisor two classes away, unbounded

| | |
|---|---|
| **Severity** | Medium — a shape component every fixed-shape flux tube builds on |
| **Target** | MSL 4.1.0, `Modelica.Magnetic.FluxTubes.Shapes.FixedShape.GenericFluxTube` |
| **Fix site** | `Shapes/FixedShape/GenericFluxTube.mo`, the `area` declaration |
| **Trigger** | `area = 0` |
| **Confirmed in** | Rumoca **and** OpenModelica 1.27.0-dev, 3 models |
| **Found by** | OMC-backed sweep of 827 models, batch cross-confirmed, 2026-09-14 |
| **Status** | Reported, not fixed |

Split from [BUG-014](BUG-014-genericfluxtube-l-unbounded-divisor.md), which now
covers `l` alone. The two are separate fixes to separate declarations and the
`area` case fails by a different route, so they are filed separately.

## Summary

```modelica
// Shapes/FixedShape/GenericFluxTube.mo
extends BaseClasses.FixedShape;
parameter SI.CrossSection area = 0.0001 "Area of cross section";
equation
  A = area;
  G_m = mu_0*mu_r*A/l;
```

`SI.CrossSection` supplies no bound of its own:

```
SI.CrossSection -> final quantity="Area", final unit="m2"   (no min)
```

A zero or negative cross-section is a value the declaration permits. Neither is
a flux tube.

## Why this one is not simply "a parameter reaching a divisor"

`area` is never a divisor. It reaches one two steps later, in the base class:

```modelica
// BaseClasses/FixedShape.mo
SI.Reluctance R_m "Magnetic reluctance";
SI.Permeance  G_m "Magnetic permeance";
equation
  R_m = 1/G_m;
  V_m = Phi*R_m;
```

`area = 0` → `A = 0` → `G_m = 0` → `R_m = 1/0`.

The parameter, the equation that consumes it, and the division that fails are in
three different places across a class boundary. Nothing in `GenericFluxTube`
divides by `area`; nothing in `FixedShape` mentions it. A check that looks at one
component at a time cannot see this, which is the same structure as
[BUG-006](BUG-006-bound-propagated-into-a-different-component.md).

`SI.Permeance` and `SI.Reluctance` are themselves unbounded, so no intermediate
declaration interrupts the chain.

## Confirmed

```console
$ rumoca compile-bitcode sensors.rbc --simulate --check --param genericFluxTube.area=0
```

Confirmed via `ModelicaTest.Magnetic.FluxTubes.Sensors`; reached 3 models in the
sweep. The declared configuration runs cleanly in both tools.

## Suggested fix

```modelica
parameter SI.CrossSection area(min=Modelica.Constants.small) = 0.0001;
```

This case additionally argues for a bound on `G_m` in `FixedShape`, since that is
where the division actually happens and it is reachable from more than one shape.
