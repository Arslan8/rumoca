# FINDING-04869: `criticalDamping.normalized` in `Continuous_SteadyState`

| | |
|---|---|
| **Model** | `ModelicaTest.Blocks.Continuous_SteadyState` |
| **Reached as** | `criticalDamping.normalized` |
| **Declaration** | `Continuous.mo:1506` |
| **Parameter** | `normalized` |
| **Claim** | a settable parameter reaches a denominator, nothing excludes zero |
| **Kind** | `divisor-reachable-zero` |
| **Severity** | medium |
| **Sanitizer** | `divisor` |
| **Fix site** | [SITE-0144](../../site-reports/SITE-0144-normalized-divisor-reachable-zero.md) |
| **Status** | **candidate — not execution-confirmed** |

## Evidence

| key | value |
|---|---|
| `parameter` | criticalDamping.normalized |
| `shape` | propagated |
| `path` | criticalDamping.normalized -> criticalDamping.alpha |
| `declared_min` | None |
| `divisor_sites` | 2 |
| `note` | reaches a denominator and nothing excludes zero |


## What this is

One occurrence. The declaration at `Continuous.mo:1506` is reached by this model through
`criticalDamping.normalized`, and the analysis reached it statically — no value has been observed
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
