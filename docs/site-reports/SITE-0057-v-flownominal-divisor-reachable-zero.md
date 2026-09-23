# SITE-0057: `V_flowNominal` — a settable parameter reaches a denominator with nothing excluding zero

| | |
|---|---|
| **Declaration** | `SimpleFriction.mo:9` |
| **Parameter** | `V_flowNominal` |
| **Reached as** | `cooling.V_flowNominal`, `innerPipe.V_flowNominal`, `outerPipe.V_flowNominal`, `pipe.V_flowNominal` … |
| **Finding** | `divisor-reachable-zero` |
| **Severity** | high |
| **Sanitizer** | `divisor` |
| **Models reaching it** | 11 |
| **Evidence** | static analysis of the canonical DAE |
| **Status** | **candidate — not execution-confirmed** |

## The claim

a settable parameter reaches a denominator with nothing excluding zero

reaches a denominator and nothing excludes zero

## What this evidence is, and is not

Static reachability only. Whether zero actually breaks this model depends on topology — a vanishing divisor in an unused branch is harmless — so execution is the oracle.

A confirmed occurrence of this class would live in
[`docs/verified bugs/`](../verified%20bugs/INSTANCES.md) with its own `BUG-` id
and a two-tool reproduction. This file has neither; it records a site the
analysis reached so the result is not lost between runs.

## How it was matched
- **parameter**: `cooling.V_flowNominal`
- **shape**: `direct`
- **path**: `cooling.V_flowNominal`
- **declared_min**: `None`
- **divisor_sites**: `1`

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
