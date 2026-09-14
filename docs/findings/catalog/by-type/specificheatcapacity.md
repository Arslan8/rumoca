# `SI.SpecificHeatCapacity` — 4 unbounded declarations

Domain: thermal

`Units.mo` declares `type SpecificHeatCapacity` with **no `min`**, so every
declaration below accepts a negative value.

## Exposed

| File | Line | Parameter | Declared modifiers |
|---|---|---|---|
| `Fluid/Examples/HeatExchanger.mo` | 146 | `c_wall` | `—` |
| `Fluid/Examples/HeatExchanger.mo` | 410 | `c_wall` | `—` |
| `Thermal/FluidHeatFlow/Media/Medium.mo` | 5 | `cp` | `—` |
| `Thermal/FluidHeatFlow/Media/Medium.mo` | 7 | `cv` | `—` |

## Guarded — these add their own bound

Same library, same quantity, bound written. This is why the exposed
cases read as omissions rather than as a deliberate choice.

| File | Line | Parameter | Declared modifiers |
|---|---|---|---|
| `Fluid/Dissipation.mo` | 12602 | `R_s` | `(min=1)` |
