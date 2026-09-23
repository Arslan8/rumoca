# FINDING-00795: `data.k` in `DifferentialAmplifier`

| | |
|---|---|
| **Model** | `Modelica.Electrical.Analog.Examples.OpAmps.DifferentialAmplifier` |
| **Reached as** | `data.k` |
| **Declaration** | `DifferentialAmplifierData.mo:16` |
| **Parameter** | `k` |
| **Claim** | a settable parameter reaches a denominator, nothing excludes zero |
| **Kind** | `divisor-reachable-zero` |
| **Severity** | high |
| **Sanitizer** | `divisor` |
| **Fix site** | [SITE-0418](../../site-reports/SITE-0418-k-divisor-reachable-zero.md) |
| **Status** | **candidate — not execution-confirmed** |

## Evidence

| key | value |
|---|---|
| `parameter` | data.k |
| `shape` | direct |
| `path` | data.k |
| `declared_min` | None |
| `divisor_sites` | 3 |
| `note` | reaches a denominator and nothing excludes zero |


## What this is

One occurrence. The declaration at `DifferentialAmplifierData.mo:16` is reached by this model through
`data.k`, and the analysis reached it statically — no value has been observed
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
