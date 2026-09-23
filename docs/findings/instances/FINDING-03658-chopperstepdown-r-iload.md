# FINDING-03658: `ILoad` in `ChopperStepDown_R`

| | |
|---|---|
| **Model** | `Modelica.Electrical.PowerConverters.Examples.DCDC.ChopperStepDown.ChopperStepDown_R` |
| **Reached as** | `ILoad` |
| **Declaration** | `ChopperStepDown.mo:9` |
| **Parameter** | `ILoad` |
| **Claim** | a settable parameter reaches a denominator, nothing excludes zero |
| **Kind** | `divisor-reachable-zero` |
| **Severity** | high |
| **Sanitizer** | `divisor` |
| **Fix site** | [SITE-0231](../../site-reports/SITE-0231-iload-divisor-reachable-zero.md) |
| **Status** | **candidate — not execution-confirmed** |

## Evidence

| key | value |
|---|---|
| `parameter` | ILoad |
| `shape` | direct |
| `path` | ILoad |
| `declared_min` | None |
| `divisor_sites` | 2 |
| `note` | reaches a denominator and nothing excludes zero |


## What this is

One occurrence. The declaration at `ChopperStepDown.mo:9` is reached by this model through
`ILoad`, and the analysis reached it statically — no value has been observed
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
