# SITE-0027: `c` — the declaration explicitly permits zero, via `min=0`

| | |
|---|---|
| **Declaration** | `Spring.mo:4` |
| **Parameter** | `c` |
| **Reached as** | `s1.c`, `s2.c`, `spring.c`, `spring.spring.c` … |
| **Finding** | `physical-bound-permits-zero` |
| **Severity** | low |
| **Sanitizer** | `physical` |
| **Models reaching it** | 18 |
| **Evidence** | static analysis of the canonical DAE |
| **Status** | **candidate — not execution-confirmed** |

## The claim

`spring1.spring.c > 0`

the declaration explicitly permits zero (`min=0`); whether zero is actually admissible needs execution, and for Mass/Inertia it is not

## What this evidence is, and is not

Weaker than an absent bound, because `min=0` is the author stating that zero is allowed rather than failing to consider it — and for `IdealCommutingSwitch.Goff` the ideal off-state conductance really is zero. It is still recorded because `Mass.m(min=0)` has exactly this shape and zero provably breaks it in two tools (BUG-002). Which of the two a given site is cannot be decided statically.

A confirmed occurrence of this class would live in
[`docs/verified bugs/`](../verified%20bugs/INSTANCES.md) with its own `BUG-` id
and a two-tool reproduction. This file has neither; it records a site the
analysis reached so the result is not lost between runs.

## How it was matched

- **quantity**: `TranslationalSpringConstant`
- **unit**: `N/m`
- **confidence**: `QUANTITY`

## Models that reach it

| Model |
|---|
| `Modelica.Mechanics.MultiBody.Examples.Elementary.FreeBody` |
| `Modelica.Mechanics.MultiBody.Examples.Elementary.HeatLosses` |
| `Modelica.Mechanics.MultiBody.Examples.Elementary.InitSpringConstant` |
| `Modelica.Mechanics.MultiBody.Examples.Elementary.PointGravityWithPointMasses` |
| `Modelica.Mechanics.MultiBody.Examples.Elementary.SpringWithMass` |
| `Modelica.Mechanics.MultiBody.Examples.Elementary.ThreeSprings` |
| `Modelica.Mechanics.Rotational.Examples.ElasticBearing` |
| `Modelica.Mechanics.Rotational.Examples.First` |
| `Modelica.Mechanics.Rotational.Examples.FirstGrounded` |
| `Modelica.Mechanics.Rotational.Examples.Utilities.Spring` |
| `Modelica.Mechanics.Translational.Examples.Damper` |
| `Modelica.Mechanics.Translational.Examples.GenerationOfFMUs` |
| `Modelica.Mechanics.Translational.Examples.InitialConditions` |
| `Modelica.Mechanics.Translational.Examples.Oscillator` |
| `Modelica.Mechanics.Translational.Examples.PreLoad` |
| `Modelica.Mechanics.Translational.Examples.Utilities.Spring` |
| `Modelica.Mechanics.Translational.Examples.WhyArrows` |
| `ModelicaTest.Translational.AllComponents` |

## Reproducing

```bash
python3 tools/sweep/static_eval.py --list tools/sweep/ALL.list \
  --out results.jsonl --keep-parameter-chains
```
