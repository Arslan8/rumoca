# BUG-014: `GenericFluxTube.l` is an unbounded divisor

| | |
|---|---|
| **Severity** | Medium — a shape component every fixed-shape flux tube builds on |
| **Target** | MSL 4.1.0, `Modelica.Magnetic.FluxTubes.Shapes.FixedShape.GenericFluxTube` |
| **Fix site** | `Shapes/FixedShape/GenericFluxTube.mo`, the `l` declaration |
| **Trigger** | `l = 0` |
| **Confirmed in** | Rumoca **and** OpenModelica 1.27.0-dev, 3 models |
| **Found by** | OMC-backed sweep of 827 models, batch cross-confirmed, 2026-09-14 |
| **Status** | Reported, not fixed |

## Summary

```modelica
// Shapes/FixedShape/GenericFluxTube.mo
extends BaseClasses.FixedShape;
parameter SI.Length l = 0.01 "Length in direction of flux";
equation
  G_m = mu_0*mu_r*A/l;
```

`l` is the divisor directly. `SI.Length` supplies no bound of its own:

```
SI.Length -> final quantity="Length", final unit="m"   (no min)
```

A zero length and a negative length are both values the declaration permits, and
neither is a flux tube.

The sibling parameter `area` in the same component fails by a longer route and is
filed separately as
[BUG-017](BUG-017-genericfluxtube-area-chain-divisor.md) — a separate declaration
needing a separate fix.

## Confirmed

In both tools, with the declared configuration clean:

```console
$ rumoca compile-bitcode sensors.rbc --simulate --check --param genericFluxTube.l=0
```

Confirmed via `ModelicaTest.Magnetic.FluxTubes.Sensors`; reached 3 models in the
sweep.

## Relationship to BUG-011

[BUG-011](BUG-011-fluxtubes-b-mymax-unguarded-divisor.md) reported
`SoftMagnetic.BaseData.B_myMax`, which `FixedShape` also divides by. Together
they make the point that `FixedShape` and its shapes divide by four separately
declared quantities — `l`, `area` (via `G_m`, [BUG-017](BUG-017-genericfluxtube-area-chain-divisor.md)),
`B_myMax`, and `G_m` itself — and none of the four declares a lower bound. Each
is its own fix.

## Suggested fix

```modelica
parameter SI.Length l(min=Modelica.Constants.small) = 0.01;
```
