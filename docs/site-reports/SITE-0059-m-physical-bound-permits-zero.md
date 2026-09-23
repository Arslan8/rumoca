# SITE-0059: `m` — the declaration explicitly permits zero, via `min=0`

| | |
|---|---|
| **Declaration** | `TwoPort.mo:5` |
| **Parameter** | `m` |
| **Reached as** | `cooling.m`, `idealPump.m`, `innerPipe.m`, `innerPump.m` … |
| **Finding** | `physical-bound-permits-zero` |
| **Severity** | low |
| **Sanitizer** | `physical` |
| **Models reaching it** | 11 |
| **Evidence** | static analysis of the canonical DAE |
| **Status** | **candidate — not execution-confirmed** |

## The claim

`volumeFlow.m > 0`

the declaration explicitly permits zero (`min=0`); whether zero is actually admissible needs execution, and for Mass/Inertia it is not

## What this evidence is, and is not

Weaker than an absent bound, because `min=0` is the author stating that zero is allowed rather than failing to consider it — and for `IdealCommutingSwitch.Goff` the ideal off-state conductance really is zero. It is still recorded because `Mass.m(min=0)` has exactly this shape and zero provably breaks it in two tools (BUG-002). Which of the two a given site is cannot be decided statically.

A confirmed occurrence of this class would live in
[`docs/verified bugs/`](../verified%20bugs/INSTANCES.md) with its own `BUG-` id
and a two-tool reproduction. This file has neither; it records a site the
analysis reached so the result is not lost between runs.

## How it was matched

- **quantity**: `Mass`
- **unit**: `kg`
- **confidence**: `QUANTITY_AND_UNIT`

## Models that reach it

| Model |
|---|
| `Modelica.Electrical.Machines.Examples.DCMachines.DCPM_Cooling` |
| `Modelica.Thermal.FluidHeatFlow.Examples.IndirectCooling` |
| `Modelica.Thermal.FluidHeatFlow.Examples.OneMass` |
| `Modelica.Thermal.FluidHeatFlow.Examples.ParallelCooling` |
| `Modelica.Thermal.FluidHeatFlow.Examples.ParallelPumpDropOut` |
| `Modelica.Thermal.FluidHeatFlow.Examples.PumpAndValve` |
| `Modelica.Thermal.FluidHeatFlow.Examples.PumpDropOut` |
| `Modelica.Thermal.FluidHeatFlow.Examples.SimpleCooling` |
| `Modelica.Thermal.FluidHeatFlow.Examples.TwoMass` |
| `Modelica.Thermal.FluidHeatFlow.Examples.TwoTanks` |
| `Modelica.Thermal.FluidHeatFlow.Examples.WaterPump` |

## Reproducing

```bash
python3 tools/sweep/static_eval.py --list tools/sweep/ALL.list \
  --out results.jsonl --keep-parameter-chains
```
