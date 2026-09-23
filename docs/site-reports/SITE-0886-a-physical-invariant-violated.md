# SITE-0886: `A` — a declared value violates a physical invariant

| | |
|---|---|
| **Declaration** | `Vehicle.mo:7` |
| **Parameter** | `A` |
| **Reached as** | `vehicleInclination.A`, `vehicleInclinationInConst.A`, `vehicleInclinationInVar.A`, `vehicleRoll.A` … |
| **Finding** | `physical-invariant-violated` |
| **Severity** | medium |
| **Sanitizer** | `physical` |
| **Models reaching it** | 1 |
| **Evidence** | static analysis of the canonical DAE |
| **Status** | **candidate — not execution-confirmed** |

## The claim

`vehicleRoll.A > 0`



## What this evidence is, and is not

The value is fixed by the declaration and is outside the physical domain. Stronger than the others: no execution is needed to see that the declared number is wrong.

A confirmed occurrence of this class would live in
[`docs/verified bugs/`](../verified%20bugs/INSTANCES.md) with its own `BUG-` id
and a two-tool reproduction. This file has neither; it records a site the
analysis reached so the result is not lost between runs.

## How it was matched

- **quantity**: `Area`
- **unit**: `m2`
- **confidence**: `QUANTITY_AND_UNIT`

## Models that reach it

| Model |
|---|
| `ModelicaTest.Translational.Vehicles` |

## Reproducing

```bash
python3 tools/sweep/static_eval.py --list tools/sweep/ALL.list \
  --out results.jsonl --keep-parameter-chains
```
