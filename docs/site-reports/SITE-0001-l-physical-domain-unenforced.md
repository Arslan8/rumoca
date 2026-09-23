# SITE-0001: `L` — nothing bounds this declaration at all

| | |
|---|---|
| **Declaration** | `Inductor.mo:4` |
| **Parameter** | `L` |
| **Reached as** | `Inductance1.L`, `Inductor1.L`, `Inductor2.L`, `Inductor3.L` … |
| **Finding** | `physical-domain-unenforced` |
| **Severity** | medium |
| **Sanitizer** | `physical` |
| **Models reaching it** | 75 |
| **Evidence** | static analysis of the canonical DAE |
| **Status** | **candidate — not execution-confirmed** |

## The claim

`L1.L > 0`

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
- **semantic_role**: `component.passive.inductance`
- **binding_source**: `component_type`
- **confidence**: `QUANTITY_AND_UNIT`
- **declaring_class**: `Modelica.Electrical.Analog.Basic.Inductor`
- **member**: `L`

## Models that reach it

| Model |
|---|
| `Modelica.Electrical.Analog.Examples.CauerLowPassAnalog` |
| `Modelica.Electrical.Analog.Examples.ChuaCircuit` |
| `Modelica.Electrical.Analog.Examples.CompareTransformers` |
| `Modelica.Electrical.Analog.Examples.ControlledSwitchWithArc` |
| `Modelica.Electrical.Analog.Examples.GenerationOfFMUs` |
| `Modelica.Electrical.Analog.Examples.Lines.CompareLineTrunks` |
| `Modelica.Electrical.Analog.Examples.Lines.SmoothStep` |
| `Modelica.Electrical.Analog.Examples.OpAmps.LCOscillator` |
| `Modelica.Electrical.Analog.Examples.ParallelResonance` |
| `Modelica.Electrical.Analog.Examples.Rectifier` |
| `Modelica.Electrical.Analog.Examples.ResonanceCircuits` |
| `Modelica.Electrical.Analog.Examples.SeriesResonance` |
| `Modelica.Electrical.Analog.Examples.ShowSaturatingInductor` |
| `Modelica.Electrical.Analog.Examples.SimpleTriacCircuit` |
| `Modelica.Electrical.Analog.Examples.SwitchWithArc` |
| `Modelica.Electrical.Analog.Examples.ThyristorBehaviourTest` |
| `Modelica.Electrical.Analog.Examples.Utilities.DirectInductor` |
| `Modelica.Electrical.Analog.Examples.Utilities.InverseInductor` |
| `Modelica.Electrical.Machines.Examples.InductionMachines.IMC_DCBraking` |
| `Modelica.Electrical.Machines.Examples.InductionMachines.IMC_DOL` |

…and 55 more; the full list is in `docs/runs/data/`.

## Reproducing

```bash
python3 tools/sweep/static_eval.py --list tools/sweep/ALL.list \
  --out results.jsonl --keep-parameter-chains
```
