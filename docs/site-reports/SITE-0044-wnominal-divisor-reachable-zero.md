# SITE-0044: `wNominal` — a settable parameter reaches a denominator with nothing excluding zero

| | |
|---|---|
| **Declaration** | `DcPermanentMagnetData.mo:13` |
| **Parameter** | `wNominal` |
| **Reached as** | `dceeData.wNominal`, `dcpmData.wNominal`, `dcpmData1.wNominal`, `dcpmData2.wNominal` … |
| **Finding** | `divisor-reachable-zero` |
| **Severity** | medium |
| **Sanitizer** | `divisor` |
| **Models reaching it** | 13 |
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
- **parameter**: `dcpmData.wNominal`
- **shape**: `propagated`
- **path**: `dcpmData.wNominal -> dcpmData.frictionParameters.wRef`
- **declared_min**: `None`
- **divisor_sites**: `8`

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
