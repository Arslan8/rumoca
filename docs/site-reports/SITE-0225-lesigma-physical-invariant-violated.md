# SITE-0225: `Lesigma` — a declared value violates a physical invariant

| | |
|---|---|
| **Declaration** | `DC_SeriesExcited.mo:86` |
| **Parameter** | `Lesigma` |
| **Reached as** | `dcse.Lesigma` |
| **Finding** | `physical-invariant-violated` |
| **Severity** | medium |
| **Sanitizer** | `physical` |
| **Models reaching it** | 3 |
| **Evidence** | static analysis of the canonical DAE |
| **Status** | **candidate — not execution-confirmed** |

## The claim

`dcse.Lesigma > 0`



## What this evidence is, and is not

The value is fixed by the declaration and is outside the physical domain. Stronger than the others: no execution is needed to see that the declared number is wrong.

A confirmed occurrence of this class would live in
[`docs/verified bugs/`](../verified%20bugs/INSTANCES.md) with its own `BUG-` id
and a two-tool reproduction. This file has neither; it records a site the
analysis reached so the result is not lost between runs.

## How it was matched

- **quantity**: `Inductance`
- **unit**: `H`
- **confidence**: `QUANTITY_AND_UNIT`

## Models that reach it

| Model |
|---|
| `Modelica.Electrical.Machines.Examples.DCMachines.DCSE_SinglePhase` |
| `Modelica.Electrical.Machines.Examples.DCMachines.DCSE_Start` |
| `Modelica.Electrical.Machines.Examples.DCMachines.DC_CompareCharacteristics` |

## Reproducing

```bash
python3 tools/sweep/static_eval.py --list tools/sweep/ALL.list \
  --out results.jsonl --keep-parameter-chains
```
