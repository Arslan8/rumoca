# SITE-0164: `k2` — a settable parameter reaches a denominator with nothing excluding zero

| | |
|---|---|
| **Declaration** | `Add.mo:7` |
| **Parameter** | `k2` |
| **Reached as** | `add.k2`, `addA.k2`, `k2` |
| **Finding** | `divisor-reachable-zero` |
| **Severity** | high |
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
- **parameter**: `add.k2`
- **shape**: `direct`
- **path**: `add.k2`
- **declared_min**: `0.0`
- **divisor_sites**: `2`

## Models that reach it

| Model |
|---|
| `Modelica.Electrical.Analog.Examples.OpAmps.Adder` |
| `Modelica.Electrical.Analog.Examples.OpAmps.ControlCircuit` |
| `Modelica.Electrical.Analog.Examples.OpAmps.OpAmpCircuits.Add` |

## Reproducing

```bash
python3 tools/sweep/static_eval.py --list tools/sweep/ALL.list \
  --out results.jsonl --keep-parameter-chains
```
