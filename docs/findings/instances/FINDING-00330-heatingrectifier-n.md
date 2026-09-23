# FINDING-00330: `HeatingDiode1.N` in `HeatingRectifier`

| | |
|---|---|
| **Model** | `Modelica.Electrical.Analog.Examples.HeatingRectifier` |
| **Reached as** | `HeatingDiode1.N` |
| **Declaration** | `Diode.mo:10` |
| **Parameter** | `N` |
| **Claim** | a settable parameter reaches a denominator, nothing excludes zero |
| **Kind** | `divisor-reachable-zero` |
| **Severity** | medium |
| **Sanitizer** | `divisor` |
| **Fix site** | [SITE-0420](../../site-reports/SITE-0420-n-divisor-reachable-zero.md) |
| **Status** | **candidate — not execution-confirmed** |

## Evidence

| key | value |
|---|---|
| `parameter` | HeatingDiode1.N |
| `shape` | product |
| `path` | HeatingDiode1.N |
| `declared_min` | None |
| `divisor_sites` | 1 |
| `note` | reaches a denominator and nothing excludes zero |


## What this is

One occurrence. The declaration at `Diode.mo:10` is reached by this model through
`HeatingDiode1.N`, and the analysis reached it statically — no value has been observed
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
