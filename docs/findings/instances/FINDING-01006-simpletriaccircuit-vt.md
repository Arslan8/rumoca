# FINDING-01006: `simpleTriac.Vt` in `SimpleTriacCircuit`

| | |
|---|---|
| **Model** | `Modelica.Electrical.Analog.Examples.SimpleTriacCircuit` |
| **Reached as** | `simpleTriac.Vt` |
| **Declaration** | `SimpleTriac.mo:17` |
| **Parameter** | `Vt` |
| **Claim** | a settable parameter reaches a denominator, nothing excludes zero |
| **Kind** | `divisor-reachable-zero` |
| **Severity** | medium |
| **Sanitizer** | `divisor` |
| **Fix site** | [SITE-0517](../../site-reports/SITE-0517-vt-divisor-reachable-zero.md) |
| **Status** | **candidate — not execution-confirmed** |

## Evidence

| key | value |
|---|---|
| `parameter` | simpleTriac.Vt |
| `shape` | propagated |
| `path` | simpleTriac.Vt -> simpleTriac.thyristor.Vt |
| `declared_min` | None |
| `divisor_sites` | 2 |
| `note` | reaches a denominator and nothing excludes zero |


## What this is

One occurrence. The declaration at `SimpleTriac.mo:17` is reached by this model through
`simpleTriac.Vt`, and the analysis reached it statically — no value has been observed
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
