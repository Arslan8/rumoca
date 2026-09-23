# SITE-0241: `linear` — a settable parameter reaches a denominator with nothing excluding zero

| | |
|---|---|
| **Declaration** | `FrictionParameters.mo:14` |
| **Parameter** | `linear` |
| **Reached as** | `dcpmData2.frictionParameters.linear`, `smpmData.frictionParameters.linear` |
| **Finding** | `divisor-reachable-zero` |
| **Severity** | medium |
| **Sanitizer** | `divisor` |
| **Models reaching it** | 2 |
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
- **parameter**: `dcpmData2.frictionParameters.linear`
- **shape**: `propagated`
- **path**: `dcpmData2.frictionParameters.linear -> dcpmData2.frictionParameters.wLinear`
- **declared_min**: `None`
- **divisor_sites**: `1`

## Models that reach it

| Model |
|---|
| `Modelica.Electrical.Machines.Examples.DCMachines.DCPM_withLosses` |
| `ModelicaTest.Electrical.Machines.SMPM_VoltageSourceWithLosses` |

## Reproducing

```bash
python3 tools/sweep/static_eval.py --list tools/sweep/ALL.list \
  --out results.jsonl --keep-parameter-chains
```
