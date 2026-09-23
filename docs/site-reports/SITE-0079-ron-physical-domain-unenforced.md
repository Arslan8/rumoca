# SITE-0079: `Ron` — nothing bounds this declaration at all

| | |
|---|---|
| **Declaration** | `IdealClosingSwitch.mo:4` |
| **Parameter** | `Ron` |
| **Reached as** | `idealCloser.Ron`, `switch2.Ron`, `switch3.Ron`, `switchYD.idealCloser.Ron` |
| **Finding** | `physical-domain-unenforced` |
| **Severity** | medium |
| **Sanitizer** | `physical` |
| **Models reaching it** | 9 |
| **Evidence** | static analysis of the canonical DAE |
| **Status** | **candidate — not execution-confirmed** |

## The claim

`idealCloser.Ron > 0`

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
| `Modelica.Electrical.Machines.Examples.InductionMachines.IMC_DOL` |
| `Modelica.Electrical.Machines.Examples.InductionMachines.IMC_Transformer` |
| `Modelica.Electrical.Machines.Examples.InductionMachines.IMC_YD` |
| `Modelica.Electrical.Machines.Examples.InductionMachines.IMC_YDarc` |
| `Modelica.Electrical.Machines.Examples.InductionMachines.IMS_Start` |
| `Modelica.Electrical.Machines.Examples.SynchronousMachines.SMEE_DOL` |
| `Modelica.Electrical.Machines.Examples.SynchronousMachines.SMPM_ResistiveBraking` |
| `Modelica.Electrical.Machines.Examples.SynchronousMachines.SMR_DOL` |
| `Modelica.Electrical.Machines.Examples.Transformers.IMC_Transformer` |

## Reproducing

```bash
python3 tools/sweep/static_eval.py --list tools/sweep/ALL.list \
  --out results.jsonl --keep-parameter-chains
```
