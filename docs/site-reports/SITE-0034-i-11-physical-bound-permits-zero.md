# SITE-0034: `I_11` — the declaration explicitly permits zero, via `min=0`

| | |
|---|---|
| **Declaration** | `Body.mo:17` |
| **Parameter** | `I_11` |
| **Reached as** | `Body1.I_11`, `b0.body.I_11`, `b1.body.I_11`, `b2.body.I_11` … |
| **Finding** | `physical-bound-permits-zero` |
| **Severity** | low |
| **Sanitizer** | `physical` |
| **Models reaching it** | 15 |
| **Evidence** | static analysis of the canonical DAE |
| **Status** | **candidate — not execution-confirmed** |

## The claim

`boxBody1.body.I_11 > 0`

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
- **confidence**: `QUANTITY_AND_UNIT`

## Models that reach it

| Model |
|---|
| `Modelica.Mechanics.MultiBody.Examples.Elementary.DoublePendulum` |
| `Modelica.Mechanics.MultiBody.Examples.Elementary.DoublePendulumInitTip` |
| `Modelica.Mechanics.MultiBody.Examples.Elementary.FreeBody` |
| `Modelica.Mechanics.MultiBody.Examples.Elementary.HeatLosses` |
| `Modelica.Mechanics.MultiBody.Examples.Elementary.InitSpringConstant` |
| `Modelica.Mechanics.MultiBody.Examples.Elementary.Pendulum` |
| `Modelica.Mechanics.MultiBody.Examples.Elementary.PointGravity` |
| `Modelica.Mechanics.MultiBody.Examples.Elementary.PointGravityWithPointMasses2` |
| `Modelica.Mechanics.MultiBody.Examples.Elementary.SpringWithMass` |
| `Modelica.Mechanics.MultiBody.Examples.Elementary.ThreeSprings` |
| `Modelica.Mechanics.MultiBody.Examples.Elementary.UserDefinedGravityField` |
| `Modelica.Mechanics.MultiBody.Examples.Loops.PlanarFourbar` |
| `Modelica.Mechanics.MultiBody.Examples.Rotational3DEffects.BevelGear1D` |
| `Modelica.Mechanics.MultiBody.Examples.Systems.RobotR3.Utilities.MechanicalStructure` |
| `ModelicaTest.Rotational.TestMove` |

## Reproducing

```bash
python3 tools/sweep/static_eval.py --list tools/sweep/ALL.list \
  --out results.jsonl --keep-parameter-chains
```
