# FINDING-04772: `openTank2.medium.cp` in `TwoTanks`

| | |
|---|---|
| **Model** | `Modelica.Thermal.FluidHeatFlow.Examples.TwoTanks` |
| **Reached as** | `openTank2.medium.cp` |
| **Declaration** | `Medium.mo:5` |
| **Parameter** | `cp` |
| **Claim** | a settable parameter reaches a denominator, nothing excludes zero |
| **Kind** | `divisor-reachable-zero` |
| **Severity** | high |
| **Sanitizer** | `divisor` |
| **Fix site** | [SITE-0056](../../site-reports/SITE-0056-cp-divisor-reachable-zero.md) |
| **Status** | **candidate — not execution-confirmed** |

## Evidence

| key | value |
|---|---|
| `parameter` | openTank2.medium.cp |
| `shape` | direct |
| `path` | openTank2.medium.cp |
| `declared_min` | None |
| `divisor_sites` | 2 |
| `note` | reaches a denominator and nothing excludes zero |


## What this is

One occurrence. The declaration at `Medium.mo:5` is reached by this model through
`openTank2.medium.cp`, and the analysis reached it statically — no value has been observed
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
