# SITE-0130: `rising` — a settable parameter reaches a denominator with nothing excluding zero

| | |
|---|---|
| **Declaration** | `Sources.mo:894` |
| **Parameter** | `rising` |
| **Reached as** | `V1.signalSource.rising`, `V2.signalSource.rising`, `VIN1.signalSource.rising`, `VIN2.signalSource.rising` … |
| **Finding** | `divisor-reachable-zero` |
| **Severity** | high |
| **Sanitizer** | `divisor` |
| **Models reaching it** | 5 |
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
- **parameter**: `V1.signalSource.rising`
- **shape**: `direct`
- **path**: `V1.signalSource.rising`
- **declared_min**: `0.0`
- **divisor_sites**: `1`

## Models that reach it

| Model |
|---|
| `Modelica.Electrical.Analog.Examples.HeatingNPN_NORGate` |
| `Modelica.Electrical.Analog.Examples.HeatingPNP_NORGate` |
| `Modelica.Electrical.Analog.Examples.NandGate` |
| `Modelica.Electrical.Analog.Examples.SimpleTriacCircuit` |
| `Modelica.Thermal.FluidHeatFlow.Examples.WaterPump` |

## Reproducing

```bash
python3 tools/sweep/static_eval.py --list tools/sweep/ALL.list \
  --out results.jsonl --keep-parameter-chains
```
