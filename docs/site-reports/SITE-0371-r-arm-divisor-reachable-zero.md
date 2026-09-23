# SITE-0371: `r_arm` — a settable parameter reaches a denominator with nothing excluding zero

| | |
|---|---|
| **Declaration** | `AdvancedSolenoid.mo:34` |
| **Parameter** | `r_arm` |
| **Reached as** | `r_arm` |
| **Finding** | `divisor-reachable-zero` |
| **Severity** | medium |
| **Sanitizer** | `divisor` |
| **Models reaching it** | 1 |
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
- **parameter**: `r_arm`
- **shape**: `propagated`
- **path**: `r_arm -> g_mAirWork.r_o -> g_mAirWork.A`
- **declared_min**: `0.0`
- **divisor_sites**: `1`

## Models that reach it

| Model |
|---|
| `Modelica.Magnetic.FluxTubes.Examples.SolenoidActuator.Components.AdvancedSolenoid` |

## Reproducing

```bash
python3 tools/sweep/static_eval.py --list tools/sweep/ALL.list \
  --out results.jsonl --keep-parameter-chains
```
