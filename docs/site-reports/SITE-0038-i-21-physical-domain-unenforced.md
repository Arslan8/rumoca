# SITE-0038: `I_21` — nothing bounds this declaration at all

| | |
|---|---|
| **Declaration** | `Body.mo:23` |
| **Parameter** | `I_21` |
| **Reached as** | `Body1.I_21`, `b0.body.I_21`, `b1.body.I_21`, `b2.body.I_21` … |
| **Finding** | `physical-domain-unenforced` |
| **Severity** | medium |
| **Sanitizer** | `physical` |
| **Models reaching it** | 15 |
| **Evidence** | static analysis of the canonical DAE |
| **Status** | **candidate — not execution-confirmed** |

## The claim

`boxBody1.body.I_21 > 0`

nothing bounds this declaration, so it permits values physics forbids

## What this evidence is, and is not

No value has been observed breaking this. The declaration simply does not exclude one, and nothing else in the model does either.

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
