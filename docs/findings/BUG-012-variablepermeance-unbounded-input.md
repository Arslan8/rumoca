# BUG-012: `VariablePermeance` takes permeance as an unbounded input and uses it as a sole coefficient

| | |
|---|---|
| **Severity** | Medium — the bound is the model's only defense, and there is none |
| **Target** | MSL 4.1.0, `Modelica.Magnetic.FluxTubes.Basic.VariablePermeance` |
| **Trigger** | a driving signal that carries the permeance input to zero or below |
| **Confirmed in** | Rumoca **and** OpenModelica 1.27.0-dev |
| **Found by** | ModelSan parameter sweep, cross-confirmed against OMC, 2026-09-13 |
| **Status** | Reported, not fixed |

## Summary

```modelica
// Basic/VariablePermeance.mo
Modelica.Blocks.Interfaces.RealInput G_m(quantity="Permeance", unit="H")
  "Magnetic permeance";
equation
  G_m * V_m = Phi;
```

`G_m` is the sole coefficient of `V_m`. At `G_m = 0` the equation reads
`0 = Phi`, which no longer determines `V_m`. Negative permeance is not a
physical quantity at all.

`G_m` carries `quantity` and `unit` but **no `min`**. Because it is an *input*
rather than a parameter, the declared bound is the only thing that can reject a
bad value — there is no default to be sensible and no binding to inspect. A
connected source is free to drive it anywhere.

## Confirmed

`ModelicaTest.Magnetic.FluxTubes.VariableComponents` drives it with a ramp.
Moving the ramp's offset to `-1` carries `G_m` through zero and negative:

| | Baseline | `rampPermeance.offset = -1` |
|---|---|---|
| OpenModelica | passes | **fails** |
| Rumoca | passes | **fails** |

```console
$ rumoca compile-bitcode variablecomponents.rbc --simulate --check \
      --param rampPermeance.offset=-1
"algebraic projection did not converge at event boundary: worst scaled residual
 row=15 target=permeance.port_p.Phi value=-1.000000e0 ratio=1.000000e10"
```

The offset is an ordinary parameter of a standard `Blocks.Sources.Ramp`, with no
bound of its own, so nothing in the assembled model objects until the solver
does.

## Why an input deserves the bound more than a parameter does

A parameter is set once, and a reviewer can see the value. An input is whatever
the connected block produces at each instant, which depends on the rest of the
model and on time. `min` on an input is a runtime-checkable contract, and it is
the only one available here.

MSL does this correctly elsewhere — `Blocks.Interfaces.RealInput` instances
routinely carry `min`/`max` in components that need them.

## Suggested fix

```modelica
Modelica.Blocks.Interfaces.RealInput G_m(
  quantity="Permeance", unit="H", min=Modelica.Constants.small)
  "Magnetic permeance";
```

Or state the degenerate case structurally, as
`Magnetic.FundamentalWave.Components.EddyCurrent` does for its own conductance.
