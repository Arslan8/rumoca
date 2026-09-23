# FINDING-00411: `oLine1.G[4].alpha` in `CompareLineTrunks`

| | |
|---|---|
| **Model** | `Modelica.Electrical.Analog.Examples.Lines.CompareLineTrunks` |
| **Reached as** | `oLine1.G[4].alpha` |
| **Declaration** | `Conductor.mo:6` |
| **Parameter** | `alpha` |
| **Claim** | a settable parameter reaches a denominator, nothing excludes zero |
| **Kind** | `divisor-reachable-zero` |
| **Severity** | medium |
| **Sanitizer** | `divisor` |
| **Fix site** | [SITE-0092](../../site-reports/SITE-0092-alpha-divisor-reachable-zero.md) |
| **Status** | **candidate — not execution-confirmed** |

## Evidence

| key | value |
|---|---|
| `parameter` | oLine1.G[4].alpha |
| `shape` | sum |
| `path` | oLine1.G[4].alpha |
| `declared_min` | None |
| `divisor_sites` | 1 |
| `note` | reaches a denominator and nothing excludes zero |


## What this is

One occurrence. The declaration at `Conductor.mo:6` is reached by this model through
`oLine1.G[4].alpha`, and the analysis reached it statically — no value has been observed
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
