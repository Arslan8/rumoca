# BUG-014: `GenericFluxTube` geometry parameters are unbounded divisors, one of them through a chain

| | |
|---|---|
| **Severity** | Medium — a shape component every fixed-shape flux tube builds on |
| **Target** | MSL 4.1.0, `Modelica.Magnetic.FluxTubes.Shapes.FixedShape.GenericFluxTube` |
| **Trigger** | `l = 0` or `area = 0` |
| **Confirmed in** | Rumoca **and** OpenModelica 1.27.0-dev, 3 models each |
| **Found by** | OMC-backed sweep of 827 models, batch cross-confirmed, 2026-09-14 |
| **Status** | Reported, not fixed |

## Summary

```modelica
// Shapes/FixedShape/GenericFluxTube.mo
extends BaseClasses.FixedShape;
parameter SI.Length l = 0.01 "Length in direction of flux";
parameter SI.CrossSection area = 0.0001 "Area of cross section";
equation
  A = area;
  G_m = mu_0*mu_r*A/l;
```

Neither parameter carries a bound, and neither type supplies one:

```
SI.Length       -> final quantity="Length", final unit="m"        (no min)
SI.CrossSection -> final quantity="Area",   final unit="m2"       (no min)
```

A length of zero, a negative length, and a zero cross-section are all values
the declaration permits. None of them is a flux tube.

## Two different failure paths

**`l = 0` is direct.** It is the divisor in `G_m = mu_0*mu_r*A/l`.

**`area = 0` is a chain**, and this is the more interesting one. It reaches a
division two steps later, in the base class:

```modelica
// BaseClasses/FixedShape.mo
SI.Reluctance R_m "Magnetic reluctance";
SI.Permeance  G_m "Magnetic permeance";
equation
  R_m = 1/G_m;
  V_m = Phi*R_m;
```

`area = 0` → `A = 0` → `G_m = 0` → `R_m = 1/0`.

So the parameter, the equation that consumes it, and the division that fails are
in three different places, across a class boundary. As with
[BUG-006](BUG-006-bound-propagated-into-a-different-component.md), a check that
looks at one component at a time cannot see it: nothing in `GenericFluxTube`
divides by `area`, and nothing in `FixedShape` mentions it.

`SI.Permeance` and `SI.Reluctance` are themselves unbounded, so no intermediate
declaration interrupts the chain either.

## Confirmed

Both parameters, in both tools, with the declared configuration clean:

```console
$ rumoca compile-bitcode sensors.rbc --simulate --check --param genericFluxTube.l=0
$ rumoca compile-bitcode sensors.rbc --simulate --check --param genericFluxTube.area=0
```

Confirmed via `ModelicaTest.Magnetic.FluxTubes.Sensors`; reached 3 models each in
the sweep.

## Relationship to BUG-011

[BUG-011](BUG-011-fluxtubes-b-mymax-unguarded-divisor.md) reported
`SoftMagnetic.BaseData.B_myMax`, which `FixedShape` also divides by. Together
they make the point that `FixedShape` and its shapes divide by four separately
declared quantities — `l`, `area` (via `G_m`), `B_myMax`, and `G_m` itself — and
none of the four declares a lower bound.

## Suggested fix

```modelica
parameter SI.Length l(min=Modelica.Constants.small) = 0.01;
parameter SI.CrossSection area(min=Modelica.Constants.small) = 0.0001;
```

The `area` case additionally argues for a bound on `G_m` in `FixedShape`, since
that is where the division actually happens and it is reachable from more than
one shape.
