# SITE-0004: `J` — the declaration explicitly permits zero, via `min=0`

| | |
|---|---|
| **Declaration** | `Inertia.mo:4` |
| **Parameter** | `J` |
| **Reached as** | `aimc.inertiaRotor.J`, `aimc.inertiaStator.J`, `aims.inertiaRotor.J`, `aims.inertiaStator.J` … |
| **Finding** | `physical-bound-permits-zero` |
| **Severity** | low |
| **Sanitizer** | `physical` |
| **Models reaching it** | 52 |
| **Evidence** | static analysis of the canonical DAE |
| **Status** | **candidate — not execution-confirmed** |

## The claim

`load.J > 0`

the declaration explicitly permits zero (`min=0`); whether zero is actually admissible needs execution, and for Mass/Inertia it is not

## What this evidence is, and is not

Weaker than an absent bound, because `min=0` is the author stating that zero is allowed rather than failing to consider it — and for `IdealCommutingSwitch.Goff` the ideal off-state conductance really is zero. It is still recorded because `Mass.m(min=0)` has exactly this shape and zero provably breaks it in two tools (BUG-002). Which of the two a given site is cannot be decided statically.

A confirmed occurrence of this class would live in
[`docs/verified bugs/`](../verified%20bugs/INSTANCES.md) with its own `BUG-` id
and a two-tool reproduction. This file has neither; it records a site the
analysis reached so the result is not lost between runs.

## How it was matched

- **quantity**: `MomentOfInertia`
- **unit**: `kg.m2`
- **semantic_role**: `component.rotational.inertia`
- **binding_source**: `component_type`
- **confidence**: `QUANTITY_AND_UNIT`
- **declaring_class**: `Modelica.Mechanics.Rotational.Components.Inertia`
- **member**: `J`

## Models that reach it

| Model |
|---|
| `Modelica.Clocked.Examples.SimpleControlledDrive.ClockedWithDiscreteController` |
| `Modelica.Clocked.Examples.SimpleControlledDrive.ClockedWithDiscreteTextbookController` |
| `Modelica.Clocked.Examples.SimpleControlledDrive.Continuous` |
| `Modelica.Clocked.Examples.SimpleControlledDrive.ExactlyClockedWithDiscreteController` |
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

…and 32 more; the full list is in `docs/runs/data/`.

## Reproducing

```bash
python3 tools/sweep/static_eval.py --list tools/sweep/ALL.list \
  --out results.jsonl --keep-parameter-chains
```
