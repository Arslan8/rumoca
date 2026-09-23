# SITE-0328: `area` — nothing bounds this declaration at all

| | |
|---|---|
| **Declaration** | `GenericFluxTube.mo:11` |
| **Parameter** | `area` |
| **Reached as** | `genericFluxTube.area`, `genericFluxTube1.area`, `genericFluxTube2.area`, `genericFluxTube3.area` |
| **Finding** | `physical-domain-unenforced` |
| **Severity** | medium |
| **Sanitizer** | `physical` |
| **Models reaching it** | 2 |
| **Evidence** | static analysis of the canonical DAE |
| **Status** | **candidate — not execution-confirmed** |

## The claim

`genericFluxTube.area > 0`

nothing bounds this declaration, so it permits values physics forbids

## What this evidence is, and is not

No value has been observed breaking this. The declaration simply does not exclude one, and nothing else in the model does either.

A confirmed occurrence of this class would live in
[`docs/verified bugs/`](../verified%20bugs/INSTANCES.md) with its own `BUG-` id
and a two-tool reproduction. This file has neither; it records a site the
analysis reached so the result is not lost between runs.

## How it was matched

- **quantity**: `Area`
- **unit**: `m2`
- **confidence**: `QUANTITY_AND_UNIT`

## Models that reach it

| Model |
|---|
| `ModelicaTest.Magnetic.FluxTubes.Sensors` |
| `ModelicaTest.Magnetic.FluxTubes.Sources` |

## Reproducing

```bash
python3 tools/sweep/static_eval.py --list tools/sweep/ALL.list \
  --out results.jsonl --keep-parameter-chains
```
