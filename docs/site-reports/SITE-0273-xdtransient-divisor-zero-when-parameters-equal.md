# SITE-0273: `xdTransient` — a divisor vanishes when two parameters are equal

| | |
|---|---|
| **Declaration** | `SynchronousMachineData.mo:29` |
| **Parameter** | `xdTransient` |
| **Reached as** | `smeeData.xdTransient` |
| **Finding** | `divisor-zero-when-parameters-equal` |
| **Severity** | high |
| **Sanitizer** | `divisor` |
| **Models reaching it** | 2 |
| **Evidence** | static analysis of the canonical DAE |
| **Status** | **candidate — not execution-confirmed** |

## The claim

a divisor vanishes when two parameters are equal

zero when the two are equal; min/max cannot express a constraint between two parameters, so an assertion is the only mechanism

## What this evidence is, and is not

No `min` can express a constraint *between* two parameters, so an assertion is the only mechanism available.

A confirmed occurrence of this class would live in
[`docs/verified bugs/`](../verified%20bugs/INSTANCES.md) with its own `BUG-` id
and a two-tool reproduction. This file has neither; it records a site the
analysis reached so the result is not lost between runs.

## How it was matched
- **parameter**: `smeeData.xdTransient`
- **shape**: `relational`
- **path**: `smeeData.xdTransient`
- **declared_min**: `None`
- **divisor_sites**: `2`

## Models that reach it

| Model |
|---|
| `Modelica.Electrical.Machines.Examples.SynchronousMachines.SMEE_DOL` |
| `Modelica.Electrical.Machines.Examples.SynchronousMachines.SMEE_Generator` |

## Reproducing

```bash
python3 tools/sweep/static_eval.py --list tools/sweep/ALL.list \
  --out results.jsonl --keep-parameter-chains
```
