# SITE-0177: `NF` — a settable parameter reaches a denominator with nothing excluding zero

| | |
|---|---|
| **Declaration** | `NPN.mo:26` |
| **Parameter** | `NF` |
| **Reached as** | `T1.NF`, `T2.NF`, `Tr.NF`, `Transistor1.Tr.NF` … |
| **Finding** | `divisor-reachable-zero` |
| **Severity** | medium |
| **Sanitizer** | `divisor` |
| **Models reaching it** | 3 |
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
- **parameter**: `Transistor1.Tr.NF`
- **shape**: `product`
- **path**: `Transistor1.Tr.NF`
- **declared_min**: `None`
- **divisor_sites**: `1`

## Models that reach it

| Model |
|---|
| `Modelica.Electrical.Analog.Examples.DifferenceAmplifier` |
| `Modelica.Electrical.Analog.Examples.HeatingNPN_NORGate` |
| `Modelica.Electrical.Analog.Examples.Utilities.Transistor` |

## Reproducing

```bash
python3 tools/sweep/static_eval.py --list tools/sweep/ALL.list \
  --out results.jsonl --keep-parameter-chains
```
