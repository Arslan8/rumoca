# FINDING-05179: `pid.unitTime` in `PIDMSL`

| | |
|---|---|
| **Model** | `PIDMSL` |
| **Reached as** | `pid.unitTime` |
| **Declaration** | `Continuous.mo:625` |
| **Parameter** | `unitTime` |
| **Claim** | a settable parameter reaches a denominator, nothing excludes zero |
| **Kind** | `divisor-reachable-zero` |
| **Severity** | high |
| **Sanitizer** | `divisor` |
| **Fix site** | [SITE-0126](../../site-reports/SITE-0126-unittime-divisor-reachable-zero.md) |
| **Status** | **candidate — not execution-confirmed** |

## Evidence

| key | value |
|---|---|
| `parameter` | pid.unitTime |
| `shape` | direct |
| `path` | pid.unitTime |
| `declared_min` | None |
| `divisor_sites` | 1 |
| `note` | reaches a denominator and nothing excludes zero |


## What this is

One occurrence. The declaration at `Continuous.mo:625` is reached by this model through
`pid.unitTime`, and the analysis reached it statically — no value has been observed
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
