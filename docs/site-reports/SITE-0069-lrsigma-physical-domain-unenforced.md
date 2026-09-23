# SITE-0069: `Lrsigma` — nothing bounds this declaration at all

| | |
|---|---|
| **Declaration** | `IM_SquirrelCage.mo:29` |
| **Parameter** | `Lrsigma` |
| **Reached as** | `aimc.Lrsigma`, `imc.Lrsigma` |
| **Finding** | `physical-domain-unenforced` |
| **Severity** | medium |
| **Sanitizer** | `physical` |
| **Models reaching it** | 10 |
| **Evidence** | static analysis of the canonical DAE |
| **Status** | **candidate — not execution-confirmed** |

## The claim

`imc.Lrsigma > 0`

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
| `Modelica.Electrical.Machines.Examples.InductionMachines.IMC_DCBraking` |
| `Modelica.Electrical.Machines.Examples.InductionMachines.IMC_DOL` |
| `Modelica.Electrical.Machines.Examples.InductionMachines.IMC_Initialize` |
| `Modelica.Electrical.Machines.Examples.InductionMachines.IMC_Inverter` |
| `Modelica.Electrical.Machines.Examples.InductionMachines.IMC_InverterDrive` |
| `Modelica.Electrical.Machines.Examples.InductionMachines.IMC_Steinmetz` |
| `Modelica.Electrical.Machines.Examples.InductionMachines.IMC_Transformer` |
| `Modelica.Electrical.Machines.Examples.InductionMachines.IMC_YD` |
| `Modelica.Electrical.Machines.Examples.InductionMachines.IMC_YDarc` |
| `Modelica.Electrical.Machines.Examples.Transformers.IMC_Transformer` |

## Reproducing

```bash
python3 tools/sweep/static_eval.py --list tools/sweep/ALL.list \
  --out results.jsonl --keep-parameter-chains
```
