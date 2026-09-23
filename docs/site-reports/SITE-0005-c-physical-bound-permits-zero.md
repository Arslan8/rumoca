# SITE-0005: `C` — the declaration explicitly permits zero, via `min=0`

| | |
|---|---|
| **Declaration** | `Capacitor.mo:4` |
| **Parameter** | `C` |
| **Reached as** | `C1.C`, `C2.C`, `C3.C`, `C4.C` … |
| **Finding** | `physical-bound-permits-zero` |
| **Severity** | low |
| **Sanitizer** | `physical` |
| **Models reaching it** | 49 |
| **Evidence** | static analysis of the canonical DAE |
| **Status** | **candidate — not execution-confirmed** |

## The claim

`C1.C > 0`

the declaration explicitly permits zero (`min=0`); whether zero is actually admissible needs execution, and for Mass/Inertia it is not

## What this evidence is, and is not

Weaker than an absent bound, because `min=0` is the author stating that zero is allowed rather than failing to consider it — and for `IdealCommutingSwitch.Goff` the ideal off-state conductance really is zero. It is still recorded because `Mass.m(min=0)` has exactly this shape and zero provably breaks it in two tools (BUG-002). Which of the two a given site is cannot be decided statically.

A confirmed occurrence of this class would live in
[`docs/verified bugs/`](../verified%20bugs/INSTANCES.md) with its own `BUG-` id
and a two-tool reproduction. This file has neither; it records a site the
analysis reached so the result is not lost between runs.

## How it was matched

- **quantity**: `Capacitance`
- **unit**: `F`
- **semantic_role**: `component.passive.capacitance`
- **binding_source**: `component_type`
- **confidence**: `QUANTITY_AND_UNIT`
- **declaring_class**: `Modelica.Electrical.Analog.Basic.Capacitor`
- **member**: `C`

## Models that reach it

| Model |
|---|
| `Modelica.Electrical.Analog.Examples.CauerLowPassAnalog` |
| `Modelica.Electrical.Analog.Examples.CauerLowPassOPV` |
| `Modelica.Electrical.Analog.Examples.CauerLowPassSC` |
| `Modelica.Electrical.Analog.Examples.ChuaCircuit` |
| `Modelica.Electrical.Analog.Examples.DemoPowerSupplyWithBuffer` |
| `Modelica.Electrical.Analog.Examples.DifferenceAmplifier` |
| `Modelica.Electrical.Analog.Examples.GenerationOfFMUs` |
| `Modelica.Electrical.Analog.Examples.HeatingMOSInverter` |
| `Modelica.Electrical.Analog.Examples.HeatingNPN_NORGate` |
| `Modelica.Electrical.Analog.Examples.HeatingPNP_NORGate` |
| `Modelica.Electrical.Analog.Examples.HeatingRectifier` |
| `Modelica.Electrical.Analog.Examples.IdealTriacCircuit` |
| `Modelica.Electrical.Analog.Examples.Lines.CompareLineTrunks` |
| `Modelica.Electrical.Analog.Examples.Lines.SmoothStep` |
| `Modelica.Electrical.Analog.Examples.NandGate` |
| `Modelica.Electrical.Analog.Examples.OpAmps.ControlCircuit` |
| `Modelica.Electrical.Analog.Examples.OpAmps.Differentiator` |
| `Modelica.Electrical.Analog.Examples.OpAmps.HighPass` |
| `Modelica.Electrical.Analog.Examples.OpAmps.Integrator` |
| `Modelica.Electrical.Analog.Examples.OpAmps.LCOscillator` |

…and 29 more; the full list is in `docs/runs/data/`.

## Reproducing

```bash
python3 tools/sweep/static_eval.py --list tools/sweep/ALL.list \
  --out results.jsonl --keep-parameter-chains
```
