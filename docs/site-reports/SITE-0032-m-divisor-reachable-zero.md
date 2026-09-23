# SITE-0032: `m` — a settable parameter reaches a denominator with nothing excluding zero

| | |
|---|---|
| **Declaration** | `CoreParameters.mo:4` |
| **Parameter** | `m` |
| **Reached as** | `dceeData.coreParameters.m`, `dcpmData.coreParameters.m`, `dcpmData1.coreParameters.m`, `dcpmData2.coreParameters.m` … |
| **Finding** | `divisor-reachable-zero` |
| **Severity** | high |
| **Sanitizer** | `divisor` |
| **Models reaching it** | 15 |
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
- **parameter**: `dcpmData.coreParameters.m`
- **shape**: `direct`
- **path**: `dcpmData.coreParameters.m`
- **declared_min**: `None`
- **divisor_sites**: `2`

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
| `Modelica.Electrical.Machines.Examples.SynchronousMachines.SMEE_DOL` |
| `Modelica.Electrical.Machines.Examples.SynchronousMachines.SMEE_Generator` |
| `Modelica.Electrical.PowerConverters.Examples.ACDC.RectifierBridge2Pulse.ThyristorBridge2Pulse_DC_Drive` |
| `Modelica.Electrical.PowerConverters.Examples.ACDC.RectifierBridge2mPulse.ThyristorBridge2mPulse_DC_Drive` |

## Reproducing

```bash
python3 tools/sweep/static_eval.py --list tools/sweep/ALL.list \
  --out results.jsonl --keep-parameter-chains
```
