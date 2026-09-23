# SITE-0093: `T` — a settable parameter reaches a denominator with nothing excluding zero

| | |
|---|---|
| **Declaration** | `Continuous.mo:354` |
| **Parameter** | `T` |
| **Reached as** | `controllerFeedbackPart1.T`, `controllerFeedbackPart2.T`, `controllerFeedbackPart3.T`, `controllerFeedbackPart4.T` … |
| **Finding** | `divisor-reachable-zero` |
| **Severity** | high |
| **Sanitizer** | `divisor` |
| **Models reaching it** | 7 |
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
- **parameter**: `firstOrder.T`
- **shape**: `direct`
- **path**: `firstOrder.T`
- **declared_min**: `None`
- **divisor_sites**: `1`

## Models that reach it

| Model |
|---|
| `Modelica.Electrical.Analog.Examples.Lines.SmoothStep` |
| `ModelicaTest.Blocks.Continuous` |
| `ModelicaTest.Blocks.Continuous_InitialState` |
| `ModelicaTest.Blocks.Continuous_SteadyState` |
| `ModelicaTest.Blocks.LimPID` |
| `ModelicaTest.Blocks.LimitersHomotopy` |
| `ModelicaTest.Blocks.UnitDeduction` |

## Reproducing

```bash
python3 tools/sweep/static_eval.py --list tools/sweep/ALL.list \
  --out results.jsonl --keep-parameter-chains
```
