# FINDING-04862: `limPID.Td` in `Continuous_InitialState`

| | |
|---|---|
| **Model** | `ModelicaTest.Blocks.Continuous_InitialState` |
| **Reached as** | `limPID.Td` |
| **Declaration** | `Continuous.mo:773` |
| **Parameter** | `Td` |
| **Claim** | a settable parameter reaches a denominator, nothing excludes zero |
| **Kind** | `divisor-reachable-zero` |
| **Severity** | medium |
| **Sanitizer** | `divisor` |
| **Fix site** | [SITE-0128](../../site-reports/SITE-0128-td-divisor-reachable-zero.md) |
| **Status** | **candidate — not execution-confirmed** |

## Evidence

| key | value |
|---|---|
| `parameter` | limPID.Td |
| `shape` | propagated |
| `path` | limPID.Td -> limPID.D.T |
| `declared_min` | 0.0 |
| `divisor_sites` | 2 |
| `note` | reaches a denominator and nothing excludes zero |


## What this is

One occurrence. The declaration at `Continuous.mo:773` is reached by this model through
`limPID.Td`, and the analysis reached it statically — no value has been observed
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
