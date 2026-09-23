# FINDING-01377: `wLoad2` in `DCPM_withLosses`

| | |
|---|---|
| **Model** | `Modelica.Electrical.Machines.Examples.DCMachines.DCPM_withLosses` |
| **Reached as** | `wLoad2` |
| **Declaration** | `DCPM_withLosses.mo:14` |
| **Parameter** | `wLoad2` |
| **Claim** | a settable parameter reaches a denominator, nothing excludes zero |
| **Kind** | `divisor-reachable-zero` |
| **Severity** | medium |
| **Sanitizer** | `divisor` |
| **Fix site** | [SITE-0406](../../site-reports/SITE-0406-wload2-divisor-reachable-zero.md) |
| **Status** | **candidate — not execution-confirmed** |

## Evidence

| key | value |
|---|---|
| `parameter` | wLoad2 |
| `shape` | propagated |
| `path` | wLoad2 -> loadTorque2.w_nominal |
| `declared_min` | None |
| `divisor_sites` | 2 |
| `note` | reaches a denominator and nothing excludes zero |


## What this is

One occurrence. The declaration at `DCPM_withLosses.mo:14` is reached by this model through
`wLoad2`, and the analysis reached it statically — no value has been observed
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
