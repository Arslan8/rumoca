# FINDING-00262: `H_NMOS.dL` in `HeatingMOSInverter`

| | |
|---|---|
| **Model** | `Modelica.Electrical.Analog.Examples.HeatingMOSInverter` |
| **Reached as** | `H_NMOS.dL` |
| **Declaration** | `NMOS.mo:19` |
| **Parameter** | `dL` |
| **Claim** | a settable parameter reaches a denominator, nothing excludes zero |
| **Kind** | `divisor-reachable-zero` |
| **Severity** | medium |
| **Sanitizer** | `divisor` |
| **Fix site** | [SITE-0174](../../site-reports/SITE-0174-dl-divisor-reachable-zero.md) |
| **Status** | **candidate — not execution-confirmed** |

## Evidence

| key | value |
|---|---|
| `parameter` | H_NMOS.dL |
| `shape` | sum |
| `path` | H_NMOS.dL |
| `declared_min` | None |
| `divisor_sites` | 1 |
| `note` | reaches a denominator and nothing excludes zero |


## What this is

One occurrence. The declaration at `NMOS.mo:19` is reached by this model through
`H_NMOS.dL`, and the analysis reached it statically — no value has been observed
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
