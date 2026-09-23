# SITE-0122: `d` — nothing bounds this declaration at all

| | |
|---|---|
| **Declaration** | `TranslatoryArmatureAndStopper.mo:11` |
| **Parameter** | `d` |
| **Reached as** | `armature.d`, `cActuator.armature.d`, `d`, `pmActuator.armature.d` |
| **Finding** | `physical-domain-unenforced` |
| **Severity** | medium |
| **Sanitizer** | `physical` |
| **Models reaching it** | 6 |
| **Evidence** | static analysis of the canonical DAE |
| **Status** | **candidate — not execution-confirmed** |

## The claim

`pmActuator.armature.d >= 0`

nothing bounds this declaration, so it permits values physics forbids

## What this evidence is, and is not

No value has been observed breaking this. The declaration simply does not exclude one, and nothing else in the model does either.

A confirmed occurrence of this class would live in
[`docs/verified bugs/`](../verified%20bugs/INSTANCES.md) with its own `BUG-` id
and a two-tool reproduction. This file has neither; it records a site the
analysis reached so the result is not lost between runs.

## How it was matched

- **quantity**: `TranslationalDampingConstant`
- **unit**: `N.s/m`
- **confidence**: `QUANTITY`

## Models that reach it

| Model |
|---|
| `Modelica.Magnetic.FluxTubes.Examples.MovingCoilActuator.ArmatureStroke` |
| `Modelica.Magnetic.FluxTubes.Examples.MovingCoilActuator.Components.ConstantActuator` |
| `Modelica.Magnetic.FluxTubes.Examples.MovingCoilActuator.Components.PermeanceActuator` |
| `Modelica.Magnetic.FluxTubes.Examples.SolenoidActuator.Components.AdvancedSolenoid` |
| `Modelica.Magnetic.FluxTubes.Examples.SolenoidActuator.Components.SimpleSolenoid` |
| `Modelica.Magnetic.FluxTubes.Examples.Utilities.TranslatoryArmatureAndStopper` |

## Reproducing

```bash
python3 tools/sweep/static_eval.py --list tools/sweep/ALL.list \
  --out results.jsonl --keep-parameter-chains
```
