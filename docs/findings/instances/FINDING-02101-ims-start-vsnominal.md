# FINDING-02101: `aimsData.VsNominal` in `IMS_Start`

| | |
|---|---|
| **Model** | `Modelica.Electrical.Machines.Examples.InductionMachines.IMS_Start` |
| **Reached as** | `aimsData.VsNominal` |
| **Declaration** | `IM_SlipRingData.mo:35` |
| **Parameter** | `VsNominal` |
| **Claim** | a settable parameter reaches a denominator, nothing excludes zero |
| **Kind** | `divisor-reachable-zero` |
| **Severity** | medium |
| **Sanitizer** | `divisor` |
| **Fix site** | [SITE-0443](../../site-reports/SITE-0443-vsnominal-divisor-reachable-zero.md) |
| **Status** | **candidate — not execution-confirmed** |

## Evidence

| key | value |
|---|---|
| `parameter` | aimsData.VsNominal |
| `shape` | propagated |
| `path` | aimsData.VsNominal -> aimsData.turnsRatio |
| `declared_min` | None |
| `divisor_sites` | 8 |
| `note` | reaches a denominator and nothing excludes zero |


## What this is

One occurrence. The declaration at `IM_SlipRingData.mo:35` is reached by this model through
`aimsData.VsNominal`, and the analysis reached it statically — no value has been observed
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
