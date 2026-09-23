# SITE-0522: `N5` — a settable parameter reaches a denominator with nothing excluding zero

| | |
|---|---|
| **Declaration** | `SmoothStep.mo:13` |
| **Parameter** | `N5` |
| **Reached as** | `N5` |
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
- **parameter**: `N5`
- **shape**: `propagated`
- **path**: `N5 -> oLine5.N`
- **declared_min**: `None`
- **divisor_sites**: `10`

## Models that reach it

| Model |
|---|
| `Modelica.Electrical.Analog.Examples.Lines.SmoothStep` |

## Reproducing

```bash
python3 tools/sweep/static_eval.py --list tools/sweep/ALL.list \
  --out results.jsonl --keep-parameter-chains
```
