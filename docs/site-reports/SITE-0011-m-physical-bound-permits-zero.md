# SITE-0011: `m` — the declaration explicitly permits zero, via `min=0`

| | |
|---|---|
| **Declaration** | `Mass.mo:3` |
| **Parameter** | `m` |
| **Reached as** | `armature.mass.m`, `cActuator.armature.mass.m`, `cLoad.m`, `directMass.mass.m` … |
| **Finding** | `physical-bound-permits-zero` |
| **Severity** | low |
| **Sanitizer** | `physical` |
| **Models reaching it** | 26 |
| **Evidence** | static analysis of the canonical DAE |
| **Status** | **candidate — not execution-confirmed** |

## The claim

`pmActuator.armature.mass.m > 0`

the declaration explicitly permits zero (`min=0`); whether zero is actually admissible needs execution, and for Mass/Inertia it is not

## What this evidence is, and is not

Weaker than an absent bound, because `min=0` is the author stating that zero is allowed rather than failing to consider it — and for `IdealCommutingSwitch.Goff` the ideal off-state conductance really is zero. It is still recorded because `Mass.m(min=0)` has exactly this shape and zero provably breaks it in two tools (BUG-002). Which of the two a given site is cannot be decided statically.

A confirmed occurrence of this class would live in
[`docs/verified bugs/`](../verified%20bugs/INSTANCES.md) with its own `BUG-` id
and a two-tool reproduction. This file has neither; it records a site the
analysis reached so the result is not lost between runs.

## How it was matched

- **quantity**: `Mass`
- **unit**: `kg`
- **semantic_role**: `component.translational.mass`
- **binding_source**: `component_type`
- **confidence**: `QUANTITY_AND_UNIT`
- **declaring_class**: `Modelica.Mechanics.Translational.Components.Mass`
- **member**: `m`

## Models that reach it

| Model |
|---|
| `Modelica.Magnetic.FluxTubes.Examples.MovingCoilActuator.ArmatureStroke` |
| `Modelica.Magnetic.FluxTubes.Examples.MovingCoilActuator.Components.ConstantActuator` |
| `Modelica.Magnetic.FluxTubes.Examples.MovingCoilActuator.Components.PermeanceActuator` |
| `Modelica.Magnetic.FluxTubes.Examples.SolenoidActuator.Components.AdvancedSolenoid` |
| `Modelica.Magnetic.FluxTubes.Examples.SolenoidActuator.Components.SimpleSolenoid` |
| `Modelica.Magnetic.FluxTubes.Examples.Utilities.TranslatoryArmatureAndStopper` |
| `Modelica.Mechanics.Rotational.Examples.RollingWheel` |
| `Modelica.Mechanics.Translational.Examples.Accelerate` |
| `Modelica.Mechanics.Translational.Examples.CompareBrakingForce` |
| `Modelica.Mechanics.Translational.Examples.Damper` |
| `Modelica.Mechanics.Translational.Examples.EddyCurrentBrake` |
| `Modelica.Mechanics.Translational.Examples.ElastoGap` |
| `Modelica.Mechanics.Translational.Examples.GenerationOfFMUs` |
| `Modelica.Mechanics.Translational.Examples.InitialConditions` |
| `Modelica.Mechanics.Translational.Examples.Oscillator` |
| `Modelica.Mechanics.Translational.Examples.PreLoad` |
| `Modelica.Mechanics.Translational.Examples.Sensors` |
| `Modelica.Mechanics.Translational.Examples.SignConvention` |
| `Modelica.Mechanics.Translational.Examples.Utilities.DirectMass` |
| `Modelica.Mechanics.Translational.Examples.Utilities.InverseMass` |

…and 6 more; the full list is in `docs/runs/data/`.

## Reproducing

```bash
python3 tools/sweep/static_eval.py --list tools/sweep/ALL.list \
  --out results.jsonl --keep-parameter-chains
```
