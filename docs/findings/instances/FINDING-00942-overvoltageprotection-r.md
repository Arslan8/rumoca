# FINDING-00942: `zDiode1.R` in `OvervoltageProtection`

| | |
|---|---|
| **Model** | `Modelica.Electrical.Analog.Examples.OvervoltageProtection` |
| **Reached as** | `zDiode1.R` |
| **Declaration** | `ZDiode.mo:8` |
| **Parameter** | `R` |
| **Claim** | a settable parameter reaches a denominator, nothing excludes zero |
| **Kind** | `divisor-reachable-zero` |
| **Severity** | high |
| **Sanitizer** | `divisor` |
| **Fix site** | [SITE-0563](../../site-reports/SITE-0563-r-divisor-reachable-zero.md) |
| **Status** | **candidate — not execution-confirmed** |

## Evidence

| key | value |
|---|---|
| `parameter` | zDiode1.R |
| `shape` | direct |
| `path` | zDiode1.R |
| `declared_min` | None |
| `divisor_sites` | 3 |
| `note` | reaches a denominator and nothing excludes zero |


## What this is

One occurrence. The declaration at `ZDiode.mo:8` is reached by this model through
`zDiode1.R`, and the analysis reached it statically — no value has been observed
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
