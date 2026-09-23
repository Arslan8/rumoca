# FINDING-05038: `genericFluxTube3.material.c_b` in `Sources`

| | |
|---|---|
| **Model** | `ModelicaTest.Magnetic.FluxTubes.Sources` |
| **Reached as** | `genericFluxTube3.material.c_b` |
| **Declaration** | `BaseData.mo:12` |
| **Parameter** | `c_b` |
| **Claim** | a settable parameter reaches a denominator, nothing excludes zero |
| **Kind** | `divisor-reachable-zero` |
| **Severity** | medium |
| **Sanitizer** | `divisor` |
| **Fix site** | [SITE-0088](../../site-reports/SITE-0088-c-b-divisor-reachable-zero.md) |
| **Status** | **candidate — not execution-confirmed** |

## Evidence

| key | value |
|---|---|
| `parameter` | genericFluxTube3.material.c_b |
| `shape` | sum |
| `path` | genericFluxTube3.material.c_b |
| `declared_min` | None |
| `divisor_sites` | 1 |
| `note` | reaches a denominator and nothing excludes zero |


## What this is

One occurrence. The declaration at `BaseData.mo:12` is reached by this model through
`genericFluxTube3.material.c_b`, and the analysis reached it statically — no value has been observed
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
