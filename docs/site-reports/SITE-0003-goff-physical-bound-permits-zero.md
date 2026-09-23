# SITE-0003: `Goff` — the declaration explicitly permits zero, via `min=0`

| | |
|---|---|
| **Declaration** | `IdealSemiconductor.mo:6` |
| **Parameter** | `Goff` |
| **Reached as** | `Ideal.Goff`, `IdealDiode1.Goff`, `IdealDiode2.Goff`, `IdealDiode3.Goff` … |
| **Finding** | `physical-bound-permits-zero` |
| **Severity** | low |
| **Sanitizer** | `physical` |
| **Models reaching it** | 52 |
| **Evidence** | static analysis of the canonical DAE |
| **Status** | **candidate — not execution-confirmed** |

## The claim

`Ideal.Goff > 0`

the declaration explicitly permits zero (`min=0`); whether zero is actually admissible needs execution, and for Mass/Inertia it is not

## What this evidence is, and is not

Weaker than an absent bound, because `min=0` is the author stating that zero is allowed rather than failing to consider it — and for `IdealCommutingSwitch.Goff` the ideal off-state conductance really is zero. It is still recorded because `Mass.m(min=0)` has exactly this shape and zero provably breaks it in two tools (BUG-002). Which of the two a given site is cannot be decided statically.

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
| `Modelica.Electrical.Analog.Examples.CharacteristicIdealDiodes` |
| `Modelica.Electrical.Analog.Examples.DemoPowerSupplyWithBuffer` |
| `Modelica.Electrical.Analog.Examples.IdealTriacCircuit` |
| `Modelica.Electrical.Analog.Examples.Rectifier` |
| `Modelica.Electrical.Analog.Examples.SimpleTriacCircuit` |
| `Modelica.Electrical.Machines.Examples.InductionMachines.IMC_InverterDrive` |
| `Modelica.Electrical.Machines.Examples.SynchronousMachines.SMPM_Braking` |
| `Modelica.Electrical.Machines.Examples.Transformers.Rectifier12pulse` |
| `Modelica.Electrical.Machines.Examples.Transformers.Rectifier6pulse` |
| `Modelica.Electrical.Polyphase.Examples.Rectifier` |
| `Modelica.Electrical.PowerConverters.Examples.ACDC.Rectifier1Pulse.Thyristor1Pulse_R` |
| `Modelica.Electrical.PowerConverters.Examples.ACDC.Rectifier1Pulse.Thyristor1Pulse_R_Characteristic` |
| `Modelica.Electrical.PowerConverters.Examples.ACDC.RectifierBridge2Pulse.DiodeBridge2Pulse` |
| `Modelica.Electrical.PowerConverters.Examples.ACDC.RectifierBridge2Pulse.HalfControlledBridge2Pulse` |
| `Modelica.Electrical.PowerConverters.Examples.ACDC.RectifierBridge2Pulse.ThyristorBridge2Pulse_DC_Drive` |
| `Modelica.Electrical.PowerConverters.Examples.ACDC.RectifierBridge2Pulse.ThyristorBridge2Pulse_R` |
| `Modelica.Electrical.PowerConverters.Examples.ACDC.RectifierBridge2Pulse.ThyristorBridge2Pulse_RL` |
| `Modelica.Electrical.PowerConverters.Examples.ACDC.RectifierBridge2Pulse.ThyristorBridge2Pulse_RLV` |
| `Modelica.Electrical.PowerConverters.Examples.ACDC.RectifierBridge2Pulse.ThyristorBridge2Pulse_RLV_Characteristic` |
| `Modelica.Electrical.PowerConverters.Examples.ACDC.RectifierBridge2mPulse.DiodeBridge2mPulse` |

…and 32 more; the full list is in `docs/runs/data/`.

## Reproducing

```bash
python3 tools/sweep/static_eval.py --list tools/sweep/ALL.list \
  --out results.jsonl --keep-parameter-chains
```
