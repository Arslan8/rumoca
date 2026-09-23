# FINDING-01043: `thyristor_v4_1.VTM` in `ThyristorBehaviourTest`

| | |
|---|---|
| **Model** | `Modelica.Electrical.Analog.Examples.ThyristorBehaviourTest` |
| **Reached as** | `thyristor_v4_1.VTM` |
| **Declaration** | `Thyristor.mo:8` |
| **Parameter** | `VTM` |
| **Claim** | a settable parameter reaches a denominator, nothing excludes zero |
| **Kind** | `divisor-reachable-zero` |
| **Severity** | medium |
| **Sanitizer** | `divisor` |
| **Fix site** | [SITE-0540](../../site-reports/SITE-0540-vtm-divisor-reachable-zero.md) |
| **Status** | **candidate — not execution-confirmed** |

## Evidence

| key | value |
|---|---|
| `parameter` | thyristor_v4_1.VTM |
| `shape` | propagated |
| `path` | thyristor_v4_1.VTM -> thyristor_v4_1.Roff |
| `declared_min` | None |
| `divisor_sites` | 5 |
| `note` | reaches a denominator and nothing excludes zero |


## What this is

One occurrence. The declaration at `Thyristor.mo:8` is reached by this model through
`thyristor_v4_1.VTM`, and the analysis reached it statically — no value has been observed
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
