# FINDING-05181: `tau_down` in `QuadrotorSIL`

| | |
|---|---|
| **Model** | `RigidBody.Examples.QuadrotorSIL` |
| **Reached as** | `tau_down` |
| **Declaration** | `QuadrotorSIL.mo:67` |
| **Parameter** | `tau_down` |
| **Claim** | a settable parameter reaches a denominator, nothing excludes zero |
| **Kind** | `divisor-reachable-zero` |
| **Severity** | medium |
| **Sanitizer** | `divisor` |
| **Fix site** | [SITE-0481](../../site-reports/SITE-0481-tau-down-divisor-reachable-zero.md) |
| **Status** | **candidate — not execution-confirmed** |

## Evidence

| key | value |
|---|---|
| `parameter` | tau_down |
| `shape` | propagated |
| `path` | tau_down -> motor[1].tau_down |
| `declared_min` | None |
| `divisor_sites` | 16 |
| `note` | reaches a denominator and nothing excludes zero |


## What this is

One occurrence. The declaration at `QuadrotorSIL.mo:67` is reached by this model through
`tau_down`, and the analysis reached it statically — no value has been observed
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
