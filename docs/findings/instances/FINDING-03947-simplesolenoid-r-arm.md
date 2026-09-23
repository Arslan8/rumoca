# FINDING-03947: `r_arm` in `SimpleSolenoid`

| | |
|---|---|
| **Model** | `Modelica.Magnetic.FluxTubes.Examples.SolenoidActuator.Components.SimpleSolenoid` |
| **Reached as** | `r_arm` |
| **Declaration** | `SimpleSolenoid.mo:30` |
| **Parameter** | `r_arm` |
| **Claim** | a settable parameter reaches a denominator, nothing excludes zero |
| **Kind** | `divisor-reachable-zero` |
| **Severity** | medium |
| **Sanitizer** | `divisor` |
| **Fix site** | [SITE-0509](../../site-reports/SITE-0509-r-arm-divisor-reachable-zero.md) |
| **Status** | **candidate — not execution-confirmed** |

## Evidence

| key | value |
|---|---|
| `parameter` | r_arm |
| `shape` | propagated |
| `path` | r_arm -> g_mAirWork.r_o -> g_mAirWork.A |
| `declared_min` | 0.0 |
| `divisor_sites` | 1 |
| `note` | reaches a denominator and nothing excludes zero |


## What this is

One occurrence. The declaration at `SimpleSolenoid.mo:30` is reached by this model through
`r_arm`, and the analysis reached it statically — no value has been observed
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
