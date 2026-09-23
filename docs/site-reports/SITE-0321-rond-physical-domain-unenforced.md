# SITE-0321: `RonD` — nothing bounds this declaration at all

| | |
|---|---|
| **Declaration** | `DcdcInverter.mo:19` |
| **Parameter** | `RonD` |
| **Reached as** | `RonD`, `dcdcInverter1.RonD`, `dcdcInverter2.RonD` |
| **Finding** | `physical-domain-unenforced` |
| **Severity** | medium |
| **Sanitizer** | `physical` |
| **Models reaching it** | 2 |
| **Evidence** | static analysis of the canonical DAE |
| **Status** | **candidate — not execution-confirmed** |

## The claim

`RonD > 0`

nothing bounds this declaration, so it permits values physics forbids

## What this evidence is, and is not

No value has been observed breaking this. The declaration simply does not exclude one, and nothing else in the model does either.

A confirmed occurrence of this class would live in
[`docs/verified bugs/`](../verified%20bugs/INSTANCES.md) with its own `BUG-` id
and a two-tool reproduction. This file has neither; it records a site the
analysis reached so the result is not lost between runs.

## How it was matched

- **quantity**: `Resistance`
- **unit**: `Ohm`
- **confidence**: `QUANTITY_AND_UNIT`

## Models that reach it

| Model |
|---|
| `Modelica.Electrical.Machines.Examples.ControlledDCDrives.Utilities.DcdcInverter` |
| `Modelica.Electrical.Machines.Examples.DCMachines.DCPM_Drive` |

## Reproducing

```bash
python3 tools/sweep/static_eval.py --list tools/sweep/ALL.list \
  --out results.jsonl --keep-parameter-chains
```
