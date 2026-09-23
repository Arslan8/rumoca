# SITE-0220: `RDS` — nothing bounds this declaration at all

| | |
|---|---|
| **Declaration** | `PMOS.mo:20` |
| **Parameter** | `RDS` |
| **Reached as** | `H_PMOS.RDS`, `Nand.TP1.RDS`, `Nand.TP2.RDS`, `TP1.RDS` … |
| **Finding** | `physical-domain-unenforced` |
| **Severity** | medium |
| **Sanitizer** | `physical` |
| **Models reaching it** | 3 |
| **Evidence** | static analysis of the canonical DAE |
| **Status** | **candidate — not execution-confirmed** |

## The claim

`H_PMOS.RDS > 0`

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
| `Modelica.Electrical.Analog.Examples.HeatingMOSInverter` |
| `Modelica.Electrical.Analog.Examples.NandGate` |
| `Modelica.Electrical.Analog.Examples.Utilities.Nand` |

## Reproducing

```bash
python3 tools/sweep/static_eval.py --list tools/sweep/ALL.list \
  --out results.jsonl --keep-parameter-chains
```
