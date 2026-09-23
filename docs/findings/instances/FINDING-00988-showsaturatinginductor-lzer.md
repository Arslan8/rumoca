# FINDING-00988: `SaturatingInductance1.Lzer` in `ShowSaturatingInductor`

| | |
|---|---|
| **Model** | `Modelica.Electrical.Analog.Examples.ShowSaturatingInductor` |
| **Reached as** | `SaturatingInductance1.Lzer` |
| **Declaration** | `SaturatingInductor.mo:12` |
| **Parameter** | `Lzer` |
| **Claim** | a divisor vanishes when two parameters are equal |
| **Kind** | `divisor-zero-when-parameters-equal` |
| **Severity** | high |
| **Sanitizer** | `divisor` |
| **Fix site** | [SITE-0565](../../site-reports/SITE-0565-lzer-divisor-zero-when-parameters-equal.md) |
| **Status** | **candidate — not execution-confirmed** |

## Evidence

| key | value |
|---|---|
| `parameter` | SaturatingInductance1.Lzer |
| `shape` | relational |
| `path` | SaturatingInductance1.Lzer |
| `declared_min` | None |
| `divisor_sites` | 1 |
| `partner` | SaturatingInductance1.Linf |
| `note` | zero when the two are equal; min/max cannot express a constraint between two parameters, so an assertion is the only mechanism |


## What this is

One occurrence. The declaration at `SaturatingInductor.mo:12` is reached by this model through
`SaturatingInductance1.Lzer`, and the analysis reached it statically — no value has been observed
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
