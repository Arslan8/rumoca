# FINDING-05043: `genericFluxTube.material.B_myMax` in `Sources`

| | |
|---|---|
| **Model** | `ModelicaTest.Magnetic.FluxTubes.Sources` |
| **Reached as** | `genericFluxTube.material.B_myMax` |
| **Declaration** | `BaseData.mo:9` |
| **Parameter** | `B_myMax` |
| **Claim** | a settable parameter reaches a denominator, nothing excludes zero |
| **Kind** | `divisor-reachable-zero` |
| **Severity** | high |
| **Sanitizer** | `divisor` |
| **Fix site** | [SITE-0090](../../site-reports/SITE-0090-b-mymax-divisor-reachable-zero.md) |
| **Status** | **candidate — not execution-confirmed** |

## Evidence

| key | value |
|---|---|
| `parameter` | genericFluxTube.material.B_myMax |
| `shape` | direct |
| `path` | genericFluxTube.material.B_myMax |
| `declared_min` | None |
| `divisor_sites` | 1 |
| `note` | reaches a denominator and nothing excludes zero |


## What this is

One occurrence. The declaration at `BaseData.mo:9` is reached by this model through
`genericFluxTube.material.B_myMax`, and the analysis reached it statically — no value has been observed
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
