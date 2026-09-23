# FINDING-02284: `smeeData.Tq0Subtransient` in `SMEE_Generator`

| | |
|---|---|
| **Model** | `Modelica.Electrical.Machines.Examples.SynchronousMachines.SMEE_Generator` |
| **Reached as** | `smeeData.Tq0Subtransient` |
| **Declaration** | `SynchronousMachineData.mo:41` |
| **Parameter** | `Tq0Subtransient` |
| **Claim** | a settable parameter reaches a denominator, nothing excludes zero |
| **Kind** | `divisor-reachable-zero` |
| **Severity** | medium |
| **Sanitizer** | `divisor` |
| **Fix site** | [SITE-0265](../../site-reports/SITE-0265-tq0subtransient-divisor-reachable-zero.md) |
| **Status** | **candidate — not execution-confirmed** |

## Evidence

| key | value |
|---|---|
| `parameter` | smeeData.Tq0Subtransient |
| `shape` | product |
| `path` | smeeData.Tq0Subtransient |
| `declared_min` | None |
| `divisor_sites` | 2 |
| `note` | reaches a denominator and nothing excludes zero |


## What this is

One occurrence. The declaration at `SynchronousMachineData.mo:41` is reached by this model through
`smeeData.Tq0Subtransient`, and the analysis reached it statically — no value has been observed
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
