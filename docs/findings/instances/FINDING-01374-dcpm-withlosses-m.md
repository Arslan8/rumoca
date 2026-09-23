# FINDING-01374: `dcpmData1.coreParameters.m` in `DCPM_withLosses`

| | |
|---|---|
| **Model** | `Modelica.Electrical.Machines.Examples.DCMachines.DCPM_withLosses` |
| **Reached as** | `dcpmData1.coreParameters.m` |
| **Declaration** | `CoreParameters.mo:4` |
| **Parameter** | `m` |
| **Claim** | a settable parameter reaches a denominator, nothing excludes zero |
| **Kind** | `divisor-reachable-zero` |
| **Severity** | high |
| **Sanitizer** | `divisor` |
| **Fix site** | [SITE-0032](../../site-reports/SITE-0032-m-divisor-reachable-zero.md) |
| **Status** | **candidate — not execution-confirmed** |

## Evidence

| key | value |
|---|---|
| `parameter` | dcpmData1.coreParameters.m |
| `shape` | direct |
| `path` | dcpmData1.coreParameters.m |
| `declared_min` | None |
| `divisor_sites` | 2 |
| `note` | reaches a denominator and nothing excludes zero |


## What this is

One occurrence. The declaration at `CoreParameters.mo:4` is reached by this model through
`dcpmData1.coreParameters.m`, and the analysis reached it statically — no value has been observed
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
