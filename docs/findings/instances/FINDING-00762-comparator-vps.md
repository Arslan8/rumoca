# FINDING-00762: `Vps` in `Comparator`

| | |
|---|---|
| **Model** | `Modelica.Electrical.Analog.Examples.OpAmps.Comparator` |
| **Reached as** | `Vps` |
| **Declaration** | `Comparator.mo:4` |
| **Parameter** | `Vps` |
| **Claim** | a divisor vanishes when two parameters are equal |
| **Kind** | `divisor-zero-when-parameters-equal` |
| **Severity** | high |
| **Sanitizer** | `divisor` |
| **Fix site** | [SITE-0564](../../site-reports/SITE-0564-vps-divisor-zero-when-parameters-equal.md) |
| **Status** | **candidate — not execution-confirmed** |

## Evidence

| key | value |
|---|---|
| `parameter` | Vps |
| `shape` | relational |
| `path` | Vps |
| `declared_min` | None |
| `divisor_sites` | 2 |
| `partner` | Vns |
| `note` | zero when the two are equal; min/max cannot express a constraint between two parameters, so an assertion is the only mechanism |


## What this is

One occurrence. The declaration at `Comparator.mo:4` is reached by this model through
`Vps`, and the analysis reached it statically — no value has been observed
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
