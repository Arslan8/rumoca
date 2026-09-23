# SITE-0187: `RonDiode` — the declaration explicitly permits zero, via `min=0`

| | |
|---|---|
| **Declaration** | `DiodeBridge2mPulse.mo:6` |
| **Parameter** | `RonDiode` |
| **Reached as** | `diodeBridge2mPulse.RonDiode`, `rectifier.RonDiode` |
| **Finding** | `physical-bound-permits-zero` |
| **Severity** | low |
| **Sanitizer** | `physical` |
| **Models reaching it** | 3 |
| **Evidence** | static analysis of the canonical DAE |
| **Status** | **candidate — not execution-confirmed** |

## The claim

`rectifier.RonDiode > 0`

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
| `Modelica.Electrical.Machines.Examples.InductionMachines.IMC_InverterDrive` |
| `Modelica.Electrical.Machines.Examples.SynchronousMachines.SMPM_Braking` |
| `Modelica.Electrical.PowerConverters.Examples.ACDC.RectifierBridge2mPulse.DiodeBridge2mPulse` |

## Reproducing

```bash
python3 tools/sweep/static_eval.py --list tools/sweep/ALL.list \
  --out results.jsonl --keep-parameter-chains
```
