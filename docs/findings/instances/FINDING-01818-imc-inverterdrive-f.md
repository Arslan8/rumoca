# FINDING-01818: `pwm.svPWM.f` in `IMC_InverterDrive`

| | |
|---|---|
| **Model** | `Modelica.Electrical.Machines.Examples.InductionMachines.IMC_InverterDrive` |
| **Reached as** | `pwm.svPWM.f` |
| **Declaration** | `SVPWM.mo:3` |
| **Parameter** | `f` |
| **Claim** | a settable parameter reaches a denominator, nothing excludes zero |
| **Kind** | `divisor-reachable-zero` |
| **Severity** | high |
| **Sanitizer** | `divisor` |
| **Fix site** | [SITE-0494](../../site-reports/SITE-0494-f-divisor-reachable-zero.md) |
| **Status** | **candidate — not execution-confirmed** |

## Evidence

| key | value |
|---|---|
| `parameter` | pwm.svPWM.f |
| `shape` | direct |
| `path` | pwm.svPWM.f |
| `declared_min` | None |
| `divisor_sites` | 1 |
| `note` | reaches a denominator and nothing excludes zero |


## What this is

One occurrence. The declaration at `SVPWM.mo:3` is reached by this model through
`pwm.svPWM.f`, and the analysis reached it statically — no value has been observed
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
