# FINDING-04800: `oneWayValve.medium.rho` in `WaterPump`

| | |
|---|---|
| **Model** | `Modelica.Thermal.FluidHeatFlow.Examples.WaterPump` |
| **Reached as** | `oneWayValve.medium.rho` |
| **Declaration** | `Medium.mo:4` |
| **Parameter** | `rho` |
| **Claim** | a settable parameter reaches a denominator, nothing excludes zero |
| **Kind** | `divisor-reachable-zero` |
| **Severity** | high |
| **Sanitizer** | `divisor` |
| **Fix site** | [SITE-0055](../../site-reports/SITE-0055-rho-divisor-reachable-zero.md) |
| **Status** | **candidate — not execution-confirmed** |

## Evidence

| key | value |
|---|---|
| `parameter` | oneWayValve.medium.rho |
| `shape` | direct |
| `path` | oneWayValve.medium.rho |
| `declared_min` | 0.0 |
| `divisor_sites` | 1 |
| `note` | reaches a denominator and nothing excludes zero |


## What this is

One occurrence. The declaration at `Medium.mo:4` is reached by this model through
`oneWayValve.medium.rho`, and the analysis reached it statically — no value has been observed
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
