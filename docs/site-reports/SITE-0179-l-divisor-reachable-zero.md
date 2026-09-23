# SITE-0179: `L` — a settable parameter reaches a denominator with nothing excluding zero

| | |
|---|---|
| **Declaration** | `PMOS.mo:13` |
| **Parameter** | `L` |
| **Reached as** | `H_PMOS.L`, `Nand.TP1.L`, `Nand.TP2.L`, `TP1.L` … |
| **Finding** | `divisor-reachable-zero` |
| **Severity** | medium |
| **Sanitizer** | `divisor` |
| **Models reaching it** | 3 |
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
- **parameter**: `H_PMOS.L`
- **shape**: `sum`
- **path**: `H_PMOS.L`
- **declared_min**: `None`
- **divisor_sites**: `1`

## Models that reach it

| Model |
|---|
| `Modelica.Electrical.Analog.Examples.HeatingMOSInverter` |
| `Modelica.Electrical.Analog.Examples.NandGate` |
| `Modelica.Electrical.Analog.Examples.Utilities.Nand` |

## Reproducing

```bash
python3 tools/sweep/static_eval.py --list tools/sweep/ALL.list \
  --out results.jsonl --keep-parameter-chains
```
