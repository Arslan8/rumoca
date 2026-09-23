# FINDING-01255: `dcdcInverter2.fS` in `DCPM_Drive`

| | |
|---|---|
| **Model** | `Modelica.Electrical.Machines.Examples.DCMachines.DCPM_Drive` |
| **Reached as** | `dcdcInverter2.fS` |
| **Declaration** | `DcdcInverter.mo:4` |
| **Parameter** | `fS` |
| **Claim** | a settable parameter reaches a denominator, nothing excludes zero |
| **Kind** | `divisor-reachable-zero` |
| **Severity** | high |
| **Sanitizer** | `divisor` |
| **Fix site** | [SITE-0237](../../site-reports/SITE-0237-fs-divisor-reachable-zero.md) |
| **Status** | **candidate — not execution-confirmed** |

## Evidence

| key | value |
|---|---|
| `parameter` | dcdcInverter2.fS |
| `shape` | direct |
| `path` | dcdcInverter2.fS |
| `declared_min` | None |
| `divisor_sites` | 4 |
| `note` | reaches a denominator and nothing excludes zero |


## What this is

One occurrence. The declaration at `DcdcInverter.mo:4` is reached by this model through
`dcdcInverter2.fS`, and the analysis reached it statically — no value has been observed
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
