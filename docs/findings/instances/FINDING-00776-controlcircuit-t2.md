# FINDING-00776: `T2` in `ControlCircuit`

| | |
|---|---|
| **Model** | `Modelica.Electrical.Analog.Examples.OpAmps.ControlCircuit` |
| **Reached as** | `T2` |
| **Declaration** | `ControlCircuit.mo:5` |
| **Parameter** | `T2` |
| **Claim** | a settable parameter reaches a denominator, nothing excludes zero |
| **Kind** | `divisor-reachable-zero` |
| **Severity** | medium |
| **Sanitizer** | `divisor` |
| **Fix site** | [SITE-0395](../../site-reports/SITE-0395-t2-divisor-reachable-zero.md) |
| **Status** | **candidate — not execution-confirmed** |

## Evidence

| key | value |
|---|---|
| `parameter` | T2 |
| `shape` | propagated |
| `path` | T2 -> Ti -> PIB.T |
| `declared_min` | None |
| `divisor_sites` | 4 |
| `note` | reaches a denominator and nothing excludes zero |


## What this is

One occurrence. The declaration at `ControlCircuit.mo:5` is reached by this model through
`T2`, and the analysis reached it statically — no value has been observed
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
