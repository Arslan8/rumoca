# SITE-0090: `B_myMax` — a settable parameter reaches a denominator with nothing excluding zero

| | |
|---|---|
| **Declaration** | `BaseData.mo:9` |
| **Parameter** | `B_myMax` |
| **Reached as** | `G_mLeakRad.material.B_myMax`, `airGap.material.B_myMax`, `core.material.B_myMax`, `g_mAirPar.material.B_myMax` … |
| **Finding** | `divisor-reachable-zero` |
| **Severity** | high |
| **Sanitizer** | `divisor` |
| **Models reaching it** | 8 |
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
- **parameter**: `leftLeg.material.B_myMax`
- **shape**: `direct`
- **path**: `leftLeg.material.B_myMax`
- **declared_min**: `None`
- **divisor_sites**: `1`

## Models that reach it

| Model |
|---|
| `Modelica.Magnetic.FluxTubes.Examples.BasicExamples.QuadraticCoreAirgap` |
| `Modelica.Magnetic.FluxTubes.Examples.BasicExamples.SaturatedInductor` |
| `Modelica.Magnetic.FluxTubes.Examples.BasicExamples.ToroidalCoreAirgap` |
| `Modelica.Magnetic.FluxTubes.Examples.BasicExamples.ToroidalCoreQuadraticCrossSection` |
| `Modelica.Magnetic.FluxTubes.Examples.SolenoidActuator.Components.AdvancedSolenoid` |
| `Modelica.Magnetic.FluxTubes.Examples.SolenoidActuator.Components.SimpleSolenoid` |
| `ModelicaTest.Magnetic.FluxTubes.Sensors` |
| `ModelicaTest.Magnetic.FluxTubes.Sources` |

## Reproducing

```bash
python3 tools/sweep/static_eval.py --list tools/sweep/ALL.list \
  --out results.jsonl --keep-parameter-chains
```
