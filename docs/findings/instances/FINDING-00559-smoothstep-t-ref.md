# FINDING-00559: `oLine50.G[15].T_ref` in `SmoothStep`

| | |
|---|---|
| **Model** | `Modelica.Electrical.Analog.Examples.Lines.SmoothStep` |
| **Reached as** | `oLine50.G[15].T_ref` |
| **Declaration** | `Conductor.mo:5` |
| **Parameter** | `T_ref` |
| **Claim** | a settable parameter reaches a denominator, nothing excludes zero |
| **Kind** | `divisor-reachable-zero` |
| **Severity** | medium |
| **Sanitizer** | `divisor` |
| **Fix site** | [SITE-0091](../../site-reports/SITE-0091-t-ref-divisor-reachable-zero.md) |
| **Status** | **candidate — not execution-confirmed** |

## Evidence

| key | value |
|---|---|
| `parameter` | oLine50.G[15].T_ref |
| `shape` | sum |
| `path` | oLine50.G[15].T_ref |
| `declared_min` | 0.0 |
| `divisor_sites` | 1 |
| `note` | reaches a denominator and nothing excludes zero |


## What this is

One occurrence. The declaration at `Conductor.mo:5` is reached by this model through
`oLine50.G[15].T_ref`, and the analysis reached it statically — no value has been observed
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
