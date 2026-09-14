# `SI.HeatCapacity` — 4 unbounded declarations

Domain: thermal

`Units.mo` declares `type HeatCapacity` with **no `min`**, so every
declaration below accepts a negative value.

## Exposed

| File | Line | Parameter | Declared modifiers |
|---|---|---|---|
| `Electrical/Machines/Examples/DCMachines/DCPM_Cooling.mo` | 13 | `Ca` | `—` |
| `Electrical/Machines/Examples/DCMachines/DCPM_Cooling.mo` | 15 | `Cc` | `—` |
| `Mechanics/MultiBody/Examples/Loops/Utilities/GasForce2.mo` | 12 | `k` | `—` |
| `Thermal/HeatTransfer/Components/HeatCapacitor.mo` | 3 | `C` | `—` |

## Guarded — these add their own bound

Same library, same quantity, bound written. This is why the exposed
cases read as omissions rather than as a deliberate choice.

| File | Line | Parameter | Declared modifiers |
|---|---|---|---|
| `Thermal/HeatTransfer/Examples/Utilities/DirectCapacity.mo` | 5 | `C` | `(min=0)` |
| `Thermal/HeatTransfer/Examples/Utilities/InverseCapacity.mo` | 5 | `C` | `(min=0)` |
