# FINDING-01462: `dcseData.wNominal` in `DCSE_Start`

| | |
|---|---|
| **Model** | `Modelica.Electrical.Machines.Examples.DCMachines.DCSE_Start` |
| **Reached as** | `dcseData.wNominal` |
| **Declaration** | `DcPermanentMagnetData.mo:13` |
| **Parameter** | `wNominal` |
| **Claim** | a settable parameter reaches a denominator, nothing excludes zero |
| **Kind** | `divisor-reachable-zero` |
| **Severity** | medium |
| **Sanitizer** | `divisor` |
| **Fix site** | [SITE-0044](../../site-reports/SITE-0044-wnominal-divisor-reachable-zero.md) |
| **Status** | **candidate — not execution-confirmed** |

## Evidence

| key | value |
|---|---|
| `parameter` | dcseData.wNominal |
| `shape` | propagated |
| `path` | dcseData.wNominal -> dcse.wNominal |
| `declared_min` | None |
| `divisor_sites` | 8 |
| `note` | reaches a denominator and nothing excludes zero |


## What this is

One occurrence. The declaration at `DcPermanentMagnetData.mo:13` is reached by this model through
`dcseData.wNominal`, and the analysis reached it statically — no value has been observed
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
