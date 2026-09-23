# SITE-0075: `Goff` — nothing bounds this declaration at all

| | |
|---|---|
| **Declaration** | `IdealDiode.mo:6` |
| **Parameter** | `Goff` |
| **Reached as** | `diode1.Goff`, `diode2.Goff`, `diode3.Goff`, `diode4.Goff` … |
| **Finding** | `physical-domain-unenforced` |
| **Severity** | medium |
| **Sanitizer** | `physical` |
| **Models reaching it** | 10 |
| **Evidence** | static analysis of the canonical DAE |
| **Status** | **candidate — not execution-confirmed** |

## The claim

`rectifier.diode_p.Goff > 0`

nothing bounds this declaration, so it permits values physics forbids

## What this evidence is, and is not

No value has been observed breaking this. The declaration simply does not exclude one, and nothing else in the model does either.

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
| `Modelica.Electrical.Machines.Examples.InductionMachines.IMC_InverterDrive` |
| `Modelica.Electrical.Machines.Examples.SynchronousMachines.SMPM_Braking` |
| `Modelica.Electrical.Machines.Examples.Transformers.Rectifier12pulse` |
| `Modelica.Electrical.Machines.Examples.Transformers.Rectifier6pulse` |
| `Modelica.Electrical.Polyphase.Examples.Rectifier` |
| `Modelica.Electrical.PowerConverters.Examples.ACDC.RectifierBridge2mPulse.DiodeBridge2mPulse` |
| `Modelica.Electrical.PowerConverters.Examples.ACDC.RectifierBridge2mPulse.HalfControlledBridge2mPulse` |
| `Modelica.Electrical.PowerConverters.Examples.ACDC.RectifierCenterTap2mPulse.DiodeCenterTap2mPulse` |
| `Modelica.Electrical.PowerConverters.Examples.ACDC.RectifierCenterTapmPulse.DiodeCenterTapmPulse` |
| `ModelicaTest.Electrical.PowerConverters.HalfControlledBridge2mPulse` |

## Reproducing

```bash
python3 tools/sweep/static_eval.py --list tools/sweep/ALL.list \
  --out results.jsonl --keep-parameter-chains
```
