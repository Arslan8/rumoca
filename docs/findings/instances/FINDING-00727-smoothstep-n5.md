# FINDING-00727: `N5` in `SmoothStep`

| | |
|---|---|
| **Model** | `Modelica.Electrical.Analog.Examples.Lines.SmoothStep` |
| **Reached as** | `N5` |
| **Declaration** | `SmoothStep.mo:13` |
| **Parameter** | `N5` |
| **Claim** | a settable parameter reaches a denominator, nothing excludes zero |
| **Kind** | `divisor-reachable-zero` |
| **Severity** | medium |
| **Sanitizer** | `divisor` |
| **Fix site** | [SITE-0522](../../site-reports/SITE-0522-n5-divisor-reachable-zero.md) |
| **Status** | **candidate — not execution-confirmed** |

## Evidence

| key | value |
|---|---|
| `parameter` | N5 |
| `shape` | propagated |
| `path` | N5 -> oLine5.N |
| `declared_min` | None |
| `divisor_sites` | 10 |
| `note` | reaches a denominator and nothing excludes zero |


## What this is

One occurrence. The declaration at `SmoothStep.mo:13` is reached by this model through
`N5`, and the analysis reached it statically — no value has been observed
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
