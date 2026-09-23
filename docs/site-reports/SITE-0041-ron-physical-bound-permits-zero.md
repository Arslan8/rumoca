# SITE-0041: `Ron` — the declaration explicitly permits zero, via `min=0`

| | |
|---|---|
| **Declaration** | `IdealSwitch.mo:4` |
| **Parameter** | `Ron` |
| **Reached as** | `idealCloser.Ron`, `idealCloser.idealClosingSwitch[1].Ron`, `idealCloser.idealClosingSwitch[2].Ron`, `idealCloser.idealClosingSwitch[3].Ron` … |
| **Finding** | `physical-bound-permits-zero` |
| **Severity** | low |
| **Sanitizer** | `physical` |
| **Models reaching it** | 14 |
| **Evidence** | static analysis of the canonical DAE |
| **Status** | **candidate — not execution-confirmed** |

## The claim

`switch1.Ron > 0`

the declaration explicitly permits zero (`min=0`); whether zero is actually admissible needs execution, and for Mass/Inertia it is not

## What this evidence is, and is not

Weaker than an absent bound, because `min=0` is the author stating that zero is allowed rather than failing to consider it — and for `IdealCommutingSwitch.Goff` the ideal off-state conductance really is zero. It is still recorded because `Mass.m(min=0)` has exactly this shape and zero provably breaks it in two tools (BUG-002). Which of the two a given site is cannot be decided statically.

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
| `Modelica.Electrical.Analog.Examples.ControlledSwitchWithArc` |
| `Modelica.Electrical.Analog.Examples.SwitchWithArc` |
| `Modelica.Electrical.Machines.Examples.DCMachines.DCPM_Drive` |
| `Modelica.Electrical.Machines.Examples.InductionMachines.IMC_DOL` |
| `Modelica.Electrical.Machines.Examples.InductionMachines.IMC_Steinmetz` |
| `Modelica.Electrical.Machines.Examples.InductionMachines.IMC_Transformer` |
| `Modelica.Electrical.Machines.Examples.InductionMachines.IMC_YD` |
| `Modelica.Electrical.Machines.Examples.InductionMachines.IMC_YDarc` |
| `Modelica.Electrical.Machines.Examples.InductionMachines.IMS_Start` |
| `Modelica.Electrical.Machines.Examples.SynchronousMachines.SMEE_DOL` |
| `Modelica.Electrical.Machines.Examples.SynchronousMachines.SMPM_ResistiveBraking` |
| `Modelica.Electrical.Machines.Examples.SynchronousMachines.SMR_DOL` |
| `Modelica.Electrical.Machines.Examples.Transformers.IMC_Transformer` |
| `Modelica.Thermal.HeatTransfer.Examples.ControlledTemperature` |

## Reproducing

```bash
python3 tools/sweep/static_eval.py --list tools/sweep/ALL.list \
  --out results.jsonl --keep-parameter-chains
```
