# SITE-0014: `C` — nothing bounds this declaration at all

| | |
|---|---|
| **Declaration** | `HeatCapacitor.mo:3` |
| **Parameter** | `C` |
| **Reached as** | `HeatCapacitor1.C`, `armature.C`, `capacitor3a.C`, `capacitor3b.C` … |
| **Finding** | `physical-domain-unenforced` |
| **Severity** | medium |
| **Sanitizer** | `physical` |
| **Models reaching it** | 22 |
| **Evidence** | static analysis of the canonical DAE |
| **Status** | **candidate — not execution-confirmed** |

## The claim

`HeatCapacitor1.C > 0`

nothing bounds this declaration, so it permits values physics forbids

## What this evidence is, and is not

No value has been observed breaking this. The declaration simply does not exclude one, and nothing else in the model does either.

A confirmed occurrence of this class would live in
[`docs/verified bugs/`](../verified%20bugs/INSTANCES.md) with its own `BUG-` id
and a two-tool reproduction. This file has neither; it records a site the
analysis reached so the result is not lost between runs.

## How it was matched

- **quantity**: `HeatCapacity`
- **unit**: `J/K`
- **confidence**: `QUANTITY_AND_UNIT`

## Models that reach it

| Model |
|---|
| `Modelica.Electrical.Analog.Examples.HeatingMOSInverter` |
| `Modelica.Electrical.Analog.Examples.HeatingNPN_NORGate` |
| `Modelica.Electrical.Analog.Examples.HeatingPNP_NORGate` |
| `Modelica.Electrical.Analog.Examples.HeatingRectifier` |
| `Modelica.Electrical.Machines.Examples.DCMachines.DCPM_Cooling` |
| `Modelica.Mechanics.Rotational.Examples.EddyCurrentBrake` |
| `Modelica.Mechanics.Translational.Examples.EddyCurrentBrake` |
| `Modelica.Thermal.FluidHeatFlow.Examples.IndirectCooling` |
| `Modelica.Thermal.FluidHeatFlow.Examples.OneMass` |
| `Modelica.Thermal.FluidHeatFlow.Examples.ParallelCooling` |
| `Modelica.Thermal.FluidHeatFlow.Examples.ParallelPumpDropOut` |
| `Modelica.Thermal.FluidHeatFlow.Examples.PumpAndValve` |
| `Modelica.Thermal.FluidHeatFlow.Examples.PumpDropOut` |
| `Modelica.Thermal.FluidHeatFlow.Examples.SimpleCooling` |
| `Modelica.Thermal.FluidHeatFlow.Examples.TwoMass` |
| `Modelica.Thermal.HeatTransfer.Examples.ControlledTemperature` |
| `Modelica.Thermal.HeatTransfer.Examples.GenerationOfFMUs` |
| `Modelica.Thermal.HeatTransfer.Examples.TwoMasses` |
| `Modelica.Thermal.HeatTransfer.Examples.Utilities.DirectCapacity` |
| `Modelica.Thermal.HeatTransfer.Examples.Utilities.InverseCapacity` |

…and 2 more; the full list is in `docs/runs/data/`.

## Reproducing

```bash
python3 tools/sweep/static_eval.py --list tools/sweep/ALL.list \
  --out results.jsonl --keep-parameter-chains
```
