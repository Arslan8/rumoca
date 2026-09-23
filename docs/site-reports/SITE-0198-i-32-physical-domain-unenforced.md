# SITE-0198: `I_32` — nothing bounds this declaration at all

| | |
|---|---|
| **Declaration** | `BodyShape.mo:34` |
| **Parameter** | `I_32` |
| **Reached as** | `b0.I_32`, `b1.I_32`, `b2.I_32`, `b3.I_32` … |
| **Finding** | `physical-domain-unenforced` |
| **Severity** | medium |
| **Sanitizer** | `physical` |
| **Models reaching it** | 3 |
| **Evidence** | static analysis of the canonical DAE |
| **Status** | **candidate — not execution-confirmed** |

## The claim

`body.I_32 > 0`

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
| `Modelica.Mechanics.MultiBody.Examples.Elementary.FreeBody` |
| `Modelica.Mechanics.MultiBody.Examples.Elementary.InitSpringConstant` |
| `Modelica.Mechanics.MultiBody.Examples.Systems.RobotR3.Utilities.MechanicalStructure` |

## Reproducing

```bash
python3 tools/sweep/static_eval.py --list tools/sweep/ALL.list \
  --out results.jsonl --keep-parameter-chains
```
