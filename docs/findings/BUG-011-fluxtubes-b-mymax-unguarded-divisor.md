# BUG-011: `SoftMagnetic.BaseData.B_myMax` is an unguarded divisor with no declared bound

| | |
|---|---|
| **Severity** | Medium — a material record every soft-magnetic flux tube reads |
| **Target** | MSL 4.1.0, `Modelica.Magnetic.FluxTubes.Material.SoftMagnetic.BaseData` |
| **Trigger** | `B_myMax = 0` |
| **Confirmed in** | Rumoca **and** OpenModelica 1.27.0-dev, on 2 models |
| **Found by** | ModelSan parameter sweep, cross-confirmed against OMC, 2026-09-13 |
| **Status** | Reported, not fixed |

## Summary

```modelica
// Material/SoftMagnetic/BaseData.mo:9
parameter SI.MagneticFluxDensity B_myMax=1
  "Flux density at maximum relative permeability";
```

No `min`. It is then divided by, in two places, with no guard:

```modelica
// BaseClasses/FixedShape.mo:31
B_N = abs(B/material.B_myMax);

// Material/SoftMagnetic/mu_rApprox.mo:26
B_N := abs(B/B_myMax);
```

At `B_myMax = 0` the normalised flux density is `inf` or `NaN`, and the
material characteristic that depends on it is meaningless.

## Confirmed on two models, in two independent tools

| Model | OMC baseline | OMC at 0 | Rumoca at 0 |
|---|---|---|---|
| `ModelicaTest.Magnetic.FluxTubes.Sources` | passes | **fails** | **fails** |
| `ModelicaTest.Magnetic.FluxTubes.Sensors` | passes | **fails** | **fails** |

```console
$ rumoca compile-bitcode sources.rbc --simulate --check \
      --param genericFluxTube.material.B_myMax=0
"algebraic projection did not converge at event boundary:
 worst scaled residual row=12 target=genericFluxTube.B value=-inf ratio=inf norm=inf"

# and the Sensors model reaches NaN rather than inf:
 worst scaled residual row=3 target=genericFluxTube.B value=NaN ratio=NaN norm=inf
```

## Why this one is clean

Unlike [BUG-010](BUG-010-inductor-documents-zero-it-cannot-honour.md), there is
no documentation claiming zero is supported, and unlike a vanishing coefficient
there is no re-indexing question: a division by zero is a division by zero. The
only reason the value is reachable is that the record declares no lower bound.

`B_myMax` is "flux density at maximum relative permeability" — a material
constant that is positive for every real material. Every entry in
`Material.SoftMagnetic` supplies a positive value; nothing but the declaration
would stop a user or a calibration loop supplying zero.

## Suggested fix

```modelica
parameter SI.MagneticFluxDensity B_myMax(min=Modelica.Constants.small)=1
  "Flux density at maximum relative permeability";
```

The same record's `mu_i` ("initial relative permeability") is also a divisor-adjacent
positive quantity declared without a bound, and is worth the same treatment.
