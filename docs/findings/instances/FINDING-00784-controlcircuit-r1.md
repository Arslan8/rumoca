# FINDING-00784: `firstOrder1A.R1` in `ControlCircuit`

| | |
|---|---|
| **Model** | `Modelica.Electrical.Analog.Examples.OpAmps.ControlCircuit` |
| **Reached as** | `firstOrder1A.R1` |
| **Declaration** | `FirstOrder.mo:6` |
| **Parameter** | `R1` |
| **Claim** | a settable parameter reaches a denominator, nothing excludes zero |
| **Kind** | `divisor-reachable-zero` |
| **Severity** | medium |
| **Sanitizer** | `divisor` |
| **Fix site** | [SITE-0169](../../site-reports/SITE-0169-r1-divisor-reachable-zero.md) |
| **Status** | **candidate — not execution-confirmed** |

## Evidence

| key | value |
|---|---|
| `parameter` | firstOrder1A.R1 |
| `shape` | propagated |
| `path` | firstOrder1A.R1 -> firstOrder1A.R2 |
| `declared_min` | None |
| `divisor_sites` | 2 |
| `note` | reaches a denominator and nothing excludes zero |


## What this is

One occurrence. The declaration at `FirstOrder.mo:6` is reached by this model through
`firstOrder1A.R1`, and the analysis reached it statically — no value has been observed
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
