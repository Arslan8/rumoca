# FINDING-04900: `ramp2.duration` in `LimitersHomotopy`

| | |
|---|---|
| **Model** | `ModelicaTest.Blocks.LimitersHomotopy` |
| **Reached as** | `ramp2.duration` |
| **Declaration** | `Sources.mo:247` |
| **Parameter** | `duration` |
| **Claim** | a settable parameter reaches a denominator, nothing excludes zero |
| **Kind** | `divisor-reachable-zero` |
| **Severity** | high |
| **Sanitizer** | `divisor` |
| **Fix site** | [SITE-0006](../../site-reports/SITE-0006-duration-divisor-reachable-zero.md) |
| **Status** | **candidate — not execution-confirmed** |

## Evidence

| key | value |
|---|---|
| `parameter` | ramp2.duration |
| `shape` | direct |
| `path` | ramp2.duration |
| `declared_min` | 0.0 |
| `divisor_sites` | 1 |
| `note` | reaches a denominator and nothing excludes zero |


## What this is

One occurrence. The declaration at `Sources.mo:247` is reached by this model through
`ramp2.duration`, and the analysis reached it statically — no value has been observed
breaking anything here.

The fix is at the declaration, not in this model. Other models reaching the same
declaration are separate files; the fix site groups them.

| Tier | Evidence | Where |
|---|---|---|
| confirmed | fails in two independent tools | [`INSTANCES.md`](../../verified%20bugs/INSTANCES.md) |
| **candidate** | **static analysis reached it** | **here** |
| latent | a declaration permits it | [`declaration-sites/`](../../declaration-sites/README.md) |

## Reproducing

```bash
python3 tools/sweep/static_eval.py --list tools/sweep/ALL.list \
  --out results.jsonl --keep-parameter-chains
```
