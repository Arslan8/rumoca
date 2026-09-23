# FINDING-00019: `invMixingUnit.tau0` in `MixingUnitWithContinuousControl`

| | |
|---|---|
| **Model** | `Modelica.Clocked.Examples.Systems.Utilities.ComponentsMixingUnit.MixingUnitWithContinuousControl` |
| **Reached as** | `invMixingUnit.tau0` |
| **Declaration** | `MixingUnit.mo:23` |
| **Parameter** | `tau0` |
| **Claim** | a settable parameter reaches a denominator, nothing excludes zero |
| **Kind** | `divisor-reachable-zero` |
| **Severity** | high |
| **Sanitizer** | `divisor` |
| **Fix site** | [SITE-0172](../../site-reports/SITE-0172-tau0-divisor-reachable-zero.md) |
| **Status** | **candidate — not execution-confirmed** |

## Evidence

| key | value |
|---|---|
| `parameter` | invMixingUnit.tau0 |
| `shape` | direct |
| `path` | invMixingUnit.tau0 |
| `declared_min` | None |
| `divisor_sites` | 14 |
| `note` | reaches a denominator and nothing excludes zero |


## What this is

One occurrence. The declaration at `MixingUnit.mo:23` is reached by this model through
`invMixingUnit.tau0`, and the analysis reached it statically — no value has been observed
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
