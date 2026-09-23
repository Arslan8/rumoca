# SITE-0121: `L2sigma` — nothing bounds this declaration at all

| | |
|---|---|
| **Declaration** | `TransformerData.mo:48` |
| **Parameter** | `L2sigma` |
| **Reached as** | `transformerData.L2sigma`, `transformerData1.L2sigma`, `transformerData2.L2sigma` |
| **Finding** | `physical-domain-unenforced` |
| **Severity** | medium |
| **Sanitizer** | `physical` |
| **Models reaching it** | 6 |
| **Evidence** | static analysis of the canonical DAE |
| **Status** | **candidate — not execution-confirmed** |

## The claim

`transformerData.L2sigma > 0`

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
| `Modelica.Electrical.Machines.Examples.InductionMachines.IMC_Transformer` |
| `Modelica.Electrical.Machines.Examples.Transformers.AsymmetricalLoad` |
| `Modelica.Electrical.Machines.Examples.Transformers.IMC_Transformer` |
| `Modelica.Electrical.Machines.Examples.Transformers.Rectifier12pulse` |
| `Modelica.Electrical.Machines.Examples.Transformers.Rectifier6pulse` |
| `Modelica.Electrical.Machines.Examples.Transformers.TransformerTestbench` |

## Reproducing

```bash
python3 tools/sweep/static_eval.py --list tools/sweep/ALL.list \
  --out results.jsonl --keep-parameter-chains
```
