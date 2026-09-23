# SITE-0105: `C1` — a settable parameter reaches a denominator with nothing excluding zero

| | |
|---|---|
| **Declaration** | `TransformerData.mo:7` |
| **Parameter** | `C1` |
| **Reached as** | `transformerData.C1`, `transformerData1.C1`, `transformerData2.C1` |
| **Finding** | `divisor-reachable-zero` |
| **Severity** | high |
| **Sanitizer** | `divisor` |
| **Models reaching it** | 6 |
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
- **parameter**: `transformerData.C1`
- **shape**: `direct`
- **path**: `transformerData.C1`
- **declared_min**: `None`
- **divisor_sites**: `2`

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
