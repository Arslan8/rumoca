# SITE-0852: `L` — nothing bounds this declaration at all

| | |
|---|---|
| **Declaration** | `ThyristorCenterTap2Pulse_RLV_Characteristic.mo:9` |
| **Parameter** | `L` |
| **Reached as** | `L` |
| **Finding** | `physical-domain-unenforced` |
| **Severity** | medium |
| **Sanitizer** | `physical` |
| **Models reaching it** | 1 |
| **Evidence** | static analysis of the canonical DAE |
| **Status** | **candidate — not execution-confirmed** |

## The claim

`L > 0`

nothing bounds this declaration, so it permits values physics forbids

## What this evidence is, and is not

No value has been observed breaking this. The declaration simply does not exclude one, and nothing else in the model does either.

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
| `Modelica.Electrical.PowerConverters.Examples.ACDC.RectifierCenterTap2Pulse.ThyristorCenterTap2Pulse_RLV_Characteristic` |

## Reproducing

```bash
python3 tools/sweep/static_eval.py --list tools/sweep/ALL.list \
  --out results.jsonl --keep-parameter-chains
```
