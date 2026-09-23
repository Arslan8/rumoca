# SITE-0047: `Ra` — nothing bounds this declaration at all

| | |
|---|---|
| **Declaration** | `DcPermanentMagnetData.mo:19` |
| **Parameter** | `Ra` |
| **Reached as** | `dceeData.Ra`, `dcpmData.Ra`, `dcpmData1.Ra`, `dcpmData2.Ra` … |
| **Finding** | `physical-domain-unenforced` |
| **Severity** | medium |
| **Sanitizer** | `physical` |
| **Models reaching it** | 13 |
| **Evidence** | static analysis of the canonical DAE |
| **Status** | **candidate — not execution-confirmed** |

## The claim

`dcpmData.Ra > 0`

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
| `Modelica.Electrical.PowerConverters.Examples.ACDC.RectifierBridge2Pulse.ThyristorBridge2Pulse_DC_Drive` |
| `Modelica.Electrical.PowerConverters.Examples.ACDC.RectifierBridge2mPulse.ThyristorBridge2mPulse_DC_Drive` |

## Reproducing

```bash
python3 tools/sweep/static_eval.py --list tools/sweep/ALL.list \
  --out results.jsonl --keep-parameter-chains
```
