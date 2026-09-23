# SITE-0054: `G` — nothing bounds this declaration at all

| | |
|---|---|
| **Declaration** | `ThermalConductor.mo:5` |
| **Parameter** | `G` |
| **Reached as** | `TC1.G`, `TC2.G`, `TC3.G`, `ThermalConductor1.G` … |
| **Finding** | `physical-domain-unenforced` |
| **Severity** | medium |
| **Sanitizer** | `physical` |
| **Models reaching it** | 13 |
| **Evidence** | static analysis of the canonical DAE |
| **Status** | **candidate — not execution-confirmed** |

## The claim

`TC1.G > 0`

nothing bounds this declaration, so it permits values physics forbids

## What this evidence is, and is not

No value has been observed breaking this. The declaration simply does not exclude one, and nothing else in the model does either.

A confirmed occurrence of this class would live in
[`docs/verified bugs/`](../verified%20bugs/INSTANCES.md) with its own `BUG-` id
and a two-tool reproduction. This file has neither; it records a site the
analysis reached so the result is not lost between runs.

## How it was matched

- **quantity**: `ThermalConductance`
- **unit**: `W/K`
- **confidence**: `QUANTITY_AND_UNIT`

## Models that reach it

| Model |
|---|
| `Modelica.Electrical.Analog.Examples.HeatingMOSInverter` |
| `Modelica.Electrical.Analog.Examples.HeatingNPN_NORGate` |
| `Modelica.Electrical.Analog.Examples.HeatingPNP_NORGate` |
| `Modelica.Electrical.Analog.Examples.HeatingRectifier` |
| `Modelica.Electrical.Analog.Examples.Resistor` |
| `Modelica.Electrical.Machines.Examples.DCMachines.DCPM_Cooling` |
| `Modelica.Thermal.FluidHeatFlow.Examples.IndirectCooling` |
| `Modelica.Thermal.FluidHeatFlow.Examples.OneMass` |
| `Modelica.Thermal.FluidHeatFlow.Examples.TwoMass` |
| `Modelica.Thermal.HeatTransfer.Examples.ControlledTemperature` |
| `Modelica.Thermal.HeatTransfer.Examples.GenerationOfFMUs` |
| `Modelica.Thermal.HeatTransfer.Examples.TwoMasses` |
| `Modelica.Thermal.HeatTransfer.Examples.Utilities.Conduction` |

## Reproducing

```bash
python3 tools/sweep/static_eval.py --list tools/sweep/ALL.list \
  --out results.jsonl --keep-parameter-chains
```
