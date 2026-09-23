# FINDING-03939: `g_mAirWork.r_i` in `SimpleSolenoid`

| | |
|---|---|
| **Model** | `Modelica.Magnetic.FluxTubes.Examples.SolenoidActuator.Components.SimpleSolenoid` |
| **Reached as** | `g_mAirWork.r_i` |
| **Declaration** | `HollowCylinderAxialFlux.mo:10` |
| **Parameter** | `r_i` |
| **Claim** | a settable parameter reaches a denominator, nothing excludes zero |
| **Kind** | `divisor-reachable-zero` |
| **Severity** | medium |
| **Sanitizer** | `divisor` |
| **Fix site** | [SITE-0243](../../site-reports/SITE-0243-r-i-divisor-reachable-zero.md) |
| **Status** | **candidate — not execution-confirmed** |

## Evidence

| key | value |
|---|---|
| `parameter` | g_mAirWork.r_i |
| `shape` | propagated |
| `path` | g_mAirWork.r_i -> g_mAirWork.A |
| `declared_min` | 0.0 |
| `divisor_sites` | 1 |
| `note` | reaches a denominator and nothing excludes zero |


## What this is

One occurrence. The declaration at `HollowCylinderAxialFlux.mo:10` is reached by this model through
`g_mAirWork.r_i`, and the analysis reached it statically — no value has been observed
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
