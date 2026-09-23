# SITE-0010: `GcRef` — a declared value violates a physical invariant

| | |
|---|---|
| **Declaration** | `CoreParameters.mo:18` |
| **Parameter** | `GcRef` |
| **Reached as** | `aimc.statorCore.coreParameters.GcRef`, `aimc.statorCoreParameters.GcRef`, `aimcData.statorCoreParameters.GcRef`, `aims.rotorCore.coreParameters.GcRef` … |
| **Finding** | `physical-invariant-violated` |
| **Severity** | medium |
| **Sanitizer** | `physical` |
| **Models reaching it** | 34 |
| **Evidence** | static analysis of the canonical DAE |
| **Status** | **candidate — not execution-confirmed** |

## The claim

`dcpmData.coreParameters.GcRef > 0`



## What this evidence is, and is not

The value is fixed by the declaration and is outside the physical domain. Stronger than the others: no execution is needed to see that the declared number is wrong.

A confirmed occurrence of this class would live in
[`docs/verified bugs/`](../verified%20bugs/INSTANCES.md) with its own `BUG-` id
and a two-tool reproduction. This file has neither; it records a site the
analysis reached so the result is not lost between runs.

## How it was matched

- **quantity**: `Conductance`
- **unit**: `S`
- **confidence**: `QUANTITY_AND_UNIT`

## Models that reach it

| Model |
|---|
| `Modelica.Electrical.Machines.Examples.DCMachines.DCEE_Start` |
| `Modelica.Electrical.Machines.Examples.DCMachines.DCPM_Cooling` |
| `Modelica.Electrical.Machines.Examples.DCMachines.DCPM_CurrentControlled` |
| `Modelica.Electrical.Machines.Examples.DCMachines.DCPM_Drive` |
| `Modelica.Electrical.Machines.Examples.DCMachines.DCPM_QuasiStatic` |
| `Modelica.Electrical.Machines.Examples.DCMachines.DCPM_Start` |
| `Modelica.Electrical.Machines.Examples.DCMachines.DCPM_Temperature` |
| `Modelica.Electrical.Machines.Examples.DCMachines.DCPM_withLosses` |
| `Modelica.Electrical.Machines.Examples.DCMachines.DCSE_SinglePhase` |
| `Modelica.Electrical.Machines.Examples.DCMachines.DCSE_Start` |
| `Modelica.Electrical.Machines.Examples.DCMachines.DC_CompareCharacteristics` |
| `Modelica.Electrical.Machines.Examples.InductionMachines.IMC_DCBraking` |
| `Modelica.Electrical.Machines.Examples.InductionMachines.IMC_DOL` |
| `Modelica.Electrical.Machines.Examples.InductionMachines.IMC_Initialize` |
| `Modelica.Electrical.Machines.Examples.InductionMachines.IMC_Inverter` |
| `Modelica.Electrical.Machines.Examples.InductionMachines.IMC_InverterDrive` |
| `Modelica.Electrical.Machines.Examples.InductionMachines.IMC_Steinmetz` |
| `Modelica.Electrical.Machines.Examples.InductionMachines.IMC_Transformer` |
| `Modelica.Electrical.Machines.Examples.InductionMachines.IMC_YD` |
| `Modelica.Electrical.Machines.Examples.InductionMachines.IMC_YDarc` |

…and 14 more; the full list is in `docs/runs/data/`.

## Reproducing

```bash
python3 tools/sweep/static_eval.py --list tools/sweep/ALL.list \
  --out results.jsonl --keep-parameter-chains
```
