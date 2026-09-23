# FINDING-03816: `r_mAirPar.material.n` in `SaturatedInductor`

| | |
|---|---|
| **Model** | `Modelica.Magnetic.FluxTubes.Examples.BasicExamples.SaturatedInductor` |
| **Reached as** | `r_mAirPar.material.n` |
| **Declaration** | `BaseData.mo:13` |
| **Parameter** | `n` |
| **Claim** | a settable parameter reaches a denominator, nothing excludes zero |
| **Kind** | `divisor-reachable-zero` |
| **Severity** | medium |
| **Sanitizer** | `divisor` |
| **Fix site** | [SITE-0089](../../site-reports/SITE-0089-n-divisor-reachable-zero.md) |
| **Status** | **candidate — not execution-confirmed** |

## Evidence

| key | value |
|---|---|
| `parameter` | r_mAirPar.material.n |
| `shape` | sum |
| `path` | r_mAirPar.material.n |
| `declared_min` | None |
| `divisor_sites` | 1 |
| `note` | reaches a denominator and nothing excludes zero |


## What this is

One occurrence. The declaration at `BaseData.mo:13` is reached by this model through
`r_mAirPar.material.n`, and the analysis reached it statically — no value has been observed
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
