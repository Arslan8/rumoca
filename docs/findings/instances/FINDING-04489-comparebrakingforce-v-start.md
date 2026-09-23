# FINDING-04489: `v_start` in `CompareBrakingForce`

| | |
|---|---|
| **Model** | `Modelica.Mechanics.Translational.Examples.CompareBrakingForce` |
| **Reached as** | `v_start` |
| **Declaration** | `CompareBrakingForce.mo:5` |
| **Parameter** | `v_start` |
| **Claim** | a settable parameter reaches a denominator, nothing excludes zero |
| **Kind** | `divisor-reachable-zero` |
| **Severity** | medium |
| **Sanitizer** | `divisor` |
| **Fix site** | [SITE-0387](../../site-reports/SITE-0387-v-start-divisor-reachable-zero.md) |
| **Status** | **candidate — not execution-confirmed** |

## Evidence

| key | value |
|---|---|
| `parameter` | v_start |
| `shape` | propagated |
| `path` | v_start -> v_nominal -> linearSpeedDependentForce.v_nominal |
| `declared_min` | None |
| `divisor_sites` | 3 |
| `note` | reaches a denominator and nothing excludes zero |


## What this is

One occurrence. The declaration at `CompareBrakingForce.mo:5` is reached by this model through
`v_start`, and the analysis reached it statically — no value has been observed
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
