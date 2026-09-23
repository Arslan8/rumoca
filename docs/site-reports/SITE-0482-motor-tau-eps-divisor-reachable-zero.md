# SITE-0482: `motor_tau_eps` — a settable parameter reaches a denominator with nothing excluding zero

| | |
|---|---|
| **Declaration** | `QuadrotorSIL.mo:68` |
| **Parameter** | `motor_tau_eps` |
| **Reached as** | `motor_tau_eps` |
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
- **parameter**: `motor_tau_eps`
- **shape**: `propagated`
- **path**: `motor_tau_eps -> motor[1].tau_eps`
- **declared_min**: `None`
- **divisor_sites**: `4`

## Models that reach it

| Model |
|---|
| `RigidBody.Examples.QuadrotorSIL` |

## Reproducing

```bash
python3 tools/sweep/static_eval.py --list tools/sweep/ALL.list \
  --out results.jsonl --keep-parameter-chains
```
