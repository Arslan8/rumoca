# FINDING-02271: `smeeData.x0` in `SMEE_Generator`

| | |
|---|---|
| **Model** | `Modelica.Electrical.Machines.Examples.SynchronousMachines.SMEE_Generator` |
| **Reached as** | `smeeData.x0` |
| **Declaration** | `SynchronousMachineData.mo:23` |
| **Parameter** | `x0` |
| **Claim** | a settable parameter reaches a denominator, nothing excludes zero |
| **Kind** | `divisor-reachable-zero` |
| **Severity** | medium |
| **Sanitizer** | `divisor` |
| **Fix site** | [SITE-0257](../../site-reports/SITE-0257-x0-divisor-reachable-zero.md) |
| **Status** | **candidate — not execution-confirmed** |

## Evidence

| key | value |
|---|---|
| `parameter` | smeeData.x0 |
| `shape` | propagated |
| `path` | smeeData.x0 -> smeeData.xmd -> smeeData.Lmd -> smee.Lmd |
| `declared_min` | None |
| `divisor_sites` | 14 |
| `note` | reaches a denominator and nothing excludes zero |


## What this is

One occurrence. The declaration at `SynchronousMachineData.mo:23` is reached by this model through
`smeeData.x0`, and the analysis reached it statically — no value has been observed
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
