# SITE-0028: `defaultWidthFraction` — a settable parameter reaches a denominator with nothing excluding zero

| | |
|---|---|
| **Declaration** | `package.mo:128` |
| **Parameter** | `defaultWidthFraction` |
| **Reached as** | `world.defaultWidthFraction` |
| **Finding** | `divisor-reachable-zero` |
| **Severity** | high |
| **Sanitizer** | `divisor` |
| **Models reaching it** | 17 |
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
- **parameter**: `world.defaultWidthFraction`
- **shape**: `direct`
- **path**: `world.defaultWidthFraction`
- **declared_min**: `None`
- **divisor_sites**: `2`

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
| `Modelica.Mechanics.MultiBody.Examples.Elementary.PointGravityWithPointMasses` |
| `Modelica.Mechanics.MultiBody.Examples.Elementary.PointGravityWithPointMasses2` |
| `Modelica.Mechanics.MultiBody.Examples.Elementary.SpringWithMass` |
| `Modelica.Mechanics.MultiBody.Examples.Elementary.ThreeSprings` |
| `Modelica.Mechanics.MultiBody.Examples.Elementary.UserDefinedGravityField` |
| `Modelica.Mechanics.MultiBody.Examples.Loops.PlanarFourbar` |
| `Modelica.Mechanics.MultiBody.Examples.Rotational3DEffects.BevelGear1D` |
| `Modelica.Mechanics.MultiBody.Examples.Systems.RobotR3.Utilities.MechanicalStructure` |
| `ModelicaTest.MultiBody.WorldGroundVisualization` |
| `ModelicaTest.Rotational.TestMove` |

## Reproducing

```bash
python3 tools/sweep/static_eval.py --list tools/sweep/ALL.list \
  --out results.jsonl --keep-parameter-chains
```
