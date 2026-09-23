# FINDING-04776: `openTank1.ATank` in `TwoTanks`

| | |
|---|---|
| **Model** | `Modelica.Thermal.FluidHeatFlow.Examples.TwoTanks` |
| **Reached as** | `openTank1.ATank` |
| **Declaration** | `OpenTank.mo:5` |
| **Parameter** | `ATank` |
| **Claim** | a settable parameter reaches a denominator, nothing excludes zero |
| **Kind** | `divisor-reachable-zero` |
| **Severity** | high |
| **Sanitizer** | `divisor` |
| **Fix site** | [SITE-0471](../../site-reports/SITE-0471-atank-divisor-reachable-zero.md) |
| **Status** | **candidate — not execution-confirmed** |

## Evidence

| key | value |
|---|---|
| `parameter` | openTank1.ATank |
| `shape` | direct |
| `path` | openTank1.ATank |
| `declared_min` | None |
| `divisor_sites` | 1 |
| `note` | reaches a denominator and nothing excludes zero |


## What this is

One occurrence. The declaration at `OpenTank.mo:5` is reached by this model through
`openTank1.ATank`, and the analysis reached it statically — no value has been observed
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
