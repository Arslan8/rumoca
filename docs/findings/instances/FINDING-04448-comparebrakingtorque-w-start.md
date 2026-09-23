# FINDING-04448: `w_start` in `CompareBrakingTorque`

| | |
|---|---|
| **Model** | `Modelica.Mechanics.Rotational.Examples.CompareBrakingTorque` |
| **Reached as** | `w_start` |
| **Declaration** | `CompareBrakingTorque.mo:5` |
| **Parameter** | `w_start` |
| **Claim** | a settable parameter reaches a denominator, nothing excludes zero |
| **Kind** | `divisor-reachable-zero` |
| **Severity** | medium |
| **Sanitizer** | `divisor` |
| **Fix site** | [SITE-0389](../../site-reports/SITE-0389-w-start-divisor-reachable-zero.md) |
| **Status** | **candidate — not execution-confirmed** |

## Evidence

| key | value |
|---|---|
| `parameter` | w_start |
| `shape` | propagated |
| `path` | w_start -> w_nominal -> linearSpeedDependentTorque.w_nominal |
| `declared_min` | None |
| `divisor_sites` | 3 |
| `note` | reaches a denominator and nothing excludes zero |


## What this is

One occurrence. The declaration at `CompareBrakingTorque.mo:5` is reached by this model through
`w_start`, and the analysis reached it statically — no value has been observed
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
