# FINDING-05180: `tau_up` in `QuadrotorSIL`

| | |
|---|---|
| **Model** | `RigidBody.Examples.QuadrotorSIL` |
| **Reached as** | `tau_up` |
| **Declaration** | `QuadrotorSIL.mo:66` |
| **Parameter** | `tau_up` |
| **Claim** | a settable parameter reaches a denominator, nothing excludes zero |
| **Kind** | `divisor-reachable-zero` |
| **Severity** | medium |
| **Sanitizer** | `divisor` |
| **Fix site** | [SITE-0480](../../site-reports/SITE-0480-tau-up-divisor-reachable-zero.md) |
| **Status** | **candidate — not execution-confirmed** |

## Evidence

| key | value |
|---|---|
| `parameter` | tau_up |
| `shape` | propagated |
| `path` | tau_up -> motor[1].tau_up |
| `declared_min` | None |
| `divisor_sites` | 16 |
| `note` | reaches a denominator and nothing excludes zero |


## What this is

One occurrence. The declaration at `QuadrotorSIL.mo:66` is reached by this model through
`tau_up`, and the analysis reached it statically — no value has been observed
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
